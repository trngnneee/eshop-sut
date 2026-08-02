[CmdletBinding()]
param(
    [string]$RepositoryRoot = "",
    [string]$OutputPath = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$taskRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($RepositoryRoot)) {
    $RepositoryRoot = Split-Path -Parent $taskRoot
}
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $taskRoot "git-commit-log.txt"
}

$RepositoryRoot = [System.IO.Path]::GetFullPath($RepositoryRoot)
$branch = (& git -C $RepositoryRoot branch --show-current)
$head = (& git -C $RepositoryRoot rev-parse HEAD)
$status = @(& git -C $RepositoryRoot status --short)
$status = @(
    $status | Where-Object {
        $_ -notmatch 'task3-cross-platform[\\/]git-commit-log\.txt$'
    }
)
$history = @(& git -C $RepositoryRoot log --date=iso-strict --pretty=format:"%H | %ad | %an | %s")

if ($LASTEXITCODE -ne 0) {
    throw "Unable to read Git history from $RepositoryRoot."
}

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add("STATUS: EXPORTED")
$lines.Add("Repository: $RepositoryRoot")
$lines.Add("Branch: $branch")
$lines.Add("HEAD: $head")
$lines.Add("Exported at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')")
$lines.Add("")
$lines.Add("WORKTREE STATUS AT EXPORT")
$lines.Add("(The export target task3-cross-platform/git-commit-log.txt is omitted from this section.)")
if ($status.Count -eq 0) {
    $lines.Add("(clean)")
}
else {
    foreach ($entry in $status) {
        $lines.Add($entry)
    }
}
$lines.Add("")
$lines.Add("COMMIT HISTORY")
foreach ($entry in $history) {
    $lines.Add($entry)
}

$utf8NoBom = [System.Text.UTF8Encoding]::new($false)
[System.IO.File]::WriteAllLines($OutputPath, [string[]]$lines.ToArray(), $utf8NoBom)
Write-Output "Exported Git commit log to $OutputPath"

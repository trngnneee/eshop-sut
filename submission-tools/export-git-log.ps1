[CmdletBinding()]
param(
    [string]$OutputPath = ''
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $repoRoot 'final-submission\git-commit-log.txt'
}

$branch = (& git -C $repoRoot branch --show-current).Trim()
$head = (& git -C $repoRoot rev-parse HEAD).Trim()
$rangeStart = (& git -C $repoRoot rev-parse 'origin/HW3-Khoa').Trim()
$range = 'origin/HW3-Khoa..HEAD'
$history = @(& git -C $repoRoot log --reverse --date=iso-strict '--pretty=format:%H|%ad|%an|%ae|%s' $range)
if ($LASTEXITCODE -ne 0) { throw 'Unable to read the HW03 Git history.' }

$lines = [System.Collections.Generic.List[string]]::new()
$lines.Add('HW03 CONSOLIDATED AUTHENTIC GIT COMMIT LOG')
$lines.Add('==========================================')
$lines.Add('')
$lines.Add('Student ID: 23127207; student name: see README.md')
$lines.Add("Branch: $branch")
$lines.Add("Snapshot date/timezone: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz')")
$lines.Add("Range: $range")
$lines.Add("Range base: $rangeStart")
$lines.Add("Snapshot HEAD: $head")
$lines.Add("Commit count in snapshot: $($history.Count)")
$lines.Add('')
$lines.Add('Generation command:')
$lines.Add('git log --reverse --date=iso-strict --pretty=format:"%H|%ad|%an|%ae|%s" origin/HW3-Khoa..HEAD')
$lines.Add('')
$lines.Add('Format:')
$lines.Add('FULL_COMMIT_HASH | AUTHOR_DATE | AUTHOR_NAME | AUTHOR_EMAIL | SUBJECT')
$lines.Add('')
$lines.Add('This file was generated after Snapshot HEAD and is committed in a finite')
$lines.Add('follow-up. That follow-up commit is intentionally absent from this snapshot;')
$lines.Add('the hashes and subjects below are direct Git output, not a reconstructed log.')
$lines.Add('')
$lines.Add('COMMITS')
$lines.Add('-------')
foreach ($entry in $history) {
    $lines.Add($entry -replace '\|', ' | ')
}

[System.IO.File]::WriteAllLines(
    [System.IO.Path]::GetFullPath($OutputPath),
    [string[]]$lines.ToArray(),
    [System.Text.UTF8Encoding]::new($false)
)
Write-Output "Exported $($history.Count) commits through $head to $OutputPath"

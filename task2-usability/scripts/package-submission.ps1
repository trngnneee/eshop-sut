[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$taskRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$repoRoot = Split-Path -Parent $taskRoot
$submissionRoot = Join-Path $repoRoot 'submission'
$zipPath = Join-Path $submissionRoot '23127207_Task2_Usability_Submission.zip'

New-Item -ItemType Directory -Path $submissionRoot -Force | Out-Null
$resolvedSubmission = (Resolve-Path -LiteralPath $submissionRoot).Path
$expectedZip = [System.IO.Path]::GetFullPath($zipPath)
if (-not $expectedZip.StartsWith($resolvedSubmission + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
    throw "Unsafe ZIP target: $expectedZip"
}
if (Test-Path -LiteralPath $expectedZip -PathType Leaf) {
    Remove-Item -LiteralPath $expectedZip -Force
}

$files = @(Get-ChildItem -LiteralPath $taskRoot -Recurse -File | Sort-Object FullName)
$recordingExtensions = @('.mp4', '.mov', '.webm', '.mkv', '.avi')
$recordings = @($files | Where-Object { $_.Extension.ToLowerInvariant() -in $recordingExtensions })
if ($recordings.Count -gt 0) {
    throw "Raw/local recording files must not be packaged: $($recordings.FullName -join ', ')"
}

$archive = [System.IO.Compression.ZipFile]::Open($expectedZip, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($file in $files) {
        $relative = [System.IO.Path]::GetRelativePath($taskRoot, $file.FullName).Replace('\', '/')
        $entryName = "task2-usability/$relative"
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
            $archive,
            $file.FullName,
            $entryName,
            [System.IO.Compression.CompressionLevel]::Optimal
        ) | Out-Null
    }
}
finally {
    $archive.Dispose()
}

$check = [System.IO.Compression.ZipFile]::OpenRead($expectedZip)
try {
    $entryNames = @($check.Entries | ForEach-Object { $_.FullName })
    foreach ($required in @(
        'task2-usability/Task2_Main_Report.pdf',
        'task2-usability/AI_Audit_Task2.pdf',
        'task2-usability/AI_Critique_Task2.pdf',
        'task2-usability/Participant_Roster.md',
        'task2-usability/Analysis/SUS_Raw_Responses.csv',
        'task2-usability/Demo_Video_Link.md',
        'task2-usability/git-commit-log.txt'
    )) {
        if ($required -notin $entryNames) { throw "Required ZIP entry missing: $required" }
    }
    if (@($entryNames | Where-Object { [System.IO.Path]::GetExtension($_).ToLowerInvariant() -in $recordingExtensions }).Count -gt 0) {
        throw 'Submission ZIP unexpectedly contains a recording file.'
    }
}
finally {
    $check.Dispose()
}

$zip = Get-Item -LiteralPath $expectedZip
Write-Host "Created private Task 2 submission ZIP: $($zip.FullName)"
Write-Host "Entries: $($files.Count); bytes: $($zip.Length); raw/local recordings: 0"

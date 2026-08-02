[CmdletBinding()]
param(
    [ValidateRange(0, 100)]
    [int]$SelfAssessedGrade = 88
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$repoRoot = Split-Path -Parent $PSScriptRoot
$finalRoot = Join-Path $repoRoot 'final-submission'
$submissionRoot = Join-Path $repoRoot 'submission'
$folderName = '23127207_HW03_AI_GUIUsability_{0:D3}' -f $SelfAssessedGrade
$stageRoot = Join-Path $submissionRoot $folderName
$zipPath = Join-Path $submissionRoot ($folderName + '.zip')
$renderRoot = Join-Path $submissionRoot '.render-hw03'
$renderer = Join-Path $PSScriptRoot 'render-markdown.js'
$chrome = 'C:\Program Files\Google\Chrome\Application\chrome.exe'

foreach ($required in @($renderer, $chrome, $finalRoot)) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Required build input is missing: $required"
    }
}

New-Item -ItemType Directory -Path $submissionRoot -Force | Out-Null
$resolvedSubmissionRoot = (Resolve-Path -LiteralPath $submissionRoot).Path

function Assert-SafeBuildTarget {
    param([Parameter(Mandatory = $true)][string]$Path)
    $full = [System.IO.Path]::GetFullPath($Path)
    if (-not $full.StartsWith($resolvedSubmissionRoot + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe build target outside submission directory: $full"
    }
}

foreach ($target in @($stageRoot, $zipPath, $renderRoot)) {
    Assert-SafeBuildTarget -Path $target
}

foreach ($target in @($stageRoot, $renderRoot)) {
    if (Test-Path -LiteralPath $target) {
        $resolved = (Resolve-Path -LiteralPath $target).Path
        Assert-SafeBuildTarget -Path $resolved
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
}
if (Test-Path -LiteralPath $zipPath -PathType Leaf) {
    Remove-Item -LiteralPath $zipPath -Force
}

New-Item -ItemType Directory -Path $stageRoot, $renderRoot -Force | Out-Null

$documents = @(
    @{ Source = 'Main_Report.md'; Pdf = 'Main_Report.pdf' },
    @{ Source = 'Bug_Report.md'; Pdf = 'Bug_Report.pdf' },
    @{ Source = 'AI_Critique.md'; Pdf = 'AI_Critique.pdf' },
    @{ Source = 'AI_Audit_Report.md'; Pdf = 'AI_Audit_Report.pdf' }
)

foreach ($document in $documents) {
    $sourcePath = Join-Path $finalRoot $document.Source
    if (-not (Test-Path -LiteralPath $sourcePath -PathType Leaf)) {
        throw "Required report source is missing: $sourcePath"
    }
    $htmlPath = Join-Path $renderRoot ([System.IO.Path]::GetFileNameWithoutExtension($document.Source) + '.html')
    $pdfPath = Join-Path $finalRoot $document.Pdf
    & node $renderer $sourcePath $htmlPath
    if ($LASTEXITCODE -ne 0) { throw "Markdown rendering failed for $sourcePath" }

    $htmlUri = ([System.Uri]$htmlPath).AbsoluteUri
    $profilePath = Join-Path $renderRoot ([System.IO.Path]::GetFileNameWithoutExtension($document.Source) + '-profile')
    & $chrome --headless --disable-gpu --no-pdf-header-footer --allow-file-access-from-files --user-data-dir="$profilePath" --print-to-pdf="$pdfPath" $htmlUri
    if ($LASTEXITCODE -ne 0) { throw "PDF rendering failed for $sourcePath" }
    $pdfDeadline = (Get-Date).AddSeconds(15)
    while (-not (Test-Path -LiteralPath $pdfPath -PathType Leaf) -and (Get-Date) -lt $pdfDeadline) {
        Start-Sleep -Milliseconds 250
    }
    if (-not (Test-Path -LiteralPath $pdfPath -PathType Leaf)) { throw "PDF was not created: $pdfPath" }
    $signature = [System.IO.File]::ReadAllBytes($pdfPath)[0..3]
    if ([System.Text.Encoding]::ASCII.GetString($signature) -ne '%PDF') { throw "Invalid PDF signature: $pdfPath" }
}

$coreFiles = @(
    'README.md',
    'Main_Report.md',
    'Main_Report.pdf',
    'Bug_Report.md',
    'Bug_Report.pdf',
    'AI_Critique.md',
    'AI_Critique.pdf',
    'AI_Audit_Report.md',
    'AI_Audit_Report.pdf',
    'git-commit-log.txt'
)
foreach ($file in $coreFiles) {
    $source = Join-Path $finalRoot $file
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Required final file is missing: $source" }
    Copy-Item -LiteralPath $source -Destination (Join-Path $stageRoot $file) -Force
}

foreach ($directory in @('task1-gui', 'task2-usability', 'task3-cross-platform')) {
    $source = Join-Path $repoRoot $directory
    Copy-Item -LiteralPath $source -Destination (Join-Path $stageRoot $directory) -Recurse -Force
}

$skillRoot = Join-Path $stageRoot 'agent-skills'
New-Item -ItemType Directory -Path $skillRoot -Force | Out-Null
foreach ($skill in @('gui-testing-skill', 'usability-testing-skill')) {
    $source = Join-Path $repoRoot ".agents\skills\$skill"
    if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md') -PathType Leaf)) { throw "Required Agent Skill is missing: $skill" }
    Copy-Item -LiteralPath $source -Destination (Join-Path $skillRoot $skill) -Recurse -Force
}

$summaryRoot = Join-Path $stageRoot 'test-summary'
New-Item -ItemType Directory -Path $summaryRoot -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot 'tests\test-summary\sprint-hw03-task2-test-run.md') -Destination $summaryRoot -Force
Copy-Item -LiteralPath (Join-Path $repoRoot 'tests\test-summary\traceability-matrix.md') -Destination $summaryRoot -Force

$sessionCount = @(Get-ChildItem -LiteralPath (Join-Path $stageRoot 'task2-usability\Sessions') -Filter 'Session_P??.md' -File).Count
$susRows = @(Import-Csv -LiteralPath (Join-Path $stageRoot 'task2-usability\Analysis\SUS_Raw_Responses.csv')).Count
$task3Screenshots = @(Get-ChildItem -LiteralPath (Join-Path $stageRoot 'task3-cross-platform\evidence') -Recurse -Filter '*.png' -File).Count
$driveText = Get-Content -LiteralPath (Join-Path $stageRoot 'task2-usability\Stage_0_Drive_Inventory.md') -Raw -Encoding UTF8
$officialDriveLinks = @([regex]::Matches($driveText, '(?m)^\| \[D(?:0[1-5]|06 replacement|07)\]\(https://drive\.google\.com/file/d/')).Count

if ($sessionCount -ne 7) { throw "Expected 7 Task 2 session reports; found $sessionCount" }
if ($susRows -ne 7) { throw "Expected 7 SUS response rows; found $susRows" }
if ($task3Screenshots -ne 160) { throw "Expected 160 cross-platform screenshots; found $task3Screenshots" }
if ($officialDriveLinks -ne 7) { throw "Expected 7 access-controlled official recording links; found $officialDriveLinks" }
if (-not (Test-Path -LiteralPath (Join-Path $stageRoot 'task1-gui\GUI_Checklist_HW3.xlsx') -PathType Leaf)) { throw 'Excel checklist is missing from staging.' }

$manifestLines = [System.Collections.Generic.List[string]]::new()
$manifestLines.Add("Package: $folderName")
$manifestLines.Add("Built: $(Get-Date -Format 'yyyy-MM-ddTHH:mm:sszzz')")
$manifestLines.Add('Student ID: 23127207; student name: see README.md')
$manifestLines.Add('Core Markdown reports: 4 + README')
$manifestLines.Add('Core PDF reports: 4')
$manifestLines.Add('GUI checklist: Markdown + XLSX')
$manifestLines.Add("Task 2 official session reports: $sessionCount")
$manifestLines.Add("Task 2 official recording links: $officialDriveLinks (access-controlled Drive; raw participant MP4s intentionally excluded for privacy and size)")
$manifestLines.Add("Task 2 SUS response sets: $susRows")
$manifestLines.Add("Task 3 screenshots: $task3Screenshots")
$manifestLines.Add('Agent Skills: gui-testing-skill, usability-testing-skill')
[System.IO.File]::WriteAllLines((Join-Path $stageRoot 'submission-manifest.txt'), $manifestLines, [System.Text.UTF8Encoding]::new($false))

$writeArchive = [System.IO.Compression.ZipFile]::Open($zipPath, [System.IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($file in Get-ChildItem -LiteralPath $stageRoot -Recurse -File | Sort-Object FullName) {
        $entryName = $file.FullName.Substring($stageRoot.Length).TrimStart('\', '/').Replace('\', '/')
        [System.IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
            $writeArchive,
            $file.FullName,
            $entryName,
            [System.IO.Compression.CompressionLevel]::Optimal
        ) | Out-Null
    }
}
finally {
    $writeArchive.Dispose()
}
if (-not (Test-Path -LiteralPath $zipPath -PathType Leaf)) { throw "ZIP was not created: $zipPath" }

$archive = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $entryNames = @($archive.Entries | ForEach-Object { $_.FullName.Replace('\', '/') })
    foreach ($required in @(
        'README.md', 'Main_Report.md', 'Main_Report.pdf', 'Bug_Report.md', 'Bug_Report.pdf',
        'AI_Critique.md', 'AI_Critique.pdf', 'AI_Audit_Report.md', 'AI_Audit_Report.pdf',
        'git-commit-log.txt', 'task1-gui/GUI_Checklist_HW3.xlsx',
        'task2-usability/Participant_Roster.md', 'task2-usability/Analysis/SUS_Raw_Responses.csv',
        'task3-cross-platform/results/Task3_Cross_Platform_Results.csv',
        'agent-skills/gui-testing-skill/SKILL.md', 'agent-skills/usability-testing-skill/SKILL.md'
    )) {
        if ($required -notin $entryNames) { throw "Required ZIP entry is missing: $required" }
    }
    $rawRecordings = @($entryNames | Where-Object { [System.IO.Path]::GetExtension($_).ToLowerInvariant() -in @('.mp4', '.mov', '.mkv', '.webm', '.avi') })
    if ($rawRecordings.Count -gt 0) { throw "Raw participant recording unexpectedly entered the ZIP: $($rawRecordings -join ', ')" }
}
finally {
    $archive.Dispose()
}

$zip = Get-Item -LiteralPath $zipPath
$sha256 = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash
Write-Host "SUBMISSION_READY: $($zip.FullName)" -ForegroundColor Green
Write-Host "Size: $($zip.Length) bytes"
Write-Host "SHA256: $sha256"
Write-Host "Staging folder: $stageRoot"

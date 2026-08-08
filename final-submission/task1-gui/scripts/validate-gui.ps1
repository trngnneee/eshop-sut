[CmdletBinding()]
param([switch]$RequireComplete)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
$taskRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$repoRoot = Split-Path -Parent $taskRoot
$finalRoot = Join-Path $repoRoot 'final-submission'
$failures = [System.Collections.Generic.List[string]]::new()
$limitations = [System.Collections.Generic.List[string]]::new()

function Assert-Gui {
    param([bool]$Condition, [string]$Message)
    if ($Condition) { Write-Host "[PASS] $Message" -ForegroundColor Green }
    else { Write-Host "[FAIL] $Message" -ForegroundColor Red; $script:failures.Add($Message) }
}

function Add-Limitation([string]$Message) {
    if (-not $script:limitations.Contains($Message)) { $script:limitations.Add($Message) }
}

$required = @(
    'GUI_Checklist_HW3.md','GUI_Checklist_HW3.xlsx',
    'results\Task1_Execution_Chrome.csv','results\Evidence_Index.csv'
)
foreach ($relative in $required) {
    Assert-Gui (Test-Path -LiteralPath (Join-Path $taskRoot $relative) -PathType Leaf) "Required artefact exists: $relative"
}

$finalRequired = @('README.md','Main_Report.md','Bug_Report.md','AI_Critique.md','AI_Audit_Report.md','git-commit-log.txt')
foreach ($relative in $finalRequired) {
    Assert-Gui (Test-Path -LiteralPath (Join-Path $finalRoot $relative) -PathType Leaf) "Consolidated artefact exists: final-submission/$relative"
}

$commitLog = Get-Content -LiteralPath (Join-Path $finalRoot 'git-commit-log.txt') -Raw -Encoding UTF8
Assert-Gui ($commitLog -match 'Snapshot HEAD: [0-9a-f]{40}' -and @([regex]::Matches($commitLog,'(?m)^[0-9a-f]{40} \|')).Count -ge 1) 'Consolidated Git log contains an authentic full-hash snapshot'

$rows = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'results\Task1_Execution_Chrome.csv'))
$ids = @($rows | ForEach-Object { $_.ID })
Assert-Gui ($rows.Count -eq 58) 'Execution CSV contains exactly 58 items'
Assert-Gui (@($ids | Sort-Object -Unique).Count -eq 58) 'All checklist IDs are unique'
Assert-Gui (@($rows | Where-Object { $_.Status -eq 'Pass' }).Count -eq 37) 'Pass count is 37'
Assert-Gui (@($rows | Where-Object { $_.Status -eq 'Fail' }).Count -eq 20) 'Fail count is 20'
Assert-Gui (@($rows | Where-Object { $_.Status -eq 'Blocked' }).Count -eq 1) 'Exactly one physical-device item is Blocked'
Assert-Gui (@($rows | Where-Object { $_.Status -eq 'Not Run' }).Count -eq 0) 'No item remains Not Run'
Assert-Gui (@($rows | Where-Object { $_.Status -notin @('Pass','Fail','Blocked','Not Run') }).Count -eq 0) 'Statuses use the allowed vocabulary'

Assert-Gui (@($rows | Where-Object { $_.Origin -eq 'AI_INITIAL' }).Count -eq 48) 'Origin count is 48 AI_INITIAL'
Assert-Gui (@($rows | Where-Object { $_.Origin -eq 'HUMAN_ADDED' }).Count -eq 10) 'Origin count is 10 HUMAN_ADDED'
foreach ($ia in @('IA-01','IA-02','IA-03','IA-04')) {
    Assert-Gui (@($rows | Where-Object { $_.IA -eq $ia }).Count -gt 0) "$ia has substantive checklist coverage"
}
Assert-Gui (@($rows | Where-Object { $_.'Execution Mode' -notin @('LIVE_LOCAL_SUT','MOCKED_NETWORK_FAILURE','MOCKED_WRITE_PREVENTION','MOCKED_EMPTY_API_STATE','MOCKED_SLOW_API','MOCKED_SLOW_WRITE','EXPO_WEB_DESKTOP_BROWSER') }).Count -eq 0) 'Every item declares an allowed execution mode'
Assert-Gui (@($rows | Where-Object { $_.'Execution Mode' -like 'MOCKED_*' }).Count -eq 5) 'Exactly five deterministic mocked-state rows are disclosed'

$badRows = @($rows | Where-Object {
    [string]::IsNullOrWhiteSpace($_.'Expected Result') -or
    [string]::IsNullOrWhiteSpace($_.'Actual Result') -or
    [string]::IsNullOrWhiteSpace($_.Notes) -or
    [string]::IsNullOrWhiteSpace($_.Evidence) -or
    [string]::IsNullOrWhiteSpace($_.'Evidence ID')
})
Assert-Gui ($badRows.Count -eq 0) 'Every row has Expected, Actual, Notes, Evidence and Evidence ID'

$failRows = @($rows | Where-Object { $_.Status -eq 'Fail' })
Assert-Gui (@($failRows | Where-Object { [string]::IsNullOrWhiteSpace($_.'Bug ID') }).Count -eq 0) 'Every Fail has a Bug ID'
$pendingIssues = @($failRows | Where-Object { $_.'GitHub Issue' -eq 'PENDING_EXTERNAL_ACTION' })
$badIssueUrls = @($failRows | Where-Object { $_.'GitHub Issue' -ne 'PENDING_EXTERNAL_ACTION' -and $_.'GitHub Issue' -notmatch '^https://github\.com/trngnneee/eshop-sut/issues/\d+$' })
Assert-Gui ($badIssueUrls.Count -eq 0) 'Every published/reused GitHub mapping has a real issue URL shape'
if ($pendingIssues.Count -gt 0) { Add-Limitation "$($pendingIssues.Count) Fail item(s) still require verified GitHub issue URLs." }

$evidencePaths = @($rows | ForEach-Object { $_.Evidence } | Sort-Object -Unique)
Assert-Gui ($evidencePaths.Count -eq 40) 'Result rows reference 40 unique screenshots'
$badEvidence = [System.Collections.Generic.List[string]]::new()
foreach ($relative in $evidencePaths) {
    $absolute = Join-Path $taskRoot $relative.Replace('/','\')
    if (-not (Test-Path -LiteralPath $absolute -PathType Leaf)) { $badEvidence.Add("Missing $relative"); continue }
    $file = Get-Item -LiteralPath $absolute
    if ($file.Length -lt 20000) { $badEvidence.Add("Too small $relative"); continue }
    $stream = [System.IO.File]::OpenRead($absolute)
    try {
        $signature = New-Object byte[] 8
        $read = $stream.Read($signature,0,8)
        if ($read -ne 8 -or [BitConverter]::ToString($signature) -ne '89-50-4E-47-0D-0A-1A-0A') { $badEvidence.Add("Invalid PNG $relative") }
    } finally { $stream.Dispose() }
}
Assert-Gui ($badEvidence.Count -eq 0) 'All 40 screenshots exist, are non-trivial and have valid PNG signatures'

$checklist = Get-Content -LiteralPath (Join-Path $taskRoot 'GUI_Checklist_HW3.md') -Raw -Encoding UTF8
$mdIds = @([regex]::Matches($checklist,'(?m)^\|\s*(GUI-[A-Z0-9-]+)\s*\|') | ForEach-Object { $_.Groups[1].Value })
Assert-Gui ($mdIds.Count -eq 58 -and @($mdIds | Sort-Object -Unique).Count -eq 58) 'Markdown checklist contains the same 58 unique IDs'
Assert-Gui ($checklist -match '37 Pass' -or $checklist -match '\*\*Pass\*\*') 'Markdown checklist contains executed statuses'
Assert-Gui ($checklist -notmatch 'Edit Category' -and $checklist -notmatch 'theo yêu cầu FR-14.*Sửa') 'Invented FR-14 Edit requirement is absent'

$xlsx = Get-Item -LiteralPath (Join-Path $taskRoot 'GUI_Checklist_HW3.xlsx')
Assert-Gui ($xlsx.Length -gt 10000) 'Excel workbook is non-trivial'
$xlsxStream = [System.IO.File]::OpenRead($xlsx.FullName)
try {
    $archive = [System.IO.Compression.ZipArchive]::new($xlsxStream,[System.IO.Compression.ZipArchiveMode]::Read)
    try { Assert-Gui (@($archive.Entries | Where-Object { $_.FullName -like 'xl/worksheets/sheet*.xml' }).Count -ge 4) 'Excel workbook contains checklist, review, summary and traceability sheets' }
    finally { $archive.Dispose() }
} finally { $xlsxStream.Dispose() }

$mainReport = Get-Content -LiteralPath (Join-Path $finalRoot 'Main_Report.md') -Raw -Encoding UTF8
Assert-Gui ($mainReport -match 'Task 1' -and $mainReport -match '37 Pass' -and $mainReport -match '20 Fail' -and $mainReport -match '1 Blocked') 'Consolidated Main Report matches Task 1 execution metrics'

$bugReport = Get-Content -LiteralPath (Join-Path $finalRoot 'Bug_Report.md') -Raw -Encoding UTF8
$missingFailedIds = @($failRows | Where-Object { $bugReport -notmatch [regex]::Escape($_.ID) })
Assert-Gui ($missingFailedIds.Count -eq 0) 'Consolidated Bug Report covers all 20 Task 1 failed assertions'

$critiqueDocument = Get-Content -LiteralPath (Join-Path $finalRoot 'AI_Critique.md') -Raw -Encoding UTF8
$critiqueMatch = [regex]::Match($critiqueDocument,'(?ms)^## Critique \([^)]+words\)\s*\r?\n\r?\n(.*?)(?=\r?\n\r?\n\*\*Word-count target:)')
$words = if ($critiqueMatch.Success) { [regex]::Matches($critiqueMatch.Groups[1].Value,"[\p{L}\p{M}\p{N}]+(?:[-'][\p{L}\p{M}\p{N}]+)*").Count } else { 0 }
Assert-Gui ($words -ge 200 -and $words -le 300) "Assignment-wide AI critique contains 200-300 words (actual: $words)"
$audit = Get-Content -LiteralPath (Join-Path $finalRoot 'AI_Audit_Report.md') -Raw -Encoding UTF8
Assert-Gui ($audit -match 'HUMAN_REVIEWED' -and $audit -match 'Task 1 corrections') 'Consolidated AI audit records Task 1 human review and corrections'

$task1Section = [regex]::Match($mainReport,'(?ms)^## 4\. Task 1.*?(?=^## 5\.)').Value
$task1DemoVerified = $task1Section -match 'https://youtu\.be/tMar6OyMG80' -and $task1Section -match 'PUBLIC_LINK_VERIFIED'
if ($task1DemoVerified) {
    Assert-Gui $true 'Task 1 GUI-testing-skill demo URL is recorded as PUBLIC_LINK_VERIFIED'
}
else {
    Add-Limitation 'Task 1 GUI-testing-skill demo still needs a real public YouTube URL.'
}
$blocked = @($rows | Where-Object { $_.Status -eq 'Blocked' })
if ($blocked.Count -gt 0) { Add-Limitation 'GUI-MOBILE-LOGIN-011 still needs a real Expo Go/physical/cloud soft-keyboard run.' }

if ($failures.Count -gt 0) {
    Write-Host "`nTASK1 STRUCTURAL VALIDATION FAILED: $($failures.Count) check(s)." -ForegroundColor Red
    exit 1
}
if ($RequireComplete -and $limitations.Count -gt 0) {
    Write-Host "`nTASK1 COMPLETION BLOCKED: $($limitations.Count) acknowledged blocker(s)." -ForegroundColor Yellow
    $limitations | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
    Write-Host 'No external URL or device evidence was fabricated.' -ForegroundColor Yellow
    exit 2
}
Write-Host "`nTASK1 PACKAGE STRUCTURALLY READY WITH DISCLOSED BLOCKERS" -ForegroundColor Cyan
$limitations | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
exit 0

[CmdletBinding()]
param([switch]$RequireComplete)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression
$taskRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
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
    'README.md','scope-analysis.md','GUI_Checklist_HW3.md','GUI_Checklist_HW3.xlsx',
    'GUI_Coverage_Matrix.md','GUI_Bug_Report_HW3.md','GUI_Test_Summary_HW3.md',
    'AI_Item_Level_Critique.md','AI_Critique_Task1.md','AI_Critique_Task1.pdf',
    'AI_Audit_Report_Task1.md','AI_Audit_Report_Task1.pdf','GUI_Test_Summary_HW3.pdf',
    'AI_Disclosure_Task1.md','git-commit-log.txt','Demo_Video_Link.md',
    'ai-output\AI_INITIAL_GUI_Checklist.md','results\Task1_Execution_Chrome.csv',
    'results\Evidence_Index.csv','scripts\sync-current-execution.py','scripts\export-commit-log.ps1'
)
foreach ($relative in $required) {
    Assert-Gui (Test-Path -LiteralPath (Join-Path $taskRoot $relative) -PathType Leaf) "Required artefact exists: $relative"
}

foreach ($pdfName in @('AI_Audit_Report_Task1.pdf', 'AI_Critique_Task1.pdf', 'GUI_Test_Summary_HW3.pdf')) {
    $pdfPath = Join-Path $taskRoot $pdfName
    if (Test-Path -LiteralPath $pdfPath -PathType Leaf) {
        Assert-Gui ((Get-Item -LiteralPath $pdfPath).Length -gt 10000) "$pdfName is non-empty and plausibly rendered"
    }
}

$commitLog = Get-Content -LiteralPath (Join-Path $taskRoot 'git-commit-log.txt') -Raw -Encoding UTF8
Assert-Gui ($commitLog -match 'STATUS: EXPORTED' -and $commitLog -match '(?m)^HEAD: [0-9a-f]{40}\r?$') 'Git commit log is an authentic full-hash export'
Assert-Gui ($commitLog -match '(?m)^[0-9a-f]{40} \| .* \| task1:') 'Git commit log contains an authentic Task 1 procedure commit'

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

$summary = Get-Content -LiteralPath (Join-Path $taskRoot 'GUI_Test_Summary_HW3.md') -Raw -Encoding UTF8
Assert-Gui ($summary -match '\| Pass \| 37 \|' -and $summary -match '\| Fail \| 20 \|' -and $summary -match '\| Blocked \| 1 \|') 'Test Summary matches the execution CSV metrics'

$critique = Get-Content -LiteralPath (Join-Path $taskRoot 'AI_Critique_Task1.md') -Raw -Encoding UTF8
$critiqueBody = ($critique -replace '(?m)^#.*$','' -replace '(?m)^\*\*.*$','')
$words = [regex]::Matches($critiqueBody,"[\p{L}\p{M}\p{N}]+(?:[-'][\p{L}\p{M}\p{N}]+)*").Count
Assert-Gui ($words -ge 200 -and $words -le 300) "AI critique contains 200-300 words (actual: $words)"
$audit = Get-Content -LiteralPath (Join-Path $taskRoot 'AI_Audit_Report_Task1.md') -Raw -Encoding UTF8
$itemReview = Get-Content -LiteralPath (Join-Path $taskRoot 'AI_Item_Level_Critique.md') -Raw -Encoding UTF8
Assert-Gui ($audit -match 'HUMAN_REVIEWED' -and $itemReview -match 'HUMAN_REVIEWED') 'AI audit and item-level critique record human review'
Assert-Gui (@([regex]::Matches($itemReview,'(?m)^\| `GUI-')).Count -eq 58) 'Item-level critique covers all 58 final IDs'

$demo = Get-Content -LiteralPath (Join-Path $taskRoot 'Demo_Video_Link.md') -Raw -Encoding UTF8
if ($demo -notmatch 'https://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[A-Za-z0-9_-]+') { Add-Limitation 'Task 1 GUI-testing-skill demo still needs a real public YouTube URL.' }
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

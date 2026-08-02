[CmdletBinding()]
param(
    [switch]$RequireComplete
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$taskRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$repoRoot = Split-Path -Parent $taskRoot
$failures = [System.Collections.Generic.List[string]]::new()
$limitations = [System.Collections.Generic.List[string]]::new()

function Assert-Task3 {
    param(
        [Parameter(Mandatory = $true)][bool]$Condition,
        [Parameter(Mandatory = $true)][string]$Message
    )
    if ($Condition) {
        Write-Host "[PASS] $Message" -ForegroundColor Green
    }
    else {
        Write-Host "[FAIL] $Message" -ForegroundColor Red
        $script:failures.Add($Message)
    }
}

function Add-Limitation {
    param([string]$Message)
    if (-not $script:limitations.Contains($Message)) {
        $script:limitations.Add($Message)
    }
}

$requiredFiles = @(
    'README.md',
    'Platform_Inventory.md',
    'Task3_Cross_Platform_Report.md',
    'Task3_Cross_Platform_Report.pdf',
    'Task3_Findings.md',
    'Cross_Platform_Matrix.md',
    'Evidence_Index.md',
    'AI_Audit_Task3.md',
    'AI_Audit_Task3.pdf',
    'AI_Critique_Task3.md',
    'AI_Critique_Task3.pdf',
    'git-commit-log.txt',
    'results\Task3_Cross_Platform_Results.csv',
    'results\Evidence_Index.csv',
    'results\run-summary.json',
    'results\derived-summary.json',
    'scripts\run-task3.js',
    'scripts\summarize-task3.js',
    'scripts\export-commit-log.ps1'
)

foreach ($relativePath in $requiredFiles) {
    Assert-Task3 (Test-Path -LiteralPath (Join-Path $taskRoot $relativePath) -PathType Leaf) "Required artefact exists: $relativePath"
}

$commitLog = Get-Content -LiteralPath (Join-Path $taskRoot 'git-commit-log.txt') -Raw -Encoding UTF8
$task3CommitCount = @([regex]::Matches($commitLog, '(?mi)^[0-9a-f]{40}\s+\|.*\|\s+task3:')).Count
Assert-Task3 ($commitLog -match '(?m)^STATUS: EXPORTED$') 'Git commit log is a real exported text artefact'
Assert-Task3 ($task3CommitCount -ge 3) "Git commit log contains at least three Task 3 procedure commits (actual: $task3CommitCount)"

$task1Checklist = Get-Content -LiteralPath (Join-Path $repoRoot 'task1-gui\GUI_Checklist_HW3.md') -Raw -Encoding UTF8
$expectedIds = @([regex]::Matches($task1Checklist, '(?m)^\|\s*(GUI-[A-Z0-9-]+)\s*\|') | ForEach-Object { $_.Groups[1].Value })
Assert-Task3 ($expectedIds.Count -eq 58) "Task 1 source contains exactly 58 checklist IDs"
Assert-Task3 (@($expectedIds | Sort-Object -Unique).Count -eq 58) "Task 1 source checklist IDs are unique"

$summary = Get-Content -LiteralPath (Join-Path $taskRoot 'results\run-summary.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$derived = Get-Content -LiteralPath (Join-Path $taskRoot 'results\derived-summary.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$rows = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'results\Task3_Cross_Platform_Results.csv'))
$evidenceRows = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'results\Evidence_Index.csv'))

Assert-Task3 ($summary.student.id -eq '23127207' -and -not [string]::IsNullOrWhiteSpace($summary.student.name) -and $summary.student.email -eq '23127207@student.hcmus.edu.vn') 'Run summary contains the required student identity/email overlay metadata'
Assert-Task3 ($summary.task3_status -eq 'BLOCKED_THIRD_REQUIRED_PLATFORM') 'Run summary preserves the honest third-platform blocker'
Assert-Task3 ([int]$summary.eligible_successful_platforms -eq 2 -and [int]$summary.required_eligible_platforms -eq 3) 'Eligibility is reported as exactly 2 of 3 required platforms'
Assert-Task3 (@($summary.platforms).Count -eq 4) 'Four executed environments are inventoried'

$expectedPlatformIds = @('chrome-windows', 'firefox-windows', 'webkit-windows', 'android-chrome-emulation')
$actualPlatformIds = @($summary.platforms | ForEach-Object { $_.platform_id })
Assert-Task3 (@($expectedPlatformIds | Where-Object { $_ -notin $actualPlatformIds }).Count -eq 0 -and @($actualPlatformIds | Where-Object { $_ -notin $expectedPlatformIds }).Count -eq 0) 'Platform inventory contains the four declared execution environments'

$eligibleIds = @($summary.platforms | Where-Object { $_.eligible_for_hw03_required_three } | ForEach-Object { $_.platform_id })
Assert-Task3 ($eligibleIds.Count -eq 2 -and 'chrome-windows' -in $eligibleIds -and 'firefox-windows' -in $eligibleIds) 'Only Chrome and Firefox are counted as rubric-eligible'
Assert-Task3 (@($summary.platforms | Where-Object { $_.platform_id -eq 'webkit-windows' }).platform_note -match 'not Apple Safari') 'WebKit is explicitly not represented as Safari'
Assert-Task3 (@($summary.platforms | Where-Object { $_.platform_id -eq 'android-chrome-emulation' }).platform_note -match 'not a physical Android') 'Pixel emulation is explicitly not represented as real Android Chrome'

Assert-Task3 ($rows.Count -eq 232) 'Result dataset contains 232 rows (58 x 4)'
Assert-Task3 ([int]$derived.checklist_item_count -eq 58 -and [int]$derived.result_row_count -eq 232) 'Derived summary matches the expected checklist/result counts'
Assert-Task3 ([int]$derived.status_consistent_items -eq 58 -and @($derived.status_inconsistent_items).Count -eq 0) 'All 58 item statuses are consistent across executed environments'

foreach ($platformId in $expectedPlatformIds) {
    $platformRows = @($rows | Where-Object { $_.platform_id -eq $platformId })
    $platformIds = @($platformRows | ForEach-Object { $_.checklist_id })
    Assert-Task3 ($platformRows.Count -eq 58) "$platformId has 58 result rows"
    Assert-Task3 (@($platformIds | Sort-Object -Unique).Count -eq 58) "$platformId has 58 unique checklist IDs"
    Assert-Task3 (@($expectedIds | Where-Object { $_ -notin $platformIds }).Count -eq 0 -and @($platformIds | Where-Object { $_ -notin $expectedIds }).Count -eq 0) "$platformId contains exactly the Task 1 checklist ID set"
    Assert-Task3 (@($platformRows | Where-Object { $_.status -eq 'Pass' }).Count -eq 34) "$platformId has 34 Pass rows"
    Assert-Task3 (@($platformRows | Where-Object { $_.status -eq 'Fail' }).Count -eq 23) "$platformId has 23 Fail rows"
    Assert-Task3 (@($platformRows | Where-Object { $_.status -eq 'Not Observable' }).Count -eq 1) "$platformId has one honestly Not Observable soft-keyboard row"
    Assert-Task3 (@($platformRows | Where-Object { [string]::IsNullOrWhiteSpace($_.actual_result) -or [string]::IsNullOrWhiteSpace($_.evidence_id) -or [string]::IsNullOrWhiteSpace($_.evidence_path) }).Count -eq 0) "$platformId rows contain actual result and evidence traceability"

    $platformJson = Get-Content -LiteralPath (Join-Path $taskRoot "results\$platformId.json") -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert-Task3 (@($platformJson.summary.scenario_errors).Count -eq 0) "$platformId has zero final harness scenario errors"
    Assert-Task3 (@($platformJson.summary.missing_ids).Count -eq 0 -and @($platformJson.summary.duplicate_ids).Count -eq 0 -and @($platformJson.summary.unexpected_ids).Count -eq 0) "$platformId JSON contains no missing/duplicate/unexpected IDs"
}

$allowedModes = @('LIVE_LOCAL_SUT', 'MOCKED_NETWORK_FAILURE', 'MOCKED_WRITE_PREVENTION', 'MOCKED_EMPTY_API_STATE', 'MOCKED_SLOW_API', 'MOCKED_SLOW_WRITE', 'EXPO_WEB_DESKTOP_BROWSER')
Assert-Task3 (@($rows | Where-Object { $_.execution_mode -notin $allowedModes }).Count -eq 0) 'Every row has an explicit allowed execution mode'
Assert-Task3 (@($rows | Where-Object { $_.execution_mode -like 'MOCKED_*' }).Count -eq 20) 'Exactly 20 deterministic mocked-state rows are labelled (5 per platform)'
Assert-Task3 (@($rows | Where-Object { $_.execution_mode -eq 'EXPO_WEB_DESKTOP_BROWSER' }).Count -eq 4) 'Four soft-keyboard limitations are labelled Expo Web desktop-browser observations'

Assert-Task3 ($evidenceRows.Count -eq 160) 'Evidence index contains 160 unique screenshot rows'
$uniqueEvidencePaths = @($rows | ForEach-Object { $_.evidence_path } | Sort-Object -Unique)
Assert-Task3 ($uniqueEvidencePaths.Count -eq 160) 'Result dataset references exactly 160 unique screenshots'

$badEvidence = [System.Collections.Generic.List[string]]::new()
foreach ($relativePath in $uniqueEvidencePaths) {
    $absolutePath = Join-Path $taskRoot $relativePath.Replace('/', '\')
    if (-not (Test-Path -LiteralPath $absolutePath -PathType Leaf)) {
        $badEvidence.Add("Missing: $relativePath")
        continue
    }
    $file = Get-Item -LiteralPath $absolutePath
    if ($file.Length -lt 20000) {
        $badEvidence.Add("Too small: $relativePath ($($file.Length) bytes)")
        continue
    }
    $stream = [System.IO.File]::OpenRead($absolutePath)
    try {
        $signature = New-Object byte[] 8
        $read = $stream.Read($signature, 0, 8)
        $expectedSignature = [byte[]](137,80,78,71,13,10,26,10)
        if ($read -ne 8 -or [System.BitConverter]::ToString($signature) -ne [System.BitConverter]::ToString($expectedSignature)) {
            $badEvidence.Add("Invalid PNG signature: $relativePath")
        }
    }
    finally {
        $stream.Dispose()
    }
}
Assert-Task3 ($badEvidence.Count -eq 0) 'All 160 referenced evidence files exist, are non-trivial PNGs and have valid signatures'
if ($badEvidence.Count -gt 0) { $badEvidence | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow } }

$matrix = Get-Content -LiteralPath (Join-Path $taskRoot 'Cross_Platform_Matrix.md') -Raw -Encoding UTF8
$index = Get-Content -LiteralPath (Join-Path $taskRoot 'Evidence_Index.md') -Raw -Encoding UTF8
Assert-Task3 (@([regex]::Matches($matrix, '(?m)^\|\s*GUI-[A-Z0-9-]+\s*\|')).Count -eq 58) 'Markdown cross-platform matrix contains 58 checklist rows'
Assert-Task3 (@([regex]::Matches($index, '(?m)^\| \[T3-')).Count -eq 160) 'Markdown evidence index contains 160 screenshot rows'

$report = Get-Content -LiteralPath (Join-Path $taskRoot 'Task3_Cross_Platform_Report.md') -Raw -Encoding UTF8
$inventory = Get-Content -LiteralPath (Join-Path $taskRoot 'Platform_Inventory.md') -Raw -Encoding UTF8
Assert-Task3 ($report -match 'BLOCKED_THIRD_REQUIRED_PLATFORM' -and $report -match '232 rows' -and $report -match '160 PNG') 'Main report states the honest status and exact execution/evidence totals'
Assert-Task3 ($inventory -match '2/3 ELIGIBLE' -and $inventory -match 'not Apple Safari' -and $inventory -match 'not a real/cloud Android') 'Platform inventory discloses eligibility and non-substitution boundaries'

$critique = Get-Content -LiteralPath (Join-Path $taskRoot 'AI_Critique_Task3.md') -Raw -Encoding UTF8
$critiqueBody = ($critique -split '(?m)^## Student review', 2)[0]
$critiqueBody = $critiqueBody -replace '(?m)^#.*$', '' -replace '(?m)^\*\*.*$', ''
$critiqueWordCount = [regex]::Matches($critiqueBody, "[\p{L}\p{M}\p{N}]+(?:[-'][\p{L}\p{M}\p{N}]+)*").Count
Assert-Task3 ($critiqueWordCount -ge 200 -and $critiqueWordCount -le 300) "AI critique contains 200-300 words (actual: $critiqueWordCount)"
if ($critique -match 'READY_FOR_STUDENT_REVIEW' -and $critique -match 'PENDING_STUDENT_REVIEW') {
    Add-Limitation 'AI Critique and Audit still require the student human-review confirmation.'
}

foreach ($pdfName in @('Task3_Cross_Platform_Report.pdf', 'AI_Audit_Task3.pdf', 'AI_Critique_Task3.pdf')) {
    $pdfPath = Join-Path $taskRoot $pdfName
    if (Test-Path -LiteralPath $pdfPath -PathType Leaf) {
        Assert-Task3 ((Get-Item -LiteralPath $pdfPath).Length -gt 10000) "$pdfName is non-empty and plausibly rendered"
    }
}

Add-Limitation 'Only two of three rubric-eligible platforms are evidenced; Safari/macOS, real/cloud Android Chrome, or Expo Go on a real phone is still required.'

if ($failures.Count -gt 0) {
    Write-Host ''
    Write-Host "TASK3 STRUCTURAL VALIDATION FAILED: $($failures.Count) check(s)." -ForegroundColor Red
    exit 1
}

if ($RequireComplete -and $limitations.Count -gt 0) {
    Write-Host ''
    Write-Host "BLOCKED_THIRD_REQUIRED_PLATFORM: completion gate found $($limitations.Count) acknowledged blocker(s)." -ForegroundColor Yellow
    $limitations | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
    Write-Host 'No unavailable platform or human review was fabricated.' -ForegroundColor Yellow
    exit 2
}

Write-Host ''
Write-Host 'TASK3 LOCAL PACKAGE STRUCTURALLY READY - THIRD REQUIRED PLATFORM STILL BLOCKED' -ForegroundColor Cyan
$limitations | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
exit 0

[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$taskRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$failures = [System.Collections.Generic.List[string]]::new()

function Assert-Submission {
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

$required = @(
    'README.md',
    'SUBMISSION_CHECKLIST.md',
    'Task2_Main_Report.md',
    'Task2_Main_Report.pdf',
    'Participant_Roster.md',
    'Pilot_Session.md',
    'Evidence_Index.md',
    'Missing_Data_and_Followup.md',
    'Video_Data_Quality_Report.md',
    'Usability_Findings.md',
    'Usability_Bug_Report.md',
    'AI_Audit_Task2.md',
    'AI_Audit_Task2.pdf',
    'AI_Critique_Task2.md',
    'AI_Critique_Task2.pdf',
    'Analysis\Observation_Metrics.csv',
    'Analysis\Findings_Register.csv',
    'Analysis\SUS_Raw_Responses.csv',
    'Analysis\SUS_Scores.csv',
    'Analysis\SUS_Results.md',
    'github-issues\DRAFT-BUG-USABILITY-01.md',
    'github-issues\DRAFT-BUG-AUTH-PLAINTEXT-01.md',
    'demo\Task2_Usability_Skill_Demo.mp4',
    'Demo_Video_Link.md'
)

foreach ($relative in $required) {
    $path = Join-Path $taskRoot $relative
    Assert-Submission (Test-Path -LiteralPath $path -PathType Leaf) "Required artefact exists: $relative"
}

$sessions = @(Get-ChildItem -LiteralPath (Join-Path $taskRoot 'Sessions') -Filter 'Session_P??.md' -File)
Assert-Submission ($sessions.Count -eq 7) 'Exactly seven official session reports exist'

for ($number = 1; $number -le 7; $number++) {
    $id = 'P{0:D2}' -f $number
    $path = Join-Path $taskRoot "Sessions\Session_$id.md"
    $content = if (Test-Path -LiteralPath $path) { Get-Content -LiteralPath $path -Raw -Encoding UTF8 } else { '' }
    Assert-Submission ($content -match '## 12\. Verification status' -and $content -match '`READY_FOR_HUMAN_REVIEW`') "$id has the honest human-review status"
    Assert-Submission ($content -match '(?m)^\|\s*T0\s*\|') "$id contains T0 coding"
    Assert-Submission ($content -match '(?m)^\|\s*T11\s*\|') "$id contains T11 coding"
    Assert-Submission ($content -match 'FAILED_OR_ABANDONED') "$id has an explicit outcome taxonomy"
}

$roster = Get-Content -LiteralPath (Join-Path $taskRoot 'Participant_Roster.md') -Raw -Encoding UTF8
$rosterRows = @([regex]::Matches($roster, '(?m)^\|\s*P0[1-7]\s*\|'))
$maskedContacts = @([regex]::Matches($roster, '(?<!\d)\d{3}\*{4}\d{3}(?!\d)'))
Assert-Submission ($rosterRows.Count -eq 7) 'Roster contains exactly seven official participant rows'
Assert-Submission ($maskedContacts.Count -eq 7) 'Roster contains seven contacts with exactly four middle digits masked'
Assert-Submission ($roster -match 'submission.*only|Moodle/TA') 'Roster is labelled for private submission handling'

$metrics = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'Analysis\Observation_Metrics.csv'))
Assert-Submission ($metrics.Count -eq 7) 'Observation metrics contain seven participant rows'
Assert-Submission (@($metrics | Where-Object { $_.Status -ne 'READY_FOR_HUMAN_REVIEW' }).Count -eq 0) 'All metric rows use the human-review status'
Assert-Submission (@($metrics | Where-Object { $_.Outcome -ne 'FAILED_OR_ABANDONED' }).Count -eq 0) 'All seven recorded outcomes match the declared taxonomy'

$sus = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'Analysis\SUS_Raw_Responses.csv'))
Assert-Submission ($sus.Count -eq 7) 'SUS raw table contains seven participant rows'
$susText = Get-Content -LiteralPath (Join-Path $taskRoot 'Analysis\SUS_Results.md') -Raw -Encoding UTF8
Assert-Submission ($susText -match '0/7') 'SUS results disclose zero complete response sets'
Assert-Submission ($susText -match 'NOT_CALCULABLE') 'SUS aggregate is explicitly not calculable'

$mainReport = Get-Content -LiteralPath (Join-Path $taskRoot 'Task2_Main_Report.md') -Raw -Encoding UTF8
Assert-Submission ($mainReport -match 'median 80') 'Main report states the calculable task-time median'
Assert-Submission ($mainReport -match 'BUG-PF-02' -and $mainReport -match 'BUG-AUTH-PLAINTEXT-01') 'Main report includes both participant-evidenced software-bug candidates'
Assert-Submission ($mainReport -match 'CONFIRMED_MISSING_DATA') 'Main report discloses confirmed missing data'

$critique = Get-Content -LiteralPath (Join-Path $taskRoot 'AI_Critique_Task2.md') -Raw -Encoding UTF8
$critiqueBody = ($critique -split '(?m)^Before submission,', 2)[0]
$critiqueBody = $critiqueBody -replace '(?m)^#.*$', '' -replace '(?m)^\*\*.*$', ''
$wordCount = [regex]::Matches($critiqueBody, "[\p{L}\p{M}\p{N}]+(?:[-'][\p{L}\p{M}\p{N}]+)*").Count
Assert-Submission ($wordCount -ge 200 -and $wordCount -le 300) "AI critique body has 200-300 words (actual: $wordCount)"
Assert-Submission ($critique -match 'READY_FOR_STUDENT_REVIEW') 'AI critique does not falsely claim human review'

foreach ($pdfName in @('Task2_Main_Report.pdf', 'AI_Audit_Task2.pdf', 'AI_Critique_Task2.pdf')) {
    $pdf = Get-Item -LiteralPath (Join-Path $taskRoot $pdfName)
    Assert-Submission ($pdf.Length -gt 10000) "$pdfName is non-empty and plausibly rendered"
}

$demo = Get-Item -LiteralPath (Join-Path $taskRoot 'demo\Task2_Usability_Skill_Demo.mp4')
Assert-Submission ($demo.Length -gt 100000) 'Local demo MP4 is non-empty'
$demoLink = Get-Content -LiteralPath (Join-Path $taskRoot 'Demo_Video_Link.md') -Raw -Encoding UTF8
Assert-Submission ($demoLink -match 'LOCAL_DEMO_READY') 'Demo metadata records the local-ready state'
Assert-Submission ($demoLink -match 'PUBLIC_UPLOAD_REQUIRED') 'Demo metadata discloses the missing public upload'

$publicAnalysisFiles = @(
    (Join-Path $taskRoot 'Task2_Main_Report.md'),
    (Join-Path $taskRoot 'Usability_Test_Summary.md'),
    (Join-Path $taskRoot 'Usability_Findings.md'),
    (Join-Path $taskRoot 'Usability_Bug_Report.md')
) + @($sessions.FullName) + @(
    (Join-Path $taskRoot 'Analysis\Observation_Metrics.csv'),
    (Join-Path $taskRoot 'Analysis\Findings_Register.csv'),
    (Join-Path $taskRoot 'Analysis\SUS_Results.md')
)
$participantNames = @(
    [regex]::Matches($roster, '(?m)^\|\s*P0[1-7]\s*\|\s*([^|]+)\|') |
        ForEach-Object { $_.Groups[1].Value.Trim() }
)
$privacyLeaks = [System.Collections.Generic.List[string]]::new()
foreach ($path in $publicAnalysisFiles) {
    $content = Get-Content -LiteralPath $path -Raw -Encoding UTF8
    foreach ($name in $participantNames) {
        if ($content -cmatch [regex]::Escape($name)) {
            $privacyLeaks.Add("$(Split-Path -Leaf $path): $name")
        }
    }
    if ($content -match '(?<!\d)0[3-9]\d{8}(?!\d)') {
        $privacyLeaks.Add("$(Split-Path -Leaf $path): possible unmasked phone")
    }
}
Assert-Submission ($privacyLeaks.Count -eq 0) 'Public analytical artefacts contain no supplied participant names or unmasked Vietnamese phone numbers'
if ($privacyLeaks.Count -gt 0) {
    $privacyLeaks | ForEach-Object { Write-Host "  $_" -ForegroundColor Yellow }
}

if ($failures.Count -gt 0) {
    Write-Host ''
    Write-Host "STRUCTURAL VALIDATION FAILED: $($failures.Count) check(s)." -ForegroundColor Red
    exit 1
}

Write-Host ''
Write-Host 'SUBMISSION PACKAGE STRUCTURALLY READY WITH DISCLOSED LIMITATIONS' -ForegroundColor Cyan
Write-Host 'This result does not claim that missing pilot, consent, eligibility, SUS, probes, publication, or human-review evidence exists.' -ForegroundColor Yellow

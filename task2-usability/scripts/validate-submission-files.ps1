[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$taskRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$repoRoot = Split-Path -Parent $taskRoot
$finalRoot = Join-Path $repoRoot 'final-submission'
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
    'Participant_Roster.md',
    'Pilot_Session.md',
    'Evidence_Index.md',
    'Missing_Data_and_Followup.md',
    'Video_Data_Quality_Report.md',
    'Analysis\Observation_Metrics.csv',
    'Analysis\Findings_Register.csv',
    'Analysis\SUS_Raw_Responses.csv',
    'Analysis\SUS_Scores.csv',
    'Analysis\SUS_Results.md',
    'Demo_Video_Link.md'
)

foreach ($relative in $required) {
    $path = Join-Path $taskRoot $relative
    Assert-Submission (Test-Path -LiteralPath $path -PathType Leaf) "Required artefact exists: $relative"
}
foreach ($relative in @('README.md','Main_Report.md','Bug_Report.md','AI_Critique.md','AI_Audit_Report.md','git-commit-log.txt')) {
    $path = Join-Path $finalRoot $relative
    Assert-Submission (Test-Path -LiteralPath $path -PathType Leaf) "Consolidated artefact exists: final-submission/$relative"
}

$sessions = @(Get-ChildItem -LiteralPath (Join-Path $taskRoot 'Sessions') -Filter 'Session_P??.md' -File)
Assert-Submission ($sessions.Count -eq 7) 'Exactly seven official session reports exist'

for ($number = 1; $number -le 7; $number++) {
    $id = 'P{0:D2}' -f $number
    $path = Join-Path $taskRoot "Sessions\Session_$id.md"
    $content = if (Test-Path -LiteralPath $path) { Get-Content -LiteralPath $path -Raw -Encoding UTF8 } else { '' }
    Assert-Submission ($content -match '## 12\. Verification status' -and $content -match '`HUMAN_REVIEWED`') "$id records completed human review"
    $expectedCodes = @(0..11 | ForEach-Object { "T$_" })
    $actualCodes = @([regex]::Matches($content, '(?m)^\|\s*(T\d+)\s*\|') | ForEach-Object { $_.Groups[1].Value })
    $codeSetIsExact = $actualCodes.Count -eq 12 -and @($actualCodes | Sort-Object -Unique).Count -eq 12 -and
        @($expectedCodes | Where-Object { $_ -notin $actualCodes }).Count -eq 0 -and
        @($actualCodes | Where-Object { $_ -notin $expectedCodes }).Count -eq 0
    Assert-Submission $codeSetIsExact "$id contains exactly one row for each session code T0 through T11"
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
Assert-Submission (@($metrics | Where-Object { $_.Status -ne 'HUMAN_REVIEWED' }).Count -eq 0) 'All metric rows record completed human review'
Assert-Submission (@($metrics | Where-Object { $_.Outcome -ne 'FAILED_OR_ABANDONED' }).Count -eq 0) 'All seven recorded outcomes match the declared taxonomy'

$findings = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'Analysis\Findings_Register.csv'))
Assert-Submission (@($findings | Where-Object { $_.type -eq 'SOFTWARE_BUG' }).Count -eq 3) 'Findings register separates exactly three software bugs'
Assert-Submission (@($findings | Where-Object { $_.type -eq 'USABILITY_ISSUE' }).Count -eq 4) 'Findings register separates exactly four usability issues'
$softwareBugRows = @($findings | Where-Object { $_.type -eq 'SOFTWARE_BUG' })
Assert-Submission (@($softwareBugRows | Where-Object { $_.github_issue -notmatch '^https://github\.com/trngnneee/eshop-sut/issues/(37|55|118)$' }).Count -eq 0) 'All software bugs map to verified canonical GitHub issue URLs (#37, #55, #118)'

$sus = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'Analysis\SUS_Raw_Responses.csv'))
Assert-Submission ($sus.Count -eq 7) 'SUS raw table contains seven participant rows'
$expectedSusIds = @('P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07')
$actualSusIds = @($sus | ForEach-Object { $_.participant_id })
Assert-Submission (@($expectedSusIds | Where-Object { $_ -notin $actualSusIds }).Count -eq 0 -and @($actualSusIds | Where-Object { $_ -notin $expectedSusIds }).Count -eq 0) 'SUS raw table contains exactly P01 through P07'
Assert-Submission (@($sus | Where-Object { $_.status -ne 'COMPLETED_USER_PROVIDED' }).Count -eq 0) 'All SUS rows retain the user-provided provenance status'
$invalidSusResponseCount = 0
foreach ($susRow in $sus) {
    foreach ($question in 1..10) {
        $susValue = [string]$susRow.("Q$question")
        if ($susValue -notmatch '^[1-5]$') {
            $invalidSusResponseCount++
        }
    }
}
Assert-Submission ($invalidSusResponseCount -eq 0) 'All 70 SUS responses are integers from 1 to 5'
$susScores = @(Import-Csv -LiteralPath (Join-Path $taskRoot 'Analysis\SUS_Scores.csv'))
$susCalculationErrors = [System.Collections.Generic.List[string]]::new()
foreach ($susRow in $sus) {
    $contributions = [System.Collections.Generic.List[int]]::new()
    foreach ($question in 1..10) {
        $rawValue = [int]$susRow.("Q$question")
        $contribution = if ($question % 2 -eq 1) { $rawValue - 1 } else { 5 - $rawValue }
        $contributions.Add($contribution)
    }
    $sum = ($contributions | Measure-Object -Sum).Sum
    $score = [decimal]$sum * [decimal]2.5
    $stored = @($susScores | Where-Object { $_.participant_id -eq $susRow.participant_id })
    $rawSeries = @(1..10 | ForEach-Object { [string]$susRow.("Q$_") }) -join ';'
    $contributionSeries = $contributions -join ';'
    if ($stored.Count -ne 1 -or $stored[0].raw_responses -ne $rawSeries -or
        $stored[0].contributions -ne $contributionSeries -or [int]$stored[0].contribution_sum -ne $sum -or
        [decimal]$stored[0].sus_score -ne $score) {
        $susCalculationErrors.Add($susRow.participant_id)
    }
}
Assert-Submission ($susCalculationErrors.Count -eq 0) 'Raw SUS odd/even contributions, sums and x2.5 participant scores are exact for P01-P07'
$susText = Get-Content -LiteralPath (Join-Path $taskRoot 'Analysis\SUS_Results.md') -Raw -Encoding UTF8
Assert-Submission ($susText -match '7/7') 'SUS results report seven complete response sets'
Assert-Submission ($susText -match '\|\s*Mean\s*\|\s*76\.79\s*\|' -and $susText -match '\|\s*Median\s*\|\s*75\s*\|' -and $susText -match '\|\s*Minimum\s*\|\s*62\.5\s*\|' -and $susText -match '\|\s*Maximum\s*\|\s*100\s*\|') 'SUS aggregates match the supplied response sets'

$mainReport = Get-Content -LiteralPath (Join-Path $finalRoot 'Main_Report.md') -Raw -Encoding UTF8
Assert-Submission ($mainReport -match 'median 80') 'Main report states the calculable task-time median'
Assert-Submission ($mainReport -match 'BUG-PF-02' -and $mainReport -match 'BUG-AUTH-PLAINTEXT-01' -and $mainReport -match 'BUG-REG-PASSWORD-POLICY-01') 'Main report includes both participant-evidenced bugs and the technical-only registration-policy bug'
Assert-Submission ($mainReport -match 'missing-data declaration' -and $mainReport -match 'not collected') 'Main report discloses confirmed missing data'
Assert-Submission ($mainReport -match 'COMPLETE_WITH_DISCLOSED_LIMITATIONS') 'Main report records the accepted package-closure state'

$completionScript = Join-Path $taskRoot 'scripts\validate-usability.ps1'
$closureOutput = @(& powershell -NoProfile -ExecutionPolicy Bypass -File $completionScript 2>&1)
$closureExit = $LASTEXITCODE
$closureText = $closureOutput -join "`n"
Assert-Submission ($closureExit -eq 0 -and $closureText -match 'COMPLETE_WITH_DISCLOSED_LIMITATIONS') 'Default completion gate closes the package with disclosed limitations'

$strictOutput = @(& powershell -NoProfile -ExecutionPolicy Bypass -File $completionScript -RequireCompleteEvidence 2>&1)
$strictExit = $LASTEXITCODE
$strictText = $strictOutput -join "`n"
Assert-Submission ($strictExit -eq 2 -and $strictText -match 'INCOMPLETE_EVIDENCE') 'Strict evidence mode preserves the honest missing-data refusal'

$critique = Get-Content -LiteralPath (Join-Path $finalRoot 'AI_Critique.md') -Raw -Encoding UTF8
$critiqueMatch = [regex]::Match($critique,'(?ms)^## Task 2 critique.*?\r?\n\r?\n(.*?)(?=\r?\n\*\*Section length:)')
$critiqueBody = if ($critiqueMatch.Success) { $critiqueMatch.Groups[1].Value } else { '' }
$wordCount = [regex]::Matches($critiqueBody, "[\p{L}\p{M}\p{N}]+(?:[-'][\p{L}\p{M}\p{N}]+)*").Count
Assert-Submission ($wordCount -ge 200 -and $wordCount -le 300) "AI critique body has 200-300 words (actual: $wordCount)"
Assert-Submission ($critique -match 'HUMAN_REVIEWED' -and $critique -match '2026-08-02') 'AI critique records the student human-review confirmation'

$demoLink = Get-Content -LiteralPath (Join-Path $taskRoot 'Demo_Video_Link.md') -Raw -Encoding UTF8
Assert-Submission ($demoLink -match 'https://youtu\.be/[A-Za-z0-9_-]+') 'Demo metadata contains a public YouTube URL'
Assert-Submission ($demoLink -match 'PUBLIC_LINK_VERIFIED') 'Demo metadata records the verified public-link state'
Assert-Submission ($demoLink -match 'YOUTUBE_LINK_ONLY' -and $demoLink -match 'LOCAL_COPY_NOT_REQUIRED') 'Demo metadata records the YouTube-link-only submission rule'

$publicAnalysisFiles = @(
    (Join-Path $finalRoot 'Main_Report.md'),
    (Join-Path $finalRoot 'Bug_Report.md'),
    (Join-Path $finalRoot 'AI_Critique.md'),
    (Join-Path $finalRoot 'AI_Audit_Report.md')
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
Write-Host 'SUBMISSION PACKAGE COMPLETE WITH DISCLOSED LIMITATIONS' -ForegroundColor Cyan
Write-Host 'This result preserves missing pilot, consent and probe disclosures; human review does not reconstruct absent evidence.' -ForegroundColor Yellow

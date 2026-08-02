[CmdletBinding()]
param(
    [string]$InputPath = "",
    [string]$OutputPath = "",
    [string]$ScoresPath = "",
    [switch]$SelfTest
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-SusCalculation {
    param(
        [Parameter(Mandatory = $true)]
        [int[]]$Responses
    )

    if ($Responses.Count -ne 10) {
        throw "A SUS response set must contain exactly 10 values."
    }

    $contributions = New-Object System.Collections.Generic.List[int]
    for ($index = 0; $index -lt 10; $index++) {
        $response = $Responses[$index]
        if ($response -lt 1 -or $response -gt 5) {
            throw "SUS response Q$($index + 1) must be an integer from 1 to 5; got '$response'."
        }

        $questionNumber = $index + 1
        if (($questionNumber % 2) -eq 1) {
            $contributions.Add($response - 1)
        }
        else {
            $contributions.Add(5 - $response)
        }
    }

    $sum = ($contributions | Measure-Object -Sum).Sum
    [PSCustomObject]@{
        Contributions = [int[]]$contributions.ToArray()
        Sum           = [int]$sum
        Score         = [double]($sum * 2.5)
    }
}

if ($SelfTest) {
    $neutral = Get-SusCalculation -Responses @(3, 3, 3, 3, 3, 3, 3, 3, 3, 3)
    if ($neutral.Score -ne 50 -or $neutral.Sum -ne 20) {
        throw "Self-test failed: ten neutral responses must score 50."
    }

    $maximum = Get-SusCalculation -Responses @(5, 1, 5, 1, 5, 1, 5, 1, 5, 1)
    if ($maximum.Score -ne 100 -or $maximum.Sum -ne 40) {
        throw "Self-test failed: the maximum response pattern must score 100."
    }

    Write-Output "PASS: SUS formula self-test returned 50 and 100 for the two known patterns."
    exit 0
}

$taskRoot = Split-Path -Parent $PSScriptRoot
if ([string]::IsNullOrWhiteSpace($InputPath)) {
    $InputPath = Join-Path $taskRoot "Analysis\SUS_Raw_Responses.csv"
}
if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $taskRoot "Analysis\SUS_Results.md"
}
if ([string]::IsNullOrWhiteSpace($ScoresPath)) {
    $ScoresPath = Join-Path $taskRoot "Analysis\SUS_Scores.csv"
}

if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) {
    throw "SUS input file not found: $InputPath"
}

$rows = @(Import-Csv -LiteralPath $InputPath)
$expectedIds = @("P01", "P02", "P03", "P04", "P05", "P06", "P07")

if ($rows.Count -ne 7) {
    throw "Expected exactly seven user-provided SUS rows; found $($rows.Count)."
}

$actualIds = @($rows | ForEach-Object { $_.participant_id })
$duplicates = @($actualIds | Group-Object | Where-Object { $_.Count -ne 1 })
if ($duplicates.Count -gt 0) {
    throw "Participant IDs must be unique. Duplicate ID(s): $($duplicates.Name -join ', ')."
}

$missingIds = @($expectedIds | Where-Object { $_ -notin $actualIds })
$unexpectedIds = @($actualIds | Where-Object { $_ -notin $expectedIds })
if ($missingIds.Count -gt 0 -or $unexpectedIds.Count -gt 0) {
    throw "SUS rows must be exactly P01 through P07. Missing: '$($missingIds -join ', ')'; unexpected: '$($unexpectedIds -join ', ')'."
}

$scoreRows = New-Object System.Collections.Generic.List[object]
foreach ($participantId in $expectedIds) {
    $row = $rows | Where-Object { $_.participant_id -eq $participantId } | Select-Object -First 1
    if ($row.status -ne "COMPLETED_USER_PROVIDED") {
        throw "$participantId status must be COMPLETED_USER_PROVIDED before analysis; got '$($row.status)'."
    }

    $responses = New-Object System.Collections.Generic.List[int]
    for ($question = 1; $question -le 10; $question++) {
        $propertyName = "Q$question"
        $raw = [string]$row.$propertyName
        $parsed = 0
        if (-not [int]::TryParse($raw, [ref]$parsed) -or $parsed -lt 1 -or $parsed -gt 5) {
            throw "$participantId $propertyName must be a genuine integer response from 1 to 5; got '$raw'."
        }
        $responses.Add($parsed)
    }

    $calculation = Get-SusCalculation -Responses ([int[]]$responses.ToArray())
    $scoreRows.Add([PSCustomObject]@{
        participant_id = $participantId
        raw_responses   = ($responses -join ";")
        contributions  = ($calculation.Contributions -join ";")
        contribution_sum = $calculation.Sum
        sus_score       = $calculation.Score
    })
}

$scores = @($scoreRows | ForEach-Object { [double]$_.sus_score } | Sort-Object)
$mean = [Math]::Round((($scores | Measure-Object -Average).Average), 2)
$median = [Math]::Round($scores[3], 2)
$minimum = [Math]::Round($scores[0], 2)
$maximum = [Math]::Round($scores[6], 2)
$unroundedMean = ($scores | Measure-Object -Average).Average
$squaredDeviationSum = ($scores | ForEach-Object { [Math]::Pow($_ - $unroundedMean, 2) } | Measure-Object -Sum).Sum
$sampleStandardDeviation = [Math]::Round([Math]::Sqrt($squaredDeviationSum / ($scores.Count - 1)), 2)
$firstQuartile = [Math]::Round($scores[1], 2)
$thirdQuartile = [Math]::Round($scores[5], 2)
$itemDiagnostics = New-Object System.Collections.Generic.List[object]
for ($question = 1; $question -le 10; $question++) {
    $itemMean = [Math]::Round((($rows | ForEach-Object { [double]$_.("Q$question") } | Measure-Object -Average).Average), 2)
    $meanContribution = if (($question % 2) -eq 1) { $itemMean - 1 } else { 5 - $itemMean }
    $itemDiagnostics.Add([PSCustomObject]@{
        Item = "Q$question"
        MeanResponse = ('{0:F2}' -f $itemMean)
        MeanContribution = ('{0:F2}' -f $meanContribution)
    })
}

$markdown = New-Object System.Collections.Generic.List[string]
$markdown.Add("# SUS Results - Seven User-Provided Response Sets")
$markdown.Add("")
$markdown.Add("**Input:** ``Analysis/SUS_Raw_Responses.csv``")
$markdown.Add("**Valid complete response sets:** 7/7")
$markdown.Add("**Identifiers:** ``P01`` through ``P07``")
$markdown.Add("**Source status:** ``COMPLETED_USER_PROVIDED``")
$markdown.Add("")
$markdown.Add("The values were supplied by the user on 2026-07-31. On 2026-08-02, the user confirmed that the seven response sets use the official participant IDs ``P01``-``P07``. This analysis verifies ID-domain completeness, uniqueness, the 1-5 response range, and SUS arithmetic; it does not independently verify collection provenance.")
$markdown.Add("")
$markdown.Add("## Per-participant calculation")
$markdown.Add("")
$markdown.Add("| Participant | Raw Q1-Q10 | Contributions Q1-Q10 | Contribution sum | SUS score |")
$markdown.Add("| :--- | :--- | :--- | ---: | ---: |")
foreach ($row in $scoreRows) {
    $markdown.Add("| $($row.participant_id) | $($row.raw_responses) | $($row.contributions) | $($row.contribution_sum) | $($row.sus_score) |")
}
$markdown.Add("")
$markdown.Add("## Descriptive aggregate")
$markdown.Add("")
$markdown.Add("| Statistic | Value |")
$markdown.Add("| :--- | ---: |")
$markdown.Add("| Mean | $mean |")
$markdown.Add("| Median | $median |")
$markdown.Add("| Minimum | $minimum |")
$markdown.Add("| Maximum | $maximum |")
$markdown.Add("")
$markdown.Add("## Item-level diagnostic summary")
$markdown.Add("")
$markdown.Add("| Item | Mean response | Mean contribution (0-4) |")
$markdown.Add("| :--- | ---: | ---: |")
foreach ($diagnostic in $itemDiagnostics) {
    $markdown.Add("| $($diagnostic.Item) | $($diagnostic.MeanResponse) | $($diagnostic.MeanContribution) |")
}
$markdown.Add("")
$markdown.Add("Across the seven scores, the sample standard deviation is $sampleStandardDeviation and the interquartile range is $firstQuartile-$thirdQuartile. The relatively lower contribution means for Q2, Q6 and Q8 identify perceived complexity, inconsistency and cumbersomeness as the most useful SUS-level follow-up signals. These are descriptive diagnostics for this sample, not inferential statistics.")
$markdown.Add("")
$markdown.Add("The detailed behavioral funnel, error-stage concentration and triangulation with findings are documented in ``Analysis/Flow_Funnel_and_SUS_Diagnostics.md``.")
$markdown.Add("")
$markdown.Add("Odd-item contribution = response - 1; even-item contribution = 5 - response; SUS score = contribution sum x 2.5.")
$markdown.Add("")
$markdown.Add("SUS is a 0-100 scale, not a percentage. These seven observations are descriptive; no statistical significance or population-wide conclusion is inferred.")

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($OutputPath, [string[]]$markdown.ToArray(), $utf8NoBom)
$scoreCsv = @($scoreRows | ConvertTo-Csv -NoTypeInformation)
[System.IO.File]::WriteAllLines($ScoresPath, [string[]]$scoreCsv, $utf8NoBom)

Write-Output "PASS: scored exactly seven structurally valid COMPLETED_USER_PROVIDED response sets for P01-P07. Collection provenance remains outside this calculation."
Write-Output "Results: $OutputPath"
Write-Output "Scores: $ScoresPath"

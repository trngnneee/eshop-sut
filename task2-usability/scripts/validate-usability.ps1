[CmdletBinding()]
param(
    [string]$TaskRoot = "",
    [switch]$RequireCompleteEvidence
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($TaskRoot)) {
    $TaskRoot = Split-Path -Parent $PSScriptRoot
}
$TaskRoot = [System.IO.Path]::GetFullPath($TaskRoot)

$issues = New-Object System.Collections.Generic.List[string]
$limitations = New-Object System.Collections.Generic.List[string]

function Add-Issue {
    param([string]$Message)
    $script:issues.Add($Message)
}

function Add-Limitation {
    param([string]$Message)
    if (-not $script:limitations.Contains($Message)) {
        $script:limitations.Add($Message)
    }
}

function Read-RequiredFile {
    param([string]$RelativePath)
    $path = Join-Path $TaskRoot $RelativePath
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        Add-Issue "Missing required file: $RelativePath"
        return $null
    }
    return Get-Content -Raw -Encoding UTF8 -LiteralPath $path
}

$requiredFiles = @(
    "Usability_Test_Plan.md",
    "Participant_Roster.md",
    "Pilot_Session.md",
    "Instruments\SUS_Form.md",
    "Instruments\Post_Session_Probes.md",
    "Instruments\Consent_Form.md",
    "Instruments\Moderator_Guide.md",
    "Usability_Findings.md",
    "Usability_Bug_Report.md",
    "Usability_Test_Summary.md",
    "Evidence_Index.md",
    "Missing_Data_and_Followup.md",
    "Analysis\SUS_Raw_Responses.csv",
    "Analysis\SUS_Results.md",
    "Analysis\SUS_Scores.csv",
    "Analysis\Observation_Metrics.csv",
    "Analysis\Findings_Register.csv",
    "AI_Audit_Task2.md",
    "AI_Critique_Task2.md",
    "Demo_Video_Link.md",
    "git-commit-log.txt"
)

foreach ($relativePath in $requiredFiles) {
    $null = Read-RequiredFile $relativePath
}

$missingData = Read-RequiredFile "Missing_Data_and_Followup.md"
$confirmedMissingMode = $false
if ($null -ne $missingData) {
    $confirmedMissingChecks = @(
        "HUMAN_REVIEWED.*CONFIRMED_MISSING_DATA",
        "MD-06.*CONFIRMED_NOT_COLLECTED.*PILOT EVIDENCE MISSING",
        "MD-09.*CONFIRMED_NOT_COLLECTED",
        "MD-10.*CONFIRMED_NOT_COLLECTED"
    )
    $confirmedMissingMode = $true
    foreach ($pattern in $confirmedMissingChecks) {
        if ($missingData -notmatch $pattern) {
            $confirmedMissingMode = $false
            Add-Issue "Missing-data register does not contain required acknowledged state matching '$pattern'."
        }
    }
}

$roster = Read-RequiredFile "Participant_Roster.md"
if ($null -ne $roster) {
    $rosterRows = @($roster -split "\r?\n" | Where-Object { $_ -match "^\|\s*P0[1-7]\s*\|" })
    if ($rosterRows.Count -ne 7) {
        Add-Issue "Participant roster must contain exactly seven rows P01-P07; found $($rosterRows.Count)."
    }

    foreach ($id in @("P01", "P02", "P03", "P04", "P05", "P06", "P07")) {
        $rowsForId = @($rosterRows | Where-Object { $_ -match "^\|\s*$id\s*\|" })
        if ($rowsForId.Count -ne 1) {
            Add-Issue "Roster must contain $id exactly once."
            continue
        }
        $row = $rowsForId[0]
        if ($row -match "<REQUIRED_REAL_DATA>|UNVERIFIED") {
            Add-Issue "$id roster row still contains a placeholder or UNVERIFIED status."
        }
        if ($row -notmatch "\*{4}") {
            Add-Issue "$id contact does not visibly mask four middle characters/digits."
        }
        if ($row -notmatch "\|\s*(?:COMPLETED|HUMAN_REVIEWED)\s*\|?\s*$") {
            Add-Issue "$id roster status must be COMPLETED or HUMAN_REVIEWED."
        }
    }
}

$pilot = Read-RequiredFile "Pilot_Session.md"
if ($null -ne $pilot) {
    $pilotComplete = $pilot -match '\*\*Status:\*\*\s*`?COMPLETED`?'
    $pilotConfirmedMissing = $confirmedMissingMode -and $pilot -match "PILOT EVIDENCE MISSING.*CONFIRMED_NOT_COLLECTED"
    if ($pilot -match "<REQUIRED_REAL_DATA>") {
        Add-Issue "Pilot session contains an unresolved real-data placeholder."
    }
    if (-not $pilotComplete -and -not $pilotConfirmedMissing) {
        Add-Issue "Pilot must be COMPLETED or explicitly CONFIRMED_NOT_COLLECTED in the missing-data register."
    }
    if ($pilotConfirmedMissing) {
        Add-Limitation "Pilot was not collected; its protocol/refinement fields remain unverified by design."
    }
    if ($pilot -notmatch "Refinement decision") {
        Add-Issue "Pilot refinement decision section is missing."
    }
}

$expectedIds = @("P01", "P02", "P03", "P04", "P05", "P06", "P07")
foreach ($id in $expectedIds) {
    $relativePath = "Sessions\Session_$id.md"
    $session = Read-RequiredFile $relativePath
    if ($null -eq $session) {
        continue
    }

    if ($session -match "<REQUIRED_REAL_DATA>|(?<!NOT_)\bUNVERIFIED\b") {
        Add-Issue "$id session still contains a placeholder or UNVERIFIED status."
    }
    $sessionClosed = $session -match '\*\*Status:\*\*\s*`?(?:COMPLETED|HUMAN_REVIEWED)`?' -or
        ($session -match '## 12\. Verification status' -and $session -match '(?m)^`HUMAN_REVIEWED`\s*$')
    if (-not $sessionClosed) {
        Add-Issue "$id top-level session status must be COMPLETED or HUMAN_REVIEWED."
    }
    foreach ($heading in @("### Clarity", "### Error recovery", "### Speed", "### Trust")) {
        if ($session -notmatch [regex]::Escape($heading)) {
            Add-Issue "$id is missing required probe heading '$heading'."
        }
    }
    foreach ($requiredLabel in @(
        "Date/time(?:, nếu quan sát được)?",
        "Device:",
        "OS:",
        "Browser/version:",
        "Total task time:",
        "Wrong turns",
        "Errors",
        "Hesitations",
        "Task-directed interventions",
        "Screen recording"
    )) {
        if ($session -notmatch $requiredLabel) {
            Add-Issue "$id is missing required field '$requiredLabel'."
        }
    }

    $rawLine = @($session -split "\r?\n" | Where-Object { $_ -match "^\|\s*Response .*\|" })
    if ($rawLine.Count -ne 1) {
        Add-Issue "$id must contain exactly one raw SUS response row."
    }
    else {
        $cells = @($rawLine[0].Split("|") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" })
        $responses = @($cells | Select-Object -Skip 1)
        if ($responses.Count -ne 10) {
            Add-Issue "$id raw SUS row must contain exactly ten responses; found $($responses.Count)."
        }
        else {
            foreach ($response in $responses) {
                if ($response -notmatch "^[1-5]$") {
                    Add-Issue "$id raw SUS response '$response' is not an integer from 1 to 5."
                }
            }
        }
    }

    if ($session -match "(?i)\bSIMULATED\b|\bSIMULATED\b|Lumiere") {
        Add-Issue "$id contains simulated/other-SUT language prohibited by the skill."
    }

    if ($session -match "NOT_RECORDED|NOT_OBSERVABLE") {
        Add-Limitation "Session environment, consent, speech/probe or timing details that are absent from source evidence remain explicitly NOT_RECORDED/NOT_OBSERVABLE."
    }
}

$susInputPath = Join-Path $TaskRoot "Analysis\SUS_Raw_Responses.csv"
if (Test-Path -LiteralPath $susInputPath -PathType Leaf) {
    $susRows = @(Import-Csv -LiteralPath $susInputPath)
    if ($susRows.Count -ne 7) {
        Add-Issue "SUS CSV must contain exactly seven rows; found $($susRows.Count)."
    }
    foreach ($id in $expectedIds) {
        $row = @($susRows | Where-Object { $_.participant_id -eq $id })
        if ($row.Count -ne 1) {
            Add-Issue "SUS CSV must contain $id exactly once."
            continue
        }
        if ($row[0].status -notin @("COMPLETED", "COMPLETED_USER_PROVIDED")) {
            Add-Issue "$id SUS CSV status must be COMPLETED or COMPLETED_USER_PROVIDED."
        }
        if ($row[0].status -eq "COMPLETED_USER_PROVIDED") {
            Add-Limitation "SUS contains seven complete user-provided response sets; collection is not visible in the supplied recordings."
        }
        for ($question = 1; $question -le 10; $question++) {
            $value = [string]$row[0].("Q$question")
            if ($value -notmatch "^[1-5]$") {
                Add-Issue "$id SUS CSV Q$question is not a genuine integer from 1 to 5."
            }
        }
    }
}

foreach ($document in @(
    "Usability_Findings.md",
    "Usability_Bug_Report.md",
    "Usability_Test_Summary.md",
    "Evidence_Index.md",
    "AI_Audit_Task2.md",
    "Demo_Video_Link.md",
    "git-commit-log.txt"
)) {
    $content = Read-RequiredFile $document
    if ($null -ne $content -and $content -match "<REQUIRED_REAL_DATA>|UNVERIFIED|READY_FOR_FIELDWORK") {
        Add-Issue "$document is not final: it contains a placeholder or non-complete status."
    }
}

$critique = Read-RequiredFile "AI_Critique_Task2.md"
if ($null -ne $critique) {
    if ($critique -notmatch '\*\*Status:\*\* `HUMAN_REVIEWED`') {
        Add-Issue "AI critique has not been marked HUMAN_REVIEWED."
    }
    $critiqueBody = ($critique -split "## Review confirmation")[0]
    $critiqueBody = $critiqueBody -replace '(?m)^#.*$', '' -replace '(?m)^\*\*.*$', ''
    $wordCount = [regex]::Matches($critiqueBody, "[\p{L}\p{M}\p{N}]+(?:[-'][\p{L}\p{M}\p{N}]+)*").Count
    if ($wordCount -lt 200 -or $wordCount -gt 300) {
        Add-Issue "AI critique body must contain 200-300 words; validator counted $wordCount."
    }
}

$results = Read-RequiredFile "Analysis\SUS_Results.md"
if ($null -ne $results) {
    foreach ($statistic in @("Mean", "Median", "Minimum", "Maximum")) {
        if ($results -notmatch "\|\s*$statistic\s*\|\s*[0-9]+(?:\.[0-9]+)?\s*\|") {
            Add-Issue "SUS results do not contain a numeric $statistic."
        }
    }
}

if ($issues.Count -gt 0) {
    Write-Output "VALIDATION_FAILED: package closure gate found $($issues.Count) unresolved issue(s)."
    foreach ($issue in $issues) {
        Write-Output " - $issue"
    }
    exit 2
}

if ($RequireCompleteEvidence -and $limitations.Count -gt 0) {
    Write-Output "INCOMPLETE_EVIDENCE: strict fieldwork gate found $($limitations.Count) acknowledged limitation(s)."
    foreach ($limitation in $limitations) {
        Write-Output " - $limitation"
    }
    Write-Output "No missing participant data was reconstructed."
    exit 2
}

if ($limitations.Count -gt 0) {
    Write-Output "COMPLETE_WITH_DISCLOSED_LIMITATIONS: package closure gate passed with $($limitations.Count) acknowledged limitation(s)."
    foreach ($limitation in $limitations) {
        Write-Output " - $limitation"
    }
    Write-Output "Strict evidence status remains INCOMPLETE_EVIDENCE; no pilot, consent, probe, environment or participant data was fabricated."
    exit 0
}

Write-Output "COMPLETE: pilot, exactly seven real sessions, SUS, probes, findings, evidence, bugs, audit, critique, demo link, and commit log passed validation."
exit 0

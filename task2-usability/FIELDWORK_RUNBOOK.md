# Fieldwork Runbook

This is the execution order for the student. Do not skip directly to analysis.

## A. Before recruitment

1. Confirm in writing that no group member uses the same primary flow.
2. Freeze the SUT commit/build and record it in the plan.
3. Choose one browser/device baseline for all official sessions unless cross-device variation is an explicit study factor.
4. Verify screen capture works without exposing notifications or personal tabs.
5. Keep the unmasked contact list outside Git; only the masked roster belongs in this repository.

Suggested commit:

```powershell
git add -- "task2-usability"
git commit -m "task2: prepare usability study protocol"
```

## B. Recruit eight separate people

- One real person for `PILOT-01`.
- Seven other real people for `P01`–`P07`.
- No person appears twice.
- Screen-recording consent is required for an official session; audio remains optional.

Do not commit the unmasked verification list.

## C. Run the pilot first

1. Complete consent.
2. Run the flow with Card A and the moderator guide.
3. Complete SUS and four probes as a rehearsal.
4. Record timing/protocol problems.
5. Write the exact refinement decision.
6. Freeze the final protocol before P01.

Suggested commit:

```powershell
git add -- "task2-usability/Pilot_Session.md" "task2-usability/Instruments"
git commit -m "task2: complete pilot and freeze protocol"
```

Pilot responses never enter `Analysis/SUS_Raw_Responses.csv`.

## D. Run P01–P07

For each participant:

1. Create the session-specific Card A alias and unique email.
2. Confirm consent before recording.
3. Read the opening and scenario verbatim.
4. Start timing on the first participant action.
5. Record timestamps, wrong turns, errors, hesitations, and exact interventions.
6. Use Card B only after the declared stuck threshold.
7. Stop timing when the participant declares completion.
8. Perform the researcher-only persistence/logout check.
9. Collect raw SUS Q1–Q10 before probes.
10. Ask Clarity, Error Recovery, Speed, and Trust probes.
11. Save evidence under the participant ID.
12. Review the session against evidence, then change its status to `COMPLETED`.
13. Enter the same raw SUS and behavioural metrics into the analysis CSV files.

Commit each session separately, for example:

```powershell
git add -- "task2-usability/Sessions/Session_P01.md" "task2-usability/evidence/P01" "task2-usability/Analysis"
git commit -m "task2: record genuine usability session P01"
```

Repeat with the matching ID through P07. Do not backdate, squash, or fabricate session commits.

## E. Analyse only after all seven sessions

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/analyze-sus.ps1"
```

Then:

1. Verify every generated score manually from its raw row.
2. Compute behavioural summaries from the seven genuine session files.
3. Cluster evidence without discarding isolated or contradictory observations.
4. Assign S1–S4 severity from impact and recovery.
5. Distinguish usability issues from reproducible software bugs.
6. Give every finding participant IDs, timestamps, evidence, a recommendation, and a retest criterion.

Suggested commit:

```powershell
git add -- "task2-usability/Analysis" "task2-usability/Usability_Findings.md"
git commit -m "task2: analyse SUS and usability findings"
```

## F. Report bugs

For every confirmed software bug:

1. Reproduce after the session.
2. Remove participant identity from the screenshot/clip.
3. Search existing Task 1/GitHub issues.
4. Create a new GitHub Issue or link the existing issue.
5. Update the bug report, finding, summary, and evidence index with the issue URL.

Suggested commit:

```powershell
git add -- "task2-usability/Usability_Bug_Report.md" "task2-usability/github-issues" "task2-usability/evidence"
git commit -m "task2: report confirmed usability-study bugs"
```

## G. Final submission gate

1. Complete the summary with genuine aggregate values.
2. Review the AI critique in your own voice and mark it `HUMAN_REVIEWED`.
3. Complete the AI audit with later interactions.
4. Add the demo-video link.
5. Export the commit log.
6. Run the completion validator.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/export-commit-log.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/validate-usability.ps1"
```

Submit as complete only when the validator prints `COMPLETE`.

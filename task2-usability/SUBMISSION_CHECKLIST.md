# Task 2 Submission Checklist

**Student:** Äáº·ng ÄÄƒng Khoa â€” 23127207  
**Prepared:** 2026-07-29, Asia/Bangkok (UTC+7)  
**Local artefact state:** `STRUCTURALLY_READY_WITH_DISCLOSED_LIMITATIONS`

## Completed locally

- [x] Seven official participant mappings P01â€“P07.
- [x] Replacement P06/HÃ¢n used; old duplicate excluded.
- [x] Masked-contact participant verification appendix prepared.
- [x] Seven session reports with T0â€“T11 and outcome coding.
- [x] Observation metrics CSV and cross-participant calculations.
- [x] SUS raw/score files explicitly report 0/7 response sets.
- [x] Six prioritized findings with participant/timestamp traceability.
- [x] Two software-bug candidates separated from usability findings.
- [x] Two local GitHub issue drafts.
- [x] Evidence index, missing-data report and video-quality report.
- [x] AI audit and 200â€“300-word critique draft.
- [x] Main report in Markdown and PDF.
- [x] AI audit and critique in Markdown and PDF.
- [x] PII-free local demo MP4.
- [x] Git history export.
- [x] Task 2 ZIP package.

## Student-only actions before upload

- [ ] Read `Task2_Main_Report.pdf` end to end and verify timestamps against the cited recordings.
- [ ] Read and revise `AI_Critique_Task2.md`; only then change its status to `HUMAN_REVIEWED`, add review date/signature to the critique and AI audit, and regenerate both PDFs.
- [ ] Confirm whether each participant was outside the HW03 class. This condition is `NOT_RECORDED`; do not mark it true without real verification.
- [ ] Decide with the instructor how to disclose the absence of pilot, consent evidence, SUS and probes. These cannot be repaired honestly from the current data.
- [ ] Independently reproduce each software bug with test-only credentials and search for duplicate GitHub issues.
- [ ] Prepare privacy-safe screenshots. Do not attach raw participant frames containing PII or plaintext passwords.
- [ ] Human-review the drafts in `github-issues/`, publish or update the real issues, and insert the final URLs into the reports.
- [ ] Upload `demo/Task2_Usability_Skill_Demo.mp4`, verify signed-out access, and update `Demo_Video_Link.md`.
- [ ] Regenerate PDFs, commit log and ZIP after any student edits.

## Missing evidence that must remain disclosed

| Rubric/data item | Current state | Honest treatment |
|---|---|---|
| Pilot | Confirmed not collected | Keep `PILOT EVIDENCE MISSING` |
| SUS Q1â€“Q10 | Confirmed not collected | Keep scores/aggregates `NOT_CALCULABLE` |
| Post-session probes | Confirmed not collected | Keep clarity/recovery/speed/trust `NOT_RECORDED` |
| Consent evidence | Confirmed unavailable | Do not claim recorded consent |
| Outside-class eligibility | Not recorded | Verify from participants or disclose |
| Usable speech/quotes | 0/7 | Do not create quotes or intervention counts |
| Redacted participant screenshots | Not created | Redact safely before sharing or omit |
| Published GitHub URLs | Not created | Add only after actual publication |
| Public demo URL | Not created | Add only after actual upload/access test |

## Submission privacy gate

- [ ] ZIP contains no raw recordings.
- [ ] ZIP contains no unmasked phone numbers.
- [ ] Public repository contains no real participant names/contacts.
- [ ] `Participant_Roster.md` is sent only through the private grading channel.
- [ ] No screenshot or clip exposes a password, email, address, name or full phone number.

## Final command sequence

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/analyze-sus.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/validate-submission-files.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/export-commit-log.ps1"
```

Do not edit the anti-fabrication validator to force `COMPLETE`; its expected refusal documents the genuine collection gaps.


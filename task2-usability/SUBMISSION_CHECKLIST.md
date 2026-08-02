# Task 2 Submission Checklist

**Student:** Đặng Đăng Khoa — 23127207
**Prepared:** 2026-07-29, Asia/Bangkok (UTC+7)
**Local artefact state:** `COMPLETE_WITH_DISCLOSED_LIMITATIONS`

## Completed locally

- [x] Seven official participant mappings P01–P07.
- [x] Replacement P06 used; old duplicate excluded.
- [x] Masked-contact participant verification appendix prepared.
- [x] Seven session reports with T0–T11 and outcome coding.
- [x] Observation metrics CSV and cross-participant calculations.
- [x] SUS raw/score files contain and calculate 7/7 user-provided response sets for P01–P07.
- [x] Seven severity-ranked findings; participant findings retain participant/timestamp traceability and the supplemental technical bug is labelled frequency N/A.
- [x] Two participant-evidenced software bugs plus one technical-only software bug, all separated from usability issues.
- [x] Three local GitHub issue drafts/canonical links.
- [x] Evidence index, missing-data report and video-quality report.
- [x] AI audit and 200–300-word critique human-reviewed on 2026-08-02.
- [x] Main report in Markdown and PDF.
- [x] AI audit and critique in Markdown and PDF.
- [x] Public YouTube demo link verified; student confirmed local MP4 is not required.
- [x] Git history export.
- [x] Package completion gate passes as `COMPLETE_WITH_DISCLOSED_LIMITATIONS`; strict fieldwork audit remains honestly `INCOMPLETE_EVIDENCE`.
- [ ] Task 2 ZIP package — no current ZIP exists.

## Student-only actions before upload

- [x] Student confirmed review of report timestamps/coding on 2026-08-02.
- [x] Student reviewed and approved `AI_Critique_Task2.md` and `AI_Audit_Task2.md` on 2026-08-02; confirmation is recorded in both artefacts.
- [x] Participant/SUS IDs standardized to P01–P07 following user confirmation on 2026-08-02.
- [x] Student human-reviewed SUS provenance on 2026-08-02; missing pilot, consent evidence and probes remain disclosed.
- [x] Independently reproduced all three software bugs with synthetic data; duplicate search completed.
- [x] Three privacy-safe reproduction screenshots created; no raw participant frame used.
- [x] Existing real issue URLs #55, #37 and #118 inserted into reports; #55/#37 evidence comments were published and verified on 2026-08-01.
- [x] Human-review #118 evidence completed; current reviewed disposition is local-only, with no claim that a fresh comment was published.
- [x] Public YouTube demo metadata verified via oEmbed on 2026-08-02 and recorded in `Demo_Video_Link.md`.
- [x] YouTube-link-only demo submission confirmed; no local MP4 restore/export action remains.
- [ ] Regenerate commit log and ZIP after final repository edits; PDFs were regenerated after human-review status updates.

## Missing evidence that must remain disclosed

| Rubric/data item | Current state | Honest treatment |
|---|---|---|
| Pilot | Confirmed not collected | Keep `PILOT EVIDENCE MISSING` |
| SUS Q1–Q10 | 7/7 sets supplied and identified as P01–P07 | Report participant scores with `COMPLETED_USER_PROVIDED` provenance; retain disclosure that collection is not visible in recordings |
| Post-session probes | Confirmed not collected | Keep clarity/recovery/speed/trust `NOT_RECORDED` |
| Consent evidence | Confirmed unavailable | Do not claim recorded consent |
| Usable speech/quotes | 0/7 | Do not create quotes or intervention counts |
| Privacy-safe reproduction screenshots | Created with synthetic data | Keep participant frames private; use fresh evidence artefacts |
| Published GitHub URLs | Existing issues #55/#37 with evidence-comment permalinks; canonical #118 linked without a fresh Task 2 comment | Do not create duplicates or claim the #118 comment was published |
| Public demo URL | Present and oEmbed-verified 2026-08-02; YouTube-link-only submission confirmed | Retain the verified URL; do not require or package a local MP4 |

## Submission privacy gate

- [ ] ZIP contains no raw recordings.
- [ ] ZIP contains no unmasked phone numbers.
- [ ] Public repository contains no real participant names/contacts.
- [ ] `Participant_Roster.md` is sent only through the private grading channel.
- [ ] No screenshot or clip exposes a password, email, address, name or full phone number.

## Final command sequence

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/analyze-sus.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/validate-usability.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/validate-submission-files.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/export-commit-log.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/package-submission.ps1"
```

The default gate validates honest package closure and must report `COMPLETE_WITH_DISCLOSED_LIMITATIONS`. The optional strict audit command `validate-usability.ps1 -RequireCompleteEvidence` must continue to report `INCOMPLETE_EVIDENCE`; do not alter source statuses or create replacement participant data to make strict evidence complete.


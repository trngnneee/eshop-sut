# Task 2 — Moderated Usability Evaluation

**SUT:** EShop Web Frontend
**Flow:** Đăng ký → Đăng nhập → Chỉnh sửa thông tin cá nhân → Đăng xuất
**Owner:** Đặng Đăng Khoa — 23127207
**Current gate:** `READY_FOR_FIELDWORK`
**Method:** Seven moderated, think-aloud sessions; SUS; four required post-session probes

## Current status

The planning package, instruments, session templates, analysis scripts, and completion validator are ready. The package is intentionally **not** marked `COMPLETE`: no participant identity, contact detail, quote, task time, observation, recording, or SUS response has been invented.

To move from `READY_FOR_FIELDWORK` to `COMPLETE`, the student must:

1. Confirm that this usability flow is not duplicated by another group member.
2. Recruit seven eligible real participants outside the HW03 class, plus one separate pilot participant.
3. Obtain informed consent, run the pilot, and record the refinement decision.
4. Run seven individual moderated sessions and enter the genuine raw data into `Sessions/Session_P01.md` through `Session_P07.md`.
5. Enter the same raw SUS responses in `Analysis/SUS_Raw_Responses.csv`.
6. Index the real evidence, analyse findings, and create GitHub Issues for every confirmed software bug.
7. Add the demo-video link, export the final Git commit log, and run the validator.

## Package map

| Deliverable | Purpose |
| :--- | :--- |
| `Usability_Test_Plan.md` | Objectives, method, sampling, metrics, protocol, and analysis plan |
| `Participant_Roster.md` | Exactly seven official participants; pilot is kept separate |
| `Pilot_Session.md` | Pilot record and required refinement decision |
| `Instruments/` | Consent, recruitment, scenario/data cards, SUS, probes, and moderator guide |
| `Sessions/` | Seven field-session records, one file per participant |
| `Analysis/` | Raw SUS and observation inputs; generated scoring output goes here |
| `Usability_Findings.md` | Evidence-backed usability findings and prioritisation |
| `Usability_Bug_Report.md` | Separation and traceability of software bugs |
| `Evidence_Index.md` | Recording/screenshot/notes inventory |
| `Usability_Test_Summary.md` | Submission-ready Task 2 report after real fieldwork |
| `AI_Audit_Task2.md` | AI interaction disclosure |
| `AI_Critique_Task2.md` | 200–300 word critique draft requiring human review |
| `scripts/analyze-sus.ps1` | Validates and scores seven genuine SUS response sets |
| `scripts/validate-usability.ps1` | Anti-fabrication completion gate |

## Commands

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/analyze-sus.ps1" -SelfTest
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/analyze-sus.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/validate-usability.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/export-commit-log.ps1"
```

The SUS analyser and completion validator are expected to refuse the initial templates. That refusal is correct until all genuine field data has been entered.

## Data-integrity rules

- Never replace a placeholder with guessed, AI-generated, or reconstructed data.
- Store only masked contact details in the repository; keep the unmasked verification list outside the submission repository.
- Do not record a participant's personal password. Use only a session-specific test password that the participant creates for EShop.
- Pilot data is not part of P01–P07 and is never included in the seven-person SUS aggregate.
- A session that declines required screen recording does not count as one of the seven official sessions; thank the person and recruit a replacement without pressure.
- Audio is optional and requires separate consent.
- Technical preflight and expert observations must remain labelled `PROVISIONAL`; they are not participant evidence.

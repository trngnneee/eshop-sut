# Task 2 — Moderated Usability Evaluation

**SUT:** EShop Web Frontend
**Flow:** Đăng ký → Đăng nhập → Chỉnh sửa thông tin cá nhân → Đăng xuất
**Student:** Đặng Đăng Khoa — 23127207
**Status:** `READY_FOR_HUMAN_REVIEW — CONFIRMED_MISSING_DATA`

## Submission snapshot

Task 2 đã có bảy participant mappings P01–P07, bảy session reports, metrics, findings, software-bug report, hai GitHub issue drafts, AI audit, AI critique draft, main report Markdown/PDF, local demo MP4 và checklist nộp bài. Replacement P06 đã thay file trùng cũ; official analysis hiện có bảy recording độc lập.

Kết quả chính:

- 7/7 `FAILED_OR_ABANDONED` theo tiêu chí SC1–SC5.
- Captured task time tính được cho 6/7; median 80 giây, range 50–136 giây.
- `BUG-PF-02`: 3/7, S1.
- `BUG-AUTH-PLAINTEXT-01`: 5/7, S2.
- SUS: 0/7 response sets, mọi aggregate `NOT_CALCULABLE`.

## Start here

1. Đọc `Task2_Main_Report.md` hoặc `Task2_Main_Report.pdf`.
2. Kiểm tra submission-only verification appendix trong `Participant_Roster.md`; không đăng roster công khai.
3. Đọc và tự sửa `AI_Critique_Task2.md`, rồi chỉ chính sinh viên mới đổi status thành `HUMAN_REVIEWED`.
4. Dùng `SUBMISSION_CHECKLIST.md` để hoàn thành các hành động bên ngoài repository.

## Package map

| Deliverable | Purpose |
|---|---|
| `Task2_Main_Report.md` / `.pdf` | Báo cáo tổng hợp để chấm |
| `Participant_Roster.md` | Tên được cung cấp và contact đã mask; submission-only |
| `Usability_Test_Plan.md` | Objectives, protocol, criteria và analysis plan |
| `Pilot_Session.md` | Disclosure rằng pilot evidence không được thu thập |
| `Sessions/` | Bảy field-session records, P01–P07 |
| `Analysis/` | Observation metrics, raw SUS state, scores và findings register |
| `Usability_Findings.md` | Detailed evidence-backed findings |
| `Usability_Bug_Report.md` | Software-bug separation và traceability |
| `github-issues/` | Local drafts; chưa được publish |
| `Evidence_Index.md` | Recording/evidence inventory và privacy state |
| `Missing_Data_and_Followup.md` | Confirmed missing data và release blockers |
| `Video_Data_Quality_Report.md` | Decode, completeness, audio và privacy review |
| `AI_Audit_Task2.md` / `.pdf` | AI interaction disclosure |
| `AI_Critique_Task2.md` / `.pdf` | 200–300-word critique draft |
| `demo/Task2_Usability_Skill_Demo.mp4` | Local PII-free demo, 72 giây |
| `Demo_Video_Link.md` | Upload/public-link state |
| `git-commit-log.txt` | Exported commit history |
| `SUBMISSION_CHECKLIST.md` | Final handoff and integrity checklist |

## Validation

From the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/analyze-sus.ps1" -SelfTest
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/analyze-sus.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/validate-usability.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/validate-submission-files.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/export-commit-log.ps1"
```

The anti-fabrication completion validator is expected to reject a “COMPLETE” claim because pilot, SUS, consent, eligibility and probes were genuinely not collected. This is an evidence limitation, not a reason to create replacement data. The structural validator checks whether the disclosed submission package is internally consistent and present.

## Privacy and integrity

- Analytical reports use P01–P07 and D01–D07 only.
- The roster contains masked contacts and must stay in a private Moodle/TA submission.
- Raw participant screenshots/clips are not exported because recordings contain PII and, in several sessions, plaintext passwords.
- Technical preflight is not participant evidence.
- No participant quote, SUS response, consent record, pilot result or intervention count has been invented.
- GitHub issues remain drafts until human review, independent reproduction, duplicate search and safe screenshot preparation.

## Conservative self-assessment

| Area | Evidence state |
|---|---|
| Seven unique participant recordings | Present and mapped |
| Session coding and traceability | Present; human timestamp review remains |
| Metrics and findings | Present within observable evidence |
| Pilot | Confirmed not collected |
| SUS / post-session probes | Confirmed not collected |
| Consent / outside-class verification | Not recorded in supplied artefacts |
| Published GitHub issues with redacted screenshots | Not yet completed |
| Public demo URL | Local MP4 ready; upload required |
| AI critique human declaration | Student action required |

This package is therefore submission-ready as an honest evidence record, but it cannot truthfully satisfy rubric rows that require data or external actions that never occurred.

# Task 2 — Moderated Usability Evaluation

**SUT:** EShop Web Frontend
**Flow:** Đăng ký → Đăng nhập → Chỉnh sửa thông tin cá nhân → Đăng xuất
**Student:** Đặng Đăng Khoa — 23127207
**Status:** `COMPLETE_WITH_DISCLOSED_LIMITATIONS — HUMAN_REVIEWED — CONFIRMED_MISSING_DATA — PUBLIC_DEMO_VERIFIED`

## Submission snapshot

Task 2 đã có bảy participant mappings P01–P07, bảy session reports, metrics, severity-ranked findings, software-bug report, ba local GitHub issue drafts/canonical links, AI audit, AI critique đã human-review, main report Markdown/PDF và checklist nộp bài. Replacement P06 đã thay file trùng cũ; official analysis hiện có bảy recording độc lập. Public YouTube demo đã được xác minh qua oEmbed ngày 2026-08-02; sinh viên xác nhận chỉ cần link YouTube và không yêu cầu repository-local MP4.

Kết quả chính:

- 7/7 `FAILED_OR_ABANDONED` theo tiêu chí SC1–SC5.
- Captured task time tính được cho 6/7; median 80 giây, range 50–136 giây.
- `BUG-PF-02`: 3/7, S1.
- `BUG-AUTH-PLAINTEXT-01`: 5/7, S2.
- `BUG-REG-PASSWORD-POLICY-01`: N/A participant frequency, S2 provisional; direct API accepts a password missing the FR-01 allowed-special-character class and the account can log in. Canonical issue #118.
- SUS dataset do người dùng cung cấp: 7/7 response sets (`P01`–`P07`), mean 76.79, median 75, range 62.5–100; người dùng xác nhận bộ ID chính thức ngày 2026-08-02.

## Start here

1. Đọc `Task2_Main_Report.md` hoặc `Task2_Main_Report.pdf`.
2. Kiểm tra submission-only verification appendix trong `Participant_Roster.md`; không đăng roster công khai.
3. AI critique/audit và participant coding đã được sinh viên xác nhận `HUMAN_REVIEWED` ngày 2026-08-02.
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
| `github-issues/` | Ba local drafts; canonical #55/#37 có published evidence comments, #118 linked nhưng fresh Task 2 comment chưa publish |
| `../tests/test-cases/register/` / `../tests/test-summary/` | EP/BVA test case, test run và FR-01 traceability cho supplemental software bug |
| `Evidence_Index.md` | Recording/evidence inventory và privacy state |
| `Missing_Data_and_Followup.md` | Confirmed missing data và release blockers |
| `Video_Data_Quality_Report.md` | Decode, completeness, audio và privacy review |
| `AI_Audit_Task2.md` / `.pdf` | AI interaction disclosure |
| `AI_Critique_Task2.md` / `.pdf` | 200–300-word critique đã human-review |
| `Demo_Video_Link.md` | Public YouTube link đã xác minh; đây là demo artefact bắt buộc duy nhất |
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
powershell -NoProfile -ExecutionPolicy Bypass -File "task2-usability/scripts/package-submission.ps1"
```

The default completion gate closes the package as `COMPLETE_WITH_DISCLOSED_LIMITATIONS` when every absent item is explicitly acknowledged and all available evidence passes validation. It exits successfully without converting missing pilot, consent, probes, environment metadata or separately supplied SUS into recorded fieldwork evidence. Use `-RequireCompleteEvidence` only for the stricter fieldwork-evidence audit; that mode truthfully returns `INCOMPLETE_EVIDENCE` for the confirmed collection gaps.

## Privacy and integrity

- Analytical reports use P01–P07 and D01–D07 only.
- The roster contains masked contacts and must stay in a private Moodle/TA submission.
- Raw participant screenshots/clips are not exported because recordings contain PII and, in several sessions, plaintext passwords.
- Independent technical reproduction is not participant evidence and never increases P01–P07 frequency.
- No participant quote, consent record, pilot result or intervention count has been invented; SUS responses are retained exactly as supplied by the user.
- Duplicate search linked canonical issues #55, #37 and #118; only #55/#37 have published Task 2 evidence comments. #118 evidence đã human-review và được giữ local-only theo current disposition.

## Conservative self-assessment

| Area | Evidence state |
|---|---|
| Seven unique participant recordings | Present and mapped |
| Session coding and traceability | Present; human review confirmed 2026-08-02 |
| Metrics and findings | Present within observable evidence |
| Pilot | Confirmed not collected |
| SUS | 7/7 user-provided sets mapped to P01–P07; collection not visible in recordings |
| Post-session probes | Confirmed not collected |
| Consent verification | Not recorded in supplied artefacts |
| Published GitHub issues with redacted screenshots | #55/#37 comments published; #118 canonical issue linked, fresh Task 2 evidence comment not published |
| Public demo URL | Present and oEmbed-verified 2026-08-02; YouTube-link-only submission confirmed |
| AI critique human declaration | `HUMAN_REVIEWED` — confirmed 2026-08-02 |

The analytical package and public demo link are human-reviewed and `COMPLETE_WITH_DISCLOSED_LIMITATIONS`. Rubric rows that require pilot, consent or probes remain unsupported because those activities did not occur; this limitation is an accepted closure state, not an instruction to reconstruct data.

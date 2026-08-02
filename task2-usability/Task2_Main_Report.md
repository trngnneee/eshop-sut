# Task 2 — Usability Evaluation Submission Report

**Student:** Đặng Đăng Khoa
**Student ID:** 23127207
**System under test:** EShop Web Frontend
**Evaluated flow:** Đăng ký → Đăng nhập → Chỉnh sửa thông tin cá nhân → Đăng xuất
**Report updated/timezone:** 2026-08-02 — Asia/Bangkok (UTC+7)
**Evidence status:** `COMPLETE_WITH_DISCLOSED_LIMITATIONS — HUMAN_REVIEWED — CONFIRMED_MISSING_DATA`

## Submission statement

Báo cáo này tổng hợp trung thực bảy recording chính thức P01–P07. Replacement P06 đã thay source trùng cũ và old duplicate không được tính. Tên thật và liên hệ đã che nằm riêng trong `Participant_Roster.md`; các báo cáo phân tích chỉ dùng participant ID. SUS không xuất hiện trong recording nhưng người dùng đã cung cấp riêng 7/7 bộ Q1–Q10 và xác nhận ngày 2026-08-02 rằng các bộ này dùng participant ID P01–P07. Pilot, consent supplement, post-session probes và usable participant speech vẫn được giữ `NOT_RECORDED` hoặc `NOT_OBSERVABLE`, không được nội suy.

## Executive result

- 7/7 official recordings là nguồn độc lập sau replacement; 7/7 decode thành công.
- 0/7 hoàn thành độc lập; 0/7 hoàn thành với hỗ trợ; 7/7 được phân loại `FAILED_OR_ABANDONED` vì không phiên nào đạt đủ SC1–SC5.
- 6/7 có captured task time tính được: median 80 giây, min 50 giây, max 136 giây.
- Observed lower bound: 17 errors, 1 wrong turn, 2 hesitations từ 5 giây trở lên với tổng 10 giây.
- Hai software-bug candidates có participant evidence: `BUG-PF-02` (3/7, S1) và `BUG-AUTH-PLAINTEXT-01` (5/7, S2). Một supplemental technical bug không có participant frequency là `BUG-REG-PASSWORD-POLICY-01` (N/A, S2 provisional).
- SUS dataset P01–P07: 7/7 complete user-provided response sets; mean 76.79, median 75, min 62.5, max 100.

## Method and success criteria

Phân tích dùng screen recording và timestamp `HH:MM:SS`. Các milestone T0–T11 được coding riêng cho từng participant. Technical preflight chỉ dùng để hiểu hệ thống, không được tính là participant evidence. Một phiên chỉ hoàn thành khi đạt toàn bộ:

1. SC1 — tạo account thành công.
2. SC2 — đăng nhập thành công bằng account vừa tạo.
3. SC3 — cập nhật đủ name, phone và address.
4. SC4 — dữ liệu cập nhật còn tồn tại sau reload/revisit.
5. SC5 — logout có behavioral success.

## Dataset and data quality

| Participant | Source alias | Completeness | Main limitation |
|---|---|---|---|
| P01 | D01 | Complete-looking | Audio silence; thiếu probes/intervention/persistence; SUS supplied separately |
| P02 | D02 | Complete; task end đã xác nhận | Ends on phone-validation alert |
| P03 | D03 | Entire session đã xác nhận | Chỉ 4,369 giây; T0 và phần lớn metrics không quan sát được |
| P04 | D04 | Complete-looking | Không usable speech; thiếu probes/persistence; SUS supplied separately |
| P05 | D05 | Complete; task end đã xác nhận | Ends at login before submit/result |
| P06 | D06 replacement | Complete; task end đã xác nhận | Ends on repeated weak-password error |
| P07 | D07 | Complete-looking | Không profile update; audio silence |

Thông tin xác minh submission-only, gồm tên được cung cấp và contact đã mask bốn chữ số giữa, nằm trong `Participant_Roster.md`. Evidence consent không được ghi nhận trong artefacts hiện có.

## Success criteria by participant

| Participant | SC1 account | SC2 login | SC3 update all fields | SC4 persistence | SC5 logout | Outcome |
|---|---|---|---|---|---|---|
| P01 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |
| P02 | PASS | PASS | FAIL | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P03 | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P04 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |
| P05 | PASS | FAIL | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P06 | FAIL | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P07 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |

Behavioral logout PASS không chứng minh token/storage deletion; auth storage state vẫn `NOT_OBSERVABLE`.

## Observed metrics

| Participant | Outcome | Task time | Wrong turns | Errors | Hesitations ≥5 s | SUS |
|---|---|---:|---:|---:|---:|---|
| P01 | FAILED_OR_ABANDONED | 111 s | 0 | 5 | 0 | 82.5 |
| P02 | FAILED_OR_ABANDONED | 94 s | NOT_OBSERVABLE | 3 | 1 | 75 |
| P03 | FAILED_OR_ABANDONED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | 100 |
| P04 | FAILED_OR_ABANDONED | 136 s | 1 | 4 | 0 | 65 |
| P05 | FAILED_OR_ABANDONED | 50 s | NOT_OBSERVABLE | 0 | 0 | 62.5 |
| P06 | FAILED_OR_ABANDONED | 52 s | 0 | 4 | 0 | 65 |
| P07 | FAILED_OR_ABANDONED | 66 s | 0 | 1 | 1 | 87.5 |

Không báo cáo seven-person median cho metric bị thiếu. Card B, moderator interventions và think-aloud reminders là `NOT_OBSERVABLE`, không được mặc định bằng 0.

## Prioritized findings

| Rank | Finding | Frequency | Severity | Recommendation |
|---:|---|---:|---:|---|
| 1 | `BUG-PF-02` — phone validation trái FR-04 | 3/7 | S1 | Cho phép 10–11 chữ số bắt đầu bằng 0; đồng bộ validator và error copy; retest persistence |
| 2 | `UF-PHONE-RECOVERY-01` — feedback dẫn tới repeated attempts | 3/7 | S1 | Feedback theo field và nêu đúng accepted format |
| 3 | `BUG-AUTH-PLAINTEXT-01` — login password hiển thị plaintext | 5/7 | S2 | Mask mặc định; reveal phải explicit và reversible; kiểm tra browser matrix |
| 4 | `BUG-REG-PASSWORD-POLICY-01` — API chấp nhận password thiếu allowed special character | N/A — technical only | S2 provisional | Enforce FR-01 tại backend; direct-API EP/BVA regression |
| 5 | `UF-REG-PASSWORD-RECOVERY-01` — password-policy recovery lặp lại | 2/7 | S2 | Live policy checklist và state-specific feedback |
| 6 | `UF-LOGIN-IDENTIFIER-01` — “Username” không nói rõ cần full email | 1/7 | S3 | Dùng nhãn Email và copy đăng nhập tiếng Việt |
| 7 | `UF-PASSWORD-MANAGER-DETOUR-01` | 1/7 | S4 | Rà soát autocomplete semantics và password-manager integration |

Chi tiết evidence timestamps, impact, contradictory evidence và acceptance criteria nằm trong `Usability_Findings.md`, `Usability_Bug_Report.md` và `Analysis/Findings_Register.csv`.

## Bugs and publication status

Hai participant-evidenced defects đã được fresh-reproduce ngày 2026-07-31 bằng synthetic data và screenshot an toàn trong `evidence/github-issue-reproduction/`. Duplicate search tìm thấy existing issue #55 cho BUG-PF-02 và #37 cho BUG-AUTH-PLAINTEXT-01; evidence được host tại commit `d9bc4c0` và publish ngày 2026-08-01 trong comments `#issuecomment-5149476574` và `#issuecomment-5149476796`.

Ngày 2026-08-02, supplemental direct-API EP/BVA test xác nhận `BUG-REG-PASSWORD-POLICY-01`: `POST /api/register` trả 200 cho synthetic password có uppercase/lowercase/digit nhưng thiếu allowed special character, và account đó login được. Frontend regex controls pass 13/13, nên defect là backend enforcement bypass. GitHub duplicate search tìm thấy canonical issue #118; không tạo issue mới. Fresh Task 2 evidence comment cho #118 chưa publish. Finding này có frequency `N/A` và không được gán cho P04/P06 vì session password bị masked. Participant recordings vẫn không được xuất frame thô vì có PII/plaintext password.

## SUS and qualitative probes

Người dùng cung cấp 70 raw responses cho P01–P07; tất cả hợp lệ trong thang 1–5. Điểm SUS lần lượt là 82.5, 75, 100, 65, 62.5, 65 và 87.5; mean 76.79, median 75, minimum 62.5 và maximum 100. Người dùng xác nhận participant IDs ngày 2026-08-02; provenance vẫn là `COMPLETED_USER_PROVIDED` vì phần thu thập không xuất hiện trong recordings. Clarity, error recovery, speed, trust và final requested change vẫn `NOT_RECORDED`; behavioral observations không được trình bày như participant quotes hoặc self-report.

## Limitations and integrity

- Pilot không được thu thập; không thể chứng minh protocol đã pilot/refine.
- Consent supplement không có evidence.
- 0/7 có usable speech; exact moderator words, quotes và interventions không thể xác minh.
- P03 chỉ dài 4,369 giây; distribution đủ bảy người không tính được.
- D02, D03, D05 và D06 kết thúc sớm nhưng người dùng xác nhận đó là toàn bộ session.
- Sample nhỏ, không ngẫu nhiên; không có claim về statistical significance hoặc generalizability.
- SUS chỉ được tính từ 70 giá trị do người dùng cung cấp cho P01–P07; không suy ra từ behavior hoặc recordings.

## Deliverable traceability

- Verification appendix: `Participant_Roster.md`
- Plan/protocol: `Usability_Test_Plan.md`, `Instruments/`
- Session coding: `Sessions/Session_P01.md`–`Session_P07.md`
- Evidence: `Stage_0_Drive_Inventory.md`, `Evidence_Index.md`, `Video_Data_Quality_Report.md`
- Metrics: `Analysis/Observation_Metrics.csv`
- SUS: `Analysis/SUS_Raw_Responses.csv`, `Analysis/SUS_Scores.csv`, `Analysis/SUS_Results.md`
- Findings and bugs: `Usability_Findings.md`, `Usability_Bug_Report.md`, `Analysis/Findings_Register.csv`, `github-issues/`
- Missing data: `Missing_Data_and_Followup.md`
- AI transparency: `AI_Audit_Task2.md`, `AI_Critique_Task2.md`
- Demo: public YouTube URL trong `Demo_Video_Link.md` đã được xác minh qua oEmbed ngày 2026-08-02; sinh viên xác nhận YouTube link là demo artefact duy nhất được yêu cầu và local MP4 không cần đóng gói.
- Submission control: `README.md`, `SUBMISSION_CHECKLIST.md`, `git-commit-log.txt`

## Final declaration

Local analytical artefacts are `COMPLETE_WITH_DISCLOSED_LIMITATIONS` and `HUMAN_REVIEWED` following student confirmation on 2026-08-02. The package-closure validator exits successfully because every unavailable fieldwork item is explicitly acknowledged; its optional strict-evidence mode remains `INCOMPLETE_EVIDENCE`. SUS has been calculated from seven user-provided response sets identified as P01–P07, and their provenance/coding has been reviewed. Missing pilot, consent and probes remain disclosed rather than reconstructed. Existing evidence comments for #55/#37 are recorded as published; #118 evidence is reviewed and retained local-only. The public YouTube demo is verified and no local MP4 is required.


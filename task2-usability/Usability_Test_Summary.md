# Task 2 — Usability Evaluation Report

**SUT:** EShop Web Frontend
**Flow:** Đăng ký → Đăng nhập → Chỉnh sửa thông tin cá nhân → Đăng xuất
**Timezone:** Asia/Bangkok (UTC+7)
**Current status:** `READY_FOR_HUMAN_REVIEW — CONFIRMED_MISSING_DATA`

## Executive summary

Mapping D01–D07→P01–P07 đã được người dùng xác nhận. Replacement D06/P06 là nguồn độc lập và old duplicate đã được supersede/loại khỏi official analysis, nên bộ chính thức hiện có 7 unique recordings. Người dùng xác nhận D02, D03, D05 và D06 là toàn bộ session, không phải file upload bị cắt; các session này thực sự kết thúc sớm trong flow. SUS, consent/eligibility supplement, post-session probes và pilot được xác nhận là không thu thập.

Theo taxonomy bắt buộc, 0/7 completed independently, 0/7 completed with assistance và 7/7 được gắn `FAILED_OR_ABANDONED`. Task end của P02, P03, P05 và P06 đã được người dùng xác nhận tại recording end. Không phiên nào đáp ứng đủ SC1–SC5.

Hai software-bug candidates có participant evidence:

1. `BUG-PF-02`: phone validation trái FR-04 ở P01/P02/P04 (3/7), ngăn required profile completion.
2. `BUG-AUTH-PLAINTEXT-01`: login password hiển thị plaintext ở P01/P02/P04/P05/P07 (5/7), gây credential exposure.

Chỉ có local GitHub issue drafts; không issue nào đã được đăng.

## 1. Objectives and method

Nghiên cứu đánh giá:

- Khả năng hiểu và hoàn thành registration/password policy.
- Chuyển từ registration sang login và tìm profile.
- Cập nhật name/phone/address, validation, error recovery và persistence.
- Task time, wrong turns, errors, repeated actions và hesitations ≥5 giây.
- Discoverability/behavioral success/trust của logout.

Phân tích dựa trên screen recordings với timestamp HH:MM:SS. Audio stream được kiểm tra nhưng không có usable speech; ASR output trên silence bị loại bỏ. Không dùng technical preflight làm participant evidence.

## 2. Data set and mapping

| Participant | File | Data quality | Outcome qualification |
|---|---|---|---|
| P01 | D01 | Complete-looking screen; audio silence | Outcome visual evidence usable; thiếu SUS/probes/intervention/persistence |
| P02 | D02 | Complete session; ends on validation alert | Task-end confirmed; failed profile update |
| P03 | D03 | Entire session confirmed; chỉ 4 giây | Task-end confirmed; phần lớn data NOT_OBSERVABLE |
| P04 | D04 | Complete-looking screen; no usable speech | Outcome visual evidence usable; thiếu SUS/probes/persistence |
| P05 | D05 | Complete session; ends at login | Task-end confirmed; login not completed |
| P06 | D06 | Replacement độc lập; complete session ends on weak-password error | Task-end confirmed; registration failed |
| P07 | D07 | Complete-looking screen; audio silence | Outcome visual evidence usable; profile update không thực hiện |

Pilot: **PILOT EVIDENCE MISSING — người dùng xác nhận không thu thập**.

## 3. Success criteria by participant

| Participant | SC1 account | SC2 login | SC3 update all fields | SC4 persistence | SC5 logout | Outcome |
|---|---|---|---|---|---|---|
| P01 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |
| P02 | PASS | PASS | FAIL | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P03 | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P04 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |
| P05 | PASS | FAIL | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P06 | FAIL | NOT_REACHED | NOT_REACHED | NOT_REACHED | NOT_REACHED | FAILED_OR_ABANDONED |
| P07 | PASS | PASS | FAIL | NOT_REACHED | PASS behavioral | FAILED_OR_ABANDONED |

Behavioral logout PASS không xác nhận token/storage deletion; auth storage state là NOT_OBSERVABLE.

## 4. Cross-participant metrics

| Participant | Outcome | Task time | Wrong turns | Errors | Hesitations ≥5 s | Task interventions | Card B | SUS |
|---|---|---:|---:|---:|---:|---|---|---|
| P01 | FAILED_OR_ABANDONED | 111 s | 0 | 5 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |
| P02 | FAILED_OR_ABANDONED | 94 s | NOT_OBSERVABLE | 3 | 1 | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |
| P03 | FAILED_OR_ABANDONED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |
| P04 | FAILED_OR_ABANDONED | 136 s | 1 | 4 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |
| P05 | FAILED_OR_ABANDONED | 50 s | NOT_OBSERVABLE | 0 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |
| P06 | FAILED_OR_ABANDONED | 52 s | 0 | 4 | 0 | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |
| P07 | FAILED_OR_ABANDONED | 66 s | 0 | 1 | 1 | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_RECORDED |

### Outcome counts

- Completed independently: 0/7.
- Completed with assistance: 0/7.
- Failed/abandoned taxonomy: 7/7; task ends đã được xác nhận cho cả bảy session.

### Time and behavior aggregates

- Total task time calculable: 6/7 (P01, P02, P04, P05, P06, P07).
- Median trong 6 calculable sessions: 80 giây.
- Min/max trong 6 calculable sessions: 50/136 giây.
- Seven-person task-time median/min/max: NOT_CALCULABLE.
- Wrong turns: observed lower bound 1; median của numeric P01/P04/P06/P07 = 0; P05 NOT_OBSERVABLE và P02/P03 NOT_OBSERVABLE, nên seven-person total/median NOT_CALCULABLE.
- Errors: observed lower bound 17; median của 6 numeric counts P01/P02/P04/P05/P06/P07 = 3,5; P03 NOT_OBSERVABLE, nên seven-person total/median NOT_CALCULABLE.
- Hesitations: 2 confirmed ở P02 và P07, tổng 10 giây; median của 6 numeric counts = 0; P03 NOT_OBSERVABLE, nên seven-person total/median NOT_CALCULABLE.
- Participant dùng Card B: NOT_OBSERVABLE; không được ghi 0 vì 7/7 thiếu usable speech.
- Moderator interventions/think-aloud reminders: NOT_OBSERVABLE.

## 5. SUS results

| Statistic | Result |
|---|---|
| Valid complete response sets | 0/7 |
| Mean | NOT_CALCULABLE |
| Median | NOT_CALCULABLE |
| Minimum | NOT_CALCULABLE |
| Maximum | NOT_CALCULABLE |

P01–P07 đều thiếu Q1–Q10 và người dùng xác nhận SUS không được thu thập. SUS giữ NOT_CALCULABLE, không được suy ra từ hành vi và không được báo cáo như phần trăm.

## 6. Findings

| Rank | Finding | Participants/frequency | Severity | Evidence | Recommendation |
|---:|---|---|---:|---|---|
| 1 | BUG-PF-02 — phone validation trái FR-04 | P01, P02, P04 — 3/7 | S1 | D01 @ 00:00:53–00:01:49; D02 @ 00:00:57–00:01:34; D04 @ 00:01:43–00:02:09 | Align validator/error copy với 10–11 digits bắt đầu bằng 0; persistence retest. |
| 2 | BUG-AUTH-PLAINTEXT-01 — password không masked | P01, P02, P04, P05, P07 — 5/7 | S2 provisional | Login intervals trong từng session report | Password input masked mặc định; explicit reversible reveal; browser matrix retest. |
| 3 | UF-PHONE-RECOVERY-01 — feedback dẫn tới repeated attempts | P01, P02, P04 — 3/7 | S1 | Cùng phone intervals; 4/2/3 repeats | Field-level accepted-format feedback sau khi sửa validator. |
| 4 | UF-REG-PASSWORD-RECOVERY-01 — repeated weak-password recovery | P04, P06 — 2/7 | S2 | D04 @ 00:00:22–00:01:01; D06 @ 00:00:22–00:00:53 | Live policy checklist và state-specific feedback; giữ password masked. |
| 5 | UF-LOGIN-IDENTIFIER-01 — `Username` không rõ là email | P07 — 1/7 | S3 | D07 @ 00:00:34–00:00:48 | Dùng `Đăng nhập`/`Email`/Vietnamese button copy. |
| 6 | UF-PASSWORD-MANAGER-DETOUR-01 | P04 — 1/7 | S4 | D04 @ 00:01:22–00:01:24 | Review autocomplete/password-manager integration. |

Không gọi các finding là “systemic”, “phổ biến” hoặc statistically significant. Login identifier impact chỉ quan sát ở P07; P01/P02/P04 là contradictory evidence vì login không có same observable error.

## 7. Software bugs and drafts

- Participant-evidenced bug candidates: 2.
- Drafts:
  - `github-issues/DRAFT-BUG-USABILITY-01.md` — BUG-PF-02.
  - `github-issues/DRAFT-BUG-AUTH-PLAINTEXT-01.md` — BUG-AUTH-PLAINTEXT-01.
- Independent reproduction: REQUIRED/PENDING.
- Duplicate search: PENDING.
- Redacted screenshot/clip: NOT_CREATED.
- New GitHub issues published: 0.

## 8. Probe synthesis

- Clarity: NOT_RECORDED for P01–P07.
- Error recovery: NOT_RECORDED for P01–P07.
- Speed: NOT_RECORDED for P01–P07.
- Trust: NOT_RECORDED for P01–P07.
- Final requested change: NOT_RECORDED for P01–P07.

Mọi qualitative impact trong findings là behavioral observation, không phải lời tự thuật của participant.

## 9. Privacy and evidence handling

- `PASSWORD_VISIBLE_IN_RECORDING — REDACTION_REQUIRED`: P01, P02, P04, P05, P07. Replacement P06 chỉ cho thấy masked registration password; name/email trên registration vẫn cần redaction.
- Name/email/phone/address xuất hiện ở registration/profile phải được che.
- Không report raw password, contact filename hoặc PII đầy đủ.
- Không có participant screenshot/clip được xuất vì chưa redaction.
- Video local analysis nằm trong ignored `analysis_assets/`; Drive không bị chỉnh sửa.

## 10. Limitations

- 7 official mappings tương ứng 7 unique recordings sau replacement; old duplicate D06 đã bị supersede và loại khỏi official analysis.
- D02/D03/D05/D06 được xác nhận là toàn bộ session nhưng kết thúc sớm trong flow; P03 chỉ dài 4,369 giây và không có observable T0.
- 0/7 có usable speech, consent, SUS hoặc post-session probes; người dùng xác nhận không có supplemental data.
- Intervention/Card B không thể quan sát; không được mặc định là 0.
- 6/7 có calculable total task time; P03 và một số full-task metrics vẫn NOT_OBSERVABLE, nên seven-person distributions không đầy đủ.
- Small non-random sample, moderated context, device/browser differences và researcher preflight exposure giới hạn khả năng generalize.
- Không có statistical significance claim.

## 11. Evidence and traceability

- Stage 0: `Stage_0_Drive_Inventory.md`.
- Session reports: `Sessions/Session_P01.md`–`Session_P07.md`.
- Evidence index: `Evidence_Index.md`.
- Raw SUS: `Analysis/SUS_Raw_Responses.csv`.
- Behavior metrics: `Analysis/Observation_Metrics.csv`.
- Findings register: `Analysis/Findings_Register.csv`.
- Detailed findings: `Usability_Findings.md`.
- Bug report: `Usability_Bug_Report.md`.
- Missing data: `Missing_Data_and_Followup.md`.
- Video quality: `Video_Data_Quality_Report.md`.

## 12. Completion declaration

`READY_FOR_HUMAN_REVIEW`

Bảy session đã được phân tích và task-end ambiguity đã được giải quyết bằng user confirmation. SUS, probes, consent/eligibility supplement và pilot được xác nhận là không thu thập nên giữ `NOT_RECORDED`/`PILOT EVIDENCE MISSING`; chúng không được tái tạo. Trước khi phát hành evidence hoặc GitHub issues vẫn cần human-review timestamps, redaction, independent bug reproduction và duplicate search.

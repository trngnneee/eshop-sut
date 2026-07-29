# Missing Data and Follow-up

**Current status:** `READY_FOR_HUMAN_REVIEW — CONFIRMED_MISSING_DATA`
**Mapping:** Đã giải quyết — D01–D07 lần lượt là P01–P07; D06 dùng replacement source
**User confirmation:** 2026-07-29 — D02, D03, D05 và D06 là toàn bộ session; SUS, consent/eligibility supplement, probes và pilot không được thu thập
**Privacy:** Chỉ dùng P01–P07/D01–D07; không ghi tên thật, số điện thoại filename hoặc PII đầy đủ

## Trạng thái dữ liệu

| ID | Dữ liệu/điểm cần xác minh | Participant | Kết luận sau xác nhận | Tác động còn lại | Trạng thái |
|---|---|---|---|---|---|
| MD-01 | Mapping D01–D07↔P01–P07 | P01–P07 | Người dùng đã xác nhận mapping một-một | Không còn mapping ambiguity | RESOLVED |
| MD-02 | D06 cũ là duplicate của D01 | P06 | Replacement D06 có hash khác D01 và full-decode PASS | Old duplicate bị loại khỏi official analysis | RESOLVED |
| MD-03 | D03 chỉ dài 00:00:04 | P03 | Người dùng xác nhận đây là toàn bộ session; T11 = 00:00:04 | T0 và phần lớn task metrics vẫn NOT_OBSERVABLE; task time không tính được | RESOLVED AS CONFIRMED EARLY END |
| MD-04 | D02 kết thúc trên phone-validation alert | P02 | Người dùng xác nhận đây là toàn bộ session; T11 = 00:01:34; captured-task time = 94 giây | True task start trước frame đầu có thể thiếu; persistence/logout NOT_REACHED | RESOLVED AS CONFIRMED TASK END |
| MD-05 | D05 kết thúc ở login | P05 | Người dùng xác nhận đây là toàn bộ session; T11 = 00:00:51; task time = 50 giây | Login submit/success và SC3–SC5 NOT_REACHED | RESOLVED AS CONFIRMED TASK END |
| MD-06 | Không có pilot recording/data | Pilot | Người dùng xác nhận pilot không được thu thập | Không thể chứng minh protocol đã pilot/refine; không được tái tạo hồi cứu | CONFIRMED_NOT_COLLECTED — **PILOT EVIDENCE MISSING** |
| MD-07 | Không có usable speech trong 7/7 official files | P01–P07 | Không có source audio/notes bổ sung được cung cấp | Quote, exact moderator words, intervention và Card B vẫn NOT_RECORDED/NOT_OBSERVABLE | CONFIRMED_NOT_RECORDED |
| MD-08 | SUS Q1–Q10 không xuất hiện | P01–P07 | Người dùng xác nhận không có SUS responses | SUS từng phiên và aggregate giữ NOT_CALCULABLE | CONFIRMED_NOT_COLLECTED |
| MD-09 | Post-session probes không xuất hiện | P01–P07 | Người dùng xác nhận probes không được thu thập | Clarity/error recovery/speed/trust/final change không thể tổng hợp từ self-report | CONFIRMED_NOT_COLLECTED |
| MD-10 | Consent và eligibility supplement không xuất hiện | P01–P07 | Người dùng xác nhận không có dữ liệu bổ sung | Không xác minh consent/eligibility từ artefacts hiện có | CONFIRMED_NOT_COLLECTED |
| MD-11 | Profile persistence không được kiểm tra | P01, P02, P04, P07; P03/P05/P06 không tới persistence | Không có supplemental persistence evidence | SC4 không thể PASS | CONFIRMED_NOT_RECORDED |
| MD-12 | Plaintext password và PII xuất hiện trong recording | P01, P02, P04, P05, P07; P06 có name/email | Chưa xuất participant screenshot/clip | Phải redact trước khi chia sẻ evidence | BLOCKING BEFORE SHARING |
| MD-13 | Replacement D06 kết thúc ở weak-password error | P06 | Người dùng xác nhận đây là toàn bộ session; T11 = 00:00:53; task time = 52 giây | Registration fail; SC2–SC5 NOT_REACHED | RESOLVED AS CONFIRMED TASK END |

## MISSING SUS FOLLOW-UP — confirmed unavailable

- P01–P07: Q1–Q10 đều `NOT_RECORDED`.
- Người dùng xác nhận không có SUS responses để bổ sung.
- SUS score từng participant và mean/median/min/max của sample giữ `NOT_CALCULABLE`; không suy ra từ hành vi.

## Đoạn cần human review

Human review dưới đây chỉ để kiểm tra coding/timestamp, không còn để xác minh clip có bị cắt hay không.

| Participant | Timestamp/artefact | Mục đích |
|---|---|---|
| P01 | D01 @ 00:00:53–00:01:49 | Kiểm tra 5 phone-validation submits và task end/logout. |
| P02 | D02 @ 00:01:29–00:01:34 | Kiểm tra hesitation 5 giây và final validation state. |
| P03 | Toàn bộ D03 | Kiểm tra rằng không có task action rõ ràng trong session 4 giây. |
| P04 | D04 @ 00:00:22–00:01:01; 00:01:43–00:02:09 | Kiểm tra registration recovery và phone-validation sequence. |
| P05 | D05 @ 00:00:24–00:00:30; 00:00:39–00:00:51 | Kiểm tra register→login transition, system prompt và task end. |
| P06 | D06 replacement @ 00:00:21–00:00:53 | Kiểm tra bốn weak-password submits và final task-end state. |
| P07 | D07 @ 00:00:34–00:00:48; 00:00:51–00:00:59 | Kiểm tra login recovery/hesitation và việc không có update submit. |

## Việc còn lại trước khi phát hành

1. Human-review các timestamp/coding nêu trên.
2. Redact toàn bộ PII và plaintext password trước khi tạo evidence attachment.
3. Fresh independent reproduction cho hai software-bug candidates.
4. Search duplicate issue và reviewer phê duyệt local GitHub drafts trước khi đăng.
5. Giữ SUS, probes, consent/eligibility và pilot ở trạng thái confirmed missing; không tự điền hoặc tái tạo.

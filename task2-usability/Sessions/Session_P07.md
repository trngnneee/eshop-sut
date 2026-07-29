# Moderated Usability Session — P07

## 1. Video and data-quality metadata

- Drive filename: `D07` — tên nguồn được ẩn vì là contact PII.
- Duration: 00:01:06 (metadata: 66,197 giây).
- Date/time, nếu quan sát được: NOT_OBSERVABLE.
- Device: Desktop/laptop screen recording; exact device NOT_OBSERVABLE.
- OS: Windows-style desktop UI observable; version NOT_OBSERVABLE.
- Browser/version: Chromium-style browser UI observable; exact browser/version NOT_OBSERVABLE.
- Screen present: YES — 1920×1008, H.264, khoảng 30 fps.
- Audio present: AAC stereo stream nhưng là digital silence; speech NOT_RECORDED.
- Video complete/cut: COMPLETE-LOOKING — bắt đầu ở product list trước register, kết thúc sau logout; participant/moderator task-end words không được ghi.
- Consent observable: NOT_RECORDED.
- Data-quality limitations: Không có usable speech, consent, moderator words, SUS hoặc probes. Decode có non-monotonic DTS warning nhưng full decode PASS. `PASSWORD_VISIBLE_IN_RECORDING — REDACTION_REQUIRED` trong login khoảng 00:00:29–00:00:48. Name, email, phone và address trên register/profile cũng cần redaction.

## 2. Outcome

- Outcome: `FAILED_OR_ABANDONED`.
- Outcome rationale: Participant đăng ký, tự recovery sau một failed login, login thành công, tìm profile và logout. Tuy nhiên participant chỉ xem/scroll profile rồi quay về product list, không đổi và lưu đủ name, phone, address, cũng không persistence check; SC3 và SC4 không đạt.
- SC1: PASS.
- SC2: PASS.
- SC3: FAIL — profile được mở nhưng không có field edit hoặc update submit.
- SC4: NOT_REACHED.
- SC5: PASS ở behavioral level — authenticated name/`Thoát` biến mất, guest `Đăng nhập`/`Đăng ký` xuất hiện. Token/storage state NOT_OBSERVABLE.

## 3. Milestones and timing

| Milestone | Timestamp | Status/evidence |
|---|---|---|
| T0 | 00:00:00 | Recording bắt đầu tại product list; scenario không được ghi. |
| T1 | 00:00:05 | Register form xuất hiện. |
| T2 | 00:00:21 | First registration submit. |
| T3 | 00:00:22 | Login page xuất hiện; registration thành công. |
| T4 | 00:00:34 | First login submit với full name trong field `Username`. |
| T5 | 00:00:48 | Second login attempt thành công sau khi đổi identifier thành full email; authenticated product list xuất hiện. |
| T6 | 00:00:51 | Profile mở từ authenticated name trên header. |
| T7 | NOT_REACHED | Không có profile-update submit. |
| T8 | NOT_REACHED | Không có profile update success. |
| T9 | NOT_OBSERVABLE | Không có data-save event hoặc usable speech. |
| T10 | 00:01:03 | Participant chọn `Thoát`. |
| T11 | 00:01:06 | Recording kết thúc sau khi guest header xuất hiện. |

- Registration time: 22 giây (`T3 − T0`).
- Login time: 26 giây (`T5 − T3`).
- Find-profile time: 3 giây (`T6 − T5`).
- Profile-update time: NOT_REACHED.
- Logout time: NOT_CALCULABLE — T8 không đạt.
- Total task time: 66 giây (`T11 − T0`).

## 4. Behavioural metrics

- Wrong turns: 0 — toàn bộ đoạn task liên quan được ghi và không có navigation sai cần quay lại; rời profile mà không update được tính vào task failure, không tính wrong turn.
- Errors: 1 — first login submit thất bại khi full name được nhập vào field `Username`.
- Hesitations >=5 seconds: 1 — khoảng 00:00:35–00:00:40, participant dừng sau login error trước khi select/sửa identifier.
- Total hesitation duration: khoảng 5 giây.
- Repeated actions: 1 — login được submit lại sau khi identifier được sửa dần từ full name sang local part rồi full email.
- Think-aloud reminders: NOT_OBSERVABLE — audio là silence.
- Neutral prompts: NOT_OBSERVABLE.
- Task-directed interventions: NOT_OBSERVABLE.
- Card B used: NOT_OBSERVABLE; không có Card B hiển thị trên screen.

## 5. Timestamped observation log

| Timestamp/time range | Screen | Participant action | Observed event | Genuine quote | Event type | Moderator intervention | Evidence reference |
|---|---|---|---|---|---|---|---|
| 00:00:00–00:00:05 | Product list → Register | Chọn `Đăng ký`. | Register được tìm thấy và mở. | NOT_RECORDED — audio silence. | SUCCESS | NOT_OBSERVABLE | D07 @ 00:00:00–00:00:05 |
| 00:00:05–00:00:22 | Register | Điền name, email, masked password và submit. | Registration thành công, không có visible validation error. | NOT_RECORDED — audio silence. | SUCCESS | NOT_OBSERVABLE | D07 @ 00:00:05–00:00:22 |
| 00:00:22–00:00:34 | Login | Nhập full name vào field `Username`, nhập plaintext password và submit. | Heading là `Đăng Ký`; password hiển thị plaintext. | NOT_RECORDED — audio silence. | ERROR | NOT_OBSERVABLE | D07 @ 00:00:22–00:00:35 |
| 00:00:35–00:00:40 | Login error | Không có input/navigation change; sau đó select lại identifier. | Error “Đăng nhập thất bại. Vui lòng kiểm tra lại.” còn hiển thị; hesitation khoảng 5 giây. | NOT_RECORDED — audio silence. | HESITATION | NOT_OBSERVABLE | D07 @ 00:00:35–00:00:40 |
| 00:00:40–00:00:48 | Login | Sửa identifier từ full name sang local part rồi full email và submit lại. | Participant tự recovery; login thành công. | NOT_RECORDED — audio silence. | REPEATED_ACTION | NOT_OBSERVABLE | D07 @ 00:00:40–00:00:48 |
| 00:00:48–00:00:51 | Product list → Profile | Chọn authenticated display name trên header. | Profile được tìm thấy trong 3 giây. | NOT_RECORDED — audio silence. | SUCCESS | NOT_OBSERVABLE | D07 @ 00:00:48–00:00:51 |
| 00:00:51–00:00:59 | Profile | Xem và scroll form; không edit field, không submit `Cập nhật`. | Participant quay về product list mà chưa làm SC3/SC4. | NOT_RECORDED — audio silence. | OTHER | NOT_OBSERVABLE | D07 @ 00:00:51–00:00:59 |
| 00:00:59–00:01:03 | Product list | Di chuyển/scroll rồi chọn `Thoát`. | Không có wrong turn hoặc update retry. | NOT_RECORDED — audio silence. | OTHER | NOT_OBSERVABLE | D07 @ 00:00:59–00:01:03 |
| 00:01:03–00:01:06 | Logout/product list | Chọn `Thoát`. | Guest header xuất hiện; behavioral logout PASS. | NOT_RECORDED — audio silence. | SUCCESS | NOT_OBSERVABLE | D07 @ 00:01:03–00:01:06 |

## 6. Intervention log

| Timestamp | Trigger | Exact moderator words | Participant response | Type | Card B |
|---|---|---|---|---|---|
| NOT_OBSERVABLE | Audio là digital silence. | NOT_RECORDED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE |

## 7. Raw SUS

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED |

- SUS score: NOT_CALCULABLE.
- Missing SUS data: Q1–Q10.
- Data source: Không có SUS form/segment; audio là silence.

## 8. Probe responses

### Clarity
- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.

### Error recovery
- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.

### Speed
- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.

### Trust
- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.

### One requested change
- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.

## 9. Evidence

- Screen recording: D07; playable/full-decode PASS, non-monotonic DTS warning noted.
- Audio: AAC stereo stream nhưng digital silence trong toàn bộ recording.
- SUS evidence: NOT_RECORDED.
- Probe evidence: NOT_RECORDED.
- Bug screenshot/clip candidates:
  - First login failure/recovery: D07 @ 00:00:34–00:00:48.
  - Plaintext password: D07 @ 00:00:29–00:00:48.
  - Redact all registration/login/profile name, email, phone, address và plaintext password trước khi dùng.

## 10. Candidate findings and bugs

- Candidate usability finding IDs:
  - `UF-LOGIN-IDENTIFIER-01` — field `Username` dẫn tới first attempt bằng full name; participant chỉ thành công sau khi chuyển sang full email. Giữ impact ở mức một participant.
- Candidate software bug IDs:
  - `BUG-AUTH-PLAINTEXT-01` — login password hiển thị plaintext. Independent reproduction required: YES.
- Issues requiring independent reproduction: `BUG-AUTH-PLAINTEXT-01`.

## 11. Missing data

- Consent, moderator, exact date/time, exact device, OS/browser version: NOT_RECORDED/NOT_OBSERVABLE.
- Quotes, interventions, Card B, SUS và probes: NOT_RECORDED/NOT_OBSERVABLE.
- Profile edit/update/persistence và T9 trust: NOT_REACHED/NOT_OBSERVABLE.
- Human review: register submit 00:00:20–00:00:22; first login/error 00:00:34–00:00:40; recovery 00:00:40–00:00:48; profile 00:00:51–00:00:59; logout 00:01:03–00:01:06.
- Privacy redactions: all registration/login/profile PII và plaintext password interval.
- Confidence:
  - Mapping D07→P07: HIGH — user confirmation.
  - T1–T8/T10 visual milestones: HIGH; T11 uses recording end after logout.
  - Login error/recovery: HIGH.
  - Hesitation duration: MEDIUM — onset/recovery rounded to whole-second frames.
  - Outcome failure on SC3/SC4 and behavioral SC5: HIGH.
  - Moderator intervention/Card B/quotes: NOT_OBSERVABLE.

## 12. Verification status

`READY_FOR_HUMAN_REVIEW`

Lý do: task screen flow được ghi tới logout; SC3/SC4 không đạt, còn audio speech, consent, SUS và probes được người dùng xác nhận là không được thu thập.

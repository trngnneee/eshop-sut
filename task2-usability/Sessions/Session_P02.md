# Moderated Usability Session — P02

## 1. Video and data-quality metadata

- Drive filename: `D02` — tên nguồn được ẩn vì là contact PII.
- Duration: 00:01:34.
- Date/time, nếu quan sát được: NOT_OBSERVABLE.
- Device: Desktop/laptop screen recording; exact device NOT_OBSERVABLE.
- OS: Desktop OS UI observable; exact OS/version NOT_OBSERVABLE.
- Browser/version: Desktop browser observable; exact browser/version NOT_OBSERVABLE.
- Screen present: YES — 2558×1350, H.264, 30 fps.
- Audio present: Có AAC stereo stream nhưng toàn bộ recording là digital silence (`mean/max -91 dB`); nội dung audio NOT_RECORDED.
- Video complete/cut: COMPLETE — người dùng xác nhận 00:01:34 là điểm kết thúc thật của session; task kết thúc khi validation alert thứ ba còn mở.
- Consent observable: NOT_RECORDED.
- Data-quality limitations: Recording bắt đầu giữa registration nên true task start trước frame đầu là NOT_OBSERVABLE. Không có usable speech, consent, SUS, probes hoặc moderator words; người dùng xác nhận các dữ liệu bổ sung này không được thu thập. `PASSWORD_VISIBLE_IN_RECORDING — REDACTION_REQUIRED` tại login khoảng 00:00:17–00:00:35. Email, tên, phone và address xuất hiện rõ; mọi screenshot/clip phải redaction.

## 2. Outcome

- Outcome: `FAILED_OR_ABANDONED` — task-end đã được người dùng xác nhận.
- Outcome rationale: Participant tạo account, login và mở profile thành công. Cả 3 submit update đều bị chặn bởi phone-validation alert; session kết thúc khi alert thứ ba còn mở. Không có successful save, persistence check hoặc logout. Người dùng xác nhận đây là toàn bộ session, nên outcome được chốt tại task end.
- SC1: PASS — registration thành công và chuyển tới login.
- SC2: PASS — login thành công và home/product list xuất hiện.
- SC3: FAIL — không có saved profile tại task end; lần submit đầu dùng giá trị phone 10 chữ số bắt đầu bằng 0 nhưng vẫn nhận phone error.
- SC4: NOT_REACHED.
- SC5: NOT_REACHED.

## 3. Milestones and timing

| Milestone | Timestamp | Status/evidence |
|---|---|---|
| T0 | 00:00:00 | First captured action là tiếp tục điền register; scenario và thao tác mở form xảy ra trước recording hoặc không được ghi. |
| T1 | 00:00:00 | Register đã mở ở frame đầu; actual open timestamp NOT_OBSERVABLE. |
| T2 | 00:00:16 | Submit registration lần đầu. |
| T3 | 00:00:17 | Login page xuất hiện; registration success. |
| T4 | 00:00:35 | Submit login lần đầu. |
| T5 | 00:00:36 | Home/product list xuất hiện ở authenticated state. |
| T6 | 00:00:42 | Profile mở từ header. |
| T7 | 00:00:57 | Submit profile update lần đầu. |
| T8 | NOT_REACHED | Ba submits đều bị phone-validation alert. |
| T9 | NOT_REACHED | Không có successful save/trust confirmation. |
| T10 | NOT_REACHED | Không có logout trong recording. |
| T11 | 00:01:34 | Task kết thúc khi validation alert thứ ba còn mở; timestamp dựa trên recording end và xác nhận của người dùng rằng đây là toàn bộ session. |

- Registration time: 17 giây (`T3 − T0`), với limitation rằng recording bắt đầu giữa registration.
- Login time: 19 giây (`T5 − T3`).
- Find-profile time: 6 giây (`T6 − T5`).
- Profile-update time: NOT_REACHED.
- Logout time: NOT_REACHED.
- Total task time: 94 giây (`T11 − T0`), là captured-task duration; true start có thể sớm hơn vì recording bắt đầu giữa registration.

## 4. Behavioural metrics

- Wrong turns: NOT_OBSERVABLE cho toàn task vì recording bắt đầu giữa registration; không có wrong turn trong phần screen được ghi.
- Errors: 3 — ba profile submits tạo cùng phone-validation alert.
- Hesitations >=5 seconds: 1 — stationary interval 00:01:29–00:01:34 trên validation alert; task-end confirmation loại bỏ cut-file ambiguity.
- Total hesitation duration: 5 giây; MEDIUM confidence vì không có speech để xác nhận participant đang đọc hay phân vân.
- Repeated actions: 2 submit repeats sau submit update đầu tiên; 3 submits tổng cộng.
- Think-aloud reminders: NOT_OBSERVABLE — audio silent.
- Neutral prompts: NOT_OBSERVABLE — audio silent.
- Task-directed interventions: NOT_OBSERVABLE — audio silent.
- Card B used: NOT_OBSERVABLE.

## 5. Timestamped observation log

| Timestamp/time range | Screen | Participant action | Observed event | Genuine quote | Event type | Moderator intervention | Evidence reference |
|---|---|---|---|---|---|---|---|
| 00:00:00–00:00:16 | Register | Tiếp tục điền form đã mở và submit. | Registration hoàn tất không có visible validation error. | NOT_RECORDED — audio silent. | SUCCESS | NOT_OBSERVABLE | D02 @ 00:00:00–00:00:17 |
| 00:00:17–00:00:35 | Login | Điền credential và submit. | Heading “Đăng Ký”, label `Username`, nút `Sign In`; participant vẫn login thành công. Password hiển thị plaintext. | NOT_RECORDED — audio silent. | OTHER | NOT_OBSERVABLE | D02 @ 00:00:17–00:00:36 |
| 00:00:36–00:00:42 | Product list → Profile | Mở profile từ header. | Điều hướng trực tiếp, không có wrong turn. | NOT_RECORDED — audio silent. | SUCCESS | NOT_OBSERVABLE | D02 @ 00:00:36–00:00:42 |
| 00:00:42–00:00:57 | Profile | Nhập phone rồi submit trước khi hoàn thành address. | Phone có 10 chữ số bắt đầu bằng 0 nhưng hệ thống trả phone-invalid alert. Phone cụ thể được redacted. | NOT_RECORDED — audio silent. | ERROR | NOT_OBSERVABLE | D02 @ 00:00:42–00:01:02 |
| 00:00:57–00:01:02 | Validation alert | Alert hiện và participant đóng sau khoảng 5 giây. | “Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số.” | NOT_RECORDED — audio silent. | SYSTEM_FEEDBACK | NOT_OBSERVABLE | D02 @ 00:00:57–00:01:02 |
| 00:01:02–00:01:13 | Profile | Điền address; phone field quan sát được là trống khi submit lần 2. | Submit lặp lại và cùng phone error xuất hiện. Không đủ bằng chứng để xác định participant tự xóa phone hay state bị mất sau error. | NOT_RECORDED — audio silent. | REPEATED_ACTION | NOT_OBSERVABLE | D02 @ 00:01:02–00:01:15 |
| 00:01:15–00:01:29 | Profile | Tiếp tục sửa address và submit lần 3 khi phone vẫn trống. | Cùng phone error; error recovery không thành công. | NOT_RECORDED — audio silent. | REPEATED_ACTION | NOT_OBSERVABLE | D02 @ 00:01:15–00:01:29 |
| 00:01:29–00:01:34 | Validation alert | Không có action trong 5 giây cuối. | Alert còn mở tại confirmed task end; mã hóa một hesitation 5 giây. | NOT_RECORDED — audio silent. | HESITATION | NOT_OBSERVABLE | D02 @ 00:01:29–00:01:34 |

## 6. Intervention log

| Timestamp | Trigger | Exact moderator words | Participant response | Type | Card B |
|---|---|---|---|---|---|
| NOT_OBSERVABLE | Audio stream là digital silence. | NOT_RECORDED | Không thể xác minh. | NOT_OBSERVABLE | NOT_OBSERVABLE |

## 7. Raw SUS

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED |

- SUS score: NOT_CALCULABLE.
- Missing SUS data: Q1–Q10.
- Data source: Không có SUS form/segment; audio silent.

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

- Screen recording: D02; playable/full-decode PASS.
- Audio: Digital silence 00:00:00–00:01:34.
- SUS evidence: NOT_RECORDED.
- Probe evidence: NOT_RECORDED.
- Bug screenshot/clip candidates:
  - Plaintext login password: D02 @ 00:00:17–00:00:35.
  - Valid-format phone rejected: D02 @ 00:00:56–00:01:02.
  - Redaction required cho password, email, name, phone và address trước khi dùng evidence.

## 10. Candidate findings and bugs

- Candidate usability finding IDs: `UF-PHONE-RECOVERY-01` — participant không recovery được sau ba submits; error modal không dẫn tới saved profile.
- Candidate software bug IDs:
  - `BUG-PF-02` — phone 10 chữ số bắt đầu bằng 0 bị từ chối; independent reproduction required: YES.
  - `BUG-AUTH-PLAINTEXT-01` — login password hiển thị plaintext; independent reproduction required: YES.
- Issues requiring independent reproduction: Cả hai bug candidates.

## 11. Missing data

- Task end đã được xác nhận tại 00:01:34; không có phần video tiếp theo. Persistence và logout: NOT_REACHED.
- SUS, probes, consent và supplemental notes: người dùng xác nhận không được thu thập; giữ NOT_RECORDED.
- Consent, exact date/time, moderator, exact device/OS/browser: NOT_RECORDED/NOT_OBSERVABLE.
- Quotes, interventions, Card B, SUS, probes: NOT_RECORDED/NOT_OBSERVABLE do audio silent và không có screen segment.
- Human review cần tập trung: registration transition 00:00:15–00:00:17; login 00:00:34–00:00:36; alerts 00:00:57–00:01:02, 00:01:13–00:01:15 và 00:01:29–00:01:34.
- Privacy redactions: password/login 00:00:17–00:00:35; mọi email, name, phone, address trên register/profile.
- Confidence:
  - Mapping D02→P02: MEDIUM — người dùng xác nhận trực tiếp, nhưng screen account data không được dùng để suy ra identity và cần human cross-check.
  - T0–T7: HIGH, ngoại trừ actual register-open time NOT_OBSERVABLE.
  - Error/repeat counts: HIGH.
  - Valid-format phone rejection: HIGH; value cụ thể redacted.
  - Hesitation cuối: MEDIUM — đủ 5 giây stationary trên alert, nhưng không có speech để xác nhận intent.
  - T11/outcome finality: HIGH — người dùng xác nhận recording end là task end.

## 12. Verification status

`READY_FOR_HUMAN_REVIEW`

Lý do: task end đã được xác nhận; observed evidence đã được mã hóa. Logout/persistence không đạt và audio/SUS/probes/consent được xác nhận là không được thu thập.

# Moderated Usability Session — P01

## 1. Video and data-quality metadata

- Drive filename: `D01` — tên nguồn được ẩn vì là contact PII.
- Duration: 00:01:52.
- Date/time, nếu quan sát được: NOT_OBSERVABLE; thời gian upload Drive không được dùng thay cho thời gian phiên.
- Device: Desktop/laptop screen recording; model thiết bị NOT_OBSERVABLE.
- OS: Windows UI observable; version NOT_OBSERVABLE.
- Browser/version: Desktop browser observable; browser/version chính xác NOT_OBSERVABLE.
- Screen present: YES — 1920×1032, H.264, 30 fps.
- Audio present: Có AAC stereo stream, nhưng toàn bộ recording là digital silence (`mean/max -91 dB`). Nội dung audio: NOT_RECORDED.
- Video complete/cut: COMPLETE-LOOKING; flow bắt đầu ở trang sản phẩm và kết thúc sau logout tại protected profile.
- Consent observable: NOT_RECORDED.
- Data-quality limitations: Không có audio hữu dụng; không quan sát consent, moderator speech, SUS hoặc probes. Login hiển thị mật khẩu rõ trong khoảng 00:00:19–00:00:33: `PASSWORD_VISIBLE_IN_RECORDING — REDACTION_REQUIRED`. Email, tên và các giá trị profile cũng xuất hiện trên screen và phải được redaction trước khi chia sẻ evidence.

## 2. Outcome

- Outcome: `FAILED_OR_ABANDONED`.
- Outcome rationale: Participant tạo account, login, tìm profile và logout thành công, nhưng không lưu được bộ dữ liệu profile. Participant submit update 5 lần; cả hai lần dùng giá trị điện thoại 10 chữ số bắt đầu bằng 0 vẫn bị từ chối. Không có successful update hoặc persistence check trước khi logout.
- SC1: PASS — account mới được tạo và hệ thống chuyển tới login.
- SC2: PASS — login thành công và trở về danh sách sản phẩm.
- SC3: FAIL — tên/điện thoại/địa chỉ không được lưu do phone validation chặn submit.
- SC4: NOT_REACHED — không có successful save để reload/persistence check.
- SC5: PASS ở mức hành vi quan sát được — sau thao tác `Thoát`, protected profile hiển thị “Vui lòng đăng nhập” và header trở về trạng thái guest. Việc token bị xóa khỏi storage: NOT_OBSERVABLE.

## 3. Milestones and timing

| Milestone | Timestamp   | Status/evidence                                                                                                         |
| --------- | ----------- | ----------------------------------------------------------------------------------------------------------------------- |
| T0        | 00:00:01    | Hành động đầu tiên quan sát được sau khi recording bắt đầu: mở đăng ký từ trang sản phẩm.                               |
| T1        | 00:00:01    | Trang “Đăng Ký Tài Khoản” mở.                                                                                           |
| T2        | 00:00:18    | Submit đăng ký lần đầu.                                                                                                 |
| T3        | 00:00:19    | Registration thành công; trang login xuất hiện.                                                                         |
| T4        | 00:00:33    | Submit login lần đầu.                                                                                                   |
| T5        | 00:00:33    | Login thành công; danh sách sản phẩm xuất hiện với trạng thái authenticated.                                            |
| T6        | 00:00:36    | Profile mở trực tiếp từ header.                                                                                         |
| T7        | 00:00:53    | Submit cập nhật profile lần đầu.                                                                                        |
| T8        | NOT_REACHED | Cả 5 lần submit đều trả lỗi phone validation; không quan sát successful save.                                           |
| T9        | NOT_REACHED | Không có saved state để participant xác nhận tin tưởng.                                                                 |
| T10       | 00:01:49    | Participant thực hiện `Thoát`.                                                                                          |
| T11       | 00:01:52    | Recording kết thúc sau khi protected profile hiển thị “Vui lòng đăng nhập”; không có verbal completion do audio silent. |

- Registration time: 18 giây (`T3 − T0`).
- Login time: 14 giây (`T5 − T3`).
- Find-profile time: 3 giây (`T6 − T5`).
- Profile-update time: NOT_REACHED (`T8` không xảy ra).
- Logout time: NOT_CALCULABLE theo công thức `T11 − T8`, vì `T8` không xảy ra.
- Total task time: 111 giây (`T11 − T0`).

## 4. Behavioural metrics

- Wrong turns: 0 — toàn bộ screen task được quan sát và participant đi trực tiếp Register → Login → Profile → Logout.
- Errors: 5 — năm submit profile đều tạo cùng phone-validation error.
- Hesitations >=5 seconds: 0 — không quan sát khoảng dừng liên tục từ 5 giây; thời gian alert hiển thị dài nhất dưới 5 giây và thời gian sửa input có thay đổi màn hình liên tục.
- Total hesitation duration: 0 giây.
- Repeated actions: 4 lần submit lặp lại sau submit đầu tiên; 5 submit update tổng cộng.
- Think-aloud reminders: NOT_OBSERVABLE — audio digital silence.
- Neutral prompts: NOT_OBSERVABLE — audio digital silence.
- Task-directed interventions: NOT_OBSERVABLE — audio digital silence; không có Card B hiển thị trên screen.
- Card B used: NOT_OBSERVABLE.

## 5. Timestamped observation log

| Timestamp/time range | Screen                   | Participant action                                              | Observed event                                                                                                                                                           | Genuine quote                | Event type      | Moderator intervention | Evidence reference      |
| -------------------- | ------------------------ | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------- | --------------- | ---------------------- | ----------------------- |
| 00:00:00–00:00:01    | Product list             | Mở chức năng đăng ký từ header.                                 | Điều hướng trực tiếp tới form đăng ký.                                                                                                                                   | NOT_RECORDED — audio silent. | SUCCESS         | NOT_OBSERVABLE         | D01 @ 00:00:00–00:00:01 |
| 00:00:01–00:00:18    | Register                 | Điền form và submit.                                            | Không quan sát validation error ở registration; account được tạo.                                                                                                        | NOT_RECORDED — audio silent. | SUCCESS         | NOT_OBSERVABLE         | D01 @ 00:00:01–00:00:19 |
| 00:00:19–00:00:33    | Login                    | Điền credential và submit.                                      | Heading hiển thị “Đăng Ký”, label `Username`, nút `Sign In`; participant vẫn login thành công, không có wrong turn quan sát được. Mật khẩu hiển thị rõ thay vì được che. | NOT_RECORDED — audio silent. | OTHER           | NOT_OBSERVABLE         | D01 @ 00:00:19–00:00:33 |
| 00:00:33–00:00:36    | Product list → Profile   | Mở profile từ header.                                           | Tìm profile trong 3 giây, không điều hướng sai.                                                                                                                          | NOT_RECORDED — audio silent. | SUCCESS         | NOT_OBSERVABLE         | D01 @ 00:00:33–00:00:36 |
| 00:00:36–00:00:53    | Profile                  | Sửa tên và địa chỉ; submit khi trường điện thoại đang trống.    | Submit 1 bị chặn bởi phone validation.                                                                                                                                   | NOT_RECORDED — audio silent. | ERROR           | NOT_OBSERVABLE         | D01 @ 00:00:36–00:00:55 |
| 00:00:53–00:00:55    | Validation alert         | Đọc/đóng alert.                                                 | Alert: “Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số.”                                                                                                     | NOT_RECORDED — audio silent. | SYSTEM_FEEDBACK | NOT_OBSERVABLE         | D01 @ 00:00:53–00:00:55 |
| 00:00:55–00:01:12    | Profile                  | Nhập một giá trị 10 chữ số bắt đầu bằng 0 và submit lần 2.      | Giá trị phù hợp hình thức FR-04 vẫn bị từ chối bởi cùng alert. Giá trị cụ thể được redacted.                                                                             | NOT_RECORDED — audio silent. | ERROR           | NOT_OBSERVABLE         | D01 @ 00:00:55–00:01:12 |
| 00:01:12–00:01:17    | Profile                  | Rút ngắn input và submit lần 3.                                 | Repeated submit; input ngắn hơn yêu cầu và tiếp tục bị từ chối.                                                                                                          | NOT_RECORDED — audio silent. | REPEATED_ACTION | NOT_OBSERVABLE         | D01 @ 00:01:12–00:01:17 |
| 00:01:17–00:01:30    | Profile                  | Tiếp tục sửa input và submit lần 4.                             | Repeated submit; cùng validation alert.                                                                                                                                  | NOT_RECORDED — audio silent. | REPEATED_ACTION | NOT_OBSERVABLE         | D01 @ 00:01:17–00:01:30 |
| 00:01:30–00:01:44    | Profile                  | Nhập một giá trị 10 chữ số khác bắt đầu bằng 0 và submit lần 5. | Lần thứ hai input phù hợp hình thức FR-04 vẫn bị từ chối. Không có error recovery thành công.                                                                            | NOT_RECORDED — audio silent. | ERROR           | NOT_OBSERVABLE         | D01 @ 00:01:30–00:01:44 |
| 00:01:44–00:01:49    | Profile                  | Trở lại form sau alert; không submit thêm.                      | Profile chưa được lưu.                                                                                                                                                   | NOT_RECORDED — audio silent. | OTHER           | NOT_OBSERVABLE         | D01 @ 00:01:44–00:01:49 |
| 00:01:49–00:01:52    | Logout/protected profile | Chọn `Thoát`.                                                   | Header trở về guest state và `/profile` hiển thị “Vui lòng đăng nhập”.                                                                                                   | NOT_RECORDED — audio silent. | SUCCESS         | NOT_OBSERVABLE         | D01 @ 00:01:49–00:01:52 |

## 6. Intervention log

| Timestamp      | Trigger                          | Exact moderator words | Participant response                                         | Type           | Card B         |
| -------------- | -------------------------------- | --------------------- | ------------------------------------------------------------ | -------------- | -------------- |
| NOT_OBSERVABLE | Audio stream là digital silence. | NOT_RECORDED          | Không thể xác minh bằng audio; screen không hiển thị Card B. | NOT_OBSERVABLE | NOT_OBSERVABLE |

## 7. Raw SUS

| Source | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Response P01 | 4 | 2 | 5 | 1 | 4 | 2 | 5 | 2 | 4 | 2 |

- SUS score: 82.5.
- Recording limitation: Không có SUS form hoặc câu trả lời SUS trong recording; audio silent.
- Data source: User-provided response set P01, supplied separately on 2026-07-31; participant ID confirmed on 2026-08-02.

## 8. Probe responses

### Clarity

- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.
- Evidence reference: D01 — không có probe segment.

### Error recovery

- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.
- Evidence reference: D01 — không có probe segment.

### Speed

- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.
- Evidence reference: D01 — không có probe segment.

### Trust

- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.
- Evidence reference: D01 — không có probe segment.

### One requested change

- Response: NOT_RECORDED.
- Verbatim/paraphrase: NOT_APPLICABLE.
- Timestamp: NOT_RECORDED.
- Evidence reference: D01 — không có probe segment.

## 9. Evidence

- Screen recording: D01, playable/full-decode PASS; source filename redacted because it is contact PII.
- Audio: AAC stream present nhưng digital silence từ 00:00:00–00:01:52.
- SUS evidence: `Analysis/SUS_Raw_Responses.csv`, row P01 (`COMPLETED_USER_PROVIDED`); not captured in D01.
- Probe evidence: NOT_RECORDED.
- Bug screenshot/clip candidates:
  - Login password plaintext: D01 @ 00:00:19–00:00:33. Redact password và email trước khi dùng.
  - Valid-format phone rejected: D01 @ 00:01:08–00:01:12 và 00:01:38–00:01:44. Redact email, name, phone và address trước khi dùng.

## 10. Candidate findings and bugs

- Candidate usability finding IDs: `UF-PHONE-RECOVERY-01` — feedback không giúp participant recovery sau 5 attempts; profile update bị chặn.
- Candidate software bug IDs:
  - `BUG-PF-02` — hai giá trị 10 chữ số bắt đầu bằng 0 bị từ chối dù phù hợp FR-04; independent reproduction required: YES.
  - `BUG-AUTH-PLAINTEXT-01` — login password được render dưới dạng plaintext; independent reproduction required: YES. Participant reaction/concern: NOT_OBSERVABLE vì audio silent.
- Issues requiring independent reproduction: Cả hai bug candidate trên.

## 11. Missing data

- Consent, moderator identity, session date/time, exact device, exact OS/browser version: NOT_RECORDED hoặc NOT_OBSERVABLE.
- Moderator words, think-aloud reminders, neutral prompts, task-directed assistance và Card B: NOT_OBSERVABLE do audio digital silence.
- Genuine participant quotes: NOT_RECORDED.
- T9/trust statement: NOT_REACHED/NOT_RECORDED.
- Persistence check: NOT_REACHED.
- SUS collection segment in D01: NOT_RECORDED; Q1–Q10 were supplied separately for P01.
- Tất cả post-session probes: NOT_RECORDED.
- Token/storage inspection sau logout: NOT_OBSERVABLE; chỉ có behavioral logout evidence.
- Các đoạn đã human-review ngày 2026-08-02: 00:00:18–00:00:20, 00:00:32–00:00:36, năm validation attempts tại 00:00:53–00:01:44 và logout tại 00:01:49–00:01:52.
- Privacy redactions: password 00:00:19–00:00:33; email/name/phone/address ở registration, login và profile; mọi screenshot/clip phải redaction trước khi chia sẻ.
- Confidence:
  - Mapping D01→P01: HIGH — người dùng xác nhận trực tiếp.
  - Screen milestones T0–T10: HIGH — page transitions và alerts quan sát trực tiếp.
  - T11: MEDIUM — dùng điểm kết thúc recording; không có verbal completion.
  - Error count và repeated submits: HIGH.
  - Valid-format phone rejection: HIGH — hai input 10 chữ số bắt đầu bằng 0 quan sát trực tiếp; giá trị đã redacted.
  - Moderator intervention/Card B: LOW/NOT_OBSERVABLE.
  - SUS/probes/quotes: HIGH confidence rằng không được ghi trong recording này vì audio là digital silence và không có segment tương ứng trên screen.

Lý do: screen task đủ để đánh giá flow và bugs; audio, consent và probes không được ghi. SUS không xuất hiện trong recording P01 nhưng response set P01 đã được cung cấp riêng và được gắn với participant ID theo xác nhận ngày 2026-08-02.

## 12. Verification status

`HUMAN_REVIEWED`

Lý do: screen milestones, task behavior và timestamps từ D01 đã được sinh viên review ngày 2026-08-02. Audio/probes/consent không được ghi, persistence không đạt và SUS P01 được cung cấp riêng; không có dữ liệu thiếu nào được tự tạo.

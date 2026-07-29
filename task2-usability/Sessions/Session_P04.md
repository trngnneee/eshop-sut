# Moderated Usability Session — P04

## 1. Video and data-quality metadata

- Drive filename: `D04` — tên nguồn được ẩn vì là contact PII.
- Duration: 00:02:16 (metadata: 135.659 giây).
- Date/time, nếu quan sát được: NOT_OBSERVABLE.
- Device: Desktop/laptop screen recording; exact device NOT_OBSERVABLE.
- OS: Windows UI observable; version NOT_OBSERVABLE.
- Browser/version: Microsoft Edge observable từ browser settings screen; version NOT_OBSERVABLE.
- Screen present: YES — 2556×1470, H.264, 30 fps.
- Audio present: AAC stereo stream có tín hiệu khoảng 0,2 giây quanh 00:00:23,5; phần còn lại là silence. Không có speech đủ dài/đủ rõ để chép: speech NOT_RECORDED.
- Video complete/cut: COMPLETE-LOOKING; bắt đầu ở register và kết thúc sau logout tại protected profile.
- Consent observable: NOT_RECORDED.
- Data-quality limitations: Không có usable speech, consent, moderator words, SUS hoặc probes. Faster-Whisper sinh transcript lặp trên silence nên bị loại bỏ hoàn toàn, không dùng làm evidence. `PASSWORD_VISIBLE_IN_RECORDING — REDACTION_REQUIRED` trong login khoảng 00:01:01–00:01:39. Email, name và phone cũng cần redaction.

## 2. Outcome

- Outcome: `FAILED_OR_ABANDONED`.
- Outcome rationale: Participant tạo account, login và logout thành công. Một update cuối nhận success alert sau khi dùng phone không bắt đầu bằng 0, nhưng address vẫn trống và display name không được thay đổi trong profile segment; không có persistence check. Vì SC3 và SC4 không đạt, outcome không thể là completed. Moderator assistance không thể xác minh vì audio không có speech usable.
- SC1: PASS.
- SC2: PASS.
- SC3: FAIL — chỉ phone nhận successful update; required new name và address không được lưu. Phone được chấp nhận cũng không bắt đầu bằng 0 như FR-04 yêu cầu.
- SC4: NOT_REACHED — không reload/persistence check.
- SC5: PASS ở behavioral level — sau `Thoát`, protected profile hiển thị “Vui lòng đăng nhập” và guest header. Token/storage state: NOT_OBSERVABLE.

## 3. Milestones and timing

| Milestone | Timestamp | Status/evidence |
|---|---|---|
| T0 | 00:00:00 | First captured action là điền register; scenario không được ghi. |
| T1 | 00:00:00 | Register đã mở ở recording start; actual open time NOT_OBSERVABLE. |
| T2 | 00:00:22 | First registration submit; password-policy validation xuất hiện. |
| T3 | 00:01:01 | Participant tự sửa password và registration thành công; login page xuất hiện. |
| T4 | 00:01:39 | First login submit. |
| T5 | 00:01:40 | Login success; product list xuất hiện. |
| T6 | 00:01:43 | Profile mở từ header. |
| T7 | 00:01:51 | First profile-update submit. |
| T8 | 00:02:07 | Success alert sau update submit thứ tư. |
| T9 | NOT_OBSERVABLE | Không có speech; việc đóng success alert rồi logout chưa đủ để khẳng định trust. |
| T10 | 00:02:12 | Participant chọn `Thoát`. |
| T11 | 00:02:16 | Recording kết thúc sau khi protected profile hiển thị “Vui lòng đăng nhập”. |

- Registration time: 61 giây (`T3 − T0`).
- Login time: 39 giây (`T5 − T3`).
- Find-profile time: 3 giây (`T6 − T5`).
- Profile-update time: 24 giây (`T8 − T6`).
- Logout time: 9 giây (`T11 − T8`).
- Total task time: 136 giây (`T11 − T0`, rounded to HH:MM:SS timestamps).

## 4. Behavioural metrics

- Wrong turns: 1 — Microsoft Edge Password Manager mở tại 00:01:22–00:01:24 trong lúc login; participant quay lại SUT.
- Errors: 4 — một invalid-password registration submit và ba phone-validation update submits.
- Hesitations >=5 seconds: 0 — trong các recovery intervals có UI/input changes liên tục; Password Manager detour kéo dài dưới 5 giây.
- Total hesitation duration: 0 giây.
- Repeated actions: 4 — một repeated registration submit và ba repeated profile-update submits.
- Think-aloud reminders: NOT_OBSERVABLE — không có speech usable.
- Neutral prompts: NOT_OBSERVABLE.
- Task-directed interventions: NOT_OBSERVABLE.
- Card B used: NOT_OBSERVABLE; không có Card B hiển thị trên screen.

## 5. Timestamped observation log

| Timestamp/time range | Screen | Participant action | Observed event | Genuine quote | Event type | Moderator intervention | Evidence reference |
|---|---|---|---|---|---|---|---|
| 00:00:00–00:00:22 | Register | Điền form và submit lần đầu. | Inline password-policy error xuất hiện: yêu cầu tối thiểu 8 ký tự và các loại ký tự quy định. | NOT_RECORDED — no usable speech. | ERROR | NOT_OBSERVABLE | D04 @ 00:00:00–00:00:22 |
| 00:00:22–00:01:01 | Register | Sửa password nhiều lần và submit lại. | Participant tự recovery; registration thành công. Không có stationary hesitation >=5s quan sát được. | NOT_RECORDED — no usable speech. | SUCCESS | NOT_OBSERVABLE | D04 @ 00:00:22–00:01:01 |
| 00:01:01–00:01:22 | Login | Điền credential. | Login heading “Đăng Ký”, label `Username`, nút `Sign In`; password hiển thị plaintext. | NOT_RECORDED — no usable speech. | OTHER | NOT_OBSERVABLE | D04 @ 00:01:01–00:01:22 |
| 00:01:22–00:01:24 | Microsoft Edge Password Manager | Rời SUT tới browser password settings rồi quay lại login. | Wrong turn làm gián đoạn login flow khoảng 2 giây. | NOT_RECORDED — no usable speech. | WRONG_TURN | NOT_OBSERVABLE | D04 @ 00:01:22–00:01:24 |
| 00:01:24–00:01:40 | Login → Product list | Tiếp tục login và submit. | Login thành công. | NOT_RECORDED — no usable speech. | SUCCESS | NOT_OBSERVABLE | D04 @ 00:01:24–00:01:40 |
| 00:01:40–00:01:43 | Product list → Profile | Mở profile từ header. | Tìm profile trong 3 giây. | NOT_RECORDED — no usable speech. | SUCCESS | NOT_OBSERVABLE | D04 @ 00:01:40–00:01:43 |
| 00:01:43–00:01:54 | Profile | Nhập phone 10 chữ số bắt đầu bằng 0 và submit lần đầu; address còn trống. | Hệ thống trả phone-invalid alert dù phone phù hợp hình thức FR-04. Giá trị được redacted. | NOT_RECORDED — no usable speech. | ERROR | NOT_OBSERVABLE | D04 @ 00:01:43–00:01:54 |
| 00:01:54–00:01:59 | Profile | Thêm một chữ số, tạo phone 11 chữ số bắt đầu bằng 0, rồi submit lần hai. | Cùng phone-invalid alert; input vẫn phù hợp hình thức FR-04. | NOT_RECORDED — no usable speech. | REPEATED_ACTION | NOT_OBSERVABLE | D04 @ 00:01:54–00:01:59 |
| 00:01:59–00:02:04 | Profile | Rút ngắn phone và submit lần ba. | Input ngắn hơn FR-04; cùng error alert. | NOT_RECORDED — no usable speech. | REPEATED_ACTION | NOT_OBSERVABLE | D04 @ 00:01:59–00:02:04 |
| 00:02:04–00:02:09 | Profile | Thay bằng phone không bắt đầu bằng 0 và submit lần bốn. | Hệ thống hiển thị “Cập nhật thành công”. Address vẫn trống. | NOT_RECORDED — no usable speech. | SYSTEM_FEEDBACK | NOT_OBSERVABLE | D04 @ 00:02:04–00:02:09 |
| 00:02:09–00:02:12 | Profile | Đóng success alert và chuyển tới logout. | Không reload/persistence check. | NOT_RECORDED — no usable speech. | OTHER | NOT_OBSERVABLE | D04 @ 00:02:09–00:02:12 |
| 00:02:12–00:02:16 | Logout/protected profile | Chọn `Thoát`. | Guest header và “Vui lòng đăng nhập” xuất hiện. | NOT_RECORDED — no usable speech. | SUCCESS | NOT_OBSERVABLE | D04 @ 00:02:12–00:02:16 |

## 6. Intervention log

| Timestamp | Trigger | Exact moderator words | Participant response | Type | Card B |
|---|---|---|---|---|---|
| NOT_OBSERVABLE | Audio chỉ có khoảng 0,2 giây non-silent signal, không đủ cho speech. | NOT_RECORDED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE |

## 7. Raw SUS

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED |

- SUS score: NOT_CALCULABLE.
- Missing SUS data: Q1–Q10.
- Data source: Không có SUS form/segment; không có usable speech.

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

- Screen recording: D04; playable/full-decode PASS.
- Audio: Silence 00:00:00–00:00:23.476 và 00:00:23.670–00:02:15.659; khoảng non-silent còn lại quá ngắn cho speech.
- SUS evidence: NOT_RECORDED.
- Probe evidence: NOT_RECORDED.
- Bug screenshot/clip candidates:
  - Plaintext password: D04 @ 00:01:01–00:01:39.
  - Valid 10/11-digit leading-zero phones rejected: D04 @ 00:01:43–00:01:59.
  - Non-leading-zero phone accepted: D04 @ 00:02:04–00:02:09.
  - Redact password, email, name và all phone values trước khi dùng.

## 10. Candidate findings and bugs

- Candidate usability finding IDs:
  - `UF-PHONE-RECOVERY-01` — participant phải thử bốn phone formats trước success alert; feedback không phản ánh rule thực tế.
  - `UF-PASSWORD-MANAGER-DETOUR-01` — browser password workflow làm participant rời SUT trong login; chỉ một participant, cần giữ isolated observation.
- Candidate software bug IDs:
  - `BUG-PF-02` — phone 10 và 11 chữ số bắt đầu bằng 0 bị từ chối; phone không bắt đầu bằng 0 lại được chấp nhận. Independent reproduction required: YES.
  - `BUG-AUTH-PLAINTEXT-01` — login password hiển thị plaintext. Independent reproduction required: YES.
- Issues requiring independent reproduction: Cả hai software bugs.

## 11. Missing data

- Consent, moderator, exact date/time, exact device, OS/browser version: NOT_RECORDED/NOT_OBSERVABLE.
- Quotes, intervention words/types, Card B, SUS và probes: NOT_RECORDED/NOT_OBSERVABLE.
- T9/trust: NOT_OBSERVABLE.
- Persistence reload/check và address/name update: NOT_REACHED.
- Human review: password-policy recovery 00:00:22–00:01:01; Password Manager 00:01:22–00:01:24; profile attempts 00:01:43–00:02:09; logout 00:02:12–00:02:16.
- Privacy redactions: registration/login/profile PII, entire plaintext password interval, all phone inputs, Password Manager screen if dùng clip.
- Confidence:
  - Mapping D04→P04: HIGH — user confirmation.
  - T0–T11 visual milestones: HIGH; T11 uses recording end after logout.
  - Registration error/recovery, wrong turn, update attempts and alerts: HIGH.
  - Phone-validation bug pattern: HIGH; raw values redacted.
  - Moderator intervention/Card B/quotes: NOT_OBSERVABLE.
  - Outcome failure on SC3/SC4: HIGH based screen requirements; no address/persistence evidence.

## 12. Verification status

`READY_FOR_HUMAN_REVIEW`

Lý do: screen flow đã được mã hóa; audio speech, consent, SUS, probes và supplemental evidence được người dùng xác nhận là không được thu thập. Persistence/full SC3 không đạt trong session.

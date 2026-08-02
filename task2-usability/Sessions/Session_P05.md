# Moderated Usability Session — P05

## 1. Video and data-quality metadata

- Drive filename: `D05` — tên nguồn được ẩn vì là contact PII.
- Duration: 00:00:51 (metadata: 50,740 giây).
- Date/time, nếu quan sát được: NOT_OBSERVABLE.
- Device: Mobile touch-screen recording; exact device/model NOT_OBSERVABLE.
- OS: iOS-style system UI observable; version NOT_OBSERVABLE.
- Browser/version: iOS mobile-browser UI observable; exact browser/version `NOT_OBSERVABLE_AFTER_HUMAN_REVIEW`.
- Screen present: YES — portrait 1242×2688, HEVC, khoảng 60 fps.
- Audio present: AAC stereo stream có trong container nhưng là digital silence; speech NOT_RECORDED.
- Video complete/cut: COMPLETE — người dùng xác nhận session thực sự kết thúc ở login tại 00:00:51.
- Consent observable: NOT_RECORDED.
- Data-quality limitations: Scenario delivery trước first captured action không được ghi. Không có usable speech, consent, moderator words, SUS segment hoặc probes trong recording; response set SUS P05 được người dùng cung cấp riêng. `PASSWORD_VISIBLE_IN_RECORDING — REDACTION_REQUIRED` trong login khoảng 00:00:39–00:00:46. Name và email cá nhân xuất hiện trong register/login cũng cần redaction.

## 2. Outcome

- Outcome: `FAILED_OR_ABANDONED` — task-end đã được người dùng xác nhận.
- Outcome rationale: Participant đăng ký thành công và tới login, nhưng task kết thúc khi vẫn ở login. Không có login submit/success, profile update, persistence check hoặc logout. Người dùng xác nhận đây là toàn bộ session.
- SC1: PASS.
- SC2: FAIL — login success không xuất hiện trước task end.
- SC3: NOT_REACHED.
- SC4: NOT_REACHED.
- SC5: NOT_REACHED.

## 3. Milestones and timing

| Milestone | Timestamp | Status/evidence |
|---|---|---|
| T0 | 00:00:01 | First captured task action: chọn `Đăng ký` từ product list. Scenario delivery không được ghi. |
| T1 | 00:00:02 | Register form xuất hiện. |
| T2 | 00:00:25 | First observed registration submit; keyboard đóng và form chuyển trạng thái. |
| T3 | 00:00:26 | Login page xuất hiện; registration thành công. |
| T4 | NOT_REACHED | Participant điền credential nhưng không có login submit quan sát được trước confirmed task end. |
| T5 | NOT_REACHED | Không có product list/authenticated header sau login. |
| T6 | NOT_REACHED | Profile không xuất hiện. |
| T7 | NOT_REACHED | Không có profile update. |
| T8 | NOT_REACHED | Không có update success. |
| T9 | NOT_OBSERVABLE | Không có usable speech hoặc persistence state. |
| T10 | NOT_REACHED | Không có logout. |
| T11 | 00:00:51 | Session kết thúc ở login; timestamp dựa trên recording end và xác nhận của người dùng. |

- Registration time: 25 giây (`T3 − T0`).
- Login time: NOT_CALCULABLE — T5 không đạt.
- Find-profile time: NOT_REACHED.
- Profile-update time: NOT_REACHED.
- Logout time: NOT_REACHED.
- Total task time: 50 giây (`T11 − T0`).

## 4. Behavioural metrics

- Wrong turns: `NOT_OBSERVABLE_AFTER_HUMAN_REVIEW` — một iOS password-manager prompt xuất hiện khoảng 00:00:27–00:00:29 rồi đóng; recording không đủ bằng chứng xác định prompt tự bật hay participant chủ động mở.
- Errors: 0 — không có validation/error message hoặc failed submit trong toàn bộ confirmed session.
- Hesitations >=5 seconds: 0 — không có stationary interval đạt ngưỡng trong toàn bộ confirmed session.
- Total hesitation duration: 0 giây.
- Repeated actions: 0 — không có repeated submit trong confirmed session.
- Think-aloud reminders: NOT_OBSERVABLE — audio là silence.
- Neutral prompts: NOT_OBSERVABLE.
- Task-directed interventions: NOT_OBSERVABLE.
- Card B used: NOT_OBSERVABLE; không có Card B hiển thị trên screen.

## 5. Timestamped observation log

| Timestamp/time range | Screen | Participant action | Observed event | Genuine quote | Event type | Moderator intervention | Evidence reference |
|---|---|---|---|---|---|---|---|
| 00:00:01–00:00:02 | Product list → Register | Chọn `Đăng ký`. | Register được tìm thấy và mở. | NOT_RECORDED — audio silence. | SUCCESS | NOT_OBSERVABLE | D05 @ 00:00:01–00:00:02 |
| 00:00:02–00:00:25 | Register | Điền name, email và password rồi submit. | Form chuyển sang login; không có visible validation error trong đoạn ghi. | NOT_RECORDED — audio silence. | SUCCESS | NOT_OBSERVABLE | D05 @ 00:00:02–00:00:26 |
| 00:00:26–00:00:30 | Login/iOS password prompt | Login xuất hiện; system password-manager prompt phủ một phần UI rồi biến mất. | Prompt/dismissal quan sát được, nhưng trigger và intent `NOT_OBSERVABLE_AFTER_HUMAN_REVIEW`. | NOT_RECORDED — audio silence. | OTHER | NOT_OBSERVABLE | D05 @ 00:00:26–00:00:30 |
| 00:00:30–00:00:39 | Login | Nhập email vào field `Username`. | Participant nhận ra đây là login dù heading hiển thị `Đăng Ký`. | NOT_RECORDED — audio silence. | OTHER | NOT_OBSERVABLE | D05 @ 00:00:30–00:00:39 |
| 00:00:39–00:00:46 | Login | Nhập password. | Password hiển thị plaintext; giá trị không được chép lại. | NOT_RECORDED — audio silence. | OTHER | NOT_OBSERVABLE | D05 @ 00:00:39–00:00:46 |
| 00:00:46–00:00:51 | Login | Keyboard đóng; màn hình vẫn ở login. | Không có login submit/success; task kết thúc tại 00:00:51 theo xác nhận của người dùng. | NOT_RECORDED — audio silence. | OTHER | NOT_OBSERVABLE | D05 @ 00:00:46–00:00:51 |

## 6. Intervention log

| Timestamp | Trigger | Exact moderator words | Participant response | Type | Card B |
|---|---|---|---|---|---|
| NOT_OBSERVABLE | Audio là digital silence. | NOT_RECORDED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE |

## 7. Raw SUS

| Source | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Response P05 | 4 | 3 | 4 | 2 | 3 | 3 | 4 | 2 | 3 | 3 |

- SUS score: 62.5.
- Recording limitation: Không có SUS form/segment; audio là silence.
- Data source: User-provided response set P05, supplied separately on 2026-07-31; participant ID confirmed on 2026-08-02.

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

- Screen recording: D05; playable/full-decode PASS.
- Audio: AAC stereo stream nhưng digital silence trong toàn bộ 00:00:00–00:00:51.
- SUS evidence: `Analysis/SUS_Raw_Responses.csv`, row P05 (`COMPLETED_USER_PROVIDED`); not captured in D05.
- Probe evidence: NOT_RECORDED.
- Bug screenshot/clip candidates:
  - Plaintext login password: D05 @ 00:00:39–00:00:46.
  - Redact name, email và toàn bộ plaintext password trước khi dùng.

## 10. Candidate findings and bugs

- Candidate usability finding IDs:
  - Không có participant-impact finding bổ sung đủ bằng chứng. Password-manager prompt 00:00:27–00:00:29 giữ là isolated `NOT_OBSERVABLE_AFTER_HUMAN_REVIEW` observation.
- Candidate software bug IDs:
  - `BUG-AUTH-PLAINTEXT-01` — login password hiển thị plaintext. Independent reproduction required: YES.
- Issues requiring independent reproduction: `BUG-AUTH-PLAINTEXT-01`.

## 11. Missing data

- Consent, moderator, exact date/time, exact device, browser/OS version: NOT_RECORDED/NOT_OBSERVABLE.
- Quotes, interventions, Card B và probes: NOT_RECORDED/NOT_OBSERVABLE. SUS Q1–Q10 được cung cấp riêng cho P05.
- Task end đã được xác nhận tại 00:00:51. Login submit/result, profile, update, persistence và logout: NOT_REACHED.
- Human review hoàn tất ngày 2026-08-02: register transition 00:00:24–00:00:27; password prompt 00:00:27–00:00:30; login input/end 00:00:39–00:00:51.
- Privacy redactions: all registration/login name/email data và plaintext password 00:00:39–00:00:46.
- Confidence:
  - Mapping D05→P05: HIGH — user confirmation.
  - T1–T3 visual milestones: HIGH; T0 MEDIUM vì scenario không được ghi.
  - Login credential input: HIGH; actual submit/login result: NOT_OBSERVABLE.
  - Password-manager prompt trigger/intent: LOW/`NOT_OBSERVABLE_AFTER_HUMAN_REVIEW`.
  - Outcome taxonomy: HIGH — người dùng xác nhận recording end là task end.

## 12. Verification status

`HUMAN_REVIEWED`

Lý do: task end ở login đã được xác nhận; observed evidence đã được mã hóa. SC2–SC5 không đạt; audio/probes/consent không được ghi; SUS P05 được cung cấp riêng và ID đã được xác nhận.

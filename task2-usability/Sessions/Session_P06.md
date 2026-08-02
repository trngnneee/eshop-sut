# Moderated Usability Session — P06

## 1. Video and data-quality metadata

- Drive filename: `D06` — replacement source do người dùng cung cấp; tên nguồn được ẩn vì là contact PII.
- Duration: 00:00:53 (metadata: 52,525 giây).
- Date/time, nếu quan sát được: NOT_OBSERVABLE.
- Device: Mobile touch-screen recording; exact device/model NOT_OBSERVABLE.
- OS: iOS-style system UI observable; version NOT_OBSERVABLE.
- Browser/version: iOS mobile-browser UI observable; exact browser/version `NOT_OBSERVABLE_AFTER_HUMAN_REVIEW`.
- Screen present: YES — portrait 1126×2436, HEVC, nominal 60 fps; full-decode PASS với non-monotonic DTS warnings.
- Audio present: AAC stereo có low-level signal (mean khoảng -74,3 dB; max khoảng -39,3 dB), nhưng VAD không phát hiện speech segment. ASR không-VAD sinh canned hallucinations và đã bị loại bỏ hoàn toàn; speech NOT_RECORDED.
- Video complete/cut: COMPLETE — người dùng xác nhận session thực sự kết thúc khi weak-password error còn hiển thị tại 00:00:53.
- Consent observable: NOT_RECORDED.
- Data-quality limitations: Không có usable speech, consent, moderator words, SUS segment hoặc probes trong recording; response set SUS P06 được người dùng cung cấp riêng. Session không tới login/profile/logout. Name và email cá nhân xuất hiện trong register cần redaction. Registration password được masked; không chép hoặc suy ra giá trị.

## 2. Outcome

- Outcome: `FAILED_OR_ABANDONED` — task-end đã được người dùng xác nhận.
- Outcome rationale: Participant mở register và submit bốn lần; cả bốn lần đều nhận weak-password error. Registration không thành công tại confirmed task end, nên SC1 fail và SC2–SC5 không đạt.
- SC1: FAIL — account chưa được tạo tại task end.
- SC2: NOT_REACHED.
- SC3: NOT_REACHED.
- SC4: NOT_REACHED.
- SC5: NOT_REACHED.

## 3. Milestones and timing

| Milestone | Timestamp | Status/evidence |
|---|---|---|
| T0 | 00:00:01 | First captured task action: chọn `Đăng ký` từ product list. Scenario delivery không được ghi. |
| T1 | 00:00:02 | Register form xuất hiện. |
| T2 | 00:00:22 | First registration submit; weak-password error xuất hiện ngay sau đó. |
| T3 | NOT_REACHED | Registration không thành công; recording kết thúc trên register. |
| T4 | NOT_REACHED | Login page không xuất hiện. |
| T5 | NOT_REACHED | Không có authenticated state. |
| T6 | NOT_REACHED | Profile không xuất hiện. |
| T7 | NOT_REACHED | Không có profile update. |
| T8 | NOT_REACHED | Không có update success. |
| T9 | NOT_OBSERVABLE | Không có data-save state hoặc usable speech. |
| T10 | NOT_REACHED | Không có logout. |
| T11 | 00:00:53 | Task kết thúc khi weak-password error vẫn hiển thị; timestamp dựa trên recording end và xác nhận của người dùng. |

- Registration time: NOT_CALCULABLE — T3 không đạt.
- Login time: NOT_REACHED.
- Find-profile time: NOT_REACHED.
- Profile-update time: NOT_REACHED.
- Logout time: NOT_REACHED.
- Total task time: 52 giây (`T11 − T0`).

## 4. Behavioural metrics

- Wrong turns: 0 — không có navigation wrong turn trong toàn bộ confirmed session.
- Errors: 4 — bốn registration submits đều tạo cùng weak-password error.
- Hesitations >=5 seconds: 0 — participant liên tục sửa input; không có stationary interval ≥5 giây trong toàn bộ confirmed session.
- Total hesitation duration: 0 giây.
- Repeated actions: 3 — ba registration submit repeats sau first submit.
- Think-aloud reminders: NOT_OBSERVABLE — không có usable speech.
- Neutral prompts: NOT_OBSERVABLE.
- Task-directed interventions: NOT_OBSERVABLE.
- Card B used: NOT_OBSERVABLE; không có Card B hiển thị trên screen.

## 5. Timestamped observation log

| Timestamp/time range | Screen | Participant action | Observed event | Genuine quote | Event type | Moderator intervention | Evidence reference |
|---|---|---|---|---|---|---|---|
| 00:00:01–00:00:02 | Product list → Register | Chọn `Đăng ký`. | Register được tìm thấy và mở. | NOT_RECORDED — no usable speech. | SUCCESS | NOT_OBSERVABLE | D06 @ 00:00:01–00:00:02 |
| 00:00:02–00:00:22 | Register | Điền name, email và masked password rồi submit lần đầu. | Weak-password validation xuất hiện; password value không quan sát/không chép lại. | NOT_RECORDED — no usable speech. | ERROR | NOT_OBSERVABLE | D06 @ 00:00:02–00:00:23 |
| 00:00:23–00:00:33 | Register | Xóa/sửa password và submit lần hai. | Cùng weak-password error xuất hiện. | NOT_RECORDED — no usable speech. | REPEATED_ACTION | NOT_OBSERVABLE | D06 @ 00:00:23–00:00:33 |
| 00:00:33–00:00:43 | Register | Tiếp tục xóa/sửa password và submit lần ba. | Cùng weak-password error xuất hiện. | NOT_RECORDED — no usable speech. | REPEATED_ACTION | NOT_OBSERVABLE | D06 @ 00:00:33–00:00:43 |
| 00:00:43–00:00:51 | Register | Sửa password lần nữa và submit lần bốn. | Cùng weak-password error xuất hiện; không có registration success. | NOT_RECORDED — no usable speech. | REPEATED_ACTION | NOT_OBSERVABLE | D06 @ 00:00:43–00:00:51 |
| 00:00:51–00:00:53 | Register error | Weak-password alert vẫn hiển thị. | Task kết thúc tại 00:00:53 theo xác nhận của người dùng. | NOT_RECORDED — no usable speech. | OTHER | NOT_OBSERVABLE | D06 @ 00:00:51–00:00:53 |

## 6. Intervention log

| Timestamp | Trigger | Exact moderator words | Participant response | Type | Card B |
|---|---|---|---|---|---|
| NOT_OBSERVABLE | Audio không có speech segment được VAD xác nhận. | NOT_RECORDED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE |

## 7. Raw SUS

| Source | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Response P06 | 3 | 2 | 4 | 3 | 4 | 2 | 4 | 3 | 3 | 2 |

- SUS score: 65.
- Recording limitation: Không có SUS form/segment và không có usable speech.
- Data source: User-provided response set P06, supplied separately on 2026-07-31; participant ID confirmed on 2026-08-02.

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

- Screen recording: D06 replacement; playable/full-decode PASS, non-monotonic DTS warnings noted.
- Integrity: SHA-256 `544EDA05B62A17088F8967433C20AF72056A080179ECB38ACE90F18CA8E31E1A`; khác D01, xác nhận đây không còn là duplicate.
- Audio: Low-level signal; VAD transcription có 0 speech segments. Non-VAD canned hallucinations bị loại bỏ, không dùng làm evidence.
- SUS evidence: `Analysis/SUS_Raw_Responses.csv`, row P06 (`COMPLETED_USER_PROVIDED`); not captured in D06.
- Probe evidence: NOT_RECORDED.
- Screenshot/clip candidates:
  - Four password-policy error cycles: D06 @ 00:00:22–00:00:53.
  - Redact name và email trước khi dùng. Password đã masked nhưng vẫn không dùng raw frame chưa review.

## 10. Candidate findings and bugs

- Candidate usability finding IDs:
  - `UF-REG-PASSWORD-RECOVERY-01` — participant nhận cùng weak-password error qua bốn submits và không hoàn thành registration tại task end. Group với P04 nhưng giữ khác biệt recovery: P04 tự sửa thành công, P06 không thành công.
- Candidate software bug IDs: NONE from P06 — masked password không cho phép xác minh input có đáp ứng policy hay không; không kết luận validator sai.
- Issues requiring independent reproduction: NONE from P06.

## 11. Missing data

- Consent, moderator, exact date/time, exact device, OS/browser version: NOT_RECORDED/NOT_OBSERVABLE.
- Quotes, intervention words/types, Card B và probes: NOT_RECORDED/NOT_OBSERVABLE. SUS Q1–Q10 được cung cấp riêng cho P06.
- Task end đã được xác nhận tại 00:00:53. Registration success, login, profile, update, persistence và logout: NOT_REACHED.
- Human review hoàn tất ngày 2026-08-02: first submit/error 00:00:21–00:00:23; repeated recovery cycles 00:00:23–00:00:51; final error/task end 00:00:51–00:00:53.
- Privacy redactions: registration name và email; giữ password masked và không chép giá trị.
- Confidence:
  - Mapping replacement D06→P06: HIGH — user confirmation.
  - File independence from D01: HIGH — distinct SHA-256 and media metadata.
  - T1/T2 and four error cycles: HIGH; timestamps rounded to whole seconds.
  - Error count/repeated actions: HIGH.
  - Absence of speech: HIGH for automated VAD; genuine quote remains NOT_RECORDED.
  - Outcome taxonomy: HIGH — người dùng xác nhận recording end là task end.

## 12. Verification status

`HUMAN_REVIEWED`

Lý do: task end ở registration error đã được xác nhận; observed evidence đã được mã hóa. SC1–SC5 không hoàn thành; speech/probes/consent không được ghi; SUS P06 được cung cấp riêng và ID đã được xác nhận.

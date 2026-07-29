# Moderated Usability Session — P03

## 1. Video and data-quality metadata

- Drive filename: `D03` — tên nguồn được ẩn vì là contact PII.
- Duration: 00:00:04 (metadata chính xác: 4.369 giây).
- Date/time, nếu quan sát được: NOT_OBSERVABLE.
- Device: Desktop/laptop screen recording; exact device NOT_OBSERVABLE.
- OS: Desktop OS UI observable; exact OS/version NOT_OBSERVABLE.
- Browser/version: Desktop browser observable; exact browser/version NOT_OBSERVABLE.
- Screen present: YES — 1376×736, H.264; average rate xấp xỉ 30 fps.
- Audio present: Có AAC stereo stream nhưng digital silence (`mean -91 dB`, `max -90.3 dB`); nội dung audio NOT_RECORDED.
- Video complete/cut: COMPLETE — người dùng xác nhận toàn bộ session chỉ dài 4,369 giây và kết thúc ở register page.
- Consent observable: NOT_RECORDED.
- Data-quality limitations: Session chỉ dài 4,369 giây; không ghi scenario, hành động task rõ ràng, registration submit, login, profile hoặc logout. SUS, probes và consent được người dùng xác nhận là không được thu thập. Full-decode thành công nhưng có non-monotonic DTS warnings. Không dùng giá trị 0 cho metrics của flow không quan sát được.

## 2. Outcome

- Outcome: `FAILED_OR_ABANDONED` — task-end đã được người dùng xác nhận.
- Outcome rationale: Session chỉ cho thấy register form trong khoảng 4 giây và kết thúc trước submit. Người dùng xác nhận đây là toàn bộ session; không success criterion nào được đáp ứng tại task end.
- SC1: NOT_REACHED.
- SC2: NOT_REACHED.
- SC3: NOT_REACHED.
- SC4: NOT_REACHED.
- SC5: NOT_REACHED.

## 3. Milestones and timing

| Milestone | Timestamp | Status/evidence |
|---|---|---|
| T0 | NOT_OBSERVABLE | Không quan sát action đầu tiên sau scenario; scenario không được ghi và form đã mở ở frame đầu. |
| T1 | 00:00:00 | Register page đã hiện tại recording start; actual open/recognition time NOT_OBSERVABLE. |
| T2 | NOT_REACHED | Không có submit registration. |
| T3 | NOT_REACHED | Không có registration success/login transition. |
| T4 | NOT_REACHED | Không có login. |
| T5 | NOT_REACHED | Không có login success. |
| T6 | NOT_REACHED | Không có profile. |
| T7 | NOT_REACHED | Không có profile update submit. |
| T8 | NOT_REACHED | Không có profile save. |
| T9 | NOT_REACHED | Không có trust/persistence statement. |
| T10 | NOT_REACHED | Không có logout. |
| T11 | 00:00:04 | Recording end là task end theo xác nhận của người dùng. |

- Registration time: NOT_OBSERVABLE.
- Login time: NOT_REACHED.
- Find-profile time: NOT_REACHED.
- Profile-update time: NOT_REACHED.
- Logout time: NOT_REACHED.
- Total task time: NOT_OBSERVABLE.

## 4. Behavioural metrics

- Wrong turns: NOT_OBSERVABLE.
- Errors: NOT_OBSERVABLE.
- Hesitations >=5 seconds: NOT_OBSERVABLE — recording ngắn hơn ngưỡng 5 giây.
- Total hesitation duration: NOT_OBSERVABLE.
- Repeated actions: NOT_OBSERVABLE.
- Think-aloud reminders: NOT_OBSERVABLE — audio silent.
- Neutral prompts: NOT_OBSERVABLE — audio silent.
- Task-directed interventions: NOT_OBSERVABLE — audio silent.
- Card B used: NOT_OBSERVABLE.

## 5. Timestamped observation log

| Timestamp/time range | Screen | Participant action | Observed event | Genuine quote | Event type | Moderator intervention | Evidence reference |
|---|---|---|---|---|---|---|---|
| 00:00:00–00:00:04 | Register | Không quan sát click, typing hoặc submit đủ rõ để mã hóa thành task action. | Register form hiển thị; video kết thúc sau 4.369 giây. | NOT_RECORDED — audio silent. | OTHER | NOT_OBSERVABLE | D03 @ 00:00:00–00:00:04 |

## 6. Intervention log

| Timestamp | Trigger | Exact moderator words | Participant response | Type | Card B |
|---|---|---|---|---|---|
| NOT_OBSERVABLE | Audio digital silence và clip 4 giây. | NOT_RECORDED | NOT_OBSERVABLE | NOT_OBSERVABLE | NOT_OBSERVABLE |

## 7. Raw SUS

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED | NOT_RECORDED |

- SUS score: NOT_CALCULABLE.
- Missing SUS data: Q1–Q10.
- Data source: Không có SUS segment.

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

- Screen recording: D03; playable/full-decode PASS WITH DTS WARNINGS.
- Audio: Digital silence 00:00:00–00:00:04.
- SUS evidence: NOT_RECORDED.
- Probe evidence: NOT_RECORDED.
- Bug screenshot/clip candidates: NONE — không đủ participant action/evidence.

## 10. Candidate findings and bugs

- Candidate usability finding IDs: NONE — clip không đủ dữ liệu.
- Candidate software bug IDs: NONE — clip không đủ dữ liệu.
- Issues requiring independent reproduction: NONE từ P03.

## 11. Missing data

- Người dùng xác nhận đây là toàn bộ session; không có phần recording bổ sung.
- Toàn bộ task actions, success criteria, timing, metrics, intervention, quote, SUS, probes, persistence và logout ngoài 4 giây đầu: NOT_RECORDED/NOT_OBSERVABLE.
- Consent, moderator, date/time, exact environment: NOT_RECORDED.
- Privacy redactions: Source filename là contact PII và phải giữ masked; không quan sát credential/profile PII trong clip 4 giây.
- Human review: Toàn bộ D03 @ 00:00:00–00:00:04.
- Confidence:
  - Mapping D03→P03: HIGH — người dùng xác nhận trực tiếp.
  - Duration/screen/audio quality: HIGH.
  - Outcome finality: HIGH — recording end được xác nhận là task end.
  - Mọi metric/task conclusion ngoài việc register page xuất hiện: NOT_OBSERVABLE.

## 12. Verification status

`READY_FOR_HUMAN_REVIEW`

Lý do: toàn bộ session đã được xác nhận nhưng chỉ dài 4,369 giây; observed evidence đã được mã hóa và phần lớn task data vẫn NOT_OBSERVABLE/NOT_REACHED.

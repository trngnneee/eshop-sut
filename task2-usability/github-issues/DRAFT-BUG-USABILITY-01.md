# [DRAFT] BUG-PF-02 — Profile rejects FR-04 leading-zero phone format

**Status:** `PARTICIPANT_EVIDENCE_RECORDED — DO_NOT_PUBLISH`
**GitHub action:** Draft only; human review, fresh independent reproduction, redaction và duplicate search bắt buộc trước khi đăng.

## Summary

Profile phone validation từ chối test phone phù hợp FR-04 (bắt đầu bằng `0`, 10–11 chữ số). Trong một observed recovery, hệ thống lại hiển thị success sau khi dùng format không bắt đầu bằng `0`.

## Requirement

FR-04: phone phải bắt đầu bằng `0` và có 10–11 chữ số.

## Environment

- SUT: EShop Web Frontend.
- URL/page: `/profile`.
- SUT commit/build: NOT_RECORDED in participant videos.
- Browsers/devices: mixed desktop recordings; exact versions NOT_OBSERVABLE.
- Account/data: test-only; không dùng hoặc đính kèm PII thật.

## Preconditions

1. Có account test hợp lệ.
2. Login thành công.
3. Mở profile.
4. Dùng generic test name/address và phone; không chép participant values.

## Steps to reproduce

1. Nhập một phone test 10 chữ số bắt đầu bằng `0`.
2. Điền các required profile fields bằng test data.
3. Chọn `Cập nhật`.
4. Lặp boundary check với phone 11 chữ số bắt đầu bằng `0`.
5. Kiểm tra control case không bắt đầu bằng `0`.
6. Nếu save thành công, reload/revisit profile để kiểm tra persistence.

## Expected result

- 10- và 11-digit leading-zero phones được chấp nhận.
- Non-leading-zero phone bị từ chối.
- Error copy phản ánh chính xác FR-04.
- Saved value tồn tại sau reload.

## Actual result from participant evidence

- P01: năm profile submits nhận phone-invalid error; không hoàn thành SC3.
- P02: first update có leading-zero 10-digit phone nhưng bị từ chối; ba submits thất bại trước confirmed task end.
- P04: leading-zero 10/11-digit phones bị từ chối; non-leading-zero format nhận success alert.

Raw phone values không được ghi trong draft.

## Participant evidence

- P01/D01 @ 00:00:53–00:01:49.
- P02/D02 @ 00:00:57–00:01:34.
- P04/D04 @ 00:01:43–00:02:09.
- Frequency: 3/7 distinct official participants.
- Genuine quote: NOT_RECORDED.

## Impact

Blocks the required profile-update task with a specification-conforming value. Participants repeat attempts; P01/P02 do not reach a successful save, and P04 only sees success with a format that violates FR-04.

## Severity/priority

- Provisional severity: `S1`.
- Priority: PRODUCT/ENGINEERING OWNER TO ASSIGN.
- Rationale: Required flow cannot be completed through a reasonable spec-compliant recovery path.

## Suggested fix

- Share a single FR-04 validator across client/server.
- Accept exactly 10–11 digits beginning with `0`.
- Reject non-leading-zero values.
- Use field-linked error copy that states the accepted rule.
- Preserve other fields and return focus to phone.

## Retest acceptance criteria

- [ ] 10-digit leading-zero boundary passes.
- [ ] 11-digit leading-zero boundary passes.
- [ ] 9-digit and 12-digit values fail with correct message.
- [ ] Non-leading-zero value fails.
- [ ] Valid saved value persists after reload/revisit.
- [ ] 5/5 usability retest participants complete first valid update without workaround/assistance.

## Evidence handling

- Screenshot/clip candidates: participant timestamps above.
- Required redaction: name, email, all phone digits, address, password and unrelated browser PII.
- Redacted participant attachment: NOT_CREATED.
- Technical preflight exists under `../evidence/technical-preflight/`, but is not participant evidence and does not replace a fresh reproduction.

## Publication gate

- [ ] Human verifies participant timestamps/counts.
- [ ] Fresh independent reproduction completed with test-only data.
- [ ] Redacted evidence created and reviewed.
- [ ] Existing GitHub issues searched; duplicate disposition recorded.
- [ ] Requirement/build/environment confirmed.
- [ ] Severity approved.
- [ ] Reviewer explicitly approves publication.
- [ ] Published URL added to all traceability files.

**Published GitHub URL:** `NOT_CREATED`

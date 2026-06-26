# AI Session Log - FR-04 & FR-10 Bug Mapping

## Metadata

| Field | Value |
| :--- | :--- |
| Date / Time | 2026-06-26 22:17:11 +07 |
| Workspace | `eshop-sut` |
| AI Agent | Codex |
| Tester in test run | Đặng Trường Nguyên |
| Scope | Map failed test cases to BUG IDs, update test case statuses, create GitHub issue-ready bug files for FR-04 and FR-10. |

## User Requests

1. Map BUG IDs, đặt tên bug, update status cho các test case FR-04 sau khi test xong trong file test run.
2. Tạo folder bug trong `tests`, dùng issue template để ghi list bug cho FR-04, để trống evidence cho tester bổ sung sau.
3. Làm tương tự cho FR-10.
4. Export session này ra `ai_log` trong `tests`.

## FR-04 Work Summary

### Input Artifact

- `tests/test-runs/fr04-profile-management-test-run.md`
- `tests/test-cases/profile_management/`

### Updates Applied

- Updated test run summary to `32` total test cases: `20 Passed`, `12 Failed`.
- Mapped all failed FR-04 rows to grouped BUG IDs by root cause.
- Updated `Status / Related bugs` in all 32 FR-04 test case files.
- Created GitHub issue-ready bug list at `tests/bug/FR-04.md`.

### FR-04 Bug Mapping

| Bug ID | Related Test Cases | Summary | Severity |
| :--- | :--- | :--- | :--- |
| `BUG-FR04-N-01` | `FR04-N-BVA-TC07` | Thiếu validate độ dài tối đa Họ Tên theo assumption BVA. | Low |
| `BUG-FR04-P-01` | `FR04-P-BVA-TC02`, `FR04-P-BVA-TC03`, `FR04-P-BVA-TC04`, `FR04-P-TC02`, `FR04-P-TC03`, `FR04-P-TC05` | Validation Số điện thoại sai rule FR-04: không chấp nhận số bắt đầu bằng `0` dài 10-11 chữ số và hiển thị rule 9-10 chữ số. | High |
| `BUG-FR04-A-01` | `FR04-A-TC01`, `FR04-A-BVA-TC01`, `FR04-A-BVA-TC07`, `FR04-A-TC03` | Thiếu validate bắt buộc, trim và giới hạn độ dài cho Địa chỉ giao hàng. | Medium |
| `BUG-FR04-R-01` | `FR04-R-TC01` | API `PUT /api/users/me` cho phép client gửi `role` và tự thay đổi quyền. | High |

### FR-04 Output Artifacts

- `tests/test-runs/fr04-profile-management-test-run.md`
- `tests/test-cases/profile_management/*.md`
- `tests/bug/FR-04.md`

## FR-10 Work Summary

### Input Artifact

- `tests/test-runs/fr10-order-state-machine-test-run.md`
- `tests/test-cases/order_state_machine/`

### Updates Applied

- Updated test run summary to `23` total test cases: `21 Passed`, `2 Failed`.
- Mapped failed FR-10 rows to BUG IDs by endpoint/root cause.
- Updated `Status / Related bugs` in all 23 FR-10 test case files.
- Created GitHub issue-ready bug list at `tests/bug/FR-10.md`.

### FR-10 Bug Mapping

| Bug ID | Related Test Cases | Summary | Severity |
| :--- | :--- | :--- | :--- |
| `BUG-FR10-S-01` | `FR10-S-TC12` | Endpoint user cancel cho phép hủy đơn hàng đang ở trạng thái `shipping`. | High |
| `BUG-FR10-S-02` | `FR10-S-TC16` | Endpoint admin status cho phép chuyển final state `canceled` sang `delivered`. | High |

### FR-10 Output Artifacts

- `tests/test-runs/fr10-order-state-machine-test-run.md`
- `tests/test-cases/order_state_machine/*.md`
- `tests/bug/FR-10.md`

## Issue File Format

The generated bug files follow the repository's issue-template style:

- `Found by Test Case`
- `Requirement liên quan`
- `Severity / Priority`
- `Environment`
- `Steps to reproduce`
- `Expected result`
- `Actual result`
- `Evidence`

Evidence placeholders were intentionally left as `[Bổ sung evidence sau]` for tester-provided screenshots, videos, logs, or API responses.

## Verification Performed

### FR-04

- Checked no remaining placeholders in FR-04 artifacts:
  - `Not Run`
  - `Failed | None`
  - `[BUG-ID]`
  - `[TC ID]`
  - `[Tóm tắt lỗi]`
- Verified test run counts:
  - `Passed 20`
  - `Failed 12`
- Verified each FR-04 BUG ID appears in:
  - `tests/test-runs/fr04-profile-management-test-run.md`
  - related failed test case files
  - `tests/bug/FR-04.md`

### FR-10

- Checked no remaining placeholders in FR-10 artifacts:
  - `Not Run`
  - `Failed | None`
  - `[BUG-ID]`
  - `[TC ID]`
  - `[Tóm tắt lỗi]`
- Verified test run counts:
  - `Passed 21`
  - `Failed 2`
- Verified each FR-10 BUG ID appears in:
  - `tests/test-runs/fr10-order-state-machine-test-run.md`
  - related failed test case files
  - `tests/bug/FR-10.md`

## Notes

- Runtime source files were inspected only to understand likely root causes; this session did not patch application code.
- Existing unrelated dirty files outside the test artifacts were left unchanged.
- Bug evidence is pending tester input.

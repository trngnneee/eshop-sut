# TC-REGISTER-011: Kiểm thử Mật khẩu để trống

## Requirement ID
FR-01

## Module / Test type / Technique
Register / Functional / Equivalence Partitioning

## Preconditions
- Người dùng đang ở form của FR-01

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Mật khẩu | [Để trống] |

## Test steps
1. Mở form FR-01.
2. Nhập các trường khác hợp lệ ngoại trừ Mật khẩu để trống.
3. Bấm nút Submit.

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập cho trường Mật khẩu.

## Status / Related bugs
Not Run / None

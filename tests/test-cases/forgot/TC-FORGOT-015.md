# TC-FORGOT-015: Kiểm thử Mật khẩu mới thiếu chữ số

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | TestTest! |
| Xác nhận mật khẩu mới | TestTest! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `TestTest!` (không có chữ số) và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì mật khẩu thiếu ít nhất 1 chữ số (theo FR-01).
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-P05 (thiếu chữ số)

## Type
Invalid

## Status / Related bugs
Not Run / None

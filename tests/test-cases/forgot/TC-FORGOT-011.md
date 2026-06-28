# TC-FORGOT-011: Kiểm thử Mật khẩu mới để trống

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
| Mật khẩu mới | [Để trống] |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Để trống trường Mật khẩu mới; nhập Xác nhận mật khẩu `NewPass1!`.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập Mật khẩu mới.
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-P01 (mật khẩu mới rỗng)

## Type
Invalid

## Status / Related bugs
Not Run / None

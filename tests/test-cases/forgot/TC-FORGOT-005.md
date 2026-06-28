# TC-FORGOT-005: Kiểm thử OTP để trống (Bước 2)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [Để trống] |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Để trống trường OTP.
3. Nhập Mật khẩu mới và Xác nhận mật khẩu hợp lệ `NewPass1!`.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập OTP.
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-O01 (OTP rỗng)

## Type
Invalid

## Status / Related bugs
Not Run / None

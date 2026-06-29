# TC-FORGOT-044: Mật khẩu mới ở biên tối thiểu, Xác nhận ở min− — không khớp — Cross-boundary

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / BVA – Cross-boundary

## Boundary under test
Mật khẩu mới at min (8) + Xác nhận at min− (7) — vi phạm ràng buộc khớp nhau tại biên

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Abc@1234 |
| Xác nhận mật khẩu mới | Abc@123 |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `Abc@1234` (8 ký tự — biên tối thiểu hợp lệ) và Xác nhận `Abc@123` (7 ký tự — dưới biên).
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì hai trường mật khẩu không khớp nhau.
- Mật khẩu không được thay đổi.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #4

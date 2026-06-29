# TC-FORGOT-039: Kiểm thử Xác nhận mật khẩu với độ dài ngay dưới tối đa (49 ký tự)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
Xác nhận mật khẩu at max− — value: 49 ký tự (`Aa1!` + 45 ký tự `x`)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| Xác nhận mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới và Xác nhận mật khẩu đều có độ dài 49 ký tự và khớp nhau.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống chấp nhận và đặt lại mật khẩu thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

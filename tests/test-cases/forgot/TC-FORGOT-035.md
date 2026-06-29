# TC-FORGOT-035: Kiểm thử Mật khẩu mới với độ dài vượt quá tối đa (51 ký tự)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
Mật khẩu mới at max+ — value: 51 ký tự (`Aa1!` + 47 ký tự `x`)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| Xác nhận mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới có độ dài 51 ký tự và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống báo lỗi độ dài Mật khẩu vượt quá giới hạn tối đa 50 ký tự.
- Mật khẩu không được thay đổi.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #7

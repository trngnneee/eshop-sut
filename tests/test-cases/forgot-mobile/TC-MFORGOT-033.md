# TC-MFORGOT-033: Kiểm thử Mật khẩu mới với độ dài ngay dưới tối đa (49 ký tự)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Boundary Value Analysis

## Boundary under test
Mật khẩu mới at max− — value: 49 ký tự (`Aa1!` + 45 ký tự `x`)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| Xác nhận mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |

## Test steps
> **Lưu ý:** Theo FR-22, Bước 2 phải có trường Xác nhận mật khẩu mới (nếu có trên UI).
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới có độ dài 49 ký tự (đủ hoa/thường/số/ký tự đặc biệt) và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống chấp nhận mật khẩu 49 ký tự và đặt lại mật khẩu thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Fail / #7
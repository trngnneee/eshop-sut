# TC-FORGOT-030: Kiểm thử Mật khẩu mới với độ dài dưới tối thiểu (7 ký tự)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
Mật khẩu mới at min− — value: `Abc@123` (7 ký tự)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Abc@123 |
| Xác nhận mật khẩu mới | Abc@123 |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `Abc@123` (7 ký tự) và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì mật khẩu không đạt tối thiểu 8 ký tự (theo FR-01).
- Mật khẩu không được thay đổi.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #7

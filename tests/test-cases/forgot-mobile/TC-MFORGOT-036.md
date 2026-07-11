# TC-MFORGOT-036: Kiểm thử Xác nhận mật khẩu với độ dài dưới tối thiểu (7 ký tự)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Boundary Value Analysis

## Boundary under test
Xác nhận mật khẩu at min− — value: `Abc@123` (7 ký tự)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Abc@1234 |
| Xác nhận mật khẩu mới | Abc@123 |

## Test steps
> **Lưu ý:** Theo FR-22, Bước 2 phải có trường Xác nhận mật khẩu mới (nếu có trên UI).
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `Abc@1234` (8 ký tự) và Xác nhận mật khẩu `Abc@123` (7 ký tự).
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì hai trường mật khẩu không khớp nhau hoặc xác nhận không đạt độ dài tối thiểu.
- Mật khẩu không được thay đổi.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #4
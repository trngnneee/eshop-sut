# TC-MFORGOT-032: Kiểm thử Mật khẩu mới với độ dài ngay trên tối thiểu (9 ký tự)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Boundary Value Analysis

## Boundary under test
Mật khẩu mới at min+ — value: `Abc@12345` (9 ký tự)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Abc@12345 |
| Xác nhận mật khẩu mới | Abc@12345 |

## Test steps
> **Lưu ý:** Theo FR-22, Bước 2 phải có trường Xác nhận mật khẩu mới (nếu có trên UI).
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `Abc@12345` (9 ký tự) và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống chấp nhận mật khẩu 9 ký tự và đặt lại mật khẩu thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Fail / #7
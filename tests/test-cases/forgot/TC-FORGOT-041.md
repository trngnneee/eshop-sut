# TC-FORGOT-041: Kiểm thử Xác nhận mật khẩu với độ dài vượt quá tối đa (51 ký tự)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Boundary Value Analysis

## Boundary under test
Xác nhận mật khẩu at max+ — value: 51 ký tự (`Aa1!` + 47 ký tự `x`)

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
| Xác nhận mật khẩu mới | Aa1!xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới 50 ký tự và Xác nhận mật khẩu 51 ký tự (không khớp độ dài).
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì hai trường mật khẩu không khớp hoặc xác nhận vượt giới hạn 50 ký tự.
- Mật khẩu không được thay đổi.

## Valid / Invalid
Invalid

## Status / Related bugs
Not Run / None

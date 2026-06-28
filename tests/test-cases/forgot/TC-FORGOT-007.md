# TC-FORGOT-007: Kiểm thử OTP có độ dài ngắn hơn 6 chữ số

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | 12345 |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP `12345` (5 chữ số).
3. Nhập Mật khẩu mới và Xác nhận mật khẩu hợp lệ `NewPass1!`.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối OTP vì độ dài không đúng 6 chữ số.
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-O03 (OTP độ dài < 6)

## Type
Invalid

## Status / Related bugs
Not Run / None

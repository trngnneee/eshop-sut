# TC-FORGOT-018: Kiểm thử Xác nhận mật khẩu không khớp Mật khẩu mới

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass2! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `NewPass1!` và Xác nhận mật khẩu `NewPass2!` (không khớp).
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì hai trường mật khẩu không khớp nhau.
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-C02 (xác nhận mật khẩu không khớp)

## Type
Invalid

## Status / Related bugs
Not Run / None

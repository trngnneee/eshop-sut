# TC-FORGOT-010: Kiểm thử OTP của email A dùng cho email B

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Tài khoản `test@eshop.com` và `admin@eshop.com` đều tồn tại trong hệ thống
- Đã lấy OTP cho `test@eshop.com` ở Bước 1

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email yêu cầu OTP (Bước 1) | test@eshop.com |
| Email khi đặt lại (Bước 2) | admin@eshop.com |
| OTP | [OTP nhận được từ yêu cầu của test@eshop.com] |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com` và ghi nhận OTP.
2. ⚠️ Gửi yêu cầu đặt lại mật khẩu với Email `admin@eshop.com` nhưng dùng OTP của `test@eshop.com` (qua API `POST /api/reset-password` hoặc thao tác tương đương nếu UI không cho đổi email).
3. Quan sát phản hồi hệ thống.

## Expected result
- Hệ thống từ chối vì OTP chỉ hợp lệ cho email đã yêu cầu.
- Mật khẩu của `admin@eshop.com` không bị thay đổi.

## Sub-domains covered
SD-O07 (OTP hợp lệ nhưng gắn với email khác)

## Type
Invalid

## Status / Related bugs
Pass / None

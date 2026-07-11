# TC-MFORGOT-016: Kiểm thử Mật khẩu mới thiếu ký tự đặc biệt

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Đã hoàn thành Bước 1 thành công với Email `test@eshop.com` và đang ở Bước 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| OTP | [OTP hợp lệ từ Bước 1] |
| Mật khẩu mới | Test1234 |
| Xác nhận mật khẩu mới | Test1234 |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `Test1234` (không có ký tự đặc biệt thuộc `@$!%*?&`) và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì mật khẩu thiếu ít nhất 1 ký tự đặc biệt (`@`, `$`, `!`, `%`, `*`, `?`, `&`) theo FR-01.
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-P06 (thiếu ký tự đặc biệt)

## Type
Invalid

## Status / Related bugs
Fail / #7
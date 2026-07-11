# TC-MFORGOT-013: Kiểm thử Mật khẩu mới thiếu chữ hoa

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
| Mật khẩu mới | test1234! |
| Xác nhận mật khẩu mới | test1234! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ.
3. Nhập Mật khẩu mới `test1234!` (không có chữ hoa) và Xác nhận mật khẩu khớp.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối vì mật khẩu thiếu ít nhất 1 chữ hoa (theo FR-01).
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-P03 (thiếu chữ hoa)

## Type
Invalid

## Status / Related bugs
Fail / #7
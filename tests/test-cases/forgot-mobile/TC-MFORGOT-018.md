# TC-MFORGOT-018: Kiểm thử Xác nhận mật khẩu không khớp Mật khẩu mới

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
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass2! |

## Test steps
> **Lưu ý:** Theo FR-22, Bước 2 phải có trường Xác nhận mật khẩu mới.
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
Fail / #4
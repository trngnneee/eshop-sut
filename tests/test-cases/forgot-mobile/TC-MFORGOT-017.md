# TC-MFORGOT-017: Kiểm thử Xác nhận mật khẩu mới để trống

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
| Xác nhận mật khẩu mới | [Để trống] |

## Test steps
> **Lưu ý:** Theo FR-22, Bước 2 phải có trường Xác nhận mật khẩu mới.
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP hợp lệ và Mật khẩu mới `NewPass1!`.
3. Để trống trường Xác nhận mật khẩu mới.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối submit và hiển thị thông báo lỗi bắt buộc nhập Xác nhận mật khẩu.
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-C01 (xác nhận mật khẩu rỗng)

## Type
Invalid

## Status / Related bugs
Fail / #4
# TC-MFORGOT-006: Kiểm thử OTP chứa ký tự không phải số

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
| OTP | 12AB56 |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Hoàn thành Bước 1 với Email `test@eshop.com`.
2. Nhập OTP `12AB56`.
3. Nhập Mật khẩu mới và Xác nhận mật khẩu hợp lệ `NewPass1!`.
4. Bấm "Đặt lại mật khẩu".

## Expected result
- Hệ thống từ chối OTP vì chỉ chấp nhận mã gồm 6 chữ số.
- Mật khẩu không được thay đổi.

## Sub-domains covered
SD-O02 (OTP chứa ký tự không phải số)

## Type
Invalid

## Status / Related bugs
Fail / #6
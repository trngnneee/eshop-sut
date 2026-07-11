# TC-MFORGOT-SUP-002: Demo hiển thị OTP trên màn hình Mobile (FR-03)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Tài khoản `test@eshop.com` tồn tại

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu (Bước 1).
2. Nhập Email `test@eshop.com`, bấm "Lấy mã OTP".
3. Quan sát hộp thông báo / message sau Bước 1 trên Mobile.
4. So sánh với giá trị `resetToken` từ API (nếu cần).

## Expected result
- Môi trường demo: màn hình hiển thị **trực tiếp** mã OTP 6 chữ số (ví dụ "Mã OTP của bạn là: 123456").
- Không chỉ hiển thị message chung không chứa mã.

## Sub-domains covered
GAP-03 — Demo OTP on screen

## Type
Valid

## Status / Related bugs
Fail / #20
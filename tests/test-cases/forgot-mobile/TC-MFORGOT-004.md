# TC-MFORGOT-004: Kiểm thử Email chưa đăng ký trong hệ thống (Bước 1)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Email `unknown.user@eshop.com` chưa tồn tại trong hệ thống
- Người dùng đang ở Bước 1 của màn hình Quên Mật Khẩu trên Mobile App

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | unknown.user@eshop.com |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu (Bước 1).
2. Nhập Email `unknown.user@eshop.com`.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống từ chối yêu cầu vì Email chưa được đăng ký.
- Không sinh OTP và không chuyển sang Bước 2.

## Sub-domains covered
SD-E03 (email hợp lệ định dạng nhưng chưa đăng ký)

## Type
Invalid

## Status / Related bugs
Pass / None
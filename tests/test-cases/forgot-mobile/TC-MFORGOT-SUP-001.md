# TC-MFORGOT-SUP-001: API sinh OTP đúng 6 chữ số + label UI Mobile

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Supplementary

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Tài khoản `test@eshop.com` tồn tại
- Backend API đang chạy tại `http://localhost:3000`

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |

## Test steps
1. Gửi `POST /api/forgot-password` với body `{"email":"test@eshop.com"}`.
2. Đọc trường `resetToken` trong response JSON; kiểm tra regex `^\\d{6}$`.
3. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu (Bước 1).
4. Nhập Email `test@eshop.com`, bấm "Lấy mã OTP", chuyển sang Bước 2.
5. Kiểm tra label OTP trên màn hình Mobile (phải mô tả **6 số**, không phải 4).

## Expected result
- API: `resetToken` gồm **đúng 6 chữ số**.
- Mobile UI: label hiển thị "Mã OTP (6 số)" hoặc tương đương; không ghi "4 số".

## Sub-domains covered
GAP-02 — OTP length contract (API + Mobile label)

## Type
Valid

## Status / Related bugs
Fail / #6
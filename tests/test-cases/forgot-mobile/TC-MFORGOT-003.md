# TC-MFORGOT-003: Kiểm thử Email sai định dạng (Bước 1)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Người dùng đang ở Bước 1 của màn hình Quên Mật Khẩu trên Mobile App

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | not-an-email |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu (Bước 1).
2. Nhập Email `not-an-email`.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống từ chối yêu cầu và hiển thị thông báo lỗi định dạng Email không hợp lệ.
- Không chuyển sang Bước 2.

## Sub-domains covered
SD-E02 (email sai định dạng)

## Type
Invalid

## Status / Related bugs
Fail / None
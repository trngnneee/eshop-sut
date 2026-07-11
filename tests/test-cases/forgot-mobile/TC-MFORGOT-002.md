# TC-MFORGOT-002: Kiểm thử Email để trống (Bước 1)

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
| Email | [Để trống] |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu (Bước 1).
2. Để trống trường Email.
3. Bấm "Lấy mã OTP".

## Expected result
- Hệ thống từ chối gửi yêu cầu và hiển thị thông báo lỗi bắt buộc nhập Email.
- Không chuyển sang Bước 2.

## Sub-domains covered
SD-E01 (email rỗng)

## Type
Invalid

## Status / Related bugs
Fail / None
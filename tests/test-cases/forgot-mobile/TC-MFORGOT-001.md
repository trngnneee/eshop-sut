# TC-MFORGOT-001: Đặt lại mật khẩu thành công với toàn bộ dữ liệu hợp lệ (on-point)

## Requirement ID
FR-22

## Module / Test type / Technique
Forgot Password (Mobile) / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Mobile App (React Native + Expo) đang chạy và kết nối Backend API tại IP LAN máy chủ
- Tài khoản `test@eshop.com` đã tồn tại trong hệ thống
- Người dùng đang ở màn hình Quên Mật Khẩu trên Mobile App

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email (Bước 1) | test@eshop.com |
| OTP (Bước 2) | [Mã OTP 6 chữ số hiển thị trên màn hình sau Bước 1] |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Mở Mobile App, vào màn hình Đăng nhập, bấm "Quên mật khẩu?" để vào màn hình Quên Mật Khẩu.
2. Nhập Email `test@eshop.com` và bấm "Lấy mã OTP".
3. Xác nhận hệ thống chuyển sang Bước 2 và hiển thị mã OTP trên màn hình (môi trường demo; nếu UI không hiển thị OTP, lấy từ response API POST /api/forgot-password).
4. Nhập OTP vừa nhận, Mật khẩu mới `NewPass1!`, và Xác nhận mật khẩu mới `NewPass1!` (nếu có trường xác nhận theo đặc tả).
5. Bấm "Đặt lại mật khẩu".

## Expected result
- Bước 1: Hệ thống sinh OTP 6 chữ số và hiển thị trên màn hình (demo).
- Bước 2: Đặt lại mật khẩu thành công; người dùng được chuyển về màn hình Đăng nhập trên Mobile App.
- Đăng nhập bằng mật khẩu mới `NewPass1!` thành công.

## Sub-domains covered
SD-E04 (email đã đăng ký, hợp lệ), SD-O06 (OTP đúng), SD-P07 (mật khẩu mạnh hợp lệ), SD-C03 (xác nhận khớp)

## Type
Valid

## Status / Related bugs
Fail / #4, #6, #20
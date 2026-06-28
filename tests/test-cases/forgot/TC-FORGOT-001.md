# TC-FORGOT-001: Đặt lại mật khẩu thành công với toàn bộ dữ liệu hợp lệ (on-point)

## Requirement ID
FR-03

## Module / Test type / Technique
Forgot Password / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Tài khoản `test@eshop.com` đã tồn tại trong hệ thống
- Người dùng đang ở trang Quên mật khẩu (`/forgot-password`)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email (Bước 1) | test@eshop.com |
| OTP (Bước 2) | [Mã OTP 6 chữ số hiển thị trên màn hình sau Bước 1] |
| Mật khẩu mới | NewPass1! |
| Xác nhận mật khẩu mới | NewPass1! |

## Test steps
1. Truy cập trang Quên mật khẩu.
2. Nhập Email `test@eshop.com` và bấm "Lấy mã OTP".
3. Xác nhận hệ thống chuyển sang Bước 2 và hiển thị mã OTP (môi trường demo).
4. Nhập OTP vừa nhận, Mật khẩu mới `NewPass1!`, Xác nhận mật khẩu mới `NewPass1!`.
5. Bấm "Đặt lại mật khẩu".

## Expected result
- Bước 1: Hệ thống sinh OTP 6 chữ số và hiển thị trên màn hình (demo).
- Bước 2: Đặt lại mật khẩu thành công; người dùng được chuyển về trang Đăng nhập.
- Đăng nhập bằng mật khẩu mới `NewPass1!` thành công.

## Sub-domains covered
SD-E04 (email đã đăng ký, hợp lệ), SD-O06 (OTP đúng), SD-P07 (mật khẩu mạnh hợp lệ), SD-C03 (xác nhận khớp)

## Type
Valid

## Status / Related bugs
Not Run / None

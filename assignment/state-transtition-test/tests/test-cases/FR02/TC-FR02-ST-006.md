# TC-FR02-ST-006: Đặt lại mật khẩu thành công mở khóa tài khoản chủ động

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] Transition Coverage (Locked -> Active via reset_password)

## Source Design Rule
- Trạng thái bắt đầu: `Locked`
- Sự kiện kích hoạt: `reset_password`
- Trạng thái đích: `Active (0 attempts)`

## Preconditions
- Tài khoản `test@eshop.com` đang bị khóa do nhập sai 3 lần (`login_attempts = 3`, `locked_until` ở tương lai).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản cần khôi phục |
| New Password | NewPassword123! | Mật khẩu mới |

## Test Steps
1. Thực hiện quy trình Quên mật khẩu và đặt lại mật khẩu mới `NewPassword123!` cho tài khoản `test@eshop.com`.
2. Truy cập trang đăng nhập, nhập Email `test@eshop.com` và mật khẩu mới `NewPassword123!`.
3. Bấm "Đăng nhập".

## Expected Result
- Bước 1: Hệ thống cho phép đặt lại mật khẩu mới thành công.
- Bước 2-3: Đăng nhập thành công và chuyển hướng về trang chủ. Trạng thái khóa tài khoản được giải phóng ngay lập tức (không cần chờ hết 30s).
- Database: `login_attempts` reset về `0`, `locked_until` được xóa.

## Status / Related Bugs
- **Result**: Failed
- **Related Bug**: BUG-FR02-ST-03

# TC-FR02-ST-008: Kiểm tra tính đóng của trạng thái Locked - Đăng nhập sai mật khẩu khi tài khoản bị khóa

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] Final State Verification (Locked + login_fail -> Locked)

## Source Design Rule
- Trạng thái bắt đầu: `Locked`
- Sự kiện kích hoạt: `login_fail` (nhập sai mật khẩu khi đang bị khóa)
- Trạng thái đích: `Locked` (không thay đổi)

## Preconditions
- Tài khoản `test@eshop.com` đang bị khóa (`login_attempts = 3`, `locked_until` ở tương lai).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản đang bị khóa |
| Wrong Password | Wrong123! | Mật khẩu sai |

## Test Steps
1. Mở trang đăng nhập EShop ngay khi tài khoản vừa bị khóa (chưa quá 30s).
2. Nhập Email `test@eshop.com` và mật khẩu sai `Wrong123!`.
3. Bấm "Đăng nhập".

## Expected Result
- Đăng nhập thất bại. Hệ thống hiển thị thông báo lỗi tài khoản đang bị khóa tạm thời.
- Database: Bộ đếm `login_attempts` không tăng thêm nữa (giữ nguyên là 3), `locked_until` không bị thay đổi hoặc kéo dài bất hợp lý.

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None

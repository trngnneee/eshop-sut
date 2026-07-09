# TC-FR02-ST-007: Kiểm tra tính đóng của trạng thái Locked - Đăng nhập đúng mật khẩu khi tài khoản bị khóa

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] Final State Verification (Locked + login_success -> Locked)

## Source Design Rule
- Trạng thái bắt đầu: `Locked`
- Sự kiện kích hoạt: `login_success` (nhập đúng mật khẩu nhưng đang bị khóa)
- Trạng thái đích: `Locked` (không thay đổi)

## Preconditions
- Tài khoản `test@eshop.com` đang bị khóa (`login_attempts = 3`, `locked_until` ở tương lai).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản đang bị khóa |
| Correct Password | Test1234! | Mật khẩu đúng |

## Test Steps
1. Mở trang đăng nhập EShop ngay khi tài khoản vừa bị khóa (chưa quá 30s).
2. Nhập Email `test@eshop.com` và mật khẩu đúng `Test1234!`.
3. Bấm "Đăng nhập".

## Expected Result
- Đăng nhập thất bại. Hệ thống hiển thị thông báo lỗi rõ ràng: Tài khoản đang bị khóa tạm thời.
- Database: Trạng thái tài khoản vẫn ở trạng thái `Locked` (`login_attempts` vẫn là 3, `locked_until` không đổi).

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None

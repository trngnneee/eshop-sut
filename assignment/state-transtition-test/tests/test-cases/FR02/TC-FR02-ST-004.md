# TC-FR02-ST-004: Đăng nhập sai 3 lần liên tiếp dẫn đến khóa tài khoản

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] State Coverage (Locked)
- [x] Transition Coverage (Failed 2nd -> Locked via login_fail)
- [x] n-Switch Coverage (1-switch: Failed 1st -> Failed 2nd -> Locked)

## Source Design Rule
- Trạng thái bắt đầu: `Failed 2nd`
- Sự kiện kích hoạt: `login_fail` (lần thứ 3 liên tiếp)
- Trạng thái đích: `Locked`

## Preconditions
- Tài khoản `test@eshop.com` đang có 2 lần đăng nhập sai liên tiếp trước đó (`login_attempts = 2`).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản hợp lệ |
| Wrong Password | Wrong123! | Mật khẩu không chính xác |

## Test Steps
1. Mở trang đăng nhập của EShop.
2. Nhập Email `test@eshop.com` và mật khẩu sai `Wrong123!`. Nhấn "Đăng nhập".
3. Xác minh lỗi hiển thị trên giao diện.
4. Kiểm tra dữ liệu trong database SQLite.

## Expected Result
- Giao diện hiển thị thông báo lỗi tài khoản bị khóa tạm thời (hoặc hiển thị thông báo khóa sau lần nhập sai thứ 3).
- Database: `login_attempts = 3` và trường `locked_until` được thiết lập thời gian khóa cụ thể tương lai (30 giây sau thời điểm hiện tại).

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None

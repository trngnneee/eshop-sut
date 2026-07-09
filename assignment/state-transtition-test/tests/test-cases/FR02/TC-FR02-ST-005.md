# TC-FR02-ST-005: Tự động mở khóa sau khi hết thời gian lockout

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] Transition Coverage (Locked -> Active via lockout_timeout)
- [x] n-Switch Coverage (1-switch: Failed 2nd -> Locked -> lockout_timeout -> Active)

## Source Design Rule
- Trạng thái bắt đầu: `Locked`
- Sự kiện kích hoạt: `lockout_timeout` (chờ 30s hết hạn khóa)
- Trạng thái đích: `Active (0 attempts)`

## Preconditions
- Tài khoản `test@eshop.com` đang bị khóa (`login_attempts = 3`, `locked_until` ở tương lai gần).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản hợp lệ |
| Correct Password | Test1234! | Mật khẩu chính xác |

## Test Steps
1. Chờ ít nhất 30 giây (hoặc thời gian quy định) kể từ lúc bị khóa để đảm bảo hết hạn lockout.
2. Mở trang đăng nhập của EShop.
3. Nhập Email `test@eshop.com` và mật khẩu đúng `Test1234!`. Nhấp "Đăng nhập".

## Expected Result
- Hệ thống cho phép đăng nhập thành công và chuyển hướng về trang chủ.
- Database: Bộ đếm `login_attempts` tự động reset về `0` và `locked_until` được chuyển về `null` hoặc quá khứ.

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None

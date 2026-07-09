# TC-FR02-ST-003: Đăng nhập sai 2 lần liên tiếp rồi đăng nhập đúng

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] State Coverage (Failed 2nd)
- [x] Transition Coverage (Failed 1st -> Failed 2nd via login_fail)
- [x] Transition Coverage (Failed 2nd -> Active via login_success)
- [x] n-Switch Coverage (1-switch: Active -> Failed 1st -> Failed 2nd)

## Source Design Rule
- Trạng thái bắt đầu: `Failed 1st` -> `Failed 2nd` -> `Active (0 attempts)`

## Preconditions
- Tài khoản `test@eshop.com` đang có 1 lần đăng nhập sai trước đó (`login_attempts = 1`).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản hợp lệ |
| Wrong Password | Wrong123! | Mật khẩu không chính xác |
| Correct Password | Test1234! | Mật khẩu chính xác |

## Test Steps
1. Mở trang đăng nhập của EShop.
2. Nhập Email `test@eshop.com` và mật khẩu sai `Wrong123!`. Nhấn "Đăng nhập".
3. Xác minh lỗi hiển thị trên giao diện và kiểm tra database.
4. Nhập mật khẩu đúng `Test1234!`. Nhấn "Đăng nhập".

## Expected Result
- Sau bước 2-3: Giao diện báo lỗi "Invalid email or password". DB cập nhật `login_attempts = 2`.
- Sau bước 4: Đăng nhập thành công, chuyển hướng về Home. DB reset `login_attempts` về `0`.

## Status / Related Bugs
- **Result**: Failed
- **Related Bug**: BUG-FR02-ST-01

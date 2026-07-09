# TC-FR02-ST-002: Đăng nhập sai 1 lần rồi đăng nhập đúng

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] State Coverage (Failed 1st)
- [x] Transition Coverage (Active -> Failed 1st via login_fail)
- [x] Transition Coverage (Failed 1st -> Active via login_success)

## Source Design Rule
- Trạng thái bắt đầu: `Active (0 attempts)` -> `Failed 1st` -> `Active (0 attempts)`

## Preconditions
- Tài khoản `test@eshop.com` đang ở trạng thái hoạt động bình thường (`login_attempts = 0`).

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
- Sau bước 2-3: Giao diện hiển thị lỗi "Invalid email or password". Trạng thái DB của user chuyển sang `login_attempts = 1`.
- Sau bước 4: Đăng nhập thành công, chuyển hướng về Home. Trạng thái DB của user reset bộ đếm `login_attempts` về `0`.

## Status / Related Bugs
- **Result**: Failed
- **Related Bug**: BUG-FR02-ST-01

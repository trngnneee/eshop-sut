# TC-FR02-ST-001: Đăng nhập thành công khi tài khoản đang hoạt động bình thường

## Requirement ID
FR02

## Module / Test Type / Technique
Login / Functional / State Transition Testing

## Target Coverage
- [x] State Coverage (Active)
- [x] Transition Coverage (Active -> Active via login_success)

## Source Design Rule
- Trạng thái bắt đầu: `Active (0 attempts)`
- Sự kiện kích hoạt: `login_success`
- Trạng thái đích: `Active (0 attempts)`

## Preconditions
- Tài khoản `test@eshop.com` đã được đăng ký và ở trạng thái hoạt động bình thường (`login_attempts = 0` in database).

## Test Data
| Field | Value | Note |
| :--- | :--- | :--- |
| Email | test@eshop.com | Tài khoản hợp lệ |
| Password | Test1234! | Mật khẩu chính xác |

## Test Steps
1. Mở trang đăng nhập của EShop tại `http://localhost:5173/login` (hoặc link tương ứng).
2. Nhập Email `test@eshop.com` và Password `Test1234!`.
3. Nhấp chọn nút "Đăng nhập".

## Expected Result
- Hệ thống đăng nhập thành công.
- Token JWT được trả về và lưu tại LocalStorage/SessionStorage.
- Người dùng được chuyển hướng về trang chủ (`/`).
- Database: Giá trị `login_attempts` của user `test@eshop.com` vẫn giữ nguyên là `0`.

## Status / Related Bugs
- **Result**: Passed
- **Related Bug**: None

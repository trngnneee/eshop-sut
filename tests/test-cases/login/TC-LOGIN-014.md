# TC-LOGIN-014: Kiểm tra đặt lại bộ đếm đăng nhập sai sau khi đăng nhập thành công
## Requirement ID
FR-02
## Module / Test type / Technique
Login / Functional / Domain Testing (State Transition)
## Preconditions
- Người dùng đã có tài khoản hợp lệ: `test@eshop.com` / `Test1234!`
- Tài khoản hiện đang có bộ đếm `login_attempts > 0` (ví dụ: đã nhập sai 1 hoặc 2 lần trước đó) và không bị khóa.
- Người dùng đang ở trang đăng nhập.
## Test data
| Email | test@eshop.com |
| Password | Test1234! |
## Test steps
1. Nhập email hợp lệ `test@eshop.com` và mật khẩu đúng `Test1234!`.
2. Nhấp nút "Đăng nhập".
3. Xác minh đăng nhập thành công và chuyển hướng đến trang chủ.
4. Truy vấn CSDL bảng `users` để kiểm tra trường `login_attempts` của tài khoản này.
## Expected result
- Đăng nhập thành công và chuyển hướng thành công.
- Bộ đếm đăng nhập sai `login_attempts` trong CSDL được đặt lại về **0** ngay lập tức.
## Status / Related bugs
Failed / BUG-FR02-A-03

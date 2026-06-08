# TC-LOGIN-002: Kiểm tra tăng bộ đếm đăng nhập sai đúng 1 đơn vị
## Requirement ID
FR-02
## Module / Test type / Technique
Login / Functional / Positive Testing
## Preconditions
- Đã đăng ký tài khoản `test@eshop.com` trên hệ thống.
- Trạng thái ban đầu của tài khoản có `login_attempts = 0` và không bị khóa.
- Người dùng đang ở trang đăng nhập.
## Test data
| Email | test@eshop.com |
| Password | WrongPassword123! |
## Test steps
1. Nhập email `test@eshop.com` và mật khẩu sai `WrongPassword123!`.
2. Nhấp nút "Đăng nhập".
3. Xác minh hệ thống báo lỗi đăng nhập không thành công.
4. Kiểm tra giá trị trường `login_attempts` của người dùng này trong cơ sở dữ liệu.
## Expected result
- Đăng nhập thất bại và hiển thị thông báo lỗi "Invalid email or password" (hoặc thông báo lỗi chung không tiết lộ nguyên nhân cụ thể).
- Giá trị `login_attempts` trong database phải tăng lên **đúng 1 đơn vị** (từ 0 lên 1).
## Status / Related bugs
Failed / Bug #1: login_attempts incremented by 2 instead of 1

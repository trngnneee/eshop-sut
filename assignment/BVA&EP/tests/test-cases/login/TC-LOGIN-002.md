# TC-LOGIN-002: Kiểm tra tăng bộ đếm đăng nhập sai đúng 1 đơn vị
## Requirement ID
FR-02
## Module / Test type / Technique
Login / Functional / Positive Testing
## Preconditions
- Đã đăng ký tài khoản `test@eshop.com` trên hệ thống.
- Trạng thái ban đầu của tài khoản có chưa nhập sai lần nào và không bị khóa.
- Người dùng đang ở trang đăng nhập.
## Test data
| Email | test@eshop.com |
| Password | WrongPassword123! |
## Test steps
1. Nhập email `test@eshop.com` và mật khẩu sai `WrongPassword123!`.
2. Nhấp nút "Đăng nhập".
3. Xác minh hệ thống báo lỗi đăng nhập không thành công.
4. Kiểm tra khả năng đăng nhập của tài khoản này qua phản hồi API.
## Expected result
- Đăng nhập thất bại và hiển thị thông báo lỗi "Invalid email or password" (hoặc thông báo lỗi chung không tiết lộ nguyên nhân cụ thể).
- Giá trị bộ đếm số lần đăng nhập sai trên hệ thống phải tăng lên **đúng 1 đơn vị** (từ 0 lên 1).
## Status / Related bugs
Fail / #31, #33

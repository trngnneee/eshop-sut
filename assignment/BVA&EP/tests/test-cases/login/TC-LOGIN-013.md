# TC-LOGIN-013: Kiểm tra đặt lại bộ đếm đăng nhập sai sau khi đăng nhập thành công
## Requirement ID
FR-02
## Module / Test type / Technique
Login / Functional / Domain Testing (State Transition)
## Preconditions
- Người dùng đã có tài khoản hợp lệ: `test@eshop.com` / `Test1234!`
- Tài khoản hiện đã có một số lần nhập sai mật khẩu trước đó (ví dụ: đã nhập sai 1 hoặc 2 lần) và không bị khóa.
- Người dùng đang ở trang đăng nhập.
## Test data
| Email | test@eshop.com |
| Password | Test1234! |
## Test steps
1. Nhập email hợp lệ `test@eshop.com` và mật khẩu đúng `Test1234!`.
2. Nhấp nút "Đăng nhập".
3. Xác minh đăng nhập thành công và chuyển hướng đến trang chủ.
4. Thực hiện đăng nhập lại bằng thông tin đúng để kiểm tra trạng thái khóa.
## Expected result
- Đăng nhập thành công và chuyển hướng thành công.
- Bộ đếm đăng nhập sai của hệ thống được đặt lại về **0** ngay lập tức.
## Status / Related bugs
Fail / #33

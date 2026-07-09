# TC-LOGIN-014: Kiểm tra tự động mở khóa tài khoản sau khi hết thời gian khóa 30 giây
## Requirement ID
FR-02
## Module / Test type / Technique
Login / Functional / Boundary Value Analysis (Time Boundary)
## Preconditions
- Người dùng đã có tài khoản hợp lệ: `test@eshop.com` / `Test1234!`
- Tài khoản vừa bị khóa do nhập sai mật khẩu 3 lần liên tiếp.
## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Email | test@eshop.com |
| Password | Test1234! |
## Test steps
1. Ngay khi tài khoản bị khóa, đợi đúng 29 giây (ngay dưới biên dưới 30s).
2. Thử đăng nhập lại bằng mật khẩu đúng `Test1234!`. Xác nhận hệ thống vẫn chặn đăng nhập với HTTP 403.
3. Đợi thêm 1 giây (đủ 30 giây - ngay tại biên dưới 30s).
4. Thử đăng nhập lại bằng mật khẩu đúng `Test1234!`.
## Expected result
- Tại bước 2 (29 giây): Đăng nhập thất bại, hiển thị thông báo tài khoản đang bị khóa (HTTP 403).
- Tại bước 4 (30 giây): Đăng nhập thành công, hệ thống cấp JWT token và chuyển hướng về trang chủ.
## Status / Related bugs
Fail / #32

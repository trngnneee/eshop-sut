# TC-LOGIN-001: Đăng nhập thành công với thông tin hợp lệ
## Requirement ID
FR-02
## Module / Test type / Technique
Login / Functional / Equivalence Partitioning
## Preconditions
- Người dùng đã có tài khoản hợp lệ trong hệ thống (ví dụ: `test@eshop.com` / `Test1234!`)
- Người dùng đang ở trang đăng nhập của Frontend Web (`http://localhost:5173/login` hoặc tương đương)
## Test data
| Email | test@eshop.com |
| Password | Test1234! |
## Test steps
1. Truy cập vào trang Đăng nhập.
2. Nhập email hợp lệ `test@eshop.com` vào trường Email.
3. Nhập password hợp lệ `Test1234!` vào trường Mật khẩu.
4. Nhấp nút "Đăng nhập".
## Expected result
- Đăng nhập thành công.
- Hệ thống trả về token JWT hợp lệ và lưu ở phía Client.
- Người dùng được chuyển về trang chủ hoặc trang cá nhân thành công.
## Status / Related bugs
Pass / None

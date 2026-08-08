# TC-LOGIN-005: Kiểm tra khoảng trắng ở đầu hoặc cuối địa chỉ Email khi đăng nhập

## Requirement ID
FR-02, FR-22

## Module / Test type / Technique
Login / Validation / Boundary Value Analysis / Robustness

## Preconditions
- Đã đăng ký tài khoản `test@eshop.com`.

## Test data
- Email: ` test@eshop.com ` (có khoảng trắng ở đầu và cuối)
- Mật khẩu: `Test1234!`

## Test steps
1. Truy cập trang Đăng nhập.
2. Nhập email có khoảng trắng ở đầu/cuối: ` test@eshop.com ` vào ô Email.
3. Nhập mật khẩu đúng `Test1234!`.
4. Nhấn nút Đăng nhập.

## Expected result
- Hệ thống tự động cắt bỏ khoảng trắng (trim) ở đầu/cuối email và đăng nhập thành công.

## Status / Related bugs
Failed / #9

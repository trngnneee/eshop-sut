# TC-LOGIN-006: Kiểm tra tính hợp lệ của JWT Token nhận được sau khi đăng nhập thành công

## Requirement ID
FR-02

## Module / Test type / Technique
Login / Auth Logic / Functional / Security

## Preconditions
- Đã đăng ký tài khoản `test@eshop.com`.

## Test data
- Email: `test@eshop.com`
- Mật khẩu: `Test1234!`

## Test steps
1. Gửi yêu cầu đăng nhập bằng thông tin đúng để lấy token JWT.
2. Sử dụng token nhận được để gửi yêu cầu truy cập API cần xác thực (ví dụ: `GET /api/users/me` với header `Authorization: Bearer <token>`).
3. Kiểm tra phản hồi của hệ thống.

## Expected result
- Đăng nhập thành công trả về JWT token.
- API `/api/users/me` xác thực token thành công và trả về thông tin cá nhân của người dùng (HTTP 200).

## Status / Related bugs
Pass / None

# TC-LOGIN-007: Kiểm tra khả năng chống tấn công SQL Injection trong trường Email đăng nhập

## Requirement ID
SEC-05

## Module / Test type / Technique
Login / Security / SQL Injection / Negative Testing

## Preconditions
- Máy chủ Backend đang chạy.

## Test data
- Email: `' OR 1=1 --`
- Mật khẩu: `any`

## Test steps
1. Truy cập trang đăng nhập hoặc gọi trực tiếp API `/api/login`.
2. Nhập payload SQL Injection `' OR 1=1 --` vào trường Email.
3. Nhập mật khẩu bất kỳ và bấm Đăng nhập.

## Expected result
- Hệ thống từ chối đăng nhập (HTTP 401 Unauthorized).
- Không xảy ra lỗi cú pháp SQL và kẻ tấn công không thể vượt qua xác thực.

## Status / Related bugs
Pass / None

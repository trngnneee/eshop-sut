# TC-LOGIN-012: Kiểm tra chặn truy cập trang Đăng nhập khi đã đăng nhập thành công (Route Guard)

## Requirement ID
FR-23

## Module / Test type / Technique
Login / Session / Route Guard / Navigation Testing

## Preconditions
- Người dùng đã đăng nhập thành công vào hệ thống.

## Test data
- Token đăng nhập đang được lưu ở client.

## Test steps
1. Khi đã đăng nhập, cố gắng truy cập trực tiếp vào đường dẫn trang Đăng nhập (`http://localhost:5173/login`).
2. Quan sát phản ứng điều hướng của hệ thống.

## Expected result
- Hệ thống phải phát hiện người dùng đã có token hợp lệ và tự động điều hướng (redirect) người dùng về trang chủ hoặc trang profile, không cho phép hiển thị lại form đăng nhập.

## Status / Related bugs
Fail / #44

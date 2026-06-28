## Test Case ID

TC-USERMGMT-003

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19, FR-12

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra người dùng có role `user` không thể truy cập API/trang Quản lý Người dùng của Admin.

## Preconditions

- Tài khoản user thường (`test@eshop.com` / `Test1234!`) tồn tại trong hệ thống.
- Tài khoản user đã đăng nhập thành công.

## Test Data

| Parameter | Value |
|-|-|
| Tài khoản | test@eshop.com / Test1234! |
| Role | user |
| Endpoint | GET /api/admin/users |

## Test Steps

1. Đăng nhập với tài khoản user thường (`test@eshop.com`).
2. Thử truy cập URL `/admin/users` trực tiếp trên trình duyệt.
3. Hoặc gọi API `GET /api/admin/users` với JWT Token của user thường.
4. Quan sát kết quả.

## Expected Result

- Trình duyệt chuyển hướng về trang lỗi / trang đăng nhập / hiển thị thông báo "Không có quyền truy cập".
- API trả về HTTP 403 Forbidden.
- Dữ liệu người dùng không được tiết lộ.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

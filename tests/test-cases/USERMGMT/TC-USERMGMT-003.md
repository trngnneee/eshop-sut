## Test Case ID

TC-USERMGMT-003

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

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
| Loại tài khoản | User thường |
| Role | user |
| Authorization Token | JWT Token của user thường |
| Endpoint | GET /api/admin/users |

## Test Steps

1. Đăng nhập với tài khoản user thường (`test@eshop.com`).
2. Hoặc gọi API `GET /api/admin/users` với JWT Token của user thường.
3. Quan sát kết quả.

## Expected Result
- API trả về HTTP 403 Forbidden.
- Dữ liệu người dùng không được tiết lộ.

## Actual Result

User thường vẫn xem được toàn bộ dữ liệu người dùng khác.

## Status

FAILED

## Bug Reference
[\[BUG\]\[User Management\] User thường có thể truy cập API quản lý người dùng của Admin](https://github.com/trngnneee/eshop-sut/issues/147#issue-4761377756)
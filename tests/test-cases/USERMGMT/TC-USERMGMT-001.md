## Test Case ID

TC-USERMGMT-001

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra Admin đã đăng nhập hợp lệ có thể xem danh sách tất cả người dùng.

## Preconditions

- Hệ thống đang hoạt động bình thường.
- Tài khoản Admin (`admin@eshop.com` / `Admin123!`) đã đăng nhập thành công.
- Có ít nhất 1 người dùng khác trong hệ thống.

## Test Data

| Parameter | Value |
|-|-|
| Tài khoản | admin@eshop.com / Admin123! |
| Role | admin |

## Test Steps

1. Đăng nhập vào hệ thống với tài khoản Admin.
2. Điều hướng tới trang Quản lý Người dùng.
3. Quan sát danh sách người dùng được hiển thị.

## Expected Result

- Danh sách tất cả người dùng được hiển thị thành công.
- Thông tin hiển thị bao gồm: ID, Họ tên, Email, Role.
- Trường mật khẩu (password) KHÔNG được hiển thị trong danh sách.

## Actual Result

Danh sách người dùng hiển thị thành công, đủ thông tin và không lộ mật khẩu.

## Status

PASSED

## Bug Reference
None
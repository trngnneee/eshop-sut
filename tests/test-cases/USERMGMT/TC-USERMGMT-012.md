## Test Case ID

TC-USERMGMT-012

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra danh sách người dùng hiển thị đầy đủ thông tin cần thiết cho mỗi tài khoản.

## Preconditions

- Admin đã đăng nhập thành công.
- Có ít nhất 1 người dùng trong hệ thống với đầy đủ thông tin.

## Test Data

| Parameter | Value |
|-|-|
| Người dùng mẫu | test@eshop.com |
| Thông tin kỳ vọng | ID, Họ tên, Email, Role |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Điều hướng tới trang Quản lý Người dùng.
3. Quan sát từng cột thông tin trong danh sách.

## Expected Result

- Danh sách hiển thị ít nhất các trường: ID người dùng, Họ tên, Email, Role.
- Không hiển thị trường mật khẩu (password).
- Thông tin hiển thị chính xác, khớp với dữ liệu thực tế.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

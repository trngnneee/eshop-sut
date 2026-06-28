## Test Case ID

TC-USERMGMT-020

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra Admin có thể xóa đúng người dùng mong muốn mà không ảnh hưởng đến các tài khoản khác (kiểm tra tính cô lập khi xóa).

## Preconditions

- Admin đã đăng nhập thành công.
- Tồn tại ít nhất 3 tài khoản người dùng thường trong hệ thống.

## Test Data

| Parameter | Value |
|-|-|
| Người dùng bị xóa | user_B (1 người dùng cụ thể) |
| Người dùng không bị xóa | user_A và user_C |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Vào trang Quản lý Người dùng, ghi nhớ danh sách hiện tại (user_A, user_B, user_C).
3. Xóa user_B.
4. Xác nhận xóa.
5. Quan sát danh sách sau khi xóa.

## Expected Result

- Chỉ user_B bị xóa khỏi danh sách.
- user_A và user_C vẫn còn trong danh sách và thông tin không thay đổi.
- Hệ thống không xóa nhầm tài khoản khác.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

## Test Case ID

TC-USERMGMT-009

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra hành vi khi cố gắng xóa người dùng có `user_id` không tồn tại trong hệ thống (invalid domain).

## Preconditions

- Admin đã đăng nhập thành công.
- `user_id` mục tiêu không tồn tại trong CSDL.

## Test Data

| Parameter | Value |
|-|-|
| user_id bị xóa | 999999 (không tồn tại) |
| Endpoint | DELETE /api/admin/users/999999 |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Gọi trực tiếp API `DELETE /api/admin/users/999999` với Bearer token của Admin.
3. Quan sát phản hồi từ server.

## Expected Result

- API trả về HTTP 404 Not Found.
- Hệ thống trả về thông báo lỗi rõ ràng: "Người dùng không tồn tại" hoặc tương đương.

## Actual Result

API trả về HTTP 200 OK. Hệ thống thông báo xóa thành công

## Status

FAILED

## Bug Reference

[\[BUG\]\[User Management\] API xóa người dùng trả về thành công khi user_id không tồn tại](https://github.com/trngnneee/eshop-sut/issues/149#issue-4761431614)

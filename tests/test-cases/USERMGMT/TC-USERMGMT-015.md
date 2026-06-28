## Test Case ID

TC-USERMGMT-015

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra user thường cố gắng xóa người dùng khác qua API — phải bị từ chối (Privilege Escalation prevention).

## Preconditions

- Tài khoản `test@eshop.com` đã đăng nhập thành công (role = user).
- Có ít nhất 1 tài khoản khác trong hệ thống.

## Test Data

| Parameter | Value |
|-|-|
| Tài khoản gọi API | test@eshop.com (role = user) |
| Endpoint | DELETE /api/admin/users/{other_user_id} |
| Token | JWT của user thường |

## Test Steps

1. Đăng nhập với tài khoản user thường, lấy JWT Token.
2. Gọi API `DELETE /api/admin/users/{other_user_id}` với JWT Token của user thường.
3. Quan sát phản hồi từ server.

## Expected Result

- API trả về HTTP 403 Forbidden.
- Không có người dùng nào bị xóa.
- Hệ thống không bị lỗi crash.

## Actual Result

API trả về HTTP 200 OK

## Status

FAILED

## Bug Reference
[\[BUG\]\[User Management\] User thường có thể xóa tài khoản khác thông qua API Admin](https://github.com/trngnneee/eshop-sut/issues/152#issue-4762394237)
## Test Case ID

TC-USERMGMT-014

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra Admin xóa người dùng có token đã hết hạn (expired JWT) — hệ thống phải từ chối.

## Preconditions

- JWT Token của Admin đã hết hạn hoặc bị giả mạo.

## Test Data

| Parameter | Value |
|-|-|
| Authorization | Bearer <expired_or_invalid_token> |
| Endpoint | DELETE /api/admin/users/{user_id} |

## Test Steps

1. Lấy một JWT Token đã hết hạn (hoặc chỉnh sửa để hết hạn sớm).
2. Gọi API `DELETE /api/admin/users/{user_id}` với token không hợp lệ.
3. Quan sát phản hồi từ server.

## Expected Result

- API trả về HTTP 401 Unauthorized.
- Không có người dùng nào bị xóa.
- Hệ thống không bị lỗi crash.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

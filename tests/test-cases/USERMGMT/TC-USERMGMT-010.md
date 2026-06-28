## Test Case ID

TC-USERMGMT-010

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra hành vi khi cố gắng xóa người dùng với `user_id` có kiểu dữ liệu không hợp lệ (non-numeric).

## Preconditions

- Admin đã đăng nhập thành công.
- Gọi API với `user_id` là chuỗi ký tự không phải số.

## Test Data

| Parameter | Value |
|-|-|
| user_id bị xóa | "abc" (không phải số nguyên) |
| Endpoint | DELETE /api/admin/users/abc |

## Test Steps

1. Đăng nhập với tài khoản Admin, lấy JWT Token.
2. Gọi API `DELETE /api/admin/users/abc` với Bearer token của Admin.
3. Quan sát phản hồi từ server.

## Expected Result

- API trả về HTTP 400 Bad Request hoặc HTTP 404 Not Found.
- Hệ thống không bị lỗi crash hay unhandled exception.
- Thông báo lỗi rõ ràng về định dạng ID không hợp lệ.

## Actual Result

API trả về 200 OK với thông báo user được xóa thành công.

## Status

FAILED

## Bug Reference
[\[BUG\]\[User Management\] API xóa người dùng chấp nhận user_id không hợp lệ và trả về thành công](https://github.com/trngnneee/eshop-sut/issues/150#issue-4762344302)

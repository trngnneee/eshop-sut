## Test Case ID

TC-USERMGMT-016

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Boundary Value Analysis (BVA)

## Test Objective

Kiểm tra hành vi khi xóa người dùng có user_id = 0 (boundary — giá trị biên dưới không hợp lệ).

## Preconditions

- Admin đã đăng nhập thành công.
- user_id = 0 không tồn tại trong hệ thống.

## Test Data

| Parameter | Value |
|-|-|
| user_id | 0 (BVA: min - 1 so với ID hợp lệ tối thiểu là 1) |
| Endpoint | DELETE /api/admin/users/0 |

## Test Steps

1. Đăng nhập với tài khoản Admin, lấy JWT Token.
2. Gọi API `DELETE /api/admin/users/0` với Bearer token của Admin.
3. Quan sát phản hồi từ server.

## Expected Result

- API trả về HTTP 400 Bad Request hoặc HTTP 404 Not Found.
- Hệ thống không bị crash.

## Actual Result

API trả về HTTP 200 OK. Hệ thống thông báo xóa thành công

## Status

FAILED

## Bug Reference
[\[BUG\]\[User Management\] API xóa người dùng trả về thành công khi user_id không tồn tại](https://github.com/trngnneee/eshop-sut/issues/149#issue-4761431614)
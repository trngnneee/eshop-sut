## Test Case ID

TC-USERMGMT-017

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing / Boundary Value Analysis (BVA)

## Test Objective

Kiểm tra xóa người dùng với user_id = 1 (boundary — giá trị ID hợp lệ tối thiểu, thường là Admin đầu tiên).

## Preconditions

- Admin đã đăng nhập thành công.
- Xác định user_id = 1 là tài khoản nào trong hệ thống (Admin hay User).
- Nếu user_id = 1 là admin đang đăng nhập → kỳ vọng bị từ chối.
- Nếu user_id = 1 là user thường → kỳ vọng xóa thành công.

## Test Data

| Parameter | Value |
|-|-|
| user_id | 1 (BVA: ID hợp lệ tối thiểu) |
| Endpoint | DELETE /api/admin/users/1 |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Xác định user_id = 1 thuộc tài khoản nào.
3. Gọi API `DELETE /api/admin/users/1` với Bearer token của Admin.
4. Quan sát phản hồi từ server.

## Expected Result

- Nếu user_id = 1 là Admin đang đăng nhập: trả về lỗi 400/403 "Không thể xóa tài khoản đang đăng nhập."
- Nếu user_id = 1 là user thường: xóa thành công, trả về HTTP 200.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

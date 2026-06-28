## Test Case ID

TC-USERMGMT-018

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing / Boundary Value Analysis (BVA)

## Test Objective

Kiểm tra xóa người dùng với user_id = 2 (BVA: min+1, ID hợp lệ kế tiếp sau ID thấp nhất).

## Preconditions

- Admin đã đăng nhập thành công.
- Tài khoản có user_id = 2 tồn tại và không phải tài khoản Admin đang đăng nhập.

## Test Data

| Parameter | Value |
|-|-|
| user_id | 2 (BVA: min+1) |
| Endpoint | DELETE /api/admin/users/2 |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Xác nhận user_id = 2 là user thường (không phải Admin đang đăng nhập).
3. Gọi API `DELETE /api/admin/users/2` với Bearer token của Admin.
4. Quan sát phản hồi.

## Expected Result

- Nếu user_id = 2 là user thường và không phải Admin đang đăng nhập: xóa thành công, HTTP 200.
- Người dùng bị xóa không còn trong danh sách.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

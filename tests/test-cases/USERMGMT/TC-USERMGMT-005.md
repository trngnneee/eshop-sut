## Test Case ID

TC-USERMGMT-005

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing / Boundary Value Analysis (BVA)

## Test Objective

Kiểm tra hiển thị danh sách khi hệ thống có đúng 0 người dùng (ngoài Admin) — BVA min boundary.

## Preconditions

- Admin đã đăng nhập thành công.
- Không có tài khoản user nào khác ngoài Admin trong hệ thống.

## Test Data

| Parameter | Value |
|-|-|
| Số người dùng trong hệ thống | 0 (chỉ có Admin) |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Điều hướng tới trang Quản lý Người dùng.
3. Quan sát giao diện.

## Expected Result

- Giao diện hiển thị trạng thái trống (empty state) với thông báo phù hợp hoặc chỉ hiển thị tài khoản Admin.
- Không có lỗi JavaScript hay lỗi hiển thị.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

## Test Case ID

TC-USERMGMT-011

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Boundary Value Analysis (BVA)

## Test Objective

Kiểm tra hiển thị danh sách khi hệ thống có nhiều người dùng (large dataset) — kiểm tra render đúng và không có lỗi hiệu năng.

## Preconditions

- Admin đã đăng nhập thành công.
- Hệ thống có nhiều tài khoản người dùng (ví dụ: 50+ tài khoản).

## Test Data

| Parameter | Value |
|-|-|
| Số người dùng | >= 50 |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Điều hướng tới trang Quản lý Người dùng.
3. Quan sát danh sách hiển thị.
4. Kiểm tra xem có phân trang (pagination) hay cuộn (scroll) không.

## Expected Result

- Tất cả người dùng được hiển thị (hoặc phân trang đúng cách).
- Không có lỗi JavaScript, không bị trắng màn hình.
- Mật khẩu không bị lộ cho bất kỳ người dùng nào trong danh sách.

## Actual Result

Danh sách người dùng được hiển thị nhưng không có phân trang.

## Status

FAILED

## Bug Reference
[\[BUG\]\[User Management\] Trang quản lý người dùng không có phân trang khi hiển thị nhiều tài khoản](https://github.com/trngnneee/eshop-sut/issues/151#issue-4762361602)
## Test Case ID

TC-USERMGMT-006

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing / Boundary Value Analysis (BVA)

## Test Objective

Kiểm tra hiển thị danh sách khi hệ thống có đúng 1 người dùng (ngoài Admin) — BVA min+1 boundary.

## Preconditions

- Admin đã đăng nhập thành công.
- Có đúng 1 tài khoản user thường trong hệ thống (ví dụ: `test@eshop.com`).

## Test Data

| Parameter | Value |
|-|-|
| Số người dùng | 1 (ví dụ: test@eshop.com) |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Điều hướng tới trang Quản lý Người dùng.
3. Quan sát danh sách hiển thị.

## Expected Result

- Danh sách hiển thị đúng 1 người dùng với đầy đủ thông tin (Họ tên, Email, Role).
- Không có lỗi hiển thị.
- Mật khẩu không được hiển thị.

## Actual Result
- Danh sách hiển thị đúng 1 người dùng thường (`test@eshop.com`).
- Không hiển thị trường mật khẩu.
- Không xảy ra lỗi giao diện hoặc lỗi tải dữ liệu.

## Status

PASSED

## Bug Reference

None
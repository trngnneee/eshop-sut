## Test Case ID

TC-USERMGMT-004

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19, FR-12

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra khách chưa đăng nhập (unauthenticated) không thể truy cập trang/API Quản lý Người dùng.

## Preconditions

- Không có session đăng nhập nào đang hoạt động.
- Không có JWT Token hợp lệ.

## Test Data

| Parameter | Value |
|-|-|
| Token | Không có (No token) |
| Endpoint | GET /api/admin/users |

## Test Steps

1. Đảm bảo đã đăng xuất khỏi hệ thống.
2. Thử gọi API `GET /api/admin/users` mà không kèm Authorization header.
3. Thử truy cập URL `/admin/users` trên trình duyệt.

## Expected Result

- API trả về HTTP 401 Unauthorized.
- Giao diện chuyển hướng về trang đăng nhập.
- Dữ liệu người dùng không được tiết lộ.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

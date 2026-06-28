## Test Case ID

TC-USERMGMT-002

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra rằng mật khẩu của người dùng không bị lộ trong danh sách (cả UI lẫn response API).

## Preconditions

- Admin đã đăng nhập thành công.
- Trang Quản lý Người dùng đang được hiển thị.

## Test Data

| Parameter | Value |
|-|-|
| Endpoint API | GET /api/admin/users |
| Token | Bearer <admin_jwt_token> |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Mở Developer Tools (F12) > Network tab.
3. Điều hướng tới trang Quản lý Người dùng.
4. Quan sát response JSON trả về từ API.
5. Kiểm tra UI không hiển thị trường mật khẩu.

## Expected Result

- Response JSON không chứa trường `password` hoặc trường `password` trả về giá trị `null` / không có.
- Giao diện không hiển thị mật khẩu (dù dạng hash hay plaintext).

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

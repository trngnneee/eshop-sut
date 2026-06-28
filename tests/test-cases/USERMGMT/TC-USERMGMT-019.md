## Test Case ID

TC-USERMGMT-019

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra rằng dữ liệu mật khẩu không bị lộ qua API response khi xem danh sách người dùng (kiểm tra ở tầng API).

## Preconditions

- Admin đã đăng nhập thành công, có JWT Token hợp lệ.

## Test Data

| Parameter | Value |
|-|-|
| Endpoint | GET /api/admin/users |
| Token | Bearer <valid_admin_token> |

## Test Steps

1. Đăng nhập với tài khoản Admin, lấy JWT Token.
2. Dùng công cụ như Postman hoặc curl để gọi API `GET /api/admin/users`.
3. Kiểm tra toàn bộ response JSON nhận được.
4. Tìm kiếm các trường có tên: `password`, `pwd`, `pass`, `hash`.

## Expected Result

- Response JSON không có trường `password` hoặc bất kỳ biến thể nào của mật khẩu.
- Nếu có trường `password`, giá trị phải là `null` hoặc không được trả về.
- Không lộ password hash, salt, hay bất kỳ thông tin liên quan đến xác thực.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

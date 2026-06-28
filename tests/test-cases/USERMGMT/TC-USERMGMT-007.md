## Test Case ID

TC-USERMGMT-007

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra Admin có thể xóa thành công một người dùng thường.

## Preconditions

- Admin đã đăng nhập thành công.
- Tồn tại ít nhất 1 tài khoản người dùng thường trong danh sách (khác với Admin đang đăng nhập).

## Test Data

| Parameter | Value |
|-|-|
| Người dùng bị xóa | user_id khác với admin đang đăng nhập |
| Ví dụ | test@eshop.com |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Điều hướng tới trang Quản lý Người dùng.
3. Chọn một người dùng thường (không phải Admin đang đăng nhập).
4. Nhấn nút "Xóa".
5. Xác nhận thao tác xóa nếu có dialog xác nhận.
6. Quan sát kết quả.

## Expected Result

- Người dùng được xóa thành công khỏi hệ thống.
- Danh sách người dùng cập nhật ngay lập tức, không còn hiển thị người dùng vừa xóa.


## Actual Result

Tài khoản bị xóa không còn hiển thị trong danh sách người dùng nữa.

## Status

PASSED

## Bug Reference
None
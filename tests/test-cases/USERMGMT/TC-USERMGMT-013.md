## Test Case ID

TC-USERMGMT-013

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra Admin xóa người dùng, sau đó danh sách được cập nhật ngay lập tức không cần reload trang.

## Preconditions

- Admin đã đăng nhập thành công.
- Tồn tại ít nhất 2 tài khoản người dùng thường trong hệ thống.

## Test Data

| Parameter | Value |
|-|-|
| Người dùng bị xóa | 1 user thường bất kỳ (không phải Admin đang đăng nhập) |

## Test Steps

1. Đăng nhập với tài khoản Admin.
2. Vào trang Quản lý Người dùng.
3. Ghi nhớ số lượng người dùng trong danh sách.
4. Nhấn nút "Xóa" cho 1 người dùng thường.
5. Xác nhận xóa (nếu có dialog).
6. Quan sát danh sách sau khi xóa.

## Expected Result

- Danh sách tự động cập nhật (giảm đi 1 người dùng) mà không cần reload trang.
- Người dùng vừa xóa không còn xuất hiện trong danh sách.
- Hệ thống hiển thị thông báo xóa thành công.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

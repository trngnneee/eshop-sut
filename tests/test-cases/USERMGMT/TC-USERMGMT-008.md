## Test Case ID

TC-USERMGMT-008

## Feature

Quản lý Người dùng (Admin) — FR-19

## Requirement Reference

FR-19

## Testing Technique

Domain Testing

## Test Objective

Kiểm tra Admin KHÔNG THỂ tự xóa chính tài khoản của mình đang đăng nhập — ràng buộc nghiệp vụ quan trọng nhất.

## Preconditions

- Admin (`admin@eshop.com`) đã đăng nhập thành công.
- Đang ở trang Quản lý Người dùng.

## Test Data

| Parameter | Value |
|-|-|
| Tài khoản đang đăng nhập | admin@eshop.com |
| Người dùng bị xóa (thử) | admin@eshop.com (chính mình) |

## Test Steps

1. Đăng nhập với tài khoản Admin (`admin@eshop.com`).
2. Điều hướng tới trang Quản lý Người dùng.
3. Tìm và chọn chính tài khoản Admin đang đăng nhập trong danh sách.
4. Nhấn nút "Xóa" (nếu nút hiển thị).
5. Hoặc gọi API `DELETE /api/admin/users/{admin_id}` với token của Admin đó.

## Expected Result

- Hệ thống TỪ CHỐI yêu cầu xóa.
- Hiển thị thông báo lỗi rõ ràng: ví dụ "Không thể xóa tài khoản đang đăng nhập."
- Tài khoản Admin không bị xóa khỏi hệ thống.
- API trả về HTTP 400 hoặc 403 với message phù hợp.
- Nút "Xóa" có thể bị ẩn hoặc bị vô hiệu hóa (disabled) cho tài khoản đang đăng nhập.

## Actual Result

## Status

NOT EXECUTED

## Bug Reference

# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-022


## Feature

Hủy đơn hàng trên phân hệ Mobile — UX


## Requirement Reference

FR-10, FR-20, FR-24


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra ứng dụng mobile hiển thị dialog xác nhận trước khi thực hiện hủy đơn hàng. Đây là hành động nguy hiểm/không thể hoàn tác, cần có xác nhận từ người dùng.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `pending` hoặc `confirmed`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | pending hoặc confirmed |
| Hành động | Nhấn nút Hủy đơn hàng |
| Kỳ vọng | Dialog xác nhận xuất hiện |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng có trạng thái `pending` hoặc `confirmed`.

4. Nhấn nút Hủy đơn hàng.

5. Quan sát xem có dialog xác nhận xuất hiện không.

6. Nhấn "Không" / "Hủy bỏ" trên dialog và kiểm tra đơn hàng không bị hủy.

7. Nhấn "Có" / "Xác nhận" trên dialog và kiểm tra đơn hàng bị hủy.


## Expected Result

- Sau khi nhấn nút Hủy, hệ thống hiển thị dialog xác nhận trước khi thực hiện.
- Dialog có nội dung rõ ràng bằng tiếng Việt (VD: "Bạn có chắc chắn muốn hủy đơn hàng này?").
- Nếu chọn "Không" → đơn hàng giữ nguyên trạng thái.
- Nếu chọn "Có" → đơn hàng được chuyển sang `canceled`.


## Actual Result



## Status

NOT EXECUTED


## Bug Reference


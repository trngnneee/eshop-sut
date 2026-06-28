# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-011


## Feature

Hủy đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra sau khi hủy đơn hàng thành công trên mobile, trạng thái đơn hàng được cập nhật thành `canceled` ngay lập tức trên giao diện mà không cần reload.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `pending` hoặc `confirmed`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | pending hoặc confirmed |
| Hành động | Hủy đơn hàng |
| Trạng thái sau khi hủy | canceled |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng có trạng thái `pending` hoặc `confirmed`.

4. Nhấn nút Hủy đơn hàng và xác nhận.

5. Quan sát trạng thái đơn hàng sau khi hủy trên giao diện.


## Expected Result

- Trạng thái đơn hàng được cập nhật thành `canceled` ngay trên giao diện mobile.
- Không cần reload hoặc thoát ra vào lại để thấy trạng thái mới.
- Nút Hủy đơn hàng biến mất sau khi hủy thành công.


## Actual Result

Trạng thái hủy đơn được cập nhật ngay trên giao diện mobile và nút hủy đơn biến mất.

## Status

PASSED


## Bug Reference
None

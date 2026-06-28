# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-009


## Feature

Hiển thị nút hủy đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra ứng dụng mobile hiển thị nút Hủy đơn hàng khi đơn hàng ở trạng thái `pending`. Theo FR-20, User được phép hủy đơn khi trạng thái là `pending`.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `pending`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | pending |
| Kỳ vọng nút Hủy | Hiển thị |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng có trạng thái `pending`.

4. Quan sát giao diện chi tiết đơn hàng.

5. Kiểm tra sự hiện diện của nút Hủy đơn hàng.


## Expected Result

- Nút Hủy đơn hàng HIỂN THỊ rõ ràng trên giao diện chi tiết đơn hàng khi trạng thái là `pending`.
- Nút Hủy có nhãn tiếng Việt phù hợp (VD: "Hủy đơn hàng").
- Nút Hủy sử dụng màu đỏ (nút nguy hiểm) theo FR-21.


## Actual Result

Nút hủy đơn hiển thị rõ ràng, có nhãn tiếng việt và màu sắc phù hợp.

## Status

PASSED


## Bug Reference
None

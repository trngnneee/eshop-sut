# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-007


## Feature

Hiển thị nút hủy đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra ứng dụng mobile ẩn/không hiển thị nút Hủy đơn hàng khi đơn hàng ở trạng thái `delivered` (Final State).


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `delivered`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | delivered |
| Kỳ vọng nút Hủy | Ẩn / Không hiển thị |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng có trạng thái `delivered`.

4. Quan sát giao diện chi tiết đơn hàng.

5. Kiểm tra sự hiện diện của nút Hủy đơn hàng.


## Expected Result

- Nút Hủy đơn hàng KHÔNG hiển thị trên giao diện chi tiết đơn hàng khi trạng thái là `delivered`.


## Actual Result

Giao diện không hiển thị nút hủy đơn.

## Status

PASSED


## Bug Reference

None
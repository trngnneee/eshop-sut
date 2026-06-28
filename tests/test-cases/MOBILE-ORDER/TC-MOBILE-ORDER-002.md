# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-002


## Feature

Hủy đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra User có thể hủy đơn hàng đang ở trạng thái `confirmed` thành công trên ứng dụng mobile.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `confirmed` (Admin đã xác nhận đơn).


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | confirmed |
| Hành động | Hủy đơn hàng |
| Trạng thái mục tiêu | canceled |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng có trạng thái `confirmed`.

4. Nhấn nút Hủy đơn hàng.

5. Xác nhận hủy (nếu có dialog xác nhận).


## Expected Result

- Đơn hàng được chuyển sang trạng thái `canceled` thành công.
- Trạng thái hiển thị được cập nhật ngay trên giao diện mobile.
- Hệ thống hiển thị thông báo hủy thành công.


## Actual Result



## Status

NOT EXECUTED


## Bug Reference


# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-004


## Feature

Hủy đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra User KHÔNG thể hủy đơn hàng đang ở trạng thái `delivered` trên ứng dụng mobile. Theo FR-10, `delivered` là trạng thái kết thúc (Final State) — không được phép chuyển sang bất kỳ trạng thái nào khác.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `delivered`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | delivered |
| Hành động | Cố gắng hủy đơn hàng |
| Trạng thái mục tiêu | canceled (không được phép — Final State) |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng có trạng thái `delivered`.

4. Kiểm tra xem nút Hủy đơn hàng có hiển thị không.

5. Nếu nút Hủy hiển thị, nhấn vào và quan sát phản hồi.


## Expected Result

- Nút Hủy đơn hàng KHÔNG hiển thị trên giao diện mobile cho đơn `delivered`.
- Giao diện không cung cấp bất kỳ cách nào để User thao tác trên đơn đã giao (Final State).
- Trạng thái đơn hàng vẫn hiển thị `delivered` trên giao diện.


## Actual Result



## Status

NOT EXECUTED


## Bug Reference


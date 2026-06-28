# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-005


## Feature

Hủy đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra User KHÔNG thể hủy đơn hàng đã ở trạng thái `canceled` trên ứng dụng mobile. Theo FR-10, `canceled` là trạng thái kết thúc (Final State) — không được phép chuyển sang bất kỳ trạng thái nào khác.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `canceled`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | canceled |
| Hành động | Cố gắng hủy đơn hàng lần nữa |
| Trạng thái mục tiêu | canceled (không được phép — đã là Final State) |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng có trạng thái `canceled`.

4. Kiểm tra xem nút Hủy đơn hàng có hiển thị không.

5. Nếu nút Hủy hiển thị, nhấn vào và quan sát phản hồi.


## Expected Result

- Nút Hủy đơn hàng KHÔNG hiển thị trên giao diện mobile cho đơn đã `canceled`.
- Giao diện không cung cấp bất kỳ cách nào để User thao tác trên đơn đã hủy (Final State).
- Trạng thái đơn hàng vẫn hiển thị `canceled` trên giao diện.


## Actual Result



## Status

NOT EXECUTED


## Bug Reference


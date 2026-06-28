# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-014


## Feature

Hiển thị trạng thái đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra trạng thái `pending` được hiển thị bằng tiếng Việt rõ ràng trên ứng dụng mobile.

## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `pending`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái backend | pending |
| Trạng thái hiển thị kỳ vọng | Tiếng Việt (VD: "Chờ xác nhận", "Đang chờ") |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Tìm đơn hàng có trạng thái `pending`.

4. Quan sát nhãn trạng thái hiển thị trên giao diện.


## Expected Result

- Trạng thái `pending` được hiển thị bằng tiếng Việt rõ ràng.
- KHÔNG hiển thị chuỗi tiếng Anh gốc "pending".
- Nhãn trạng thái dễ đọc và dễ hiểu cho người dùng Việt Nam.


## Actual Result

Trạng thái hiển thị bằng tiếng Việt rõ ràng.

## Status

PASSED


## Bug Reference

None
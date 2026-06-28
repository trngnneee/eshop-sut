# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-018


## Feature

Hiển thị trạng thái đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-11, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra trạng thái `canceled` được hiển thị bằng tiếng Việt rõ ràng trên ứng dụng mobile. Theo FR-11, trạng thái phải được dịch sang tiếng Việt.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng ở trạng thái `canceled`.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái backend | canceled |
| Trạng thái hiển thị kỳ vọng | Tiếng Việt (VD: "Đã hủy") |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Tìm đơn hàng có trạng thái `canceled`.

4. Quan sát nhãn trạng thái hiển thị trên giao diện.


## Expected Result

- Trạng thái `canceled` được hiển thị bằng tiếng Việt rõ ràng (VD: "Đã hủy").
- KHÔNG hiển thị chuỗi tiếng Anh gốc "canceled".
- Nhãn trạng thái dễ đọc và dễ hiểu cho người dùng Việt Nam.


## Actual Result

Trạng thái hiển thị bằng tiếng Việt rõ ràng.

## Status

PASSED


## Bug Reference

None
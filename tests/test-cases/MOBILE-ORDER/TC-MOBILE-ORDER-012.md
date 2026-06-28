# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-012


## Feature

Hủy đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra sau khi đơn hàng đã bị hủy (canceled), User không thể hủy lại lần nữa trên mobile. Đây là ràng buộc Final State — trạng thái `canceled` không được phép chuyển sang bất kỳ trạng thái nào khác.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User vừa hủy thành công 1 đơn hàng (đơn đang ở trạng thái `canceled`).


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái hiện tại | canceled |
| Hành động | Cố hủy đơn lần nữa |
| Kỳ vọng | Không được phép — Final State |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Chọn đơn hàng vừa bị hủy (trạng thái `canceled`).

4. Kiểm tra xem nút Hủy có hiển thị không.

5. Quan sát giao diện chi tiết đơn hàng — kiểm tra không có thao tác nào cho phép thay đổi trạng thái.


## Expected Result

- Nút Hủy KHÔNG hiển thị trên giao diện mobile cho đơn đã `canceled`.
- Giao diện không cung cấp bất kỳ cách nào để thay đổi trạng thái đơn đã hủy (Final State).
- Trạng thái đơn hàng vẫn hiển thị `canceled` trên giao diện.


## Actual Result

Không có nút hủy đơn hiển thị trên giao diện mobile.

## Status

PASSED


## Bug Reference

None
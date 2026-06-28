# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-019


## Feature

Hiển thị trạng thái đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra mỗi trạng thái đơn hàng có màu sắc phân biệt rõ ràng trên ứng dụng mobile.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có đơn hàng ở ít nhất 3 trạng thái khác nhau (VD: pending, confirmed, delivered).


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái cần kiểm tra | pending, confirmed, shipping, delivered, canceled |
| Yêu cầu | Mỗi trạng thái có màu riêng biệt |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Quan sát màu sắc badge/nhãn trạng thái của mỗi đơn hàng.

4. So sánh màu sắc giữa các trạng thái khác nhau.

5. Kiểm tra xem mỗi trạng thái có màu riêng biệt hay không.


## Expected Result

- Mỗi trạng thái (`pending`, `confirmed`, `shipping`, `delivered`, `canceled`) có một màu sắc riêng biệt.
- Màu sắc phải dễ phân biệt bằng mắt thường.
- Màu sắc phải nhất quán — cùng 1 trạng thái luôn hiển thị cùng 1 màu.
- Không có 2 trạng thái nào dùng chung 1 màu sắc.


## Actual Result

Các trạng thái không có phân biệt màu sắc chỉ hiển thị dạng text bình thường.

## Status

FAILED


## Bug Reference

[\[BUG\]\[Mobile Order\] Trạng thái đơn hàng không có màu sắc phân biệt trên ứng dụng Mobile](https://github.com/trngnneee/eshop-sut/issues/154#issue-4763031532)
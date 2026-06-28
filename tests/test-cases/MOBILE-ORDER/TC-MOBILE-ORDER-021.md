# Test Case Template


## Test Case ID

TC-MOBILE-ORDER-021


## Feature

Lịch sử đơn hàng trên phân hệ Mobile


## Requirement Reference

FR-10, FR-11, FR-20


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra trang lịch sử đơn hàng trên mobile hiển thị đầy đủ thông tin: Mã đơn, Ngày đặt, Tổng tiền, Trạng thái hiện tại. Theo FR-11.


## Preconditions

- Hệ thống backend đang hoạt động.
- User đã đăng nhập trên mobile app.
- User có ít nhất 1 đơn hàng.


## Test Data

| Parameter | Value |
|-|-|
| Thông tin cần hiển thị | Mã đơn, Ngày đặt, Tổng tiền, Trạng thái |
| Đơn vị tiền | ₫ (có phân cách hàng nghìn) |


## Test Steps

1. Mở ứng dụng mobile và đăng nhập bằng tài khoản user.

2. Vào mục Lịch sử đơn hàng.

3. Kiểm tra mỗi đơn hàng trong danh sách có hiển thị đủ 4 thông tin: Mã đơn, Ngày đặt, Tổng tiền, Trạng thái.

4. Kiểm tra định dạng tiền tệ (₫, phân cách hàng nghìn).


## Expected Result

- Mỗi đơn hàng hiển thị đầy đủ: **Mã đơn**, **Ngày đặt**, **Tổng tiền**, **Trạng thái hiện tại**.
- Tổng tiền hiển thị đúng đơn vị ₫ với định dạng phân cách hàng nghìn (VD: 500,000 ₫).
- Trạng thái được dịch sang tiếng Việt và có màu phân biệt.
- Không có thông tin nào bị thiếu hoặc hiển thị sai.


## Actual Result



## Status

NOT EXECUTED


## Bug Reference


## Test Case ID

TC-PRODUCT-003


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Domain Testing / Boundary Value Analysis


## Test Objective

Kiểm tra giá sản phẩm hiển thị đúng đơn vị ₫ và có phân cách hàng nghìn.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.
- Hệ thống có ít nhất 1 sản phẩm với giá dương.


## Test Data

| Parameter | Value |
|-|-|
| Giá sản phẩm | 1234567 |


## Test Steps

1. Truy cập trang chủ.
2. Quan sát giá của một sản phẩm bất kỳ.
3. Kiểm tra định dạng hiển thị của giá.


## Expected Result

Giá được hiển thị theo định dạng tiền tệ Việt Nam, có ký hiệu ₫ và phân cách hàng nghìn.


## Actual Result

Chưa thực thi.


## Status

NOT EXECUTED


## Bug Reference

None


## Tester Notes

Không có.

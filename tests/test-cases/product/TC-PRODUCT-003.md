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
| Giá sản phẩm | 1.234.567 ₫ |


## Test Steps

1. Truy cập trang chủ.
2. Quan sát giá của một sản phẩm bất kỳ.
3. Kiểm tra định dạng hiển thị của giá.


## Expected Result

Giá được hiển thị theo định dạng tiền tệ Việt Nam, có ký hiệu ₫ và phân cách hàng nghìn dùng dấu (.) theo quy định của Điều 11 Luật Kế toán 2015 quy định về chữ viết, chữ số sử dụng trong kế toán.


## Actual Result
Giá sản phẩm hiển thị là 28,000,000 VND.
- Dùng dấu phẩy (,) để phân cách hàng nghìn.
- Hiển thị đơn vị tiền tệ là VND.


## Status

FAILED


## Bug Reference

[BUG][Product] Lỗi hiển thị đơn vị tiền tệ của sản phẩm
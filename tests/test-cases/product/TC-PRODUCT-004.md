## Test Case ID

TC-PRODUCT-004


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra mỗi sản phẩm có ảnh và alt text mô tả.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.
- Hệ thống có dữ liệu sản phẩm hợp lệ.


## Test Data

| Parameter | Value |
|-|-|
| Sản phẩm | Một sản phẩm có ảnh hợp lệ |


## Test Steps

1. Truy cập trang chủ. 
2. Quan sát ảnh của một sản phẩm bất kỳ.

## Expected Result

- Hình ảnh sản phẩm được hiển thị đúng trên danh sách sản phẩm.
- Khi hình ảnh không thể tải, nội dung mô tả thay thế (alt text) được hiển thị.


## Actual Result

- Hình ảnh sản phẩm được hiển thị đúng.
- Khi hình ảnh không thể tải, nội dung mô tả thay thế (alt text) không được hiển thị.

## Status

FAILED


## Bug Reference

[BUG][Product] Lỗi hiển thị alt text


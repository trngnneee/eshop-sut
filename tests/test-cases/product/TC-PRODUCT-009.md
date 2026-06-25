## Test Case ID

TC-PRODUCT-009


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Boundary Value Analysis


## Test Objective

Kiểm tra trang chủ có đúng một thẻ h1.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.


## Test Data

| Parameter | Value |
|-|-|
| Số lượng h1 | 1 |


## Test Steps

1. Truy cập trang chủ.
2. Đếm số thẻ h1 trên trang bằng công cụ kiểm tra DOM.
3. Xác nhận số lượng thẻ h1.


## Expected Result

Trang chủ chỉ có đúng 1 thẻ h1.


## Actual Result

Trang có đến 2 thẻ h1.


## Status

FAILED


## Bug Reference

[BUG][Product] Lỗi số lượng thẻ h1

## Test Case ID

TC-PRODUCT-010


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Boundary Value Analysis


## Test Objective

Kiểm tra sau khi tìm kiếm, trang vẫn chỉ có đúng một thẻ h1.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.
- Hệ thống có dữ liệu sản phẩm hợp lệ.


## Test Data

| Parameter | Value |
|-|-|
| Từ khóa tìm kiếm | Tên sản phẩm hợp lệ đã có trong CSDL |


## Test Steps

1. Truy cập trang chủ.
2. Thực hiện một lượt tìm kiếm hợp lệ.
3. Đếm số thẻ h1 trên trang kết quả.


## Expected Result

Trang kết quả tìm kiếm vẫn chỉ có đúng 1 thẻ h1.


## Actual Result

Trang kết quả tìm kiếm có 2 thẻ h1.


## Status

FAILED


## Bug Reference

[BUG-FR05-06](https://github.com/trngnneee/eshop-sut/issues/30#issue-4747029719)


## Test Case ID

TC-PRODUCT-006


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra empty state khi tìm kiếm không có kết quả.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.
- Có sẵn dữ liệu sản phẩm để tìm kiếm.


## Test Data

| Parameter | Value |
|-|-|
| Từ khóa tìm kiếm | Chuỗi không khớp với tên sản phẩm nào |


## Test Steps

1. Truy cập trang chủ.
2. Nhập một từ khóa không khớp vào ô tìm kiếm.
3. Thực hiện tìm kiếm.


## Expected Result

Hệ thống hiển thị thông báo empty state phù hợp khi không có kết quả.


## Actual Result

Khi không có sản phẩm thì trang hiển thị màn hình trắng, không hiển thị thông tin là không có sản phẩm cho người dùng.


## Status

FAILED


## Bug Reference

[BUG-FR05-04](https://github.com/trngnneee/eshop-sut/issues/28#issue-4746603879)


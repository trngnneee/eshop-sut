## Test Case ID

TC-PRODUCT-005


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra trạng thái loading khi dữ liệu đang được tải.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.
- Có thể quan sát trạng thái tải dữ liệu.


## Test Data

| Parameter | Value |
|-|-|
| Trạng thái dữ liệu | Đang tải |


## Test Steps

1. Truy cập trang chủ.
2. Quan sát ngay khi dữ liệu chưa được tải xong.
3. Kiểm tra thành phần loading.


## Expected Result

Giao diện hiển thị trạng thái loading trong lúc dữ liệu đang tải.


## Actual Result

Trang hiển thị màn hình trắng cho đến khi dữ liệu được tải xong.


## Status

FAILED


## Bug Reference

[BUG-FR05-03](https://github.com/trngnneee/eshop-sut/issues/27#issue-4746377610)
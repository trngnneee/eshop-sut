## Test Case ID

TC-PRODUCT-008


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra từ khóa tìm kiếm chứa HTML được hiển thị an toàn.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.


## Test Data

| Parameter | Value |
|-|-|
| Từ khóa tìm kiếm | `<script>alert(1)</script>` |


## Test Steps

1. Truy cập trang chủ.
2. Nhập từ khóa có chứa `<script>alert(1)</script>` vào ô tìm kiếm.
3. Thực hiện tìm kiếm.
4. Quan sát cách giao diện hiển thị chuỗi nhập vào.


## Expected Result

Từ khóa được hiển thị như văn bản thuần, không render HTML và không thực thi script.


## Actual Result

Không thực thi script.


## Status

PASSED


## Bug Reference

None

## Test Case ID

TC-PRODUCT-013


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra chức năng tìm kiếm sản phẩm có xử lý an toàn với input chứa HTML/JavaScript injection.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.
- Thanh tìm kiếm sản phẩm khả dụng.


## Test Data

| Parameter | Value |
|-|-|
| Search input | `<image src=1 href=1 onerror="javascript:alert(1)"></image>` |


## Test Steps

1. Truy cập trang chủ.
2. Nhập đoạn HTML sau vào thanh tìm kiếm:
   `<image src=1 href=1 onerror="javascript:alert(1)"></image>`
3. Nhấn nút tìm kiếm.
4. Quan sát hành vi của hệ thống.


## Expected Result

Hệ thống xử lý input như dữ liệu văn bản thông thường:
- Không thực thi JavaScript.
- Không hiển thị popup alert.
- Không cho phép chèn HTML trái phép vào giao diện.


## Actual Result

Popup alert("1") được hiển thị khi nhập payload vào ô tìm kiếm, cho thấy JavaScript trong input đã được thực thi.


## Status

FAILED

## Bug Reference

[BUG-FR05-07](https://github.com/trngnneee/eshop-sut/issues/53#issue-4748338316)



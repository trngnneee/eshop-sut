## Test Case ID

TC-PRODUCT-014


## Feature

Xem danh sách & Tìm kiếm sản phẩm


## Requirement Reference

FR-05


## Testing Technique

Domain Testing


## Test Objective

Kiểm tra chức năng tìm kiếm sản phẩm có xử lý an toàn với input chứa SQL Injection payload.


## Preconditions

- Người dùng đang mở trang chủ của Frontend Web.
- Thanh tìm kiếm sản phẩm khả dụng.


## Test Data

| Parameter | Value |
|-|-|
| Search input | `' OR 1=1 --` |


## Test Steps

1. Truy cập trang chủ.
2. Nhập payload sau vào thanh tìm kiếm:
   `' OR 1=1 --`
3. Nhấn nút tìm kiếm.
4. Quan sát kết quả trả về.


## Expected Result

Hệ thống phải:
- Xử lý input như chuỗi văn bản bình thường
- Không thay đổi logic query tìm kiếm
- Không trả về toàn bộ dữ liệu bất thường
- Không hiển thị lỗi SQL hoặc stack trace


## Actual Result

Hệ thống trả về toàn bộ sản phẩm trong database khi nhập payload `' OR 1=1 --`, cho thấy điều kiện tìm kiếm bị vô hiệu hóa và logic truy vấn có thể bị ảnh hưởng bởi input người dùng.


## Status

FAILED


## Bug Reference

[\[BUG\]\[Search\] Chức năng tìm kiếm không xử lý input đặc biệt dẫn đến SQL Injection vulnerability](https://github.com/trngnneee/eshop-sut/issues/60#issue-4753686069)
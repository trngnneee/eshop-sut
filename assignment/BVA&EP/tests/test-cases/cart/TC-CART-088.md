# TC-CART-088: Tắt mạng/server lỗi khi thêm vào giỏ

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Giao diện đang mở.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Ngắt kết nối mạng hoặc tắt server backend.
2. Nhấn thêm sản phẩm vào giỏ hàng từ trang chủ.
3. Quan sát xem giao diện hiển thị thông báo lỗi thân thiện hay không, badge số lượng trên navbar có bị tăng ảo hay không.


## Expected result
- Hiển thị lỗi, không cập nhật badge sai nếu thêm thất bại

## Status / Related bugs
Fail / BUG-FR07-B-18

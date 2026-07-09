# TC-CART-074: Double click nút 'Thêm vào giỏ hàng' rất nhanh

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Người dùng đã đăng nhập.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Truy cập trang chi tiết sản phẩm.
2. Nhấp liên tục nút 'Thêm vào giỏ hàng' thật nhanh (double submit).
3. Vào kiểm tra số lượng sản phẩm trong giỏ hàng.


## Expected result
- Quantity tăng đúng 2 hoặc hệ thống chống double click rõ ràng, không tạo dòng lỗi

## Status / Related bugs
Fail / BUG-FR07-B-11

# TC-CART-078: Giỏ hàng chứa sản phẩm đã bị xóa khỏi hệ thống

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Đã thêm sản phẩm trước khi sản phẩm đó bị Admin xóa.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Thêm sản phẩm A vào giỏ hàng.
2. Admin xóa sản phẩm A khỏi hệ thống (hoặc dùng API xóa sản phẩm).
3. F5 lại trang giỏ hàng của người dùng.


## Expected result
- Hiển thị thông báo sản phẩm không còn tồn tại và yêu cầu xóa khỏi cart

## Status / Related bugs
Fail / BUG-FR07-B-14

# TC-CART-075: Double click nút 'Xóa' rất nhanh

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Có ít nhất 1 sản phẩm trong giỏ hàng.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Truy cập trang giỏ hàng /cart.
2. Nhấp đúp liên tục nút 'Xóa' bên cạnh sản phẩm thật nhanh.
3. Xác minh danh sách giỏ hàng hiển thị.


## Expected result
- Chỉ xóa đúng 1 item, không lỗi UI/API

## Status / Related bugs
Fail / BUG-FR07-B-05

# TC-CART-079: Giỏ hàng chứa sản phẩm hết hàng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Sản phẩm A chuyển trạng thái hết hàng sau khi đã nằm trong giỏ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Thêm sản phẩm A vào giỏ hàng.
2. Người dùng khác mua hết tồn kho sản phẩm A hoặc Admin điều chỉnh số tồn kho của sản phẩm A về 0.
3. F5 lại trang giỏ hàng và thực hiện Checkout.


## Expected result
- Không cho checkout/thêm tiếp, hiển thị cảnh báo hết hàng

## Status / Related bugs
Not Run / None

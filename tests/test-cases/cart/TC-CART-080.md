# TC-CART-080: Giỏ hàng chứa sản phẩm bị thay đổi giá sau khi đã thêm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Giá sản phẩm bị thay đổi bởi hệ thống sau khi đã nằm trong giỏ.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Thêm sản phẩm A (giá 10.000đ) vào giỏ hàng.
2. Admin đổi giá sản phẩm A thành 15.000đ.
3. F5 lại trang giỏ hàng xem giá sản phẩm và tổng tiền hiển thị.


## Expected result
- Cart cập nhật giá mới hoặc hiển thị thông báo giá đã thay đổi

## Status / Related bugs
Not Run / None

# TC-CART-076: Nhấn checkout khi giỏ hàng trống

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Giỏ hàng rỗng.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
Không có

## Test steps
1. Vào trang giỏ hàng đang trống.
2. Nhấp nút Thanh toán (Checkout) hoặc chuyển hướng trực tiếp tới trang thanh toán `/checkout`.
3. Quan sát xem hệ thống có chặn và hiển thị thông báo giỏ hàng trống hay không.


## Expected result
- Không cho checkout, hiển thị thông báo cart trống

## Status / Related bugs
Not Run / None

# TC-CART-077: Nhấn checkout khi giỏ hàng có item quantity không hợp lệ do API tạo ra

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Blackbox / Robustness & Integration

## Preconditions
- Tài khoản có giỏ hàng chứa dữ liệu bẩn.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| quantity | `-2` |

## Test steps
1. Dùng API / Postman để đẩy sản phẩm với quantity âm hoặc bằng 0 vào giỏ hàng thành công.
2. Truy cập giao diện giỏ hàng và nhấp nút Thanh toán (Checkout).
3. Quan sát phản hồi của trang thanh toán.


## Expected result
- Không cho checkout hoặc báo lỗi dữ liệu giỏ hàng

## Status / Related bugs
Not Run / None

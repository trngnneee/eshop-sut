# TC-CHECKOUT-023: Mỗi dòng sản phẩm hiển thị đúng thành tiền

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có sản phẩm; đã biết đơn giá và số lượng

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Đơn giá | 200.000 ₫ |
| Số lượng | 2 |
| Thành tiền kỳ vọng | 400.000 ₫ |

## Test steps
1. Đăng nhập; thêm sản phẩm (đơn giá 200.000 ₫, số lượng 2) vào giỏ.
2. Mở trang Thanh toán.
3. Đối chiếu thành tiền từng dòng với đơn giá × số lượng.

## Expected result
- Thành tiền mỗi dòng = đơn giá × số lượng, hiển thị đúng trên trang thanh toán.

## Sub-domains covered
SD-P04 (thành tiền từng dòng hiển thị đúng)

## Type
Valid

## Status / Related bugs
Not Run / None

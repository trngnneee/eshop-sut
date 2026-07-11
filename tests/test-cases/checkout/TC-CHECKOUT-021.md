# TC-CHECKOUT-021: Mỗi dòng sản phẩm hiển thị đúng tên

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có ít nhất 2 sản phẩm khác nhau với tên đã biết

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm A | Tên SP A |
| Sản phẩm B | Tên SP B |

## Test steps
1. Đăng nhập; thêm 2 sản phẩm khác nhau vào giỏ; ghi nhận tên từng sản phẩm.
2. Mở trang Thanh toán.
3. Đối chiếu tên hiển thị trên từng dòng với tên trong giỏ hàng.

## Expected result
- Mỗi dòng trong danh sách đặt mua hiển thị **đúng tên sản phẩm** tương ứng (FR-08).

## Sub-domains covered
SD-P02 (tên sản phẩm hiển thị đúng từng dòng)

## Type
Valid

## Status / Related bugs
Not Run / None

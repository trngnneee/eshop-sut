# TC-CHECKOUT-022: Mỗi dòng sản phẩm hiển thị đúng số lượng

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có sản phẩm với số lượng > 1

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng | 3 |

## Test steps
1. Đăng nhập; thêm 1 sản phẩm với số lượng = 3 vào giỏ.
2. Mở trang Thanh toán.
3. Kiểm tra số lượng hiển thị trên dòng sản phẩm.

## Expected result
- Dòng sản phẩm hiển thị số lượng = 3 (khớp giỏ hàng).

## Sub-domains covered
SD-P03 (số lượng hiển thị đúng từng dòng)

## Type
Valid

## Status / Related bugs
Not Run / None

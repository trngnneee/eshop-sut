# TC-CHECKOUT-005: Tổng tiền thanh toán hiển thị khớp với tổng giỏ hàng

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có ít nhất 1 sản phẩm; đã biết đơn giá và số lượng từng mục

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tổng kỳ vọng | Σ (đơn giá × số lượng) của tất cả mục trong giỏ |

## Test steps
1. Đăng nhập và thêm sản phẩm vào giỏ; ghi nhận tổng tiền tại trang Giỏ hàng.
2. Mở trang Thanh toán.
3. Đối chiếu tổng tiền thanh toán hiển thị với tổng đã ghi nhận ở bước 1.

## Expected result
- Tổng tiền thanh toán **được tính tự động từ giỏ hàng** và hiển thị đúng giá trị.
- Giá trị hiển thị bằng tổng (đơn giá × số lượng) của toàn bộ sản phẩm trong giỏ.

## Sub-domains covered
SD-T01 (tổng tiền tự động tính và hiển thị đúng)

## Type
Valid

## Status / Related bugs
Not Run / None

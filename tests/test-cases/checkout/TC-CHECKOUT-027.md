# TC-CHECKOUT-027: Badge số lượng giỏ hàng về 0 sau thanh toán thành công

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có sản phẩm trước thanh toán

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số mục trước thanh toán | ≥ 1 |

## Test steps
1. Đăng nhập; thêm sản phẩm; xác nhận badge/link Giỏ hàng hiển thị số lượng > 0.
2. Hoàn tất thanh toán thành công.
3. Quan sát badge số lượng trên thanh điều hướng.

## Expected result
- Sau thanh toán, badge giỏ hàng = 0 hoặc không hiển thị (giỏ đã xóa theo FR-08).

## Sub-domains covered
SD-O02 (phản hồi UI sau xóa giỏ — badge)

## Type
Valid

## Status / Related bugs
Not Run / None

# TC-CHECKOUT-007: Giỏ hàng được xóa sau thanh toán thành công

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có ít nhất 1 sản phẩm trước khi thanh toán

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm trong giỏ trước thanh toán | ≥ 1 mục |

## Test steps
1. Đăng nhập và thêm sản phẩm vào giỏ hàng.
2. Xác nhận giỏ hàng không trống.
3. Hoàn tất thanh toán thành công.
4. Kiểm tra lại trạng thái giỏ hàng.

## Expected result
- **Sau thanh toán thành công, giỏ hàng được xóa** (FR-08).
- Giỏ hàng trống; không còn sản phẩm từ đơn vừa thanh toán.

## Sub-domains covered
SD-O01 (giỏ hàng xóa sau thanh toán thành công)

## Type
Valid

## Status / Related bugs
Not Run / None

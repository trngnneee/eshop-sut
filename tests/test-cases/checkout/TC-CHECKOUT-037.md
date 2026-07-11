# TC-CHECKOUT-037: Thanh toán với sản phẩm giá thấp nhất hợp lệ (price min on-point)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Đơn giá sản phẩm at min — value: số dương nhỏ nhất hợp lệ (> 0, theo FR-15)

## Preconditions
- Người dùng đã đăng nhập
- Có sản phẩm với giá dương nhỏ nhất trong danh mục (ví dụ 1.000 ₫ hoặc 0,01 đơn vị)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Đơn giá | Giá dương nhỏ nhất có trong hệ thống |
| Số lượng | 1 |

## Test steps
1. Chọn sản phẩm có đơn giá dương nhỏ nhất; thêm vào giỏ (qty = 1).
2. Mở trang Thanh toán; đối chiếu tổng tiền.
3. Hoàn tất thanh toán.

## Expected result
- Tổng tiền = đơn giá nhỏ nhất × 1; thanh toán thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

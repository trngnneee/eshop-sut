# TC-CHECKOUT-034: Thanh toán với số lượng tại biên min++ (qty = 3)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số lượng sản phẩm at min++ — value: 3

## Preconditions
- Người dùng đã đăng nhập
- Giỏ có 1 sản phẩm với số lượng = 3

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng | 3 |
| Tổng kỳ vọng | đơn giá × 3 |

## Test steps
1. Đăng nhập; thêm 1 sản phẩm với số lượng = 3.
2. Mở trang Thanh toán; đối chiếu tổng tiền.
3. Hoàn tất thanh toán.

## Expected result
- Tổng tiền = đơn giá × 3; thanh toán thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

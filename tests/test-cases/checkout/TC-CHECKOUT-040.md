# TC-CHECKOUT-040: Thanh toán với số lượng rất lớn hợp lệ (qty = 99)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số lượng sản phẩm at high valid — value: 99

## Preconditions
- Người dùng đã đăng nhập
- Giỏ có 1 sản phẩm với số lượng = 99

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng | 99 |
| Tổng kỳ vọng | đơn giá × 99 |

## Test steps
1. Đăng nhập; thêm 1 sản phẩm với số lượng = 99.
2. Mở trang Thanh toán; đối chiếu tổng tiền.
3. Hoàn tất thanh toán.

## Expected result
- Tổng = đơn giá × 99; thanh toán thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

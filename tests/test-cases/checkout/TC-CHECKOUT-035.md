# TC-CHECKOUT-035: Thanh toán với số lượng lớn hợp lệ (qty = 10)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số lượng sản phẩm at high valid — value: 10

## Preconditions
- Người dùng đã đăng nhập
- Giỏ có 1 sản phẩm với số lượng = 10

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng | 10 |
| Tổng kỳ vọng | đơn giá × 10 |

## Test steps
1. Đăng nhập; thêm 1 sản phẩm với số lượng = 10.
2. Mở trang Thanh toán; đối chiếu tổng và thành tiền dòng.
3. Hoàn tất thanh toán.

## Expected result
- Tổng tiền = đơn giá × 10; thanh toán thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

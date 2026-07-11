# TC-CHECKOUT-011: Thanh toán với số lượng sản phẩm tại biên min+ (qty = 2)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số lượng sản phẩm at min+ — value: 2

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có 1 sản phẩm với số lượng = 2

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng | 2 |
| Đơn giá (ví dụ) | 150.000 ₫ |
| Tổng kỳ vọng | 300.000 ₫ (= đơn giá × 2) |

## Test steps
1. Đăng nhập và thêm 1 sản phẩm với số lượng = 2 vào giỏ.
2. Ghi nhận đơn giá sản phẩm.
3. Mở trang Thanh toán.
4. Đối chiếu tổng tiền hiển thị và hoàn tất thanh toán.

## Expected result
- Tổng tiền thanh toán = đơn giá × 2.
- Thanh toán thành công; tổng tiền đơn hàng khớp giá trị tại biên min+.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

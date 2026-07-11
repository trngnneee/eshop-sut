# TC-CHECKOUT-010: Thanh toán với số lượng sản phẩm tại biên tối thiểu (qty = 1)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số lượng sản phẩm at min — value: 1 (theo FR-06: số nguyên dương, tối thiểu 1)

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có 1 sản phẩm với số lượng = 1

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng | 1 |
| Đơn giá (ví dụ) | 150.000 ₫ |
| Tổng kỳ vọng | 150.000 ₫ (= đơn giá × 1) |

## Test steps
1. Đăng nhập và thêm 1 sản phẩm với số lượng = 1 vào giỏ.
2. Ghi nhận đơn giá sản phẩm.
3. Mở trang Thanh toán.
4. Đối chiếu tổng tiền hiển thị và hoàn tất thanh toán.

## Expected result
- Tổng tiền thanh toán = đơn giá × 1.
- Thanh toán thành công với tổng tiền đúng tại biên tối thiểu hợp lệ.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

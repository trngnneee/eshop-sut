# TC-CHECKOUT-036: Thanh toán với 3 loại sản phẩm tại biên min++ (cart types)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số loại sản phẩm at min++ — value: 3

## Preconditions
- Người dùng đã đăng nhập
- Giỏ có 3 sản phẩm khác nhau, mỗi loại qty = 1

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số loại | 3 |
| Tổng kỳ vọng | giá A + giá B + giá C |

## Test steps
1. Đăng nhập; thêm 3 sản phẩm khác nhau (qty = 1 mỗi loại).
2. Mở trang Thanh toán; xác nhận 3 dòng và tổng tiền.
3. Hoàn tất thanh toán.

## Expected result
- Hiển thị 3 dòng; tổng = tổng 3 đơn giá; thanh toán thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

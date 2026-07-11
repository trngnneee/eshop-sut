# TC-CHECKOUT-041: Thanh toán với 4 loại sản phẩm (cart types high valid)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số loại sản phẩm at high valid — value: 4

## Preconditions
- Người dùng đã đăng nhập
- Giỏ có 4 sản phẩm khác nhau

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số loại | 4 |
| Tổng kỳ vọng | tổng 4 đơn giá |

## Test steps
1. Thêm 4 sản phẩm khác nhau (qty = 1 mỗi loại).
2. Mở trang Thanh toán; xác nhận 4 dòng và tổng.
3. Hoàn tất thanh toán.

## Expected result
- Hiển thị đủ 4 dòng; tổng đúng; thanh toán thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

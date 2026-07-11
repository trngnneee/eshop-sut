# TC-CHECKOUT-014: Thanh toán với số loại sản phẩm tại biên min+ (2 loại)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số loại sản phẩm trong giỏ at min+ — value: 2

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có 2 loại sản phẩm khác nhau, mỗi loại số lượng = 1

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số loại sản phẩm | 2 |
| Sản phẩm A | 1 × đơn giá A |
| Sản phẩm B | 1 × đơn giá B |
| Tổng kỳ vọng | đơn giá A + đơn giá B |

## Test steps
1. Đăng nhập và thêm 2 sản phẩm khác nhau vào giỏ (mỗi loại số lượng = 1).
2. Ghi nhận đơn giá từng sản phẩm và tổng kỳ vọng.
3. Mở trang Thanh toán; xác nhận hiển thị 2 dòng sản phẩm.
4. Đối chiếu tổng tiền và hoàn tất thanh toán.

## Expected result
- Danh sách hiển thị đủ 2 sản phẩm.
- Tổng tiền = tổng thành tiền 2 dòng; thanh toán thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

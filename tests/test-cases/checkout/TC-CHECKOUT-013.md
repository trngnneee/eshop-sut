# TC-CHECKOUT-013: Thanh toán với số loại sản phẩm tại biên tối thiểu (1 loại)

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Số loại sản phẩm trong giỏ at min — value: 1

## Preconditions
- Người dùng đã đăng nhập
- Giỏ hàng có đúng 1 loại sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số loại sản phẩm | 1 |
| Số lượng mỗi loại | 1 |

## Test steps
1. Đăng nhập và thêm đúng 1 loại sản phẩm vào giỏ.
2. Mở trang Thanh toán.
3. Xác nhận danh sách hiển thị 1 dòng và tổng tiền đúng.
4. Hoàn tất thanh toán.

## Expected result
- Giao diện hiển thị đúng 1 sản phẩm.
- Thanh toán thành công tại biên tối thiểu số loại sản phẩm hợp lệ.

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

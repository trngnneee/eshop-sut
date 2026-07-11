# TC-CHECKOUT-044: Tổng tiền hiển thị khớp khi thay đổi số lượng ngay trước thanh toán

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Boundary Value Analysis

## Boundary under test
Tổng tiền sau thay đổi qty tại biên — tăng từ 1 lên 2 ngay trước checkout

## Preconditions
- Người dùng đã đăng nhập
- Giỏ có 1 sản phẩm; có thể chỉnh số lượng từ trang Giỏ hàng

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng ban đầu | 1 |
| Số lượng sau chỉnh | 2 |
| Tổng kỳ vọng | đơn giá × 2 |

## Test steps
1. Thêm sản phẩm qty = 1 vào giỏ.
2. Tại Giỏ hàng, tăng số lượng lên 2 (nút +).
3. Ngay lập tức tiến hành thanh toán; đối chiếu tổng hiển thị.

## Expected result
- Tổng tiền thanh toán tự động cập nhật = đơn giá × 2 (không còn × 1).

## Valid / Invalid
Valid

## Status / Related bugs
Not Run / None

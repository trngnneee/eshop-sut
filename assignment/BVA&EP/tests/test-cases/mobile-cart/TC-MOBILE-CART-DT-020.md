# TC-MOBILE-CART-DT-020: Hệ thống tính toán chính xác số tiền giảm giá theo tỷ lệ phần trăm (percent)
## Requirement ID
FR-21 / FR-24
## Module / Test type / Technique
Checkout / Coupons / Functional / Positive / Equivalence Partitioning
## Preconditions
- Tài khoản khách hàng đã đăng nhập thành công.
- Mã giảm giá "SAVE10" (giảm 10% - tức 0.1, giá trị đơn hàng tối thiểu 300,000 ₫) đang hoạt động trên hệ thống.
- Người dùng có sản phẩm trong giỏ hàng có tổng giá trị là 350,000 ₫.
## Test data
| Mã giảm giá | SAVE10 (type: percent, discount_value: 0.1, min_order_amount: 300,000 ₫) |
| Tổng tiền đơn hàng | 350,000 ₫ |
## Test steps
1. Đăng nhập vào ứng dụng và thêm sản phẩm để giỏ hàng có tổng tiền là 350,000 ₫.
2. Điều hướng tới màn hình Thanh toán (Checkout).
3. Tại ô nhập mã giảm giá, nhập "SAVE10" và nhấn "Áp dụng".
4. Quan sát số tiền được giảm giá và tổng tiền thanh toán sau khi giảm giá.
## Expected result
- Mã giảm giá áp dụng thành công.
- Số tiền giảm giá (`discount_amount`) phải được tính đúng là: 350,000 ₫ * 10% = 35,000 ₫.
- Số tiền thanh toán cuối cùng (`final_amount`) là: 350,000 ₫ - 35,000 ₫ = 315,000 ₫.
## Status / Related bugs
Fail / BUG-FR21-D-06

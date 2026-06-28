# TC-MOBILE-CART-BVA-023: Áp dụng mã giảm giá thành công khi tổng tiền đơn hàng bằng đúng giá trị tối thiểu yêu cầu (min_order_amount)
## Requirement ID
FR-21 / FR-24
## Module / Test type / Technique
Checkout / Coupons / Functional / Positive / Boundary Value Analysis
## Preconditions
- Tài khoản khách hàng đã đăng nhập thành công.
- Mã giảm giá "SAVE10" (giảm 10%, giá trị đơn hàng tối thiểu 300,000 ₫) đang hoạt động trên hệ thống.
- Người dùng có sản phẩm trong giỏ hàng có tổng giá trị đúng bằng 300,000 ₫ (ví dụ: sản phẩm giá 300,000 ₫ hoặc tổ hợp sản phẩm).
## Test data
| Mã giảm giá | SAVE10 (min_order_amount: 300,000 ₫) |
| Tổng tiền đơn hàng | 300,000 ₫ |
## Test steps
1. Đăng nhập vào ứng dụng và thêm sản phẩm có tổng giá trị đúng 300,000 ₫ vào giỏ hàng.
2. Tiến hành chuyển sang màn hình Thanh toán (Checkout).
3. Tại ô nhập mã giảm giá, nhập "SAVE10" và nhấn "Áp dụng".
4. Quan sát thông báo từ ứng dụng và số tiền được giảm hiển thị trên màn hình.
## Expected result
- Mã giảm giá được áp dụng thành công.
- Ứng dụng hiển thị thông báo thành công.
- Số tiền giảm giá được tính là 30,000 ₫ và tổng tiền thanh toán mới là 270,000 ₫.
## Status / Related bugs
Failed / BUG-FR21-D-05

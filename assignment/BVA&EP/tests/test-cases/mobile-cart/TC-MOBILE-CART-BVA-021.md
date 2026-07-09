# TC-MOBILE-CART-BVA-021: Đặt hàng thành công khi số dòng sản phẩm trong giỏ hàng bằng 1
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Functional / Positive / Boundary Value Analysis
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập.
- Giỏ hàng có đúng 1 dòng sản phẩm (ví dụ: "iPhone 15 Pro Max", quantity = 1).
- Thông tin giao hàng đã được cập nhật đầy đủ.
## Test data
| Product in cart | iPhone 15 Pro Max (Quantity: 1) |
## Test steps
1. Mở giỏ hàng, xác nhận có đúng 1 sản phẩm.
2. Nhấn "Tiến hành thanh toán" để sang màn hình Checkout.
3. Nhấn "Xác Nhận Thanh Toán".
## Expected result
- Đơn hàng được tạo thành công trên hệ thống.
- Giỏ hàng của người dùng được làm trống.
- Đơn hàng trong database lưu đúng thông tin của 1 sản phẩm đã mua.
## Status / Related bugs
Pass / None

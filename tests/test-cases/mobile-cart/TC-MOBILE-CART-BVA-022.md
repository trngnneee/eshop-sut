# TC-MOBILE-CART-BVA-022: Đặt hàng thành công khi số dòng sản phẩm trong giỏ hàng bằng 2
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Functional / Positive / Boundary Value Analysis
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập.
- Giỏ hàng có đúng 2 dòng sản phẩm khác nhau.
- Thông tin giao hàng đã được cập nhật đầy đủ.
## Test data
| Product 1 | iPhone 15 Pro Max (Quantity: 1) |
| Product 2 | Samsung Galaxy S24 Ultra (Quantity: 1) |
## Test steps
1. Mở giỏ hàng, xác nhận có đúng 2 sản phẩm khác nhau.
2. Nhấn "Tiến hành thanh toán" để chuyển sang màn hình Checkout.
3. Nhấn "Xác Nhận Thanh Toán".
## Expected result
- Đơn hàng được tạo thành công trên hệ thống.
- Giỏ hàng của người dùng được làm trống.
- Đơn hàng trong database lưu đúng thông tin của cả 2 dòng sản phẩm đã mua.
## Status / Related bugs
Passed

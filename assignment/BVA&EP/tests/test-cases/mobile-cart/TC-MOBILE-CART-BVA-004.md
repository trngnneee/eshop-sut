# TC-MOBILE-CART-BVA-004: Đặt hàng thành công với số lượng ở biên tồn kho cận trên (Quantity = maxStock - 1)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Functional / Positive / Boundary Value Analysis
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập.
- Sản phẩm "Tai nghe AirPods Pro 2" (giá 6,000,000 ₫) có số lượng tồn kho khả dụng là 5.
- Khách hàng đã cập nhật thông tin giao hàng đầy đủ.
## Test data
| Product in cart | Tai nghe AirPods Pro 2 |
| Stock available | 5 |
| Order quantity | 4 |
## Test steps
1. Mở màn hình chi tiết sản phẩm "Tai nghe AirPods Pro 2".
2. Thiết lập số lượng mua là 4 và nhấn "Thêm vào giỏ hàng".
3. Mở giỏ hàng, xác nhận số lượng là 4 và tổng tiền tạm tính là 24,000,000 ₫.
4. Tiến hành thanh toán và nhấn "Xác Nhận Thanh Toán".
## Expected result
- Đơn hàng được tạo thành công trên hệ thống.
- Tổng số lượng tồn kho khả dụng của sản phẩm "Tai nghe AirPods Pro 2" giảm đi 4 (còn lại 1).
- Giỏ hàng của người dùng được làm trống.
## Status / Related bugs
Pass / None

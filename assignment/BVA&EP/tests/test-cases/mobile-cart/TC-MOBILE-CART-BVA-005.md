# TC-MOBILE-CART-BVA-005: Đặt hàng thành công với số lượng ở biên tồn kho cực đại (Quantity = maxStock)
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
| Order quantity | 5 |
## Test steps
1. Mở màn hình chi tiết sản phẩm "Tai nghe AirPods Pro 2".
2. Thiết lập số lượng mua là 5 và nhấn "Thêm vào giỏ hàng".
3. Mở giỏ hàng, xác nhận số lượng là 5 và tổng tạm tính là 30,000,000 ₫.
4. Tiến hành thanh toán và nhấn "Xác Nhận Thanh Toán".
## Expected result
- Đơn hàng được tạo thành công trên hệ thống.
- Tổng số lượng tồn kho khả dụng của sản phẩm "Tai nghe AirPods Pro 2" giảm đi 5 (còn lại 0 - Hết hàng).
- Giỏ hàng của người dùng được làm trống.
## Status / Related bugs
Pass / None

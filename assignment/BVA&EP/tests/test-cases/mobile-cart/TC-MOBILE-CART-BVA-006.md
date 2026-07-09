# TC-MOBILE-CART-BVA-006: Chặn đặt hàng với số lượng vượt biên tồn kho (Quantity = maxStock + 1)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Functional / Negative / Boundary Value Analysis
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập.
- Sản phẩm "Tai nghe AirPods Pro 2" (giá 6,000,000 ₫) có số lượng tồn kho khả dụng là 5.
- Khách hàng đã cập nhật thông tin giao hàng đầy đủ.
## Test data
| Product in cart | Tai nghe AirPods Pro 2 |
| Stock available | 5 |
| Order quantity | 6 |
## Test steps
1. Mở màn hình chi tiết sản phẩm "Tai nghe AirPods Pro 2".
2. Thiết lập số lượng mua là 6 và nhấn "Thêm vào giỏ hàng".
3. Mở giỏ hàng, xác nhận số lượng là 6 và tiến hành thanh toán.
4. Tại màn hình Checkout, nhấn "Xác Nhận Thanh Toán".
## Expected result
- Backend API từ chối tạo đơn hàng và trả về lỗi: "Số lượng đặt hàng vượt quá hàng tồn kho khả dụng" (hoặc mã lỗi tương đương).
- Không có đơn hàng nào được tạo và tồn kho của sản phẩm không thay đổi.
## Status / Related bugs
Pass / None

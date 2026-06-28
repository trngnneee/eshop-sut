# TC-MOBILE-CART-DT-019: Đặt hàng thành công nhưng kiểm tra tính toàn vẹn của địa chỉ giao hàng trong CSDL orders
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Database / Functional / Positive / Equivalence Partitioning
## Preconditions
- Tài khoản customer hợp lệ đã tồn tại (test@eshop.com)
- Khách hàng đã cập nhật đầy đủ thông tin giao hàng trong hồ sơ: Họ tên ("Nguyễn Văn A"), SĐT ("912345678"), Địa chỉ ("123 Đường Lê Lợi, Quận 1, TP. HCM")
- Khách hàng đã đăng nhập thành công và có sản phẩm trong giỏ hàng
## Test data
| Product in cart | iPhone 15 Pro Max (Quantity: 1) |
| Shipping Address | 123 Đường Lê Lợi, Quận 1, TP. HCM |
## Test steps
1. Trên giao diện Mobile, truy cập giỏ hàng và tiến hành thanh toán.
2. Tại màn hình Checkout, kiểm tra thông tin địa chỉ hiển thị.
3. Nhấn "Xác Nhận Thanh Toán" để đặt hàng thành công.
4. Truy vấn cơ sở dữ liệu SQLite: chạy lệnh `SELECT * FROM orders WHERE user_id = [UserID] ORDER BY id DESC LIMIT 1;`.
5. Kiểm tra giá trị của cột `shipping_address` của đơn hàng vừa tạo.
## Expected result
- Màn hình mobile thông báo đặt hàng thành công.
- Cột `shipping_address` trong bảng `orders` của cơ sở dữ liệu phải lưu trữ đúng chuỗi địa chỉ giao hàng của người dùng: "123 Đường Lê Lợi, Quận 1, TP. HCM" (được tự động lấy từ hồ sơ cá nhân hoặc gửi từ client).
- Không được mang giá trị rỗng (`""`), `NULL`, hoặc `undefined`.
## Status / Related bugs
Not Executed

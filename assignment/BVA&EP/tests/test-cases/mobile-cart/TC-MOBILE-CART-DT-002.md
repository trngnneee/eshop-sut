# TC-MOBILE-CART-DT-002: Đặt hàng thành công trên Mobile với giỏ hàng có nhiều sản phẩm khác loại
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Checkout / Functional / Positive / Equivalence Partitioning
## Preconditions
- Tài khoản customer hợp lệ đã tồn tại (test@eshop.com / Test1234!)
- Khách hàng đã cập nhật đầy đủ thông tin Họ tên, SĐT, Địa chỉ trong hồ sơ
- Khách hàng đã đăng nhập thành công trên app mobile
- Các sản phẩm "iPhone 15 Pro Max" và "Samsung Galaxy S24 Ultra" có sẵn trong hệ thống
## Test data
| User account | test@eshop.com / Test1234! |
| Product 1 | iPhone 15 Pro Max (Price: 30,000,000 ₫, Quantity: 1) |
| Product 2 | Samsung Galaxy S24 Ultra (Price: 28,000,000 ₫, Quantity: 1) |
## Test steps
1. Mở ứng dụng EShop Mobile và đăng nhập.
2. Tại trang chủ, tìm "iPhone 15 Pro Max" và nhấn "Thêm vào giỏ".
3. Tìm tiếp "Samsung Galaxy S24 Ultra" và nhấn "Thêm vào giỏ".
4. Nhấn vào tab "Giỏ" trên thanh điều hướng.
5. Kiểm tra danh sách hiển thị đủ 2 sản phẩm và tổng tạm tính là 58,000,000 ₫.
6. Nhấn "Tiến hành thanh toán" để sang màn hình Checkout.
7. Kiểm tra lại danh sách sản phẩm hiển thị trên màn hình Checkout.
8. Nhấn "Xác Nhận Thanh Toán".
## Expected result
- Màn hình thông báo thanh toán thành công.
- Trạng thái giỏ hàng được làm sạch về rỗng.
- Đơn hàng mới trong CSDL phải lưu trữ đầy đủ 2 sản phẩm đã mua cùng tổng tiền 58,000,000 ₫.
## Status / Related bugs
Pass / None

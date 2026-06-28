# TC-MOBILE-CART-DT-001: Đặt hàng thành công trên Mobile với giỏ hàng có 1 sản phẩm hợp lệ
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Checkout / Functional / Positive / Equivalence Partitioning
## Preconditions
- Tài khoản customer hợp lệ đã tồn tại (test@eshop.com / Test1234!)
- Khách hàng đã cập nhật đầy đủ thông tin Họ tên ("Nguyễn Văn A"), SĐT ("912345678"), Địa chỉ ("123 Đường Lê Lợi, Quận 1, TP. HCM") trong hồ sơ
- Khách hàng đã đăng nhập thành công trên app mobile
- Sản phẩm "iPhone 15 Pro Max" có tồn tại trong hệ thống và còn hàng trong kho
## Test data
| User account | test@eshop.com / Test1234! |
| Product added | iPhone 15 Pro Max (Price: 30,000,000 ₫, Quantity: 1) |
| Shipping Address | Nguyễn Văn A - 912345678 - 123 Đường Lê Lợi, Quận 1, TP. HCM |
## Test steps
1. Mở ứng dụng EShop Mobile.
2. Đăng nhập bằng tài khoản customer mẫu.
3. Trên trang chủ, tìm sản phẩm "iPhone 15 Pro Max".
4. Nhấn "Thêm vào giỏ" (Quantity mặc định = 1).
5. Nhấn vào tab "Giỏ" trên thanh tiêu đề để mở màn hình Giỏ Hàng.
6. Xác nhận sản phẩm và tổng tiền tạm tính là 30,000,000 ₫.
7. Nhấn "Tiến hành thanh toán" để sang màn hình Checkout (Xác Nhận Đơn Hàng).
8. Nhấn "Xác Nhận Thanh Toán".
## Expected result
- Màn hình thông báo "Thanh toán thành công!" hiển thị.
- Trạng thái giỏ hàng được làm trống (hiển thị "Giỏ hàng của bạn đang trống" và Badge trên thanh tiêu đề hiển thị Giỏ (0)).
- Một đơn hàng mới được tạo trong database với trạng thái "pending" và tổng tiền là 30,000,000 ₫.
## Status / Related bugs
Not Executed

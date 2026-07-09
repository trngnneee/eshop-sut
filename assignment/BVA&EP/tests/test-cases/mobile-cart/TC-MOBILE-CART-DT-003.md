# TC-MOBILE-CART-DT-003: Chặn truy cập màn hình Checkout khi người dùng chưa đăng nhập (Guest)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Checkout / Security / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đang sử dụng ứng dụng mobile ở trạng thái chưa đăng nhập (Guest)
- Có sản phẩm "iPhone 15 Pro Max" trong hệ thống
## Test data
| User Token | None (Guest) |
| Product added | iPhone 15 Pro Max (Quantity: 1) |
## Test steps
1. Mở ứng dụng EShop Mobile (không thực hiện đăng nhập).
2. Thêm sản phẩm "iPhone 15 Pro Max" vào giỏ hàng.
3. Nhấn vào tab "Giỏ" để xem giỏ hàng.
4. Tại màn hình Giỏ Hàng, nhấn nút "Tiến hành thanh toán".
## Expected result
- Hệ thống hiển thị hộp thoại cảnh báo (Alert) với nội dung: "Bạn cần đăng nhập để thanh toán!".
- Sau khi đóng thông báo, người dùng được điều hướng tự động sang màn hình Đăng Nhập (Login).
- Người dùng không được phép truy cập màn hình Checkout (Xác Nhận Đơn Hàng).
## Status / Related bugs
Pass / None

# TC-MOBILE-CART-DT-012: Chặn đặt hàng khi sản phẩm trong giỏ hàng vượt quá số lượng tồn kho
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và đang mở app mobile.
- Sản phẩm "Tai nghe AirPods Pro 2" trong hệ thống có số lượng tồn kho thực tế là 5 sản phẩm.
- Người dùng đã thêm sản phẩm vào giỏ hàng và chuyển sang màn hình Checkout.
## Test data
| Product | Tai nghe AirPods Pro 2 (Stock: 5) |
| Order quantity | 6 |
## Test steps
1. Tại màn hình giỏ hàng hoặc chi tiết sản phẩm, cố gắng thiết lập số lượng mua là 6.
2. Tiến hành chuyển sang màn hình Checkout và nhấn nút "Xác Nhận Thanh Toán".
3. Hệ thống gửi yêu cầu POST `/api/checkout` với số lượng mua là 6.
4. Quan sát phản hồi từ Backend API và UI hiển thị.
## Expected result
- Backend API từ chối tạo đơn hàng và trả về mã lỗi thích hợp (ví dụ: HTTP 400 Bad Request kèm thông điệp "Số lượng đặt hàng vượt quá hàng tồn kho khả dụng").
- Mobile frontend hiển thị thông báo lỗi chi tiết cho khách hàng.
- Đơn hàng không được tạo trong cơ sở dữ liệu.
## Status / Related bugs
Pass / None

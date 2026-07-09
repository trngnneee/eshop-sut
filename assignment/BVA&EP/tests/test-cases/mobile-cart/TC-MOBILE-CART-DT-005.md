# TC-MOBILE-CART-DT-005: Đặt hàng thất bại khi Token đăng nhập hết hạn hoặc sai chữ ký
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / API / Security / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã mở ứng dụng di động.
- Giỏ hàng đã có sản phẩm.
- Người dùng đã chuyển sang giao diện Checkout.
- Token JWT lưu trữ tại client đã hết hạn hoặc bị can thiệp thay đổi signature.
## Test data
| User Token | Expired / Tampered JWT Token |
| Product added | iPhone 15 Pro Max (Quantity: 1) |
## Test steps
1. Trên giao diện Checkout, nhấn nút "Xác Nhận Thanh Toán".
2. Hệ thống gửi yêu cầu `POST /api/checkout` kèm theo Token đã hết hạn / sai chữ ký trong Headers.
3. Quan sát phản hồi của Backend API và giao diện mobile.
## Expected result
- Backend trả về mã lỗi HTTP 401 Unauthorized (hoặc HTTP 403 Forbidden).
- Ứng dụng di động hiển thị thông báo lỗi thanh toán thân thiện (ví dụ: "Đăng nhập hết hạn, vui lòng đăng nhập lại").
- Đơn hàng mới không được tạo trong cơ sở dữ liệu.
- Giỏ hàng của người dùng không bị xóa sạch.
## Status / Related bugs
Pass / None

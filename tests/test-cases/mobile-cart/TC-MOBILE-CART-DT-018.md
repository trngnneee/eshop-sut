# TC-MOBILE-CART-DT-018: Backend kiểm tra và từ chối đặt hàng khi đơn giá hoặc tổng tiền bị thay đổi bất thường (Price Tampering)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / API / Security / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và đang mở app mobile.
- Giỏ hàng có sản phẩm "iPhone 15 Pro Max" (giá gốc: 30,000,000 ₫).
- Kẻ tấn công sử dụng công cụ Proxy (như Charles Proxy/Burp Suite) để bắt và sửa đổi HTTP Request payload gửi từ ứng dụng mobile lên server.
## Test data
| Product added | iPhone 15 Pro Max (Price: 30,000,000 ₫, Quantity: 1) |
| Original total_amount | 30000000 |
| Intercepted total_amount | 1000 (Sửa đổi giá trị thành 1,000 ₫) |
## Test steps
1. Tại màn hình Checkout trên mobile, nhấn "Xác Nhận Thanh Toán".
2. Sử dụng công cụ Burp Suite bắt request `POST /api/checkout`.
3. Sửa giá trị của trường `total_amount` trong JSON body từ `30000000` thành `1000`.
4. Cho request tiếp tục truyền đi đến Backend API.
5. Quan sát phản hồi từ server.
## Expected result
- Backend API từ chối tạo đơn hàng và trả về mã lỗi HTTP 400 Bad Request kèm theo thông điệp lỗi (ví dụ: "Tổng tiền đơn hàng không khớp với giá trị thực của sản phẩm").
- Không có đơn hàng nào được tạo trong cơ sở dữ liệu với giá trị giả mạo 1,000 ₫.
## Status / Related bugs
Not Executed

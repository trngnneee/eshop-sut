# TC-MOBILE-CART-BVA-020: Chặn đặt hàng khi số dòng sản phẩm trong giỏ hàng bằng 0
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Functional / Negative / Boundary Value Analysis
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập.
- Giỏ hàng trống (0 dòng sản phẩm).
## Test data
| User Token | Valid Customer Token |
| Cart Items | Empty list [] (0 items) |
## Test steps
1. Nhấn nút "Tiến hành thanh toán" để sang màn hình Checkout.
2. Hoặc cố tình gửi HTTP POST request trực tiếp đến `/api/checkout` với danh sách items rỗng.
3. Quan sát kết quả.
## Expected result
- Trên giao diện: Người dùng không được chuyển sang màn hình checkout hoặc nút "Xác Nhận Thanh Toán" bị khóa/không có hiệu lực.
- Gửi trực tiếp API: Backend API trả về lỗi HTTP 400 Bad Request kèm thông báo "Không được đặt hàng khi giỏ hàng trống".
## Status / Related bugs
Pass / None

# TC-MOBILE-CART-DT-004: Chặn truy cập màn hình Checkout khi giỏ hàng trống
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Checkout / Functional / Negative / Equivalence Partitioning
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập
- Giỏ hàng của người dùng hiện đang trống (không có sản phẩm nào)
## Test data
| User Token | Valid Customer Token |
| Cart Items | Empty list [] |
## Test steps
1. Mở ứng dụng EShop Mobile và đăng nhập.
2. Nhấn vào tab "Giỏ" trên thanh điều hướng để mở màn hình Giỏ Hàng.
3. Quan sát giao diện màn hình Giỏ Hàng và kiểm tra sự xuất hiện của nút "Tiến hành thanh toán".
## Expected result
- Màn hình hiển thị thông báo "Giỏ hàng của bạn đang trống".
- Nút "Tiến hành thanh toán" không hiển thị hoặc bị khóa (disabled) để ngăn người dùng chuyển qua màn hình checkout khi không có hàng.
## Status / Related bugs
Pass / None

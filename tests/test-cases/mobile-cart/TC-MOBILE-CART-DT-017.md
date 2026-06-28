# TC-MOBILE-CART-DT-017: Ngăn chặn tạo đơn hàng trùng lặp khi người dùng bấm nút đặt hàng nhiều lần liên tiếp
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Checkout / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và đang mở app mobile.
- Giỏ hàng có sản phẩm "iPhone 15 Pro Max".
- Đã điền đầy đủ thông tin giao hàng và đang ở màn hình Checkout.
## Test data
| Product | iPhone 15 Pro Max (Quantity: 1) |
| Checkout action | Bấm liên tiếp nút đặt hàng 3 lần thật nhanh |
## Test steps
1. Tại màn hình Checkout, nhấp liên tục 3 lần thật nhanh vào nút "Xác Nhận Thanh Toán".
2. Hệ thống gửi yêu cầu checkout lên máy chủ backend.
3. Quan sát giao diện và kiểm tra số đơn hàng mới được tạo trong database.
## Expected result
- Ứng dụng di động phải khóa nút đặt hàng ngay lập tức sau click đầu tiên và hiển thị trạng thái đang tải (Loading).
- Chỉ có 1 yêu cầu thanh toán được gửi đi hoặc API backend chỉ xử lý và tạo 1 đơn hàng duy nhất cho lượt bấm này.
- Database không xuất hiện nhiều đơn hàng giống nhau về thông tin, sản phẩm, và tổng tiền.
## Status / Related bugs
Not Executed

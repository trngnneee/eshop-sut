# TC-MOBILE-CART-DT-009: Xóa sản phẩm khỏi giỏ hàng trên mobile thành công
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Functional / Positive / Equivalence Partitioning
## Preconditions
- Người dùng đang ở màn hình Giỏ Hàng của ứng dụng di động.
- Trong giỏ hàng đang có ít nhất 1 sản phẩm (ví dụ: "iPhone 15 Pro Max").
## Test data
| Product in cart | iPhone 15 Pro Max (Price: 30,000,000 ₫, Quantity: 1) |
## Test steps
1. Tại màn hình Giỏ Hàng, tìm dòng sản phẩm "iPhone 15 Pro Max".
2. Nhấn nút "Xóa" bên cạnh dòng sản phẩm đó.
3. Quan sát giỏ hàng sau khi nhấn.
## Expected result
- Sản phẩm "iPhone 15 Pro Max" biến mất khỏi danh sách giỏ hàng.
- Màn hình hiển thị trạng thái giỏ hàng trống và thông báo "Giỏ hàng của bạn đang trống".
- Tổng tạm tính của giỏ hàng cập nhật về 0 ₫.
- Badge số lượng giỏ hàng trên Navbar giảm về 0.
## Status / Related bugs
Pass / None

# TC-MOBILE-CART-DT-007: Cập nhật tăng số lượng trực tiếp trong giỏ hàng thành công
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Functional / Positive / Equivalence Partitioning
## Preconditions
- Người dùng đã đăng nhập và mở màn hình Giỏ Hàng.
- Giỏ hàng đang có sản phẩm "iPhone 15 Pro Max" với số lượng là 1.
## Test data
| Product in cart | iPhone 15 Pro Max (Price: 30,000,000 ₫) |
| New Quantity input | 2 |
## Test steps
1. Tại màn hình Giỏ Hàng, tìm ô nhập số lượng cho sản phẩm "iPhone 15 Pro Max" (hiện tại hiển thị là 1).
2. Xóa số 1 và nhập vào số 2.
3. Nhấp chuột ra ngoài hoặc hoàn tất nhập để kích hoạt cập nhật.
4. Quan sát số lượng mới hiển thị và tổng tiền tạm tính.
## Expected result
- Ô nhập số lượng cập nhật và hiển thị đúng giá trị là 2.
- Thành tiền dòng sản phẩm và Tổng tạm tính của giỏ hàng cập nhật thành 60,000,000 ₫.
## Status / Related bugs
Not Executed

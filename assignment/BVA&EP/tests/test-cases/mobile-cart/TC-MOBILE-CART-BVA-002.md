# TC-MOBILE-CART-BVA-002: Cập nhật số lượng sản phẩm trong giỏ hàng bằng 1 (Min)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Functional / Positive / Boundary Value Analysis
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập và đang mở màn hình Giỏ Hàng.
- Giỏ hàng có sản phẩm "iPhone 15 Pro Max" (Quantity = 2).
## Test data
| Product in cart | iPhone 15 Pro Max |
| New Quantity input | 1 |
## Test steps
1. Tại màn hình Giỏ Hàng, tìm ô số lượng của "iPhone 15 Pro Max".
2. Thay đổi giá trị thành 1.
3. Hoàn tất việc nhập.
## Expected result
- Ô nhập số lượng hiển thị đúng 1.
- Tổng tạm tính của giỏ hàng cập nhật thành 30,000,000 ₫.
## Status / Related bugs
Pass / None

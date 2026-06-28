# TC-MOBILE-CART-BVA-001: Cập nhật số lượng sản phẩm trong giỏ hàng về biên dưới cực tiểu (Quantity = 0)
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Functional / Negative / Boundary Value Analysis
## Preconditions
- Tài khoản customer hợp lệ đã đăng nhập và đang mở màn hình Giỏ Hàng.
- Giỏ hàng có sản phẩm "iPhone 15 Pro Max" (Quantity = 1).
## Test data
| Product in cart | iPhone 15 Pro Max (Price: 30,000,000 ₫) |
| New Quantity input | 0 |
## Test steps
1. Tại màn hình Giỏ Hàng, tìm ô số lượng của "iPhone 15 Pro Max".
2. Thay đổi giá trị hiển thị thành 0.
3. Hoàn tất việc nhập.
## Expected result
- Ứng dụng từ chối cập nhật số lượng thành 0.
- Số lượng hiển thị tự động quay về (fallback) giá trị 1.
- Tổng tạm tính của giỏ hàng vẫn giữ nguyên là 30,000,000 ₫.
## Status / Related bugs
Not Executed

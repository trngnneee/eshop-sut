# TC-MOBILE-CART-DT-010: Cập nhật số lượng về 0 hoặc số âm phải tự động đưa về 1 hoặc báo lỗi
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đã mở màn hình Giỏ Hàng của ứng dụng di động.
- Trong giỏ hàng đang có sản phẩm "iPhone 15 Pro Max" với số lượng là 1.
## Test data
| Product in cart | iPhone 15 Pro Max |
| Invalid inputs | Test case 1: 0, Test case 2: -5 |
## Test steps
1. Nhập số 0 vào ô nhập số lượng của sản phẩm "iPhone 15 Pro Max".
2. Quan sát phản hồi của ứng dụng di động.
3. Nhập số -5 vào ô nhập số lượng của sản phẩm "iPhone 15 Pro Max".
4. Quan sát phản hồi của ứng dụng di động.
## Expected result
- Ứng dụng từ chối cập nhật số lượng thành 0 hoặc số âm.
- Số lượng hiển thị tự động hồi quy (fallback) về giá trị mặc định là 1 (hoặc giữ nguyên giá trị trước đó là 1).
- Tổng tạm tính của giỏ hàng vẫn giữ nguyên là 30,000,000 ₫, không bị tính toán ra 0 hoặc số âm.
## Status / Related bugs
Pass / None

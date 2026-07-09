# TC-MOBILE-CART-DT-011: Cập nhật số lượng bằng chữ hoặc ký tự đặc biệt trên mobile
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Functional / Negative / Equivalence Partitioning
## Preconditions
- Người dùng đang mở màn hình Giỏ Hàng trên app mobile.
- Trong giỏ hàng đang có sản phẩm "iPhone 15 Pro Max" với số lượng là 1.
## Test data
| Product in cart | iPhone 15 Pro Max |
| Invalid inputs | "abc", "@#$" |
## Test steps
1. Tại ô nhập số lượng của "iPhone 15 Pro Max", cố gắng nhập chuỗi chữ cái "abc".
2. Quan sát ô hiển thị số lượng và tổng tạm tính.
3. Thử tiếp tục nhập các ký tự đặc biệt "@#$".
4. Quan sát kết quả.
## Expected result
- Ứng dụng từ chối cập nhật số lượng thành các giá trị không phải số.
- Số lượng hiển thị tự động hồi quy về giá trị mặc định là 1.
- Tổng tạm tính của giỏ hàng vẫn hiển thị đúng 30,000,000 ₫.
## Status / Related bugs
Pass / None

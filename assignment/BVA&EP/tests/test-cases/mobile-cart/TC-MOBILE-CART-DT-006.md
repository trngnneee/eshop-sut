# TC-MOBILE-CART-DT-006: Thêm trùng sản phẩm vào giỏ hàng trên mobile phải cộng dồn số lượng
## Requirement ID
FR-21 / FR24
## Module / Test type / Technique
Shopping Cart / Functional / Positive / Equivalence Partitioning
## Preconditions
- Người dùng đang mở ứng dụng di động EShop.
- Sản phẩm "iPhone 15 Pro Max" tồn tại trên hệ thống.
- Giỏ hàng hiện tại đang trống.
## Test data
| Product to add | iPhone 15 Pro Max |
| Step 1 Quantity | 1 |
| Step 2 Quantity | 2 |
## Test steps
1. Tại màn hình danh sách sản phẩm, nhấn nút "Thêm vào giỏ" cho sản phẩm "iPhone 15 Pro Max" (số lượng thêm = 1).
2. Vào màn hình chi tiết sản phẩm "iPhone 15 Pro Max".
3. Nhập số lượng là 2 và nhấn nút "Thêm vào giỏ hàng".
4. Nhấn vào tab "Giỏ" trên thanh điều hướng để mở màn hình Giỏ Hàng.
5. Quan sát danh sách sản phẩm hiển thị trong giỏ hàng.
## Expected result
- Trong giỏ hàng chỉ hiển thị duy nhất 1 dòng sản phẩm "iPhone 15 Pro Max".
- Số lượng hiển thị của sản phẩm đó phải là 3 (cộng dồn 1 + 2 = 3).
- Không được tạo thành 2 dòng sản phẩm trùng lặp tên/ID.
- Tổng tạm tính hiển thị đúng giá trị của 3 sản phẩm (90,000,000 ₫).
## Status / Related bugs
Pass / None

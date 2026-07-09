# TC-CART-060: Kiểm tra hiển thị thông tin tồn kho và ngăn chặn chọn số lượng vượt quá tồn kho khả dụng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Boundary Value Analysis

## Preconditions
- Đã đăng nhập tài khoản người dùng.
- Có sản phẩm A với số lượng khả dụng trong kho thực tế là 5.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Số lượng mua thử nghiệm | `6` |

## Test steps
1. Truy cập trang chi tiết sản phẩm A.
2. Xác minh giao diện hiển thị thông tin số lượng còn lại của sản phẩm (ví dụ: hiển thị "Còn lại: 5").
3. Nhập số lượng mua là 6 vào ô số lượng hoặc nhấn nút tăng số lượng lên 6.
4. Nhấp nút "Thêm vào giỏ hàng".

## Expected result
- Giao diện chi tiết sản phẩm hiển thị rõ ràng số lượng tồn kho khả dụng còn lại là 5 cái.
- Khi người dùng nhập số lượng là 6 (vượt quá tồn kho 5), hệ thống hiển thị cảnh báo lỗi tức thì.
- Hệ thống chặn hành động thêm vào giỏ hàng, nút "Thêm vào giỏ hàng" có thể bị vô hiệu hóa hoặc trả về thông báo lỗi trực quan (ví dụ: "Số lượng vượt quá hàng tồn kho khả dụng").

## Status / Related bugs
Fail / BUG-FR07-B-12

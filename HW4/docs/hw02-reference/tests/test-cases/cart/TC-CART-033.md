# TC-CART-033: Xóa sản phẩm cuối cùng chuyển về empty state

## Requirement ID
FR-07, FR-24

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có duy nhất 1 sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Nhấp vào nút Xóa sản phẩm duy nhất đó.
3. Nhấp chọn 'Đồng ý/Xác nhận' trên hộp thoại xác nhận.

## Expected result
- Sản phẩm bị xóa thành công.
- Giao diện lập tức chuyển đổi về trạng thái giỏ hàng trống (Empty State) hiển thị đầy đủ văn bản thông báo, icon/ảnh minh họa và nút điều hướng 'Tiếp tục mua sắm'.

## Status / Related bugs
Not Run / None

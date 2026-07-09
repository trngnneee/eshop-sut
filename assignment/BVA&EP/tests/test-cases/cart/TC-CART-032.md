# TC-CART-032: Xác nhận xóa sản phẩm

## Requirement ID
FR-07, FR-24

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A.
- Đã nhấp nút Xóa của sản phẩm A và hộp thoại xác nhận đang hiển thị.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Nhấp chọn nút 'Đồng ý/Xác nhận' (Confirm) trên hộp thoại xác nhận.

## Expected result
- Hộp thoại xác nhận đóng lại.
- Sản phẩm A bị loại bỏ hoàn toàn khỏi bảng giỏ hàng.
- Tổng cộng giỏ hàng được tính toán lại chính xác và hiển thị toast thông báo thành công.

## Status / Related bugs
Fail / BUG-FR07-B-05

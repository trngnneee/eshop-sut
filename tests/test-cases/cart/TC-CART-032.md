# TC-CART-032: Hủy xóa sản phẩm

## Requirement ID
FR-07, FR-24

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A.
- Đã nhấp vào nút Xóa của sản phẩm A và hộp thoại xác nhận đang hiển thị.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Nhấp chọn nút 'Hủy' (Cancel) trên hộp thoại xác nhận xóa.

## Expected result
- Hộp thoại xác nhận đóng lại.
- Sản phẩm A vẫn nằm trong giỏ hàng, số lượng và tổng cộng giỏ hàng giữ nguyên không thay đổi.

## Status / Related bugs
Not Run / None

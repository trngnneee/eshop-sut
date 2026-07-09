# TC-CART-028: Tổng cộng cập nhật realtime khi đổi quantity

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A (đơn giá 100000) với số lượng ban đầu là 1.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Nhấp vào nút '+' để tăng số lượng sản phẩm A lên 2.
3. Quan sát giá trị hiển thị ở phần 'Tổng cộng'.

## Expected result
- Giá trị tại dòng 'Tổng cộng' thay đổi lập tức sang '200.000 ₫' mà không cần reload/tải lại trang.

## Status / Related bugs
Pass / None

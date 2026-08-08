# TC-CART-036: Badge cập nhật sau khi tăng quantity

## Requirement ID
FR-23

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng hiện tại có 1 sản phẩm A với số lượng là 1. Badge hiển thị số 1.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Nhấp vào nút '+' của sản phẩm A để tăng số lượng lên 2.
3. Quan sát badge giỏ hàng trên navbar.

## Expected result
- Badge giỏ hàng trên navbar cập nhật theo tổng số lượng sản phẩm mới là 2.

## Status / Related bugs
Not Run / None

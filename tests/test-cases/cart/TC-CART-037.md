# TC-CART-037: Badge cập nhật sau khi xóa sản phẩm

## Requirement ID
FR-23

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng đang có 2 sản phẩm A (SL 1) và B (SL 1). Badge hiển thị 2.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Thực hiện xóa hoàn toàn sản phẩm B ra khỏi giỏ hàng.
3. Quan sát badge giỏ hàng trên navbar.

## Expected result
- Badge giỏ hàng lập tức cập nhật giảm xuống còn 1.

## Status / Related bugs
Not Run / None

# TC-CART-029: Tổng cộng cập nhật sau khi xóa sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có Sản phẩm A (Thành tiền: 200.000 ₫) và Sản phẩm B (Thành tiền: 150.000 ₫).
- Tổng cộng ban đầu là 350.000 ₫.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Thực hiện xóa Sản phẩm A khỏi giỏ hàng (và xác nhận xóa).
3. Quan sát giá trị tại dòng 'Tổng cộng'.

## Expected result
- Sau khi sản phẩm A biến mất khỏi giỏ hàng, Tổng cộng cập nhật ngay về '150.000 ₫' chính xác theo các sản phẩm còn lại.

## Status / Related bugs
Pass / None

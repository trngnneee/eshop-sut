# TC-CART-016: Nhập quantity = 2

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / BVA - Min + 1

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Quantity input | `2` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập số '2' vào ô số lượng của sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài.

## Expected result
- Số lượng được cập nhật thành 2.
- Thành tiền và Tổng cộng giỏ hàng được cập nhật tương ứng chính xác.

## Status / Related bugs
Not Run / None

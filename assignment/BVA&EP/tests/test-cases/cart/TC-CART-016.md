# TC-CART-016: Nhập quantity = 5

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / EP - Valid

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Quantity input | `5` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập số '5' vào ô số lượng của sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài.

## Expected result
- Hợp lệ, số lượng cập nhật thành 5.
- Thành tiền cập nhật bằng Đơn giá x 5, tổng cộng thay đổi tương ứng.

## Status / Related bugs
Fail / BUG-FR07-B-04

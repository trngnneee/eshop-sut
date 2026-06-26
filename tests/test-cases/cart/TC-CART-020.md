# TC-CART-020: Nhập quantity thập phân

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / EP - Invalid

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Quantity input | `1.5` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập số '1.5' vào ô số lượng của sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài.

## Expected result
- Hành động không hợp lệ. Hệ thống chỉ chấp nhận số nguyên dương.
- Giá trị tự động làm tròn hoặc trả về số cũ, không thực hiện cập nhật giá trị số thập phân.

## Status / Related bugs
Not Run / None

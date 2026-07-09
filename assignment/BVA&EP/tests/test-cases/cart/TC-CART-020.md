# TC-CART-020: Nhập quantity là chữ

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
| Quantity input | `abc` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập chuỗi chữ 'abc' vào ô số lượng của sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài.

## Expected result
- Hành động không hợp lệ, hệ thống không chấp nhận nhập ký tự không phải số.
- Số lượng sản phẩm không thay đổi.

## Status / Related bugs
Fail / BUG-FR07-B-04

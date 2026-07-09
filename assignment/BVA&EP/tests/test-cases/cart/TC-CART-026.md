# TC-CART-026: Tính subtotal cho 1 sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Domain Testing

## Preconditions
- Người dùng đã đăng nhập.
- Sản phẩm A có đơn giá 100000 và số lượng trong giỏ hàng là 3.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Price | `100000` |
| Quantity | `3` |

## Test steps
1. Truy cập trang `/cart`.
2. Quan sát cột Thành tiền của sản phẩm A.

## Expected result
- Thành tiền hiển thị chính xác là '300.000 ₫'.

## Status / Related bugs
Pass / None

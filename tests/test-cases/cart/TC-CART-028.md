# TC-CART-028: Tính tổng cộng cho nhiều sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Domain Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có 2 sản phẩm: Sản phẩm A (đơn giá 100000, số lượng 2), Sản phẩm B (đơn giá 50000, số lượng 3).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm A | `Giá 100000, SL 2` |
| Sản phẩm B | `Giá 50000, SL 3` |

## Test steps
1. Truy cập trang `/cart`.
2. Quan sát dòng Tổng cộng giỏ hàng.

## Expected result
- Tổng cộng hiển thị chính xác là '350.000 ₫' (100.000 x 2 + 50.000 x 3 = 350.000).

## Status / Related bugs
Not Run / None

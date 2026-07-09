# TC-CART-035: Badge cập nhật sau khi thêm sản phẩm

## Requirement ID
FR-23, FR-24

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng hiện tại có 3 sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm thêm mới | `Sản phẩm C` |

## Test steps
1. Tìm sản phẩm C và nhấn nút 'Thêm vào giỏ hàng'.
2. Quan sát badge giỏ hàng trên thanh điều hướng.

## Expected result
- Badge lập tức cập nhật tăng thêm 1 đơn vị thành 4.

## Status / Related bugs
Pass / None

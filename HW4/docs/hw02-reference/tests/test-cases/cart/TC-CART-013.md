# TC-CART-013: Sản phẩm khác ID được hiển thị thành dòng riêng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Domain Testing

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng hiện tại trống.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm 1 | `Sản phẩm A (ID: 1)` |
| Sản phẩm 2 | `Sản phẩm B (ID: 2)` |

## Test steps
1. Thêm Sản phẩm A (ID: 1) vào giỏ hàng.
2. Thêm Sản phẩm B (ID: 2) vào giỏ hàng.
3. Truy cập trang `/cart`.

## Expected result
- Bảng giỏ hàng hiển thị 2 dòng sản phẩm riêng biệt dành riêng cho Sản phẩm A và Sản phẩm B.

## Status / Related bugs
Not Run / None

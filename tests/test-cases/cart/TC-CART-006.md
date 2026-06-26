# TC-CART-006: Hiển thị ảnh và tên sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / UI Requirement / UI Requirement

## Preconditions
- Người dùng đã đăng nhập vào hệ thống.
- Giỏ hàng có ít nhất 1 sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | `Sản phẩm A (có hình ảnh minh họa)` |

## Test steps
1. Truy cập trang `/cart`.
2. Quan sát cột 'Sản phẩm' trong bảng giỏ hàng.

## Expected result
- Cột 'Sản phẩm' hiển thị hình ảnh đại diện (thumbnail) của sản phẩm.
- Tên sản phẩm hiển thị chính xác, rõ ràng bên cạnh hoặc bên dưới hình ảnh.

## Status / Related bugs
Not Run / None

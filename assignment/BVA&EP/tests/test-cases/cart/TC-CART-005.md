# TC-CART-005: Hiển thị đầy đủ các cột trong bảng giỏ hàng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Domain Testing

## Preconditions
- Người dùng đã đăng nhập vào hệ thống.
- Giỏ hàng của người dùng có ít nhất 1 sản phẩm.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm trong giỏ hàng | `Sản phẩm A` |

## Test steps
1. Truy cập trang `/cart`.
2. Quan sát các cột hiển thị trong bảng danh sách sản phẩm.

## Expected result
- Bảng giỏ hàng hiển thị đầy đủ các cột: Sản phẩm (bao gồm ảnh và tên sản phẩm), Đơn giá, Số lượng, Thành tiền, và Thao tác (nút xóa/chỉnh sửa).

## Status / Related bugs
Pass / None

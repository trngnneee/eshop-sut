# TC-CART-012: Không tạo dòng mới khi thêm sản phẩm trùng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / State Testing

## Preconditions
- Người dùng đã đăng nhập.
- Sản phẩm A đã có trong giỏ hàng.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | `Sản phẩm A` |

## Test steps
1. Thực hiện hành động thêm sản phẩm A vào giỏ hàng thêm nhiều lần nữa.
2. Truy cập trang `/cart`.

## Expected result
- Bảng danh sách giỏ hàng không xuất hiện nhiều dòng sản phẩm trùng ID với sản phẩm A.
- Chỉ có duy nhất một dòng cho sản phẩm A và số lượng tăng lên tương ứng.

## Status / Related bugs
Pass / None

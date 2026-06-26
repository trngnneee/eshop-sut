# TC-CART-011: Thêm sản phẩm từ trang chi tiết sản phẩm

## Requirement ID
FR-07, FR-24

## Module / Test type / Technique
Cart / Functional / Functional Testing

## Preconditions
- Người dùng đã đăng nhập vào hệ thống.
- Người dùng đang ở trang chi tiết của sản phẩm A (`/products/:id`).

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm | `Sản phẩm A` |
| Số lượng thêm | `1` |

## Test steps
1. Tại trang chi tiết sản phẩm A, chọn số lượng là 1.
2. Nhấp vào nút 'Thêm vào giỏ hàng'.
3. Kiểm tra giỏ hàng bằng cách vào trang `/cart`.

## Expected result
- Sản phẩm được thêm vào giỏ hàng ngay sau khi thực hiện thao tác click.
- Toast thông báo thành công hiển thị và giỏ hàng ghi nhận sản phẩm A với số lượng tương ứng.

## Status / Related bugs
Not Run / None

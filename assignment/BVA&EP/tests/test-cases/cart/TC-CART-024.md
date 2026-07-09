# TC-CART-024: Nhấn nút `-` khi quantity > 1

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Functional + State

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A với số lượng ban đầu là 3.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Nhấp vào nút '-' tương ứng với sản phẩm A.

## Expected result
- Số lượng sản phẩm giảm xuống còn 2.
- Thành tiền của sản phẩm và Tổng cộng giỏ hàng cập nhật giảm đi tương ứng realtime.

## Status / Related bugs
Fail / BUG-FR07-B-04

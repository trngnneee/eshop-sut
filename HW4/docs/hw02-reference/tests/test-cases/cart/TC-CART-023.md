# TC-CART-023: Nhấn nút `+` để tăng số lượng

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Functional + State

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A với số lượng ban đầu là 1.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Nhấp vào nút '+' tương ứng với sản phẩm A.

## Expected result
- Số lượng sản phẩm tăng lên 2.
- Thành tiền của sản phẩm A và Tổng cộng giỏ hàng cập nhật tăng lên tương ứng theo thời gian thực (realtime).

## Status / Related bugs
Not Run / None

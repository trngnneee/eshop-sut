# TC-CART-025: Nhấn nút `-` khi quantity = 1

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / BVA

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A với số lượng là 1.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Truy cập trang `/cart`.
2. Nhấp vào nút '-' hoặc kiểm tra trạng thái nút '-' của sản phẩm A.

## Expected result
- Nút '-' bị vô hiệu hóa (disabled) hoặc khi click vào, hệ thống không cho phép giảm số lượng xuống 0.

## Status / Related bugs
Not Run / None

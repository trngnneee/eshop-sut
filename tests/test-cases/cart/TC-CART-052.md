# TC-CART-052: Mở cart ở tab khác sau khi thêm sản phẩm

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / Multi-tab State

## Preconditions
- Người dùng đăng nhập.
- Thêm sản phẩm thành công vào giỏ hàng.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Không có | |

## Test steps
1. Mở một tab mới trên cùng một trình duyệt.
2. Truy cập đường dẫn `http://localhost:5173/cart`.

## Expected result
- Tab mới hiển thị chính xác trạng thái giỏ hàng mới nhất chứa các sản phẩm đã thêm.

## Status / Related bugs
Not Run / None

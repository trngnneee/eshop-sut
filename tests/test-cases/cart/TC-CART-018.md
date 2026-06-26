# TC-CART-018: Nhập quantity = 0

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / BVA - Min - 1

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A với số lượng là 1.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Quantity input | `0` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập số '0' vào ô số lượng của sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài.

## Expected result
- Hành động bị từ chối, hệ thống không cho phép cập nhật số lượng xuống 0.
- Giá trị trong ô số lượng tự động reset về giá trị hợp lệ trước đó hoặc hiển thị cảnh báo lỗi.

## Status / Related bugs
Not Run / None

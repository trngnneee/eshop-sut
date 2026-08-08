# TC-CART-021: Nhập quantity là ký tự đặc biệt

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / EP - Invalid

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Quantity input | `@#$` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập các ký tự đặc biệt '@#$' vào ô nhập số lượng sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài.

## Expected result
- Hành động không hợp lệ, hệ thống từ chối cập nhật số lượng.

## Status / Related bugs
Not Run / None

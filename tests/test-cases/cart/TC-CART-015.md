# TC-CART-015: Nhập quantity = 1

## Requirement ID
FR-07

## Module / Test type / Technique
Cart / Functional / BVA - Min

## Preconditions
- Người dùng đã đăng nhập.
- Giỏ hàng có sản phẩm A với số lượng ban đầu là 2.

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Quantity input | `1` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập trực tiếp số '1' vào ô nhập số lượng (quantity input) của sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài ô nhập (blur) để hệ thống cập nhật.

## Expected result
- Số lượng được chấp nhận và cập nhật thành 1 thành công.
- Thành tiền của sản phẩm và Tổng cộng giỏ hàng được tính toán cập nhật chính xác theo số lượng 1.

## Status / Related bugs
Not Run / None

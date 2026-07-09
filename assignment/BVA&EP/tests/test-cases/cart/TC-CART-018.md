# TC-CART-018: Nhập quantity âm

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
| Quantity input | `-1` |

## Test steps
1. Truy cập trang `/cart`.
2. Nhập số '-1' vào ô số lượng của sản phẩm A.
3. Nhấn Enter hoặc nhấp ra ngoài.

## Expected result
- Hành động không hợp lệ, hệ thống từ chối cập nhật.
- Giá trị số lượng không thay đổi, giữ nguyên giá trị hợp lệ cũ.

## Status / Related bugs
Fail / BUG-FR07-B-04

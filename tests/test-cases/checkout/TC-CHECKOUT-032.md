# TC-CHECKOUT-032: API từ chối khi items rỗng nhưng total_amount > 0

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- Giỏ hàng có sản phẩm (cartTotal > 0)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| items | [] (mảng rỗng) |
| total_amount | 500.000 |

## Test steps
1. Đăng nhập; thêm sản phẩm vào giỏ; ghi nhận `cartTotal`.
2. Gửi checkout với `items: []` và `total_amount` = 500.000.
3. Ghi nhận phản hồi và đơn hàng.

## Expected result
- Backend không tin `total_amount` khi không có sản phẩm tương ứng.
- Từ chối đơn hoặc tính lại từ giỏ thực tế phía server.

## Sub-domains covered
SD-T08 (items rỗng + total_amount dương — không nhất quán)

## Type
Invalid

## Status / Related bugs
Not Run / None

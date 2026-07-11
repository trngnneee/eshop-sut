# TC-CHECKOUT-029: API từ chối total_amount âm

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- Giỏ hàng có sản phẩm

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| total_amount (client gửi) | -1 |

## Test steps
1. Đăng nhập; thêm sản phẩm vào giỏ; ghi nhận `cartTotal`.
2. Gửi yêu cầu checkout với `total_amount` = -1.
3. Ghi nhận phản hồi và đơn hàng (nếu có).

## Expected result
- Backend không chấp nhận `total_amount` âm.
- Đơn hàng lưu tổng đúng bằng `cartTotal`, hoặc API trả lỗi.

## Sub-domains covered
SD-T05 (total_amount âm — phân vùng không hợp lệ)

## Type
Invalid

## Status / Related bugs
Not Run / None

# TC-CHECKOUT-031: API từ chối total_amount không phải số

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
| total_amount (client gửi) | "abc" |

## Test steps
1. Đăng nhập; thêm sản phẩm vào giỏ.
2. Gửi yêu cầu checkout với `total_amount` = `"abc"` (chuỗi).
3. Ghi nhận phản hồi.

## Expected result
- API trả lỗi validation hoặc backend bỏ qua giá trị client và tự tính tổng đúng.
- Không lưu đơn với tổng tiền sai do chuỗi không hợp lệ.

## Sub-domains covered
SD-T07 (total_amount kiểu chuỗi — phân vùng không hợp lệ)

## Type
Invalid

## Status / Related bugs
Not Run / None

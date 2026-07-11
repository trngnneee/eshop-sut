# TC-CHECKOUT-030: API từ chối khi thiếu trường total_amount

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
| total_amount | [Không gửi trong body] |

## Test steps
1. Đăng nhập; thêm sản phẩm vào giỏ.
2. Gửi yêu cầu checkout **không** có trường `total_amount` trong body.
3. Ghi nhận phản hồi.

## Expected result
- Backend tự tính tổng từ giỏ hàng/sản phẩm, hoặc trả lỗi yêu cầu hợp lệ.
- Không lưu đơn với tổng tiền null/undefined nếu tạo đơn.

## Sub-domains covered
SD-T06 (total_amount thiếu/null)

## Type
Invalid

## Status / Related bugs
Not Run / None

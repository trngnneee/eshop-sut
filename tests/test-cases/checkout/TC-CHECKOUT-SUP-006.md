# TC-CHECKOUT-SUP-006: Backend tính tổng từ đơn giá × số lượng từng dòng

## Requirement ID
FR-08

## Module / Test type / Technique
Checkout / Functional / Domain Testing – Supplementary

## Preconditions
- Người dùng đã đăng nhập; có JWT hợp lệ
- Giỏ có ≥ 2 sản phẩm với đơn giá và số lượng đã biết

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| SP A | giá A × qty A |
| SP B | giá B × qty B |
| Tổng kỳ vọng | (giá A × qty A) + (giá B × qty B) |

## Test steps
1. Thêm 2 sản phẩm vào giỏ; tính tay `expectedTotal`.
2. Gửi checkout hợp lệ (hoặc đọc từ response đơn hàng).
3. So sánh `total_amount` lưu CSDL với `expectedTotal`.

## Expected result
- `total_amount` đơn hàng = Σ (price × quantity) của từng dòng trong giỏ.
- Xác nhận backend **tự tính lại** tổng, không chỉ echo giá trị client.

## Sub-domains covered
GAP-03 — server-side aggregation contract

## Type
Valid

## Status / Related bugs
Not Run / None

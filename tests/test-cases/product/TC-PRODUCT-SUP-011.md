# TC-PRODUCT-SUP-011: Giá hiển thị ký hiệu ₫ và phân cách hàng nghìn (FR-21)

## Requirement ID
FR-15, FR-21

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Supplementary

## Preconditions
- Admin đã đăng nhập
- Danh sách có ít nhất một sản phẩm với giá ≥ 1.000

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Trang | Quản lý Sản phẩm — danh sách |

## Test steps
1. Mở danh sách sản phẩm Admin.
2. Quan sát cột / vùng hiển thị Giá.

## Expected result
- Giá hiển thị ký hiệu `₫` (theo FR-21).
- Giá có định dạng phân cách hàng nghìn (ví dụ `199.000 ₫` hoặc `199,000 ₫`).

## Sub-domains covered
GAP-09 — FR-21 currency format

## Type
Valid

## Status / Related bugs
Fail / #15, #18, #19

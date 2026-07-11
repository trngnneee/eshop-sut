# TC-PRODUCT-SUP-005: Trường bắt buộc có ký hiệu * trên form Thêm (FR-22)

## Requirement ID
FR-15, FR-22

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Supplementary

## Preconditions
- Admin đã đăng nhập
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Form | Thêm sản phẩm |

## Test steps
1. Mở form Thêm sản phẩm.
2. Kiểm tra nhãn các trường Tên, Giá, Danh mục (hoặc nội dung form).

## Expected result
- Các trường bắt buộc (Tên, Giá, Danh mục) có ký hiệu `*` bên cạnh nhãn hoặc trong form (FR-22).

## Sub-domains covered
GAP-03 — FR-22 required field marker

## Type
Valid

## Status / Related bugs
Fail / #15, #18

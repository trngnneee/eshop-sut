# TC-PRODUCT-SUP-010: Sửa sản phẩm với Giá = 1 (biên hợp lệ) thành công

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis – Supplementary

## Boundary under test
Giá = 1 trên form Sửa — min on-point

## Preconditions
- Admin đã đăng nhập
- Có sản phẩm để sửa

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Giá mới | 1 |
| Tên | Giữ hợp lệ |

## Test steps
1. Mở form Sửa một sản phẩm.
2. Đổi Giá thành `1`; giữ Tên hợp lệ.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống chấp nhận Giá = 1 (> 0).
- Sản phẩm cập nhật thành công.

## Sub-domains covered
GAP-08 — Edit valid boundary (price min)

## Type
Valid

## Status / Related bugs
Fail / #15, #18

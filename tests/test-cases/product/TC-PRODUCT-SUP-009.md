# TC-PRODUCT-SUP-009: Sửa sản phẩm với Tên 255 ký tự (biên hợp lệ) thành công

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis – Supplementary

## Boundary under test
Tên 255 ký tự trên form Sửa — max on-point

## Preconditions
- Admin đã đăng nhập
- Có sản phẩm để sửa

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên mới | Chuỗi 255 ký tự `A` |
| Giá | Giữ hợp lệ |

## Test steps
1. Mở form Sửa một sản phẩm.
2. Đổi Tên thành chuỗi 255 ký tự; giữ Giá hợp lệ.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống chấp nhận cập nhật (cùng ràng buộc max 255 như form Thêm).
- Sản phẩm lưu tên mới thành công.

## Sub-domains covered
GAP-08 — Edit valid boundary (name max)

## Type
Valid

## Status / Related bugs
Fail / #15, #18

# TC-PRODUCT-SUP-008: Tên sản phẩm chỉ gồm khoảng trắng bị từ chối

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Supplementary

## Preconditions
- Admin đã đăng nhập
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | `   ` (chỉ khoảng trắng) |
| Giá | 100000 |
| Danh mục | Hợp lệ |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên chỉ gồm khoảng trắng; Giá và Danh mục hợp lệ.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm (coi như tên không hợp lệ / rỗng sau trim).
- Không có sản phẩm mới trong danh sách.

## Sub-domains covered
GAP-07 — whitespace-only name

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

# TC-PRODUCT-SUP-006: Thông báo lỗi hiển thị trên nút Submit (FR-22)

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
| Tên sản phẩm | [Để trống] |
| Giá | 100000 |

## Test steps
1. Mở form Thêm sản phẩm.
2. Để trống Tên; nhập Giá hợp lệ; chọn Danh mục.
3. Bấm Lưu / Xác nhận.
4. So sánh vị trí thông báo lỗi với nút Submit.

## Expected result
- Hệ thống hiển thị thông báo lỗi.
- Thông báo lỗi nằm **trên** nút Submit (theo FR-22), không chỉ bên dưới.

## Sub-domains covered
GAP-04 — FR-22 error position

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

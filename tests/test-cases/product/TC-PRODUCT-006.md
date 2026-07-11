# TC-PRODUCT-006: Kiểm thử Giá âm

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Sản phẩm giá âm |
| Giá | -50000 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá `-50000`, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm.
- Hiển thị thông báo lỗi (Giá phải dương).
- Không có sản phẩm mới được thêm vào danh sách.

## Sub-domains covered
SD-P02 (giá âm)

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

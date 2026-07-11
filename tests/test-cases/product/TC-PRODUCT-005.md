# TC-PRODUCT-005: Kiểm thử Giá bằng 0

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
| Tên sản phẩm | Sản phẩm giá zero |
| Giá | 0 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá `0`, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm (đặc tả: Giá phải là số dương > 0).
- Hiển thị thông báo lỗi phù hợp.
- Không có sản phẩm mới được thêm vào danh sách.

## Sub-domains covered
SD-P01 (giá = 0)

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

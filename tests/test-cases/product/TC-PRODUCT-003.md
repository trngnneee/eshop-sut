# TC-PRODUCT-003: Kiểm thử Tên sản phẩm để trống

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
| Tên sản phẩm | [Để trống] |
| Giá | 199000 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Để trống trường Tên sản phẩm.
3. Nhập Giá hợp lệ và chọn Danh mục.
4. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm.
- Hiển thị thông báo lỗi bắt buộc nhập Tên sản phẩm.
- Không có sản phẩm mới được thêm vào danh sách.

## Sub-domains covered
SD-N01 (tên rỗng)

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

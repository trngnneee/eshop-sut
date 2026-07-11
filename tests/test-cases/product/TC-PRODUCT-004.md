# TC-PRODUCT-004: Kiểm thử Giá để trống

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
| Tên sản phẩm | Quần jean nữ |
| Giá | [Để trống] |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ và chọn Danh mục.
3. Để trống trường Giá.
4. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm (Giá là trường bắt buộc).
- Hiển thị thông báo lỗi bắt buộc nhập Giá.
- Không có sản phẩm mới được thêm vào danh sách.

## Sub-domains covered
SD-P00 (giá rỗng)

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

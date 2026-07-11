# TC-PRODUCT-007: Kiểm thử Giá không phải số

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
| Tên sản phẩm | Sản phẩm giá chữ |
| Giá | mười nghìn |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá là chuỗi không phải số, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm.
- Hiển thị thông báo lỗi định dạng Giá không hợp lệ.
- Không có sản phẩm mới được thêm vào danh sách.

## Sub-domains covered
SD-P03 (giá không phải số)

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

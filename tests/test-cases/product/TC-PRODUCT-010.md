# TC-PRODUCT-010: Sửa một sản phẩm — các sản phẩm khác giữ nguyên

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Danh sách có ít nhất hai sản phẩm khác nhau (A và B)

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm sửa | Sản phẩm A |
| Tên mới (A) | Tên đã chỉnh sửa |
| Sản phẩm đối chiếu | Sản phẩm B (không thao tác) |

## Test steps
1. Ghi nhận đầy đủ Tên, Giá, Danh mục của sản phẩm A và sản phẩm B.
2. Sửa chỉ sản phẩm A: đổi Tên sang giá trị mới; bấm Lưu.
3. Tải lại danh sách sản phẩm.
4. Đối chiếu sản phẩm B với dữ liệu đã ghi nhận ở bước 1.

## Expected result
- Sản phẩm A phản ánh thay đổi vừa thực hiện.
- Sản phẩm B **giữ nguyên** Tên, Giá và Danh mục như trước khi sửa A.
- Tổng số sản phẩm trong danh sách không thay đổi (không thêm, không xóa).

## Sub-domains covered
SD-ISO01 (sửa độc lập — chỉ sản phẩm được chọn bị thay đổi)

## Type
Valid

## Status / Related bugs
Fail / #15, #18

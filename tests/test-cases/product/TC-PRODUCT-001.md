# TC-PRODUCT-001: Thêm sản phẩm thành công với toàn bộ dữ liệu hợp lệ (on-point)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Hệ thống có ít nhất một danh mục trong danh sách có sẵn

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Áo thun nam basic |
| Giá | 199000 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở chức năng Quản lý Sản phẩm (FR-15).
2. Chọn Thêm sản phẩm mới.
3. Nhập Tên, Giá và chọn Danh mục theo bảng Test data.
4. Bấm Lưu / Xác nhận.
5. Quay lại danh sách sản phẩm và tìm sản phẩm vừa tạo.

## Expected result
- Hệ thống chấp nhận dữ liệu và tạo sản phẩm thành công.
- Sản phẩm mới xuất hiện trong danh sách với đúng Tên và Giá đã nhập.
- Danh mục hiển thị khớp lựa chọn.

## Sub-domains covered
SD-N02 (tên hợp lệ), SD-P04 (giá dương), SD-C02 (danh mục từ danh sách có sẵn), SD-CR01 (Thêm — Create)

## Type
Valid

## Status / Related bugs
Fail / #15, #18

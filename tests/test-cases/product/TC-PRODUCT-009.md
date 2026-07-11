# TC-PRODUCT-009: Sửa sản phẩm thành công với dữ liệu hợp lệ

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Có ít nhất một sản phẩm trong danh sách

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm sửa | Một sản phẩm có sẵn trong danh sách |
| Tên mới | Áo khoác dù mùa đông |
| Giá mới | 450000 |
| Danh mục mới | Một danh mục hợp lệ khác (nếu có) hoặc giữ danh mục cũ |

## Test steps
1. Mở chức năng Quản lý Sản phẩm và ghi nhận Tên, Giá hiện tại của sản phẩm mục tiêu.
2. Chọn Sửa trên sản phẩm đó.
3. Cập nhật Tên và Giá theo bảng Test data; chọn Danh mục hợp lệ.
4. Bấm Lưu / Xác nhận.
5. Mở lại chi tiết hoặc dòng sản phẩm vừa sửa.

## Expected result
- Hệ thống chấp nhận dữ liệu và cập nhật thành công (chức năng Sửa — Update).
- Sản phẩm hiển thị Tên và Giá mới.
- Không tạo thêm bản ghi sản phẩm mới.

## Sub-domains covered
SD-N02 (tên hợp lệ), SD-P04 (giá dương), SD-C02 (danh mục hợp lệ), SD-UP01 (Sửa — Update)

## Type
Valid

## Status / Related bugs
Fail / #15, #18

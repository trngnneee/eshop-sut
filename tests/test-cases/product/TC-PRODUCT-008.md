# TC-PRODUCT-008: Kiểm thử không chọn Danh mục

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
| Tên sản phẩm | Sản phẩm không danh mục |
| Giá | 150000 |
| Danh mục | [Không chọn] |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên và Giá hợp lệ.
3. Không chọn Danh mục (để trạng thái trống / mặc định).
4. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm (đặc tả: Danh mục bắt buộc, phải chọn từ danh sách có sẵn).
- Hiển thị thông báo lỗi bắt buộc chọn Danh mục.
- Không có sản phẩm mới được thêm vào danh sách.

## Sub-domains covered
SD-C01 (không chọn danh mục)

## Type
Invalid

## Status / Related bugs
Fail / #15, #18

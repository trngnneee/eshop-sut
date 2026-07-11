# TC-PRODUCT-011: Xóa sản phẩm thành công

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Có ít nhất một sản phẩm có thể xóa trong danh sách

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Sản phẩm xóa | Một sản phẩm xác định trong danh sách (ghi nhận Tên trước khi xóa) |

## Test steps
1. Mở chức năng Quản lý Sản phẩm; ghi nhận Tên sản phẩm mục tiêu.
2. Chọn Xóa trên sản phẩm đó.
3. Xác nhận thao tác xóa nếu hệ thống yêu cầu.
4. Tải lại danh sách và tìm sản phẩm đã xóa.

## Expected result
- Hệ thống xóa sản phẩm thành công (chức năng Xóa — Delete).
- Sản phẩm không còn xuất hiện trong danh sách.
- Các sản phẩm khác vẫn hiển thị bình thường.

## Sub-domains covered
SD-DL01 (Xóa — Delete)

## Type
Valid

## Status / Related bugs
Fail / #15, #18

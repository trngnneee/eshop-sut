# TC-PRODUCT-020: Kiểm thử Tên sản phẩm với độ dài dưới tối thiểu (0 ký tự)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Tên sản phẩm tại min− — value: 0 ký tự (để trống)

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | [Để trống — 0 ký tự] |
| Giá | 100000 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Để trống trường Tên (0 ký tự); nhập Giá hợp lệ và chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm (tên bắt buộc, độ dài tối thiểu hiệu lực là 1 ký tự).
- Hiển thị thông báo lỗi bắt buộc nhập Tên.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #15, #18

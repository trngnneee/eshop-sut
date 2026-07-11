# TC-PRODUCT-021: Kiểm thử Tên sản phẩm với độ dài biên tối thiểu (1 ký tự)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Tên sản phẩm tại min — value: 1 ký tự (`X`)

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | X |
| Giá | 100000 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên có đúng 1 ký tự, Giá hợp lệ, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống chấp nhận tên 1 ký tự và không báo lỗi độ dài.
- Sản phẩm được tạo thành công.

## Valid / Invalid
Valid (về độ dài)

## Status / Related bugs
Fail / #15, #18

# TC-PRODUCT-023: Kiểm thử Tên sản phẩm với độ dài ngay dưới tối đa (254 ký tự)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Tên sản phẩm tại max− — value: 254 ký tự

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Chuỗi gồm 254 ký tự `A` |
| Giá | 100000 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên có đúng 254 ký tự, Giá hợp lệ, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống chấp nhận tên 254 ký tự và không báo lỗi độ dài.
- Sản phẩm được tạo thành công.

## Valid / Invalid
Valid (về độ dài)

## Status / Related bugs
Fail / #15, #18

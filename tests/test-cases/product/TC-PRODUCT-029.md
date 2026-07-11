# TC-PRODUCT-029: Kiểm thử Giá ngay trên biên tối thiểu hợp lệ (2)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Giá tại min+ — value: 2 (ngay trên min số nguyên dương)

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Sản phẩm giá hai đồng |
| Giá | 2 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá `2`, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống chấp nhận Giá `2` và không báo lỗi giá trị.
- Sản phẩm được tạo thành công.

## Valid / Invalid
Valid

## Status / Related bugs
Fail / #15, #18

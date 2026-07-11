# TC-PRODUCT-028: Kiểm thử Giá tại biên tối thiểu hợp lệ (1)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Giá tại min — value: 1 (số nguyên dương nhỏ nhất, > 0)

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Sản phẩm giá một đồng |
| Giá | 1 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá `1`, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống chấp nhận Giá `1` và không báo lỗi giá trị.
- Sản phẩm được tạo thành công với Giá = 1.

## Valid / Invalid
Valid

## Status / Related bugs
Fail / #15, #18

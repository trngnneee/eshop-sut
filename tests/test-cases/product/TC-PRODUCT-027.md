# TC-PRODUCT-027: Kiểm thử Giá ngay dưới ranh giới hợp lệ (−1)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Giá tại min− — value: −1 (ngay dưới ngưỡng dương)

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Sản phẩm giá âm biên |
| Giá | -1 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá `-1`, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm.
- Hiển thị thông báo lỗi (Giá phải dương).

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #15, #18

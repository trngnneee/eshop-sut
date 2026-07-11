# TC-PRODUCT-030: Kiểm thử Giá thập phân dương nhỏ nhất (0.01)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Giá tại min thập phân — value: 0.01 (> 0, số dương nhỏ nhất nếu hệ thống hỗ trợ thập phân)

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Sản phẩm giá thập phân |
| Giá | 0.01 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá `0.01`, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Theo FR-15 (Giá > 0), giá trị `0.01` thuộc phân vùng hợp lệ và **phải được chấp nhận**.
- Sản phẩm được tạo thành công với Giá = 0.01.

## Valid / Invalid
Valid

## Status / Related bugs
Fail / #15, #18

# TC-PRODUCT-026: Kiểm thử Giá tại biên không hợp lệ trên ranh giới (0)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Giá tại max của phân vùng không hợp lệ — value: 0 (không thỏa > 0)

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Sản phẩm giá zero |
| Giá | 0 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên hợp lệ, Giá `0`, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm (đặc tả FR-15: Giá phải > 0; `0` nằm ngay trên ranh giới không hợp lệ).
- Hiển thị thông báo lỗi phù hợp.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #15, #18

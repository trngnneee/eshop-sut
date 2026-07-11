# TC-PRODUCT-025: Kiểm thử Tên sản phẩm với độ dài vượt quá tối đa (256 ký tự)

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Tên sản phẩm tại max+ — value: 256 ký tự

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Form Thêm sản phẩm đang mở

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên sản phẩm | Chuỗi gồm 256 ký tự `A` |
| Giá | 100000 |
| Danh mục | Một danh mục hợp lệ từ dropdown |

## Test steps
1. Mở form Thêm sản phẩm.
2. Nhập Tên có đúng 256 ký tự, Giá hợp lệ, chọn Danh mục.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối tạo sản phẩm (vượt giới hạn tối đa 255 ký tự).
- Hiển thị thông báo lỗi độ dài Tên.
- Không có sản phẩm mới được thêm vào danh sách.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #15, #18

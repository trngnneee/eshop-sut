# TC-PRODUCT-031: Sửa sản phẩm với Tên 256 ký tự bị từ chối — Cross-boundary

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Tên sản phẩm tại max+ trên form Sửa — value: 256 ký tự

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Có ít nhất một sản phẩm trong danh sách

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên mới | Chuỗi gồm 256 ký tự `A` |
| Giá | Giữ nguyên giá hợp lệ hiện tại |
| Danh mục | Giữ nguyên hoặc chọn danh mục hợp lệ |

## Test steps
1. Mở form Sửa một sản phẩm có sẵn.
2. Thay Tên bằng chuỗi 256 ký tự; giữ các trường khác hợp lệ.
3. Bấm Lưu / Xác nhận.

## Expected result
- Hệ thống từ chối cập nhật (cùng ràng buộc max 255 ký tự như khi Thêm).
- Sản phẩm giữ nguyên Tên cũ trong danh sách.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #15, #18

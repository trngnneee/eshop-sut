# TC-PRODUCT-032: Sửa sản phẩm với Giá 0 bị từ chối — Cross-boundary

## Requirement ID
FR-15

## Module / Test type / Technique
Admin Product / Functional / Boundary Value Analysis

## Boundary under test
Giá tại max phân vùng không hợp lệ trên form Sửa — value: 0

## Preconditions
- Admin đã đăng nhập vào phân hệ Web Admin
- Có ít nhất một sản phẩm trong danh sách

## Test data
| Tham số | Giá trị thử nghiệm |
| :--- | :--- |
| Tên | Giữ nguyên tên hợp lệ hiện tại |
| Giá mới | 0 |
| Danh mục | Giữ nguyên hoặc chọn danh mục hợp lệ |

## Test steps
1. Mở form Sửa một sản phẩm có sẵn; ghi nhận Giá hiện tại.
2. Đổi Giá sang `0`.
3. Bấm Lưu / Xác nhận.
4. Kiểm tra Giá hiển thị trong danh sách.

## Expected result
- Hệ thống từ chối cập nhật (cùng ràng buộc Giá > 0 như khi Thêm).
- Sản phẩm giữ nguyên Giá cũ.

## Valid / Invalid
Invalid

## Status / Related bugs
Fail / #15, #18

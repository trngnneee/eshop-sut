# TC-DASHBOARD-DT-016: Kiểm tra dashboard xử lý khi API /api/admin/orders trả về mảng rỗng
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công.
- Database hoặc Mock API trả về danh sách orders rỗng (`[]`).
## Test data
- `orders = []`
## Test steps
1. Đăng nhập bằng tài khoản admin.
2. Mở giao diện Dashboard của Web Admin.
3. Quan sát các card số liệu thống kê.
## Expected result
- Giao diện Dashboard hiển thị bình thường mà không bị crash.
- Card 'Tổng số đơn hàng' hiển thị giá trị là `0`.
- Card 'Tổng doanh thu (Delivered)' hiển thị giá trị là `0 ₫`.
- Phần danh sách đơn hàng gần đây (recent orders) hiển thị trạng thái trống (empty state) hợp lý.
## Status / Related bugs
Pass / None

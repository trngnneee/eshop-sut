# TC-DASHBOARD-BVA-011: Kiểm tra recent orders list ở biên 0 item
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API trả về danh sách đơn hàng gần đây (recent orders) rỗng.
## Test data
- `recentOrders.length = 0`
## Test steps
1. Đăng nhập admin.
2. Mở giao diện Dashboard.
3. Quan sát phần hiển thị bảng đơn hàng gần đây (recent orders table).
## Expected result
- Giao diện Dashboard hiển thị bình thường, không crash.
- Bảng hiển thị thông báo trạng thái trống thân thiện như "No recent orders" hoặc "Không có đơn hàng nào gần đây".
## Status / Related bugs
Pass / None

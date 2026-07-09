# TC-DASHBOARD-BVA-012: Kiểm tra recent orders list ở biên 1 item
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Positive / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API trả về danh sách đơn hàng gần đây (recent orders) có duy nhất 1 đơn hàng.
## Test data
- `recentOrders.length = 1`
## Test steps
1. Đăng nhập admin.
2. Mở giao diện Dashboard.
3. Quan sát phần hiển thị bảng đơn hàng gần đây.
## Expected result
- Bảng hiển thị chính xác thông tin của duy nhất 1 đơn hàng đó.
- Layout không bị lệch, giao diện hiển thị gọn gàng.
## Status / Related bugs
Pass / None

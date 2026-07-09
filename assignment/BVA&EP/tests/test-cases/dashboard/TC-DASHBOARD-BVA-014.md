# TC-DASHBOARD-BVA-014: Kiểm tra recent orders list vượt giới hạn hiển thị 1 item
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Giao diện Dashboard được thiết lập giới hạn hiển thị `displayLimit` đơn hàng gần đây (ví dụ: 5 hoặc 10).
- Mock API trả về danh sách đơn hàng nhiều hơn `displayLimit` 1 đơn hàng.
## Test data
- `recentOrders.length = displayLimit + 1` (ví dụ: 6 hoặc 11 đơn hàng).
## Test steps
1. Mock API trả về danh sách có số lượng đơn hàng lớn hơn giới hạn hiển thị tối đa 1 đơn vị.
2. Đăng nhập admin và truy cập Dashboard.
3. Quan sát số lượng dòng hiển thị ở bảng recent orders.
## Expected result
- Dashboard chỉ hiển thị tối đa đúng `displayLimit` đơn hàng (đơn hàng mới nhất).
- Hoặc hệ thống phải có cơ chế phân trang (pagination) / cuộn (scroll) hợp lý.
- Giao diện bảng không bị tràn ra ngoài hoặc gây vỡ layout trang.
## Status / Related bugs
Pass / None

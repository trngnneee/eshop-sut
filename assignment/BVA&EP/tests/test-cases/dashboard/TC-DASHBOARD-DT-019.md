# TC-DASHBOARD-DT-019: Kiểm tra dashboard khi chỉ có order trạng thái cancelled
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công.
- Database chỉ có đơn hàng ở trạng thái `cancelled`, không có đơn hàng nào ở trạng thái `delivered`.
## Test data
- 1 order `cancelled` có `total_amount = 100,000 ₫`.
## Test steps
1. Mở giao diện Dashboard.
2. Kiểm tra chỉ số 'Tổng doanh thu'.
## Expected result
- 'Tổng doanh thu (Delivered)' phải bằng `0 ₫`.
- Đơn hàng bị hủy (`cancelled`) không được cộng vào tổng doanh thu của hệ thống.
## Status / Related bugs
Pass / None

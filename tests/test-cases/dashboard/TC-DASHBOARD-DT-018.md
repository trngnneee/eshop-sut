# TC-DASHBOARD-DT-018: Kiểm tra dashboard khi chỉ có order trạng thái pending
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công.
- Database chỉ có đơn hàng ở trạng thái `pending`, không có đơn hàng nào ở trạng thái `delivered`.
## Test data
- 1 order `pending` có `total_amount = 100,000 ₫`.
## Test steps
1. Mở giao diện Dashboard.
2. Kiểm tra các chỉ số 'Tổng số đơn hàng' và 'Tổng doanh thu'.
## Expected result
- 'Tổng số đơn hàng' tăng theo quy tắc của hệ thống (ví dụ: hiển thị `1`).
- 'Tổng doanh thu (Delivered)' bắt buộc phải hiển thị bằng `0 ₫` (vì doanh thu chỉ tính từ đơn hàng có trạng thái `delivered`).
## Status / Related bugs
Passed / None
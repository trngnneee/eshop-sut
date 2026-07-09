# TC-DASHBOARD-DT-023: Kiểm tra doanh thu không bị nhân đôi (regression test)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Regression / Equivalence Partitioning
## Preconditions
- Lỗi hiển thị doanh thu nhân đôi (BUG-FR13-C-01) đã được khắc phục trên hệ thống.
- Admin đã đăng nhập thành công.
- Database có 1 đơn hàng đã giao (`delivered`) với số tiền cụ thể.
## Test data
- 1 delivered order, `total_amount = 100,000 ₫`.
## Test steps
1. Mở giao diện Dashboard.
2. Kiểm tra phần hiển thị 'Tổng doanh thu (Delivered)'.
## Expected result
- Giao diện hiển thị đúng giá trị thực tế của đơn hàng là `100,000 ₫` hoặc `100000`, không được nhân đôi thành `200,000 ₫`.
## Status / Related bugs
Fail / BUG-FR13-C-01

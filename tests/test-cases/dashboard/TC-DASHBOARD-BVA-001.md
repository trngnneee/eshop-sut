# TC-DASHBOARD-BVA-001: Kiểm tra biên dưới của Tổng số đơn hàng bằng 0 (Min)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Database trống không có đơn hàng nào
## Test data
| Total Orders | 0 đơn hàng |
## Test steps
1. Tải trang Dashboard.
2. Kiểm tra số hiển thị ở Tổng số đơn hàng.
## Expected result
- Số đơn hàng hiển thị: 0
## Status / Related bugs
Passed / None

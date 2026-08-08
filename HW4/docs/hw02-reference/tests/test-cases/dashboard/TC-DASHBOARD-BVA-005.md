# TC-DASHBOARD-BVA-005: Kiểm tra biên dưới của Tổng doanh thu bằng 0 ₫ (Min)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Database có đơn hàng nhưng không có đơn nào delivered
## Test data
| Total Revenue | 0 ₫ |
## Test steps
1. Tải trang Dashboard.
2. Xem số liệu Tổng doanh thu.
## Expected result
- Tổng doanh thu hiển thị: 0 ₫
## Status / Related bugs
Passed / None

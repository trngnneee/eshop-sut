# TC-DASHBOARD-BVA-002: Kiểm tra biên dưới + 1 của Tổng số đơn hàng bằng 1 (Min + 1)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Database có đúng 1 đơn hàng
## Test data
| Total Orders | 1 đơn hàng |
## Test steps
1. Seed đúng 1 đơn hàng vào database.
2. Tải trang Dashboard.
3. Kiểm tra số đơn hàng hiển thị.
## Expected result
- Số đơn hàng hiển thị: 1
## Status / Related bugs
Pass / None

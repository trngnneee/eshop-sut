# TC-DASHBOARD-BVA-006: Kiểm tra biên dưới + 1 của Tổng doanh thu bằng 1 ₫ (Min + 1)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- DB có 1 đơn hàng duy nhất delivered với total_amount = 1
## Test data
| Total Revenue | 1 ₫ (1 đơn hàng delivered giá trị 1) |
## Test steps
1. Seed đơn hàng có giá trị 1 vào database.
2. Tải trang Dashboard.
3. Kiểm tra Tổng doanh thu hiển thị.
## Expected result
- Tổng doanh thu hiển thị chính xác: 1 ₫ (không nhân đôi).
## Status / Related bugs
Fail / BUG-FR13-C-01

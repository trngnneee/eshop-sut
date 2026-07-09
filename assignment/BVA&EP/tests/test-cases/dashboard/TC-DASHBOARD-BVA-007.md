# TC-DASHBOARD-BVA-007: Kiểm tra biên dưới - 1 của Tổng doanh thu bằng -1 ₫ (Min - 1)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Mock API trả về tổng doanh thu âm -1 ₫
## Test data
| Total Revenue | -1 ₫ |
## Test steps
1. Mock API trả về đơn hàng delivered có total_amount = -1.
2. Tải trang Dashboard.
3. Xem card Tổng doanh thu.
## Expected result
- Không hiển thị doanh thu âm -1 ₫ ra UI.
- Doanh thu hiển thị mặc định 0 ₫ hoặc báo lỗi dữ liệu.
## Status / Related bugs
Pass / None

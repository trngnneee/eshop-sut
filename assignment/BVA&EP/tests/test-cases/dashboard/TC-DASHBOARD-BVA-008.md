# TC-DASHBOARD-BVA-008: Kiểm tra biên trên của Tổng doanh thu với số cực lớn (999,999,999,999 ₫)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Mock API trả về tổng doanh thu cực lớn
## Test data
| Total Revenue | 999,999,999,999 ₫ |
## Test steps
1. Mock API trả về tổng doanh thu cực lớn.
2. Tải trang Dashboard.
3. Kiểm tra hiển thị card Tổng doanh thu.
## Expected result
- Số doanh thu hiển thị đúng định dạng: 999,999,999,999 ₫ (không vỡ khung card, không mất định dạng phân tách hàng nghìn).
## Status / Related bugs
Pass / None

# TC-DASHBOARD-BVA-004: Kiểm tra biên trên của Tổng số đơn hàng với số lượng lớn (100,000 đơn hàng)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Mock API trả về mảng chứa 100,000 đơn hàng
## Test data
| Total Orders | 100,000 đơn hàng |
## Test steps
1. Thiết lập mock API trả về mảng 100,000 đơn hàng.
2. Tải trang Dashboard.
3. Kiểm tra card Tổng số đơn hàng.
## Expected result
- Số đơn hàng hiển thị: 100,000.
- Giao diện hiển thị bình thường, không vỡ card hay mất số.
## Status / Related bugs
Passed / None

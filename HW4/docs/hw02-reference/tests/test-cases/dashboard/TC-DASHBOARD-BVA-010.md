# TC-DASHBOARD-BVA-010: Kiểm tra biên trên của API Response Time (5100ms - Quá biên timeout)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Mock delay API GET /api/admin/orders trong 5100ms
## Test data
| API Delay | 5100ms (timeout threshold = 5000ms) |
## Test steps
1. Thiết lập mock delay API là 5100ms.
2. Tải trang Dashboard.
3. Quan sát giao diện.
## Expected result
- Hiển thị Loading state trong 5 giây.
- Sau 5 giây, hệ thống kích hoạt timeout, hiển thị thông báo lỗi kết nối thân thiện.
## Status / Related bugs
Passed / None

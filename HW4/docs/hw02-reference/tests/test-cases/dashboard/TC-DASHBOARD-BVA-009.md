# TC-DASHBOARD-BVA-009: Kiểm tra biên dưới của API Response Time (4900ms - Cận dưới timeout)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Mock delay API GET /api/admin/orders trong 4900ms
## Test data
| API Delay | 4900ms (timeout threshold = 5000ms) |
## Test steps
1. Thiết lập mock delay API là 4900ms.
2. Tải trang Dashboard.
3. Theo dõi loading state và kết quả.
## Expected result
- Hiển thị trạng thái Loading trong khoảng 4.9 giây.
- Sau đó load thành công giao diện Dashboard và hiển thị dữ liệu bình thường.
## Status / Related bugs
Passed / None

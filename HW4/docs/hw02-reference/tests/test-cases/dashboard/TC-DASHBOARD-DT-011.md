# TC-DASHBOARD-DT-011: Xử lý dữ liệu khi API trả về sai định dạng JSON (Object thay vì Array)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Robustness / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công
- Mock API trả về JSON Object thay vì JSON Array đơn hàng
## Test data
| API response | { "status": "error", "message": "server error" } |
## Test steps
1. Thiết lập mock API trả về object thay vì array.
2. Truy cập Dashboard.
3. Quan sát giao diện.
## Expected result
- Hệ thống bắt exception thành công, không crash script toàn trang Admin.
- Hiển thị thông báo lỗi hoặc fallback UI thích hợp.
## Status / Related bugs
Passed / None

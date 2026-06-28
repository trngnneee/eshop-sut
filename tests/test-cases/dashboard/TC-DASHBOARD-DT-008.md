# TC-DASHBOARD-DT-008: Xử lý lỗi thân thiện khi API GET /api/admin/orders gặp sự cố lỗi Server (HTTP 500)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Robustness / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công
- Server API giả lập lỗi 500 khi gọi endpoint /api/admin/orders
## Test data
| Endpoint | /api/admin/orders |
| API Status | HTTP 500 Internal Server Error |
## Test steps
1. Chặn hoặc mock API trả về lỗi 500 đối với request GET /api/admin/orders.
2. Tải trang Dashboard.
3. Quan sát giao diện UI.
## Expected result
- Giao diện trang Admin không bị crash trắng trang.
- Hiển thị thông báo lỗi thân thiện trên UI (ví dụ: 'Không thể tải dữ liệu thống kê' hoặc thông báo tương tự).
- Fallback hiển thị an toàn.
## Status / Related bugs
Passed / None

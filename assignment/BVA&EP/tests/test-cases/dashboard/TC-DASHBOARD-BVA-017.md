# TC-DASHBOARD-BVA-017: Kiểm tra API response đúng ngưỡng timeout
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Có thể trì hoãn (delay) API response của dashboard đúng bằng ngưỡng timeout quy định (ví dụ: 5000ms).
## Test data
- API delay đúng `5000ms` (ngưỡng timeout threshold).
## Test steps
1. Cấu hình Mock server hoặc mạng để làm chậm API response đúng `5000ms`.
2. Đăng nhập admin và truy cập Dashboard.
## Expected result
- Hệ thống hiển thị biểu tượng loading trong lúc chờ dữ liệu.
- Hệ thống xử lý theo đúng quy tắc timeout (ví dụ: ngắt request và hiển thị thông báo lỗi quá hạn kết nối hoặc hiển thị dữ liệu bình thường nếu request kịp hoàn tất ở giây thứ 5), không được treo trang vĩnh viễn.
## Status / Related bugs
Pass / None

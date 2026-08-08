# TC-DASHBOARD-DT-002: Chặn truy cập Dashboard đối với người dùng chưa đăng nhập (Guest)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Security / Equivalence Partitioning
## Preconditions
- Người dùng chưa đăng nhập (không có token lưu trong localStorage/cookie)
## Test data
| Authorization Header | Trống |
## Test steps
1. Mở trình duyệt ở chế độ ẩn danh.
2. Truy cập trực tiếp đường dẫn trang Web Admin (http://localhost:5174).
3. Quan sát phản hồi và giao diện hiển thị.
## Expected result
- Giao diện Dashboard không được load.
- Trình duyệt tự động chuyển hướng người dùng về trang Đăng nhập (/login) hoặc hiển thị thông báo lỗi 401 Unauthorized.
## Status / Related bugs
Passed / None

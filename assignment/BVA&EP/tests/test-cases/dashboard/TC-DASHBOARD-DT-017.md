# TC-DASHBOARD-DT-017: Kiểm tra dashboard xử lý khi API /api/admin/users trả về lỗi 500
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API hoặc server trả về lỗi `500 Internal Server Error` đối với API `/api/admin/users`.
## Test data
- API `/api/admin/users` trả về mã lỗi HTTP 500.
## Test steps
1. Đăng nhập bằng tài khoản admin.
2. Mở giao diện Dashboard.
3. Quan sát phần hiển thị số lượng người dùng (users card).
## Expected result
- Giao diện Dashboard hiển thị thông báo lỗi hoặc fallback UI cho phần users (ví dụ: hiển thị "N/A" hoặc "Lỗi tải dữ liệu"), không hiển thị trắng trang.
- Các phần thông tin khác (doanh thu, đơn hàng, sản phẩm) vẫn hiển thị bình thường nếu các API tương ứng trả dữ liệu thành công.
## Status / Related bugs
Fail / BUG-FR13-C-03

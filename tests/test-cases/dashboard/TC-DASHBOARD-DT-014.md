# TC-DASHBOARD-DT-014: Kiểm tra user customer không được gọi API /api/admin/orders bằng token hợp lệ
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Security / Equivalence Partitioning
## Preconditions
- Backend đang chạy.
- Có tài khoản customer hợp lệ tồn tại trong hệ thống.
## Test data
- Customer account token hợp lệ.
## Test steps
1. Đăng nhập hệ thống bằng tài khoản customer.
2. Sao chép access token (JWT token) nhận được từ client.
3. Gửi request `GET /api/admin/orders` kèm theo token customer trên header `Authorization`.
## Expected result
- API phải trả về mã lỗi `403 Forbidden` hoặc thông báo lỗi không có quyền admin.
- Không được trả về thông tin danh sách orders.
## Status / Related bugs
Failed / BUG-FR13-C-02
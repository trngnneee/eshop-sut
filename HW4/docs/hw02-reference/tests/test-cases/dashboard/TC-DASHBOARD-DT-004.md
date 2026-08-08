# TC-DASHBOARD-DT-004: Kiểm tra phân quyền API backend khi gọi GET /api/admin/orders bằng token Customer
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Security / API / Equivalence Partitioning
## Preconditions
- Tài khoản khách hàng thường đã đăng nhập thành công ở frontend web và lấy được token JWT
## Test data
| Request Method | GET |
| Endpoint | /api/admin/orders |
| Authorization Header | Bearer <customer_jwt_token> |
## Test steps
1. Sử dụng công cụ API test (như Postman hoặc cURL) tạo request GET gửi đến http://localhost:3000/api/admin/orders.
2. Đính kèm token JWT của khách hàng thường vào Header Authorization.
3. Gửi request và quan sát HTTP Status Code cũng như Response Body.
## Expected result
- Server từ chối xử lý yêu cầu.
- Trả về mã trạng thái HTTP 403 Forbidden (hoặc 401 Unauthorized).
- Response body chứa thông báo lỗi phân quyền, không chứa danh sách đơn hàng.
## Status / Related bugs
Failed / BUG-FR13-C-02

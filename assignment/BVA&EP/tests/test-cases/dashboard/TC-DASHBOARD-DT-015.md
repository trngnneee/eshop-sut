# TC-DASHBOARD-DT-015: Kiểm tra token bị chỉnh sửa role từ customer thành admin không được truy cập dashboard API
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Security / Equivalence Partitioning
## Preconditions
- Có customer token hợp lệ.
- Có thể chỉnh sửa payload token (ví dụ: qua jwt.io hoặc tool trung gian) nhưng signature không hợp lệ (JWT signature key không đổi).
## Test data
- Token bị chỉnh sửa role thành `admin` nhưng signature không hợp lệ.
## Test steps
1. Lấy customer token hợp lệ từ hệ thống.
2. Chỉnh sửa phần payload của token để đổi thuộc tính `role` thành `admin` mà không ký lại token bằng signature key hợp lệ.
3. Gửi request đến `/api/admin/orders` kèm theo token đã sửa đổi.
## Expected result
- API phải từ chối token sai signature.
- Trả về mã lỗi `401 Unauthorized` hoặc `403 Forbidden`.
## Status / Related bugs
Pass / None

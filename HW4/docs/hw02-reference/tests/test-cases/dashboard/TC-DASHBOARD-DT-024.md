# TC-DASHBOARD-DT-024: Kiểm tra backend admin APIs đã kiểm tra role sau khi fix BUG-FR13-C-02
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Regression / Equivalence Partitioning
## Preconditions
- Lỗi thiếu kiểm soát phân quyền (BUG-FR13-C-02) đã được vá ở Backend API.
- Có tài khoản customer hợp lệ.
## Test data
- Customer token hợp lệ.
## Test steps
1. Sử dụng customer token hợp lệ để gọi API `/api/admin/users`.
2. Sử dụng customer token hợp lệ để gọi API `/api/admin/orders`.
## Expected result
- Cả hai endpoint API trên đều phải chặn request và trả về mã lỗi HTTP `403 Forbidden`.
- Tuyệt đối không trả về thông tin nhạy cảm của admin cho tài khoản customer.
## Status / Related bugs
Failed / BUG-FR13-C-02
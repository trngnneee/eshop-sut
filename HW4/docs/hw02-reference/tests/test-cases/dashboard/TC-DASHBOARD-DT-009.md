# TC-DASHBOARD-DT-009: Xử lý dữ liệu khi đơn hàng có total_amount mang số tiền âm
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Robustness / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công
- Mock API trả về 1 đơn hàng delivered có total_amount là số âm (-50,000 ₫)
## Test data
| Mock Order | status = 'delivered', total_amount = -50,000 ₫ |
## Test steps
1. Thiết lập mock API /api/admin/orders trả về đơn hàng lỗi giá trị âm.
2. Truy cập tab Dashboard.
3. Kiểm tra số liệu hiển thị.
## Expected result
- Hệ thống xử lý an toàn (ví dụ: bỏ qua đơn hàng âm không cộng vào doanh thu hoặc báo lỗi dữ liệu).
- Tuyệt đối không hiển thị doanh thu âm hoặc chữ số âm trên UI.
## Status / Related bugs
Passed / None

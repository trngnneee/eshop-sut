# TC-DASHBOARD-DT-010: Xử lý dữ liệu khi đơn hàng có total_amount là null, undefined hoặc NaN
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Robustness / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công
- Mock API trả về đơn hàng delivered có total_amount = null hoặc NaN
## Test data
| Mock Order | status = 'delivered', total_amount = null |
## Test steps
1. Thiết lập mock API trả về đơn hàng lỗi định dạng số tiền.
2. Truy cập Dashboard.
3. Quan sát giá trị Tổng doanh thu hiển thị.
## Expected result
- Không hiển thị chữ 'NaN', 'null', hay 'undefined ₫' trên giao diện.
- Tổng doanh thu hiển thị an toàn ở dạng mặc định (0 ₫) hoặc thông báo lỗi phù hợp.
## Status / Related bugs
Passed / None

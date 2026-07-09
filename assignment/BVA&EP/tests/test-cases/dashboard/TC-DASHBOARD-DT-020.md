# TC-DASHBOARD-DT-020: Kiểm tra dashboard khi order thiếu field total_amount
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Equivalence Partitioning
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API orders trả về một object đơn hàng bị thiếu thuộc tính `total_amount`.
## Test data
- Order object không chứa trường `total_amount`.
## Test steps
1. Thiết lập Mock API orders để phản hồi dữ liệu order bị thiếu thuộc tính `total_amount`.
2. Đăng nhập admin và mở giao diện Dashboard.
## Expected result
- Giao diện Dashboard hiển thị bình thường mà không bị crash.
- Doanh thu không hiển thị dạng lỗi chữ `NaN`, `undefined` hoặc lỗi giao diện tương tự.
- Hệ thống nên bỏ qua order bị lỗi hoặc hiển thị fallback (coi như giá trị bằng 0).
## Status / Related bugs
Fail / BUG-FR13-C-04

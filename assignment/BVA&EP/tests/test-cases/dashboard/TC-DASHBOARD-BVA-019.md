# TC-DASHBOARD-BVA-019: Kiểm tra total products bằng decimal
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API summary trả về số lượng sản phẩm là số thập phân.
## Test data
- `totalProducts = 10.5`
## Test steps
1. Mock API trả về `totalProducts = 10.5`.
2. Mở giao diện Dashboard.
3. Quan sát card số lượng sản phẩm (products card).
## Expected result
- Dashboard không hiển thị số thập phân đối với số lượng sản phẩm.
- Số lượng sản phẩm phải được làm tròn theo quy tắc hệ thống (ví dụ: làm tròn thành 11 hoặc 10) hoặc báo lỗi dữ liệu không hợp lệ.
## Status / Related bugs
Fail / BUG-FR13-C-05

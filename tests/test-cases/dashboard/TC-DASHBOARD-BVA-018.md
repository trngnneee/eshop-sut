# TC-DASHBOARD-BVA-018: Kiểm tra total users bằng giá trị âm
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API summary trả về số lượng người dùng là số âm.
## Test data
- `totalUsers = -1`
## Test steps
1. Mock API trả về `totalUsers = -1`.
2. Mở giao diện Dashboard.
3. Quan sát card số lượng người dùng (users card).
## Expected result
- Giao diện Dashboard không được hiển thị số người dùng âm.
- Hệ thống cần fallback về giá trị hiển thị `0` hoặc hiển thị lỗi dữ liệu không hợp lệ.
## Status / Related bugs
Failed / BUG-FR13-C-05
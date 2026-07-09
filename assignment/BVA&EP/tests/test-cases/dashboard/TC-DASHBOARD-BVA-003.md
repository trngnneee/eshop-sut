# TC-DASHBOARD-BVA-003: Kiểm tra biên dưới - 1 của Tổng số đơn hàng bằng -1 (Min - 1)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công
- Mock API trả về số lượng đơn hàng âm -1
## Test data
| Total Orders | -1 đơn hàng (giả lập lỗi API) |
## Test steps
1. Mock API trả về danh sách đơn hàng có kích thước bất thường âm.
2. Tải trang Dashboard.
3. Quan sát UI hiển thị.
## Expected result
- Không hiển thị số âm -1 ra UI.
- Hiển thị 0 hoặc báo lỗi dữ liệu.
## Status / Related bugs
Pass / None

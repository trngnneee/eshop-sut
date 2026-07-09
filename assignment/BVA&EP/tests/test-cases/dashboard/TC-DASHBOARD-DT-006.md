# TC-DASHBOARD-DT-006: Hiển thị Dashboard khi hệ thống chưa có đơn hàng nào (Database rỗng)
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Positive / Equivalence Partitioning
## Preconditions
- Database rỗng không có bất kỳ đơn hàng nào
- Admin đã đăng nhập thành công và ở tab Dashboard
## Test data
| Orders in DB | 0 đơn hàng |
## Test steps
1. Truy cập tab Dashboard.
2. Kiểm tra các số liệu hiển thị.
## Expected result
- Hệ thống hoạt động bình thường, không crash.
- Card 'Tổng số đơn hàng' hiển thị giá trị là 0.
- Card 'Tổng doanh thu (Delivered)' hiển thị giá trị là 0 ₫.
## Status / Related bugs
Pass / None

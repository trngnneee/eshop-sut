# TC-DASHBOARD-DT-007: Hiển thị Dashboard khi có đơn hàng nhưng không có đơn nào ở trạng thái 'delivered'
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Positive / Equivalence Partitioning
## Preconditions
- Database có các đơn hàng nhưng tất cả đều ở trạng thái pending, confirmed, shipping hoặc canceled (không có delivered)
- Admin đã đăng nhập và truy cập Dashboard
## Test data
| Orders in DB | 4 đơn hàng (2 pending, 1 confirmed, 1 canceled) |
## Test steps
1. Truy cập tab Dashboard.
2. Quan sát các thông số hiển thị.
## Expected result
- Giao diện Dashboard hiển thị thành công.
- Card 'Tổng số đơn hàng' hiển thị giá trị là 4.
- Card 'Tổng doanh thu (Delivered)' hiển thị giá trị là 0 ₫.
## Status / Related bugs
Passed / None

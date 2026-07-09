# TC-DASHBOARD-DT-001: Hiển thị Dashboard thành công khi có đơn hàng mẫu hợp lệ
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Positive / Equivalence Partitioning
## Preconditions
- Tài khoản admin hợp lệ tồn tại trong hệ thống (admin@eshop.com / Admin123!)
- Admin đã đăng nhập thành công và token được lưu trữ tại client
- Database có dữ liệu mẫu: 1 đơn pending 100k, 2 đơn delivered mỗi đơn 200k
## Test data
| Admin account | admin@eshop.com / Admin123! |
| Orders in DB | 1 pending (100,000 ₫), 2 delivered (200,000 ₫ mỗi đơn) |
## Test steps
1. Truy cập vào trang Web Admin (http://localhost:5174).
2. Đăng nhập bằng tài khoản admin hợp lệ.
3. Nhấn vào tab Dashboard trên thanh menu điều hướng.
4. Quan sát số liệu hiển thị trên giao diện.
## Expected result
- Giao diện Dashboard hiển thị thành công.
- Card 'Tổng số đơn hàng' hiển thị giá trị là 3.
- Card 'Tổng doanh thu (Delivered)' hiển thị giá trị là 400,000 ₫ (200k + 200k = 400k, không tính đơn pending).
## Status / Related bugs
Fail / BUG-FR13-C-01

# TC-DASHBOARD-BVA-015: Kiểm tra total revenue với giá trị rất lớn không làm vỡ layout
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Có đơn hàng mẫu đã giao với giá trị doanh thu cực lớn (ví dụ: hàng trăm tỷ đồng) để kiểm tra khả năng đáp ứng của giao diện Admin.
## Test data
- `total_amount = 999,999,999,999` (hoặc `999999999999999`).
## Test steps
1. Seed hoặc mock dữ liệu đơn hàng đã giao (`delivered`) có giá trị doanh thu rất lớn.
2. Mở Dashboard và kiểm tra card hiển thị doanh thu.
## Expected result
- Doanh thu được format đúng định dạng tiền tệ (ví dụ: hiển thị dấu phân cách hàng nghìn).
- Chuỗi ký tự doanh thu hiển thị đầy đủ, không bị tràn ra ngoài viền card, không bị che mất chữ, không bị xuống dòng lỗi hoặc làm ảnh hưởng layout của các card kế bên.
## Status / Related bugs
Passed / None
# TC-DASHBOARD-BVA-016: Kiểm tra total revenue khi vượt giới hạn Number an toàn
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Negative / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Mock API orders trả về tổng doanh thu cực lớn vượt quá giới hạn an toàn của kiểu dữ liệu số trong Javascript (`Number.MAX_SAFE_INTEGER`).
## Test data
- `total_amount > Number.MAX_SAFE_INTEGER` (vượt quá `9,007,199,254,740,991`).
## Test steps
1. Thiết lập Mock API trả về doanh thu lớn hơn `Number.MAX_SAFE_INTEGER`.
2. Truy cập Dashboard và quan sát số liệu doanh thu.
## Expected result
- Hệ thống xử lý an toàn: không crash ứng dụng, không hiển thị sai lệch số liệu một cách nghiêm trọng hoặc có cơ chế hiển thị fallback (ví dụ: dùng BigInt hoặc chuỗi string để định dạng).
## Status / Related bugs
Passed / None
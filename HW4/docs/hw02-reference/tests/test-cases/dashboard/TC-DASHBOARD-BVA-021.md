# TC-DASHBOARD-BVA-021: Kiểm tra responsive dưới breakpoint tablet 1px
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Sử dụng công cụ DevTools trên trình duyệt để kiểm tra giao diện responsive.
## Test data
- Chiều rộng màn hình (Viewport Width) = `767px` (breakpoint - 1px).
## Test steps
1. Mở giao diện Dashboard.
2. Bật công cụ F12 (DevTools) và chọn chế độ Responsive.
3. Thiết lập chiều rộng viewport bằng đúng `767px`.
4. Quan sát các card số liệu, bảng biểu và thanh menu điều hướng.
## Expected result
- Giao diện chuyển đổi một cách chính xác sang trạng thái layout dành cho Mobile (ví dụ: sidebar tự thu gọn thành menu hamburger, các card hiển thị dạng dọc xếp chồng).
- Layout không bị vỡ hoặc lỗi hiển thị.
## Status / Related bugs
Passed / None
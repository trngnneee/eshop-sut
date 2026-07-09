# TC-DASHBOARD-BVA-020: Kiểm tra responsive tại đúng breakpoint tablet
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Sử dụng công cụ DevTools trên trình duyệt để kiểm tra giao diện responsive.
## Test data
- Chiều rộng màn hình (Viewport Width) = `768px` (đúng điểm breakpoint của tablet).
## Test steps
1. Mở giao diện Dashboard.
2. Bật công cụ F12 (DevTools) và chọn chế độ Responsive.
3. Thiết lập chiều rộng viewport bằng đúng `768px`.
4. Quan sát các card số liệu, bảng biểu và thanh menu điều hướng.
## Expected result
- Giao diện không bị chồng lấn, vỡ hoặc mất chữ.
- Sidebar, header, các bảng và card số liệu tự động co giãn và hoạt động bình thường, hiển thị đúng layout cho breakpoint này.
## Status / Related bugs
Pass / None

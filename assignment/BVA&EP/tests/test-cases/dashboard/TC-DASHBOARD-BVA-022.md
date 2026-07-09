# TC-DASHBOARD-BVA-022: Kiểm tra responsive trên breakpoint tablet 1px
## Requirement ID
FR-13
## Module / Test type / Technique
Dashboard / Functional / Edge Case / Boundary Value Analysis
## Preconditions
- Admin đã đăng nhập thành công.
- Sử dụng công cụ DevTools trên trình duyệt để kiểm tra giao diện responsive.
## Test data
- Chiều rộng màn hình (Viewport Width) = `769px` (breakpoint + 1px).
## Test steps
1. Mở giao diện Dashboard.
2. Bật công cụ F12 (DevTools) và chọn chế độ Responsive.
3. Thiết lập chiều rộng viewport bằng đúng `769px`.
4. Quan sát layout hiển thị.
## Expected result
- Giao diện hiển thị đúng layout cho Tablet / Desktop nhỏ.
- Không chuyển đổi nhầm sang giao diện Mobile.
- Các thành phần co giãn tốt và không bị chồng lấn.
## Status / Related bugs
Pass / None

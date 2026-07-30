# [BUG-GUI-03] Admin Login Accessibility Defect & Browser Native Alert Popup Use

**Platform:** Web Admin  
**Screen/Route:** / (Unauthenticated State)  
**Related Requirement:** FR-12 (Access Control)  
**Severity:** Medium | **Priority:** Medium  
**Status:** PENDING_EXTERNAL_ACTION  

## Description & Steps to Reproduce
1. Truy cập http://localhost:5174/
2. Kiểm tra mã HTML của các ô input email và password.
3. Nhập email/mật khẩu sai và bấm 'Login'.

## Expected Result
- Các ô input có thẻ <label> đi kèm cho accessibility.
- Báo lỗi đăng nhập hiển thị dạng banner màu đỏ inline bên trong form.

## Actual Result
- Thiếu hoàn toàn thẻ <label> (chỉ dùng placeholder).
- Khi đăng nhập sai hoặc không có quyền Admin, SUT bật cửa sổ popup alert() native của trình duyệt gây ngắt đoạn trải nghiệm.

## Evidence Screenshot
![Screenshot](../../evidence/admin-login/BUG-GUI-03_admin-login.png)

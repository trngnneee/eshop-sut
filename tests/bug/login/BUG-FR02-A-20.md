# BUG-FR02-A-20: Tính năng Remember Me (Duy trì đăng nhập) chưa được triển khai ở cả Frontend và Backend

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 20 |
| **BugID** | `BUG-FR02-A-20` |
| **Status** | **Open** |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Tính năng Remember Me chưa được phát triển. Giao diện Login.jsx thiếu hộp chọn (checkbox) Remember Me, đồng thời Backend API không hỗ trợ cơ chế lưu trữ phiên lâu dài (ví dụ Cookie có cờ HttpOnly/Secure/SameSite) để duy trì trạng thái đăng nhập sau khi đóng trình duyệt. |
| **Steps to reproduce** | 1. Mở trang Đăng nhập.<br>2. Giao diện không có checkbox 'Remember me'.<br>3. Kiểm tra mã nguồn backend/server.js tại API `/api/login`, không có logic xử lý tham số rememberMe hay thiết lập Cookie bảo mật. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | Medium |
| **Attachment (Link to file)** | [Login.jsx](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/frontend-web/src/pages/Login.jsx) |
| **Date** | 2026-06-26 |
| **Reporter** | AI Tester (Antigravity) |

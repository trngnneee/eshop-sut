# BUG-FR02-A-01: Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 01 |
| **BugID** | `BUG-FR02-A-01` |
| **Status** | **Open** |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Ở `backend/server.js`, mỗi lần người dùng đăng nhập sai mật khẩu, hệ thống tăng bộ đếm thêm `2` đơn vị thay vì `1` đơn vị như đặc tả. |
| **Steps to reproduce** | 1. Đăng ký tài khoản mới.<br>2. Gửi 1 yêu cầu POST đăng nhập sai tới `/api/login` với tài khoản vừa tạo.<br>3. Truy vấn Database bảng `users` để kiểm tra trường `login_attempts`. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js#L57) |
| **Evidence (Screenshot)** | ![Screenshot](../evidence/BUG-FR02-A-01_screenshot.png) |
| **Date** | 2026-06-23 |
| **Reporter** | AI Tester (Antigravity) |

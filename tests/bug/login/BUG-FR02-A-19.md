# BUG-FR02-A-19: Đặt lại mật khẩu thành công không giải phóng trạng thái khóa tài khoản và không reset bộ đếm lần đăng nhập sai

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 19 |
| **BugID** | `BUG-FR02-A-19` |
| **Status** | **Open** |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Khi người dùng thực hiện đặt lại mật khẩu thành công bằng API `/api/reset-password`, hệ thống chỉ cập nhật trường `password` và `reset_token = NULL`, nhưng quên không reset trường `login_attempts` về `0` và `locked_until` về `NULL` trong CSDL. Điều này khiến tài khoản vẫn giữ nguyên trạng thái bị khóa ngay cả khi người dùng đã cập nhật xong mật khẩu mới, bắt buộc người dùng phải đợi hết thời gian khóa mới đăng nhập được. |
| **Steps to reproduce** | 1. Nhập mật khẩu sai 3 lần liên tiếp để khóa tài khoản `test_tc31@eshop.com`.<br>2. Gọi API `/api/forgot-password` để lấy reset token.<br>3. Gọi API `/api/reset-password` bằng reset token để cập nhật mật khẩu mới.<br>4. Thử đăng nhập ngay bằng mật khẩu mới.<br>5. Đăng nhập vẫn bị chặn bằng HTTP 403 do trường `locked_until` vẫn tồn tại giá trị trong DB. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js#L89) |
| **Date** | 2026-06-26 |
| **Reporter** | AI Tester (Antigravity) |

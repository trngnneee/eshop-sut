# BUG-FR02-A-03: Race condition do xử lý yêu cầu đăng nhập bất đồng bộ

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 03 |
| **BugID** | `BUG-FR02-A-03` |
| **Status** | **Open** |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Backend trả về phản hồi HTTP ngay lập tức mà không đợi giao dịch xử lý yêu cầu đăng nhập hoàn thành, dẫn đến việc đọc dữ liệu kế tiếp bị sai lệch. |
| **Steps to reproduce** | 1. Gửi request đăng nhập sai mật khẩu.<br>2. Thực hiện nhanh yêu cầu đăng nhập tiếp theo trước khi hệ thống kịp ghi nhận trạng thái.<br>3. Kiểm tra xem tài khoản có thể vượt quá số lần đăng nhập sai quy định mà không bị khóa ngay lập tức hay không. |
| **Severity** | Major |
| **Frequency** | Intermittent |
| **Priority** | High |
| **Evidence (Screenshot)** | ![Screenshot](../evidence/BUG-FR02-A-03_screenshot.png) |
| **Date** | 2026-06-23 |
| **Reporter** | Khoa |

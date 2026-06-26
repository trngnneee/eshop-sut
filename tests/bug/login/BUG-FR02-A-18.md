# BUG-FR02-A-18: Hệ thống phân biệt chữ hoa/chữ thường (case-sensitive) đối với Email đăng nhập

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 18 |
| **BugID** | `BUG-FR02-A-18` |
| **Status** | **Open** |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | SQLite thực hiện so khớp trường bằng toán tử `=` phân biệt chữ hoa chữ thường đối với ASCII theo mặc định. Khi đăng ký email bằng chữ thường `test_tc29@eshop.com`, nếu người dùng đăng nhập bằng email viết hoa/thường xen kẽ `TeSt_tC29@eShOp.CoM` và mật khẩu đúng, hệ thống so khớp trực tiếp dẫn đến không tìm thấy user và trả về lỗi HTTP 401. Lỗi này cũng làm vô hiệu hóa cơ chế khóa tài khoản khi hacker brute-force bằng các casing khác nhau của email. |
| **Steps to reproduce** | 1. Đăng ký tài khoản `test_tc29@eshop.com` bằng chữ thường.<br>2. Gửi yêu cầu đăng nhập POST tới `/api/login` với email `TeSt_tC29@eShOp.CoM` và mật khẩu đúng.<br>3. Kết quả trả về HTTP 401 thay vì đăng nhập thành công. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js#L35) |
| **Evidence (Screenshot)** | ![Screenshot](../evidence/BUG-FR02-A-18_screenshot.png) |
| **Date** | 2026-06-26 |
| **Reporter** | AI Tester (Antigravity) |

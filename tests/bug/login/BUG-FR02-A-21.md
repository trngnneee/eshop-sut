# BUG-FR02-A-21: Hệ thống thiếu cơ chế Refresh Token và Token Rotation để gia hạn phiên làm việc an toàn

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 21 |
| **BugID** | `BUG-FR02-A-21` |
| **Status** | **Open** |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản |
| **Summary** | Hệ thống hoàn toàn không triển khai cơ chế Refresh Token hay xoay vòng token (Token Rotation). Khi đăng nhập thành công, hệ thống chỉ trả về một Access Token (JWT) duy nhất có thời hạn vô hạn (hoặc hữu hạn nhưng không có cách nào tự động làm mới), gây nguy cơ mất an toàn bảo mật cao nếu token bị đánh cắp. |
| **Steps to reproduce** | 1. Đọc tệp tin `backend/server.js`.<br>2. Tìm kiếm các endpoint liên quan đến làm mới token như `/api/refresh-token` hay logic xử lý refresh token trong CSDL bảng `users`. Không có kết quả nào. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | Medium |
| **Attachment (Link to file)** | [server.js](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js) |
| **Date** | 2026-06-26 |
| **Reporter** | AI Tester (Antigravity) |

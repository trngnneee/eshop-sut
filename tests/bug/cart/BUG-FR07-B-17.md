# BUG-FR07-B-17: Thiếu cơ chế thu hồi Token JWT cũ sau khi người dùng bấm đăng xuất

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 17 |
| **BugID** | `BUG-FR07-B-17` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Hệ thống sử dụng cơ chế xác thực stateless JWT nhưng backend không triển khai danh sách đen (Blacklist) để thu hồi token sau khi người dùng bấm đăng xuất, khiến token cũ vẫn sử dụng được bình thường. |
| **Steps to reproduce** | 1. Đăng nhập tài khoản và lưu token JWT.
2. Thực hiện hành động Đăng xuất (Logout) trên client.
3. Dùng token JWT cũ gửi request gọi API `GET /api/cart`. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Evidence (Screenshot)** | Server vẫn trả dữ liệu giỏ hàng thành công (200 OK) thay vì 401 Unauthorized. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

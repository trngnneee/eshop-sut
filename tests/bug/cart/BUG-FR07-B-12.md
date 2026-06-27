# BUG-FR07-B-12: Backend API không validate tính toàn vẹn của sản phẩm thêm vào giỏ hàng

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 12 |
| **BugID** | `BUG-FR07-B-12` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | API `POST /api/cart` không validate sự tồn tại và tính hợp lệ của các trường bắt buộc như `id` và `price`. Backend chấp nhận thêm sản phẩm thiếu ID, thiếu giá, hoặc giá <= 0 vào giỏ hàng. |
| **Steps to reproduce** | 1. Đăng nhập và lấy token JWT.
2. Gửi request POST tới `/api/cart` với body thiếu trường `id`.
3. Kiểm tra giỏ hàng bằng GET `/api/cart`. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js#L290) |
| **Evidence (Screenshot)** | Ghi nhận response HTTP 200 OK thay vì HTTP 400 Bad Request. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

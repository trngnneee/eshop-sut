# BUG-FR07-B-01: Backend API không validate số lượng sản phẩm thêm vào giỏ hàng

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 01 |
| **BugID** | `BUG-FR07-B-01` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Tại `backend/server.js`, API `POST /api/cart` trực tiếp ghi nhận mọi giá trị quantity gửi lên (như 0, âm, thập phân, hoặc trống) mà không validate điều kiện số nguyên dương. |
| **Steps to reproduce** | 1. Đăng nhập và lấy token JWT.
2. Gửi POST tới `/api/cart` với body chứa `quantity = -5`.
3. Kiểm tra giỏ hàng bằng GET `/api/cart`. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Evidence (Screenshot)** | Ghi nhận response HTTP 200 OK thay vì HTTP 400 Bad Request. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

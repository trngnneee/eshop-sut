# BUG-FR07-B-16: Lỗ hổng cho phép gán thuộc tính đặc quyền (Mass Assignment / Extra Fields)

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 16 |
| **BugID** | `BUG-FR07-B-16` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | API `POST /api/cart` chấp nhận lưu trữ và trả về tất cả các trường dữ liệu thừa gửi lên từ client-side như `isAdmin: true` hay `discount: 90` mà không thực hiện lọc bỏ. |
| **Steps to reproduce** | 1. Đăng nhập.
2. Gửi request POST tới `/api/cart` với body chứa `{"productId": 1, "quantity": 1, "isAdmin": true}`.
3. Gọi GET `/api/cart` và kiểm tra các trường trả về. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](../../../backend/server.js#L290) |
| **Evidence (Screenshot)** | Các trường thừa được lưu trữ và trả về nguyên vẹn trong giỏ hàng. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

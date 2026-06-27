# BUG-FR07-B-15: Backend API không kiểm tra kiểu dữ liệu của trường quantity (Type Validation)

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 15 |
| **BugID** | `BUG-FR07-B-15` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | API `POST /api/cart` chấp nhận lưu trữ các giá trị số lượng `quantity` không phải số nguyên như chuỗi ký tự `"2"` hoặc giá trị `null` mà không báo lỗi. |
| **Steps to reproduce** | 1. Đăng nhập.
2. Gửi request POST tới `/api/cart` với body chứa `quantity: "2"`.
3. Xác minh phản hồi từ API. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Evidence (Screenshot)** | Ghi nhận response HTTP 200 OK cho kiểu dữ liệu không hợp lệ. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

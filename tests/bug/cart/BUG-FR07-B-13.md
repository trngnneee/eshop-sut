# BUG-FR07-B-13: Backend API cho phép giả mạo đơn giá của sản phẩm (Price Tampering)

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 13 |
| **BugID** | `BUG-FR07-B-13` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | API `POST /api/cart` trực tiếp sử dụng giá trị `price` truyền từ Client-side và lưu vào giỏ hàng mà không đối chiếu với giá trị thực tế trong Cơ sở dữ liệu. |
| **Steps to reproduce** | 1. Đăng nhập và lấy token JWT.
2. Gửi request POST tới `/api/cart` với body chứa `productId: 1`, `price: 1000` (giá gốc sản phẩm 1 là 100.000đ).
3. Gọi GET `/api/cart` và kiểm tra giá trị đơn giá lưu trong giỏ. |
| **Severity** | Critical |
| **Frequency** | Always |
| **Priority** | High |
| **Evidence (Screenshot)** | Lưu đơn giá giả mạo thành công vào giỏ hàng. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

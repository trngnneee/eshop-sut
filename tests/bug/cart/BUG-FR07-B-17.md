# BUG-FR07-B-17: Giao diện cho phép thanh toán (Checkout) khi giỏ hàng trống

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 17 |
| **BugID** | `BUG-FR07-B-17` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Giao diện giỏ hàng `/cart` không vô hiệu hóa nút Thanh toán và không chặn chuyển hướng sang `/checkout` khi giỏ hàng hoàn toàn trống rỗng hoặc chứa số lượng sản phẩm không hợp lệ. |
| **Steps to reproduce** | 1. Đảm bảo giỏ hàng rỗng.
2. Truy cập `/cart` và nhấp nút 'Thanh toán'. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | Medium |
| **Evidence (Screenshot)** | ![Evidence](evidences/BUG-FR07-B-17.png) |
| **Date** | 2026-06-27 |
| **Reporter** | Khoa |

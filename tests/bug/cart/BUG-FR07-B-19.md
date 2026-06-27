# BUG-FR07-B-19: Thiếu hiển thị ảnh mặc định (Fallback image) khi URL ảnh sản phẩm bị lỗi

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 19 |
| **BugID** | `BUG-FR07-B-19` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Giao diện trang giỏ hàng hiển thị biểu tượng ảnh vỡ và phá vỡ layout bảng hiển thị khi URL hình ảnh sản phẩm bị lỗi 404 hoặc không hợp lệ. |
| **Steps to reproduce** | 1. Thêm sản phẩm có URL ảnh bị lỗi vào giỏ.
2. Truy cập `/cart` và quan sát ảnh sản phẩm. |
| **Severity** | Minor |
| **Frequency** | Always |
| **Priority** | Low |
| **Evidence (Screenshot)** | Hiển thị icon ảnh lỗi mà không load ảnh fallback. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

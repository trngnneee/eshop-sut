# BUG-FR07-B-11: Trang giỏ hàng không bảo vệ quyền truy cập khi chưa đăng nhập

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 11 |
| **BugID** | `BUG-FR07-B-11` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Trang giỏ hàng `/cart` không kiểm tra trạng thái đăng nhập khi được load (mount), cho phép người dùng chưa đăng nhập truy cập trực tiếp thay vì tự động chuyển hướng về `/login`. |
| **Steps to reproduce** | 1. Xóa token / dùng tab ẩn danh.
2. Truy cập trực tiếp đường dẫn `/cart`. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [Cart.jsx](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/frontend-web/src/pages/Cart.jsx#L6) |
| **Evidence (Screenshot)** | Giao diện trang giỏ hàng vẫn hiển thị thay vì redirect về trang Login. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

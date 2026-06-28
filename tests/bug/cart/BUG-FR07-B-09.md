# BUG-FR07-B-09: Không cần đăng nhập vẫn cho phép thêm sản phẩm vào giỏ hàng

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 09 |
| **BugID** | `BUG-FR07-B-09` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Hệ thống cho phép người dùng chưa đăng nhập thực hiện thêm sản phẩm vào giỏ hàng thành công (không yêu cầu token xác thực hoặc không chặn ở Frontend/Backend), dẫn đến việc giỏ hàng hoạt động không có định danh người dùng. |
| **Steps to reproduce** | 1. Đảm bảo chưa đăng nhập (xóa token / dùng tab ẩn danh).
2. Truy cập trang chi tiết sản phẩm hoặc gửi yêu cầu API POST /api/cart không có Header Authorization chứa token JWT.
3. Nhấn 'Thêm vào giỏ hàng' hoặc gửi request qua Postman. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](../../../backend/server.js#L280) |
| **Evidence (Screenshot)** | API trả về 200 OK và sản phẩm được ghi nhận vào giỏ hàng thành công mà không yêu cầu xác thực người dùng. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

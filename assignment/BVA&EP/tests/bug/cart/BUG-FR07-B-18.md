# BUG-FR07-B-18: Thiếu xử lý lỗi kết nối mạng hoặc sập máy chủ trên giao diện

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 18 |
| **BugID** | `BUG-FR07-B-18` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Found by Test Case** | TC-CART-088 |
| **GitHub Issue** | https://github.com/trngnneee/eshop-sut/issues/145 |
| **Summary** | Khi API thêm sản phẩm thất bại do mất kết nối mạng hoặc sập server, Frontend vẫn tự động tăng số lượng badge trên Navbar mà không hiển thị thông báo lỗi phù hợp cho người dùng. |
| **Steps to reproduce** | 1. Tắt kết nối mạng hoặc server backend.
2. Nhấn nút 'Thêm vào giỏ hàng' và quan sát badge Navbar. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | Medium |
| **Attachment (Link to file)** | [ProductDetail.jsx](../../../frontend-web/src/pages/ProductDetail.jsx#L66) |
| **Evidence (Screenshot)** | Badge Navbar tăng ảo mặc dù API thêm giỏ hàng thất bại. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

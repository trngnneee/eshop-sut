# BUG-FR07-B-10: Giỏ hàng không đồng bộ với Backend khi xóa sản phẩm

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 10 |
| **BugID** | `BUG-FR07-B-10` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Nhấn nút 'Xóa' chỉ xóa sản phẩm ở React state phía Client. Backend không được thiết lập API xóa (`DELETE /api/cart`), dẫn đến việc khi reload (F5) trang, sản phẩm đã xóa lại tự động xuất hiện. |
| **Steps to reproduce** | 1. Thêm sản phẩm.
2. Vào `/cart` và bấm nút Xóa sản phẩm đó.
3. Nhấn F5 (reload trang). |
| **Severity** | Critical |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js#L280) |
| **Evidence (Screenshot)** | Sản phẩm tự động hiển thị trở lại sau khi reload trang. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

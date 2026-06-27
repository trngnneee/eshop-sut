# BUG-FR07-B-02: Backend API không cộng dồn số lượng cho sản phẩm trùng ID

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 02 |
| **BugID** | `BUG-FR07-B-02` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Tại `backend/server.js`, API `POST /api/cart` thực hiện đẩy trực tiếp request body vào mảng cart mà không kiểm tra trùng lặp ID sản phẩm, dẫn đến tạo các bản ghi thừa thay vì cộng dồn. |
| **Steps to reproduce** | 1. Gửi POST tới `/api/cart` thêm sản phẩm A với số lượng 1.
2. Gửi tiếp POST tới `/api/cart` thêm sản phẩm A với số lượng 2.
3. Gọi GET `/api/cart` kiểm tra cấu trúc dữ liệu trả về. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [server.js](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/backend/server.js#L290) |
| **Evidence (Screenshot)** | Trả về 2 dòng sản phẩm riêng biệt thay vì 1 dòng có quantity = 3. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

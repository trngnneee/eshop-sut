# BUG-FR02-A-15: Giao diện đăng nhập Admin thiếu nhãn thông tin, thiếu dấu * bắt buộc và nút hiện mật khẩu

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 15 |
| **BugID** | `BUG-FR02-A-15` |
| **Status** | **Open** |
| **Requirement Name** | FR-02 Đăng nhập & Khóa tài khoản, FR-21 Tiêu chuẩn Giao diện, FR-22 Form Requirements |
| **Summary** | Giao diện Đăng nhập Admin (`http://localhost:5174/`) thiếu nhãn label mô tả trường thông tin (khiến placeholder biến mất khi nhập liệu), thiếu dấu hoa thị đỏ `*` bắt buộc, thiếu nút Toggle ẩn/hiện mật khẩu, nút submit bằng tiếng Anh và thiếu thuộc tính `type="email"` ở trường Email. |
| **Steps to reproduce** | 1. Di chuyển vào `frontend-admin` và khởi chạy giao diện admin bằng `npm run dev`.<br>2. Truy cập `http://localhost:5174/` trên trình duyệt.<br>3. Nhập dữ liệu `admin@eshop.com` vào trường Email (quan sát thấy gợi ý placeholder biến mất và không có nhãn label bên ngoài để hướng dẫn người dùng).<br>4. Kiểm tra sự xuất hiện của dấu `*`, nút ẩn/hiện mật khẩu và ngôn ngữ nút bấm submit. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Attachment (Link to file)** | [App.jsx](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/frontend-admin/src/App.jsx#L195-L211) |
| **Evidence (Screenshot)** | ![Screenshot](../evidence/BUG-FR02-A-15_screenshot.png) |
| **Date** | 2026-06-26 |
| **Reporter** | AI Tester (Antigravity) |

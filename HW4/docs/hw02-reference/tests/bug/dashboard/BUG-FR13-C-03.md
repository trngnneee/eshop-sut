# BUG-FR13-C-03: Lỗi API /api/admin/users 500 ngắt toàn bộ tiến trình fetchData của dashboard
 
| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 03 |
| **BugID** | `BUG-FR13-C-03` |
| **Status** | **Open** |
| **Requirement Name** | FR-13 Dashboard (Robustness) |
| **Summary** | Khi một trong các API phục vụ Dashboard (ví dụ: API lấy danh sách người dùng `/api/admin/users`) gặp lỗi hệ thống (HTTP 500), giao diện Admin Dashboard bị ngắt tiến trình tải và không thể hiển thị số liệu của các mục khác (như doanh thu, đơn hàng, danh mục) mặc dù các API tương ứng vẫn hoạt động bình thường. |
| **Steps to reproduce** | 1. Đăng nhập admin.<br>2. Giả lập/mock API `/api/admin/users` trả về lỗi HTTP 500.<br>3. Truy cập Dashboard.<br>4. Quan sát số liệu ở các card doanh thu, đơn hàng, danh mục (chúng sẽ trống trơn hoặc giữ giá trị cũ thay vì hiển thị dữ liệu thực tế). |
| **Severity** | Medium |
| **Frequency** | Always |
| **Priority** | Medium |
| **Evidence (Screenshot)** | ![Evidence](evidences/BUG-FR13-C-03.png) |
| **Date** | 2026-06-28 |
| **Reporter** | Khoa |

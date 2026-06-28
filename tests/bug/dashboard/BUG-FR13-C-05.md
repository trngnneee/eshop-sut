# BUG-FR13-C-05: Giao diện hiển thị trực tiếp số liệu thống kê âm hoặc thập phân mà không kiểm tra tính hợp lệ dữ liệu
 
| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 05 |
| **BugID** | `BUG-FR13-C-05` |
| **Status** | **Open** |
| **Requirement Name** | FR-13 Dashboard (UI/UX / Integrity) |
| **Summary** | Các card hiển thị số liệu thống kê trên Dashboard (Tổng số người dùng, Tổng số sản phẩm) hiển thị trực tiếp dữ liệu thô nhận được từ API mà không có cơ chế validate dữ liệu ở frontend. Khi API trả về số âm hoặc số thập phân (ví dụ: `totalUsers = -1`, `totalProducts = 10.5`), UI hiển thị trực tiếp giá trị lỗi này mà không tự động chuyển về 0 hoặc làm tròn. |
| **Steps to reproduce** | 1. Đăng nhập admin.<br>2. Mock API trả về `totalUsers = -1` và `totalProducts = 10.5`.<br>3. Truy cập Dashboard.<br>4. Quan sát số hiển thị trên card Users là `-1` và card Products là `10.5`. |
| **Severity** | Minor |
| **Frequency** | Always |
| **Priority** | Low |
| **Evidence (Screenshot)** | ![Evidence](evidences/BUG-FR13-C-05.png) |
| **Date** | 2026-06-28 |
| **Reporter** | Khoa |

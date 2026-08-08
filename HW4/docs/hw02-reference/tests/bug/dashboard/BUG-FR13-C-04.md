# BUG-FR13-C-04: Order thiếu total_amount dẫn đến tính toán ra NaN hiển thị trên giao diện
 
| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 04 |
| **BugID** | `BUG-FR13-C-04` |
| **Status** | **Open** |
| **Requirement Name** | FR-13 Dashboard (UI/UX / Robustness) |
| **Summary** | Khi danh sách đơn hàng trả về từ API chứa đơn hàng thiếu trường thông tin tổng số tiền (`total_amount`), giao diện Admin Dashboard không xử lý ngoại lệ mà hiển thị giá trị lỗi `NaN ₫` tại mục 'Tổng doanh thu (Delivered)'. |
| **Steps to reproduce** | 1. Đăng nhập admin.<br>2. Thiết lập Mock API trả về danh sách orders chứa ít nhất một order đã giao (`delivered`) nhưng thiếu trường `total_amount`.<br>3. Truy cập Dashboard.<br>4. Quan sát số hiển thị ở 'Tổng doanh thu (Delivered)' sẽ là `NaN ₫`. |
| **Severity** | Medium |
| **Frequency** | Always |
| **Priority** | Medium |
| **Evidence (Screenshot)** | ![Evidence](evidences/BUG-FR13-C-04.png) |
| **Date** | 2026-06-28 |
| **Reporter** | Khoa |

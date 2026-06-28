# BUG-FR13-C-04: Order thiếu total_amount dẫn đến tính toán ra NaN hiển thị trên giao diện
 
| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 04 |
| **BugID** | `BUG-FR13-C-04` |
| **Status** | **Open** |
| **Requirement Name** | FR-13 Dashboard (UI/UX / Robustness) |
| **Summary** | Tại `frontend-admin/src/App.jsx:217-220`, hàm `reduce` tính toán `totalRevenue` thực hiện phép toán `sum + o.total_amount * 2`. Nếu một đơn hàng trong danh sách thiếu trường `total_amount` (ví dụ: `undefined` hoặc `null`), phép toán này trả về `NaN`, kéo theo toàn bộ `totalRevenue` bị chuyển thành `NaN` và hiển thị `NaN ₫` trên giao diện. |
| **Steps to reproduce** | 1. Đăng nhập admin.<br>2. Thiết lập Mock API trả về danh sách orders chứa ít nhất một order đã giao (`delivered`) nhưng thiếu trường `total_amount`.<br>3. Truy cập Dashboard.<br>4. Quan sát số hiển thị ở 'Tổng doanh thu (Delivered)' sẽ là `NaN ₫`. |
| **Severity** | Medium |
| **Frequency** | Always |
| **Priority** | Medium |
| **Evidence (Screenshot)** | ![Evidence](evidences/BUG-FR13-C-04.png) |
| **Date** | 2026-06-28 |
| **Reporter** | Khoa |

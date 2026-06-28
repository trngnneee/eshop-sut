# BUG-FR21-D-05: Hệ thống không áp dụng được mã giảm giá khi tổng giá trị đơn hàng bằng đúng giá trị tối thiểu quy định

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 06 |
| **BugID** | `BUG-FR21-D-05` |
| **Status** | **Open** |
| **Requirement Name** | Mobile Cart & Checkout |
| **Summary** | Khi người dùng áp dụng mã giảm giá có điều kiện giá trị đơn hàng tối thiểu (min_order_amount), hệ thống từ chối áp dụng và báo lỗi nếu tổng tiền giỏ hàng bằng chính xác giá trị tối thiểu đó. Mã giảm giá chỉ có thể được áp dụng khi tổng tiền lớn hơn hẳn giá trị tối thiểu. |
| **Steps to reproduce** | 1. Đăng nhập vào ứng dụng.<br>2. Thêm sản phẩm sao cho tổng giá trị đơn hàng bằng đúng giá trị tối thiểu của mã giảm giá (ví dụ: mã "SAVE10" yêu cầu tối thiểu 300,000 ₫, thêm sản phẩm có giá trị đúng 300,000 ₫).<br>3. Điều hướng tới trang Checkout, nhập mã giảm giá và nhấn "Áp dụng".<br>4. Quan sát kết quả hiển thị thông báo lỗi. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Evidence (Screenshot)** | ![Evidence](evidences/BUG-FR21-D-05.jpg) |
| **Date** | 2026-06-29 |
| **Reporter** | Khoa |

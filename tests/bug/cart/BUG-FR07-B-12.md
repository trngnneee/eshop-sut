# BUG-FR07-B-12: Không hiển thị số lượng hàng tồn kho khả dụng và thiếu cảnh báo khi số lượng vượt quá hàng tồn

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | TEMP1 |
| **BugID** | `BUG-FR07-B-12` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Trên giao diện chi tiết sản phẩm và giỏ hàng, hệ thống không hiển thị số lượng sản phẩm còn lại trong kho. Đồng thời, khi người dùng chọn hoặc nhập số lượng mua lớn hơn số lượng hàng tồn kho khả dụng thực tế, hệ thống vẫn cho phép thực hiện hoặc không hiển thị bất kỳ cảnh báo/lỗi nào để người dùng biết. |
| **Steps to reproduce** | 1. Đăng nhập và truy cập trang chi tiết của một sản phẩm (ví dụ: sản phẩm chỉ còn 3 cái trong kho).<br>2. Quan sát giao diện (không thấy thông tin hiển thị số lượng sản phẩm khả dụng trong kho).<br>3. Thử tăng số lượng mua lên thành 10 cái (hoặc một số lượng bất kỳ vượt quá mức tồn kho).<br>4. Nhấp nút "Thêm vào giỏ hàng" hoặc quan sát phản hồi trên giao diện. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Evidence (Screenshot)** | Giao diện không giới hạn số lượng chọn, không hiển thị số lượng còn lại, và cho phép thêm số lượng vượt quá tồn kho vào giỏ hàng mà không cảnh báo. |
| **Date** | 2026-06-27 |
| **Reporter** | AI Tester (Antigravity) |

# BUG-FR07-B-19: Giỏ hàng không được làm sạch sau khi thanh toán thành công (checkout success)

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 19 |
| **BugID** | `BUG-FR07-B-19` |
| **Status** | **Open** |
| **Requirement Name** | FR-08 Thanh toán |
| **Found by Test Case** | TC-CART-089 |
| **GitHub Issue** | https://github.com/trngnneee/eshop-sut/issues/167 |
| **Summary** | Sau khi thanh toán đơn hàng thành công, giỏ hàng không tự động làm trống, các sản phẩm đã thanh toán vẫn tiếp tục hiển thị trong giỏ hàng. |
| **Steps to reproduce** | 1. Đăng nhập và thêm sản phẩm vào giỏ hàng.<br>2. Nhấn nút Thanh toán để chuyển sang trang `/checkout`.<br>3. Bấm nút Thanh toán trên trang checkout để hoàn thành đơn hàng.<br>4. Nhận thông báo 'Thanh toán thành công!'.<br>5. Nhấp nút 'Quay lại trang chủ' và mở lại trang giỏ hàng `/cart`. |
| **Severity** | Major |
| **Frequency** | Always |
| **Priority** | High |
| **Evidence (Screenshot)** | ![Evidence](evidences/BUG-FR07-B-19.png) |
| **Date** | 2026-06-28 |
| **Reporter** | Khoa |

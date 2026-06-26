# BUG-FR07-B-07: Trang giỏ hàng không hiển thị hình ảnh đại diện sản phẩm

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **No.** | 07 |
| **BugID** | `BUG-FR07-B-07` |
| **Status** | **Open** |
| **Requirement Name** | FR-07 Giỏ hàng & Điều hướng |
| **Summary** | Cột 'Sản phẩm' trong bảng giỏ hàng chỉ hiển thị văn bản tên sản phẩm mà không hiển thị hình ảnh thumbnail như quy định. |
| **Steps to reproduce** | 1. Truy cập `/cart`.
2. Quan sát cột Sản phẩm. |
| **Severity** | Minor |
| **Frequency** | Always |
| **Priority** | Low |
| **Attachment (Link to file)** | [Cart.jsx](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/frontend-web/src/pages/Cart.jsx#L45) |
| **Evidence (Screenshot)** | Cột chỉ có text `{item.name}`, không có thẻ `<img>` hiển thị ảnh. |
| **Date** | 2026-06-26 |
| **Reporter** | AI Tester (Antigravity) |

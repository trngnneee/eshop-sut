# Feature Input Specification: [FEATURE_ID] - [FEATURE_NAME]

## 1. Thông Tin Chung (General Information)
* **Feature ID:** [Ví dụ: FR-07]
* **Feature Name:** [Ví dụ: Giỏ hàng - Shopping Cart]
* **Pool:** [Pool A / Pool B / Pool C / Pool D]
* **Target Role/User:** [Ví dụ: Khách vãng lai, Thành viên, Quản trị viên]
* **Description:** [Mô tả ngắn gọn chức năng làm nhiệm vụ gì]

## 2. Liên Kết Thành Phần (System Integration)
* **Related UI Pages:** [Các trang giao diện liên quan, ví dụ: /cart, /products]
* **Related API Endpoints:** [Các API liên quan nếu có, ví dụ: POST /api/cart/add]

## 3. Điều Kiện Tiền Quyết & Nghiệp Vụ (Preconditions & Business Rules)
* **Preconditions:**
  - [Điều kiện 1, ví dụ: Người dùng đã truy cập trang chi tiết sản phẩm]
  - [Điều kiện 2, ví dụ: Sản phẩm còn hàng trong kho (Stock > 0)]
* **Business Rules & Constraints:**
  - [Luật 1, ví dụ: Số lượng sản phẩm thêm vào giỏ phải từ 1 đến 100]
  - [Luật 2, ví dụ: Khi sản phẩm đã có trong giỏ, thêm tiếp sẽ tăng số lượng thay vì tạo dòng mới]

## 4. Các Trường Dữ Liệu Đầu Vào (Input Fields Specification)
| Tên Trường (Field Name) | Kiểu Dữ Liệu (Data Type) | Bắt Buộc (Required) | Ràng Buộc / Giới Hạn (Constraints / Limits) |
| :--- | :--- | :--- | :--- |
| [Ví dụ: quantity] | [Ví dụ: Integer] | [Yes/No] | [Ví dụ: Min: 1, Max: 100, Giá trị mặc định: 1] |

## 5. Kết Quả Mong Đợi (Expected Outcomes)
* **Khi dữ liệu hợp lệ:** [Ví dụ: Sản phẩm được thêm vào giỏ hàng thành công, hiển thị toast thông báo, số lượng giỏ hàng trên header tăng lên]
* **Khi dữ liệu không hợp lệ:** [Ví dụ: Hiển thị thông báo lỗi ngay dưới trường nhập hoặc hiển thị toast lỗi, không thêm vào giỏ]

## 6. Rủi Ro Đã Biết & Lưu Ý (Known Risks & Notes)
* **Known Risks:** [Ví dụ: Tranh chấp tồn kho khi nhiều người mua cùng lúc; Lỗi mất giỏ hàng khi session/cookie hết hạn]
* **Screenshots/Reference Links:**
  - [Link hình ảnh chụp giao diện hiện tại hoặc tài liệu mockup nếu có]

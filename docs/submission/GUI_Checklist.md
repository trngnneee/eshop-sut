# Checklist Kiểm Thử GUI (GUI Checklist)

Tài liệu này chứa cấu trúc bảng checklist kiểm thử giao diện (GUI) áp dụng cho hệ thống EShop. Sinh viên sẽ điền danh sách các mục kiểm thử cụ thể được sinh ra từ Kỹ năng Agent (Agent Skill) hoặc thiết kế thủ công vào bảng dưới đây.

---

## 1. Tóm Tắt Thực Thi Kiểm Thử (Test Summary)

- **Tổng số màn hình kiểm thử:** 2 (Web Customer Profile, Web Admin User Management)
- **Tổng số checklist item đã thiết kế:** 44
- **Tổng số item Đạt (Passed):** 36
- **Tổng số item Không đạt (Failed):** 8
- **Tỉ lệ đạt:** 81.8%

---

## 2. Bảng Checklist Chi Tiết

| ID | Khía Cạnh (Interface Aspect) | Mục Kiểm Thử (Checklist Item Description) | Trạng Thế (Passed/Failed/N/A) | Ghi Chú / Mô Tả Lỗi (Notes - Bắt buộc nếu Failed) | Minh chứng (Evidence) |
|---|---|---|---|---|---|
| IA-01-01 | IA-01: General UI standards | Phông chữ và kích thước chữ đồng nhất trên toàn bộ các trường nhập liệu, nhãn (labels) và các nút của trang cá nhân. | Passed | | - |
| IA-01-02 | IA-01: General UI standards | Tông màu của nút "Cập nhật" và "Hủy đơn" tuân thủ theo bảng màu thương hiệu của hệ thống EShop. | Passed | | - |
| IA-01-03 | IA-01: General UI standards | Bố cục trang cá nhân hiển thị tương thích (responsive) trên màn hình di động mà không bị tràn ngang hoặc che khuất thông tin. | Passed | | - |
| IA-01-04 | IA-01: General UI standards | Các tiêu đề cột trong bảng Lịch sử đơn hàng hiển thị đầy đủ, không bị xuống dòng ngắt quãng gây khó đọc. | Passed | | - |
| IA-01-05 | IA-01: General UI standards | Giá trị tổng số tiền đơn hàng hiển thị đúng định dạng tiền tệ (VD: "₫" hoặc "VND" và có dấu phân cách hàng nghìn). | Passed | Hiển thị đúng định dạng dấu phẩy phân cách hàng nghìn và ký hiệu ₫ | - |
| IA-01-06 | IA-01: General UI standards | Định dạng ngày tháng đặt hàng hiển thị thống nhất và dễ đọc (VD: DD/MM/YYYY). | Passed | Sử dụng toLocaleDateString() hiển thị ngày của trình duyệt | - |
| IA-01-07 | IA-01: General UI standards | Cột checkbox lựa chọn tại trang quản trị người dùng (Admin) thẳng hàng và có kích thước cân đối. | Passed | | - |
| IA-01-08 | IA-01: General UI standards | Tiêu đề bảng và nội dung các ô trong trang quản lý người dùng sử dụng cùng một kiểu phông chữ. | Passed | | - |
| IA-01-09 | IA-01: General UI standards | Các nút thao tác ("Xóa", "Hủy đơn") căn lề gọn gàng và không đè lên các thành phần khác. | Passed | | - |
| IA-01-10 | IA-01: General UI standards | Đường viền bảng và các phân chia hàng trong bảng lịch sử đơn hàng rõ ràng, thẩm mỹ. | Passed | | - |
| IA-01-11 | IA-01: General UI standards | Logo ứng dụng EShop hiển thị cân đối và rõ nét trên cả thanh tiêu đề người dùng và admin. | Passed | | - |
| IA-01-12 | IA-01: General UI standards | Ô nhập Email bị vô hiệu hóa (disabled) hiển thị màu nền khác biệt (xám nhẹ) để biểu thị trạng thái chỉ đọc. | Passed | Trường email hiển thị màu xám bg-gray-100 và không cho phép chỉnh sửa | - |
| IA-02-01 | IA-02: Forms | Form cập nhật thông tin cá nhân bắt buộc người dùng nhập "Họ Tên" (không được để trống). | Passed | Thuộc tính required của thẻ input | - |
| IA-02-02 | IA-02: Forms | Thông báo lỗi hoặc cảnh báo của trình duyệt xuất hiện khi cố ý gửi form cập nhật thông tin mà để trống "Họ Tên". | Passed | Hiển thị bong bóng báo lỗi mặc định của HTML5 | - |
| IA-02-03 | IA-02: Forms | Trường số điện thoại giới hạn định dạng và kiểm tra tính hợp lệ khi người dùng nhập sai số chữ số hoặc ký tự lạ. | Failed | Regex `/^[1-9][0-9]{8,9}$/` chặn tất cả số điện thoại Việt Nam bắt đầu bằng số 0 | [bug_profile_phone.png](./screenshots/bug_profile_phone.png) |
| IA-02-04 | IA-02: Forms | Vị trí các thông báo lỗi biểu mẫu hiển thị gần với trường nhập liệu tương ứng để người dùng dễ nhận biết. | Failed | Lỗi định dạng SĐT chỉ hiển thị qua hàm alert() chung chung thay vì thông báo lỗi dưới chân trường nhập | [bug_profile_phone.png](./screenshots/bug_profile_phone.png) |
| IA-02-05 | IA-02: Forms | Nút submit "Cập nhật" hoạt động chính xác khi click, gửi đúng payload dữ liệu lên server. | Passed | Hoạt động tốt khi các dữ liệu đầu vào hợp lệ | - |
| IA-02-06 | IA-02: Forms | Thứ tự di chuyển bằng phím Tab (Tab Order) trên biểu mẫu thông tin cá nhân đi theo trình tự logic (Họ tên -> Số điện thoại -> Địa chỉ -> Cập nhật). | Passed | | - |
| IA-02-07 | IA-02: Forms | Các ô nhập liệu có chỉ báo tiêu điểm rõ ràng (focus ring/border outline) khi người dùng click hoặc tab vào. | Passed | | - |
| IA-02-08 | IA-02: Forms | Vùng nhập "Địa chỉ giao hàng" (textarea) có kích thước mặc định hợp lý và cho phép co giãn hoặc có cuộn trang nếu văn bản quá dài. | Passed | | - |
| IA-02-09 | IA-02: Forms | Trường Email bị vô hiệu hóa không nhận tiêu điểm (focus) khi nhấn Tab. | Passed | | - |
| IA-02-10 | IA-02: Forms | Các văn bản gợi ý (placeholder) trong các ô nhập liệu mô tả đúng định dạng mong đợi (VD: "VD: 0912345678", "Nhập địa chỉ của bạn"). | Passed | | - |
| IA-02-11 | IA-02: Forms | Biểu mẫu đăng nhập Admin tự động nhận focus vào trường Email khi tải trang và cho phép submit bằng phím Enter. | Failed | Khi tải trang Admin Login, con trỏ không tự động focus vào ô email, người dùng phải click thủ công | [admin_users.png](./screenshots/admin_users.png) |
| IA-03-01 | IA-03: Navigation | Liên kết điều hướng của "Hồ sơ" trên thanh menu người dùng được làm nổi bật khi đang ở trang cá nhân. | Passed | | - |
| IA-03-02 | IA-03: Navigation | Bấm vào các liên kết trên thanh điều hướng (Home, Cart, Profile) chuyển hướng đúng trang mà không tải lại toàn bộ trang (Single Page App). | Passed | Chuyển hướng mượt mà không load lại trang | - |
| IA-03-03 | IA-03: Navigation | Thanh điều hướng bên (Sidebar) của Admin: bấm chọn "Người dùng" chuyển hướng sang đúng danh sách quản lý người dùng. | Passed | | - |
| IA-03-04 | IA-03: Navigation | Nút "Đăng xuất" trong trang Admin hoạt động đúng, xóa sạch token phiên làm việc và đưa về trang đăng nhập. | Passed | | - |
| IA-03-05 | IA-03: Navigation | Nút "Back" của trình duyệt hoạt động chuẩn xác khi người dùng quay lại trang Home từ trang Profile. | Passed | | - |
| IA-03-06 | IA-03: Navigation | Click vào logo EShop chuyển hướng người dùng về trang chủ (hoặc Dashboard đối với Admin). | Passed | | - |
| IA-03-07 | IA-03: Navigation | Trạng thái active trên Sidebar của Admin thay đổi linh hoạt tương ứng với tab đang được chọn. | Passed | | - |
| IA-03-08 | IA-03: Navigation | Nút "Hủy đơn" trong Lịch sử đơn hàng thực hiện hủy mà không chuyển hướng người dùng sang trang khác. | Passed | | - |
| IA-03-09 | IA-03: Navigation | Thanh menu di động hoặc nút điều hướng có kích thước đủ lớn để dễ tương tác bằng ngón tay. | Passed | | - |
| IA-03-10 | IA-03: Navigation | Tiêu đề của tab trình duyệt thay đổi tương ứng theo phân hệ (ví dụ: "Profile" hoặc "Admin Dashboard"). | Failed | Tiêu đề tab trình duyệt luôn giữ nguyên mặc định "Vite + React" ở cả hai phân hệ | [customer_profile.png](./screenshots/customer_profile.png) |
| IA-04-01 | IA-04: Feedback / state | Hiển thị thông báo thành công rõ ràng sau khi người dùng cập nhật hồ sơ cá nhân thành công. | Passed | Hiển thị alert("Cập nhật thành công!") | - |
| IA-04-02 | IA-04: Feedback / state | Hiển thị thông báo thành công sau khi người dùng hủy đơn hàng thành công. | Passed | Hiển thị alert("Hủy đơn thành công!") | - |
| IA-04-03 | IA-04: Feedback / state | Xử lý trạng thái trống (Empty State): Khi người dùng chưa có đơn hàng nào, hiển thị thông báo "Bạn chưa có đơn hàng nào." thay vì để bảng trống trơn. | Passed | | - |
| IA-04-04 | IA-04: Feedback / state | Xử lý trạng thái trống (Empty State): Khi danh sách người dùng trống, hiển thị thông báo thay thế phù hợp. | Failed | Nếu bảng người dùng Admin không có dữ liệu, giao diện chỉ hiển thị header bảng mà không có thông báo trống | [admin_users.png](./screenshots/admin_users.png) |
| IA-04-05 | IA-04: Feedback / state | Trạng thái của đơn hàng trong bảng Lịch sử đơn hàng được phân biệt bằng màu sắc trực quan (Đã giao: Xanh lá, Đã hủy: Đỏ, Đang giao: Xanh dương, Chờ xác nhận: Vàng). | Passed | | - |
| IA-04-06 | IA-04: Feedback / state | Các nút bấm thay đổi màu sắc hoặc độ mờ (opacity) khi di chuột qua (hover state). | Passed | | - |
| IA-04-07 | IA-04: Feedback / state | Khi di chuột qua các hàng của bảng, hàng tương ứng được làm nổi bật (row hover highlight). | Failed | Không có hiệu ứng hover highlight dòng trên các bảng danh sách người dùng và đơn hàng | [admin_checkboxes.png](./screenshots/admin_checkboxes.png) |
| IA-04-08 | IA-04: Feedback / state | Hiển thị thông báo lỗi cụ thể khi máy chủ gặp sự cố hoặc việc cập nhật thông tin thất bại. | Passed | | - |
| IA-04-09 | IA-04: Feedback / state | Hiển thị chỉ báo loading (spinner hoặc chữ "Đang tải...") khi dữ liệu đơn hàng đang được tải từ server. | Failed | Bảng trống trơn trong khi gọi API lấy đơn hàng trước khi render | [customer_profile.png](./screenshots/customer_profile.png) |
| IA-04-10 | IA-04: Feedback / state | Hiển thị hộp thoại xác nhận (Confirm Dialog) trước khi thực hiện xóa người dùng ở phân hệ Admin. | Failed | Click "Xóa" là người dùng bị xóa ngay lập tức khỏi DB mà không hỏi lại | [admin_users.png](./screenshots/admin_users.png) |
| IA-04-11 | IA-04: Feedback / state | Trạng thái vô hiệu hóa (disabled) của nút bấm được thể hiện rõ bằng độ mờ và con trỏ chuột không cho phép click. | Passed | | - |

---

*(Bảng trên đã được bổ sung cột Evidence và cập nhật đầy đủ thông tin trạng thái thực thi sau khi hoàn tất kiểm thử GUI)*

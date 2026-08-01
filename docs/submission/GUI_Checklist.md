# Checklist Kiểm Thử GUI (GUI Checklist)

Tài liệu này chứa cấu trúc bảng checklist kiểm thử giao diện (GUI) áp dụng cho hệ thống EShop. Sinh viên sẽ điền danh sách các mục kiểm thử cụ thể được sinh ra từ Kỹ năng Agent (Agent Skill) hoặc thiết kế thủ công vào bảng dưới đây.

---

## 1. Tóm Tắt Thực Thi Kiểm Thử (Test Summary)

- **Tổng số màn hình kiểm thử:** 2 (Web Customer Profile, Web Admin User Management)
- **Tổng số checklist item đã thiết kế:** 42
- **Tổng số item Đạt (Passed):** 35
- **Tổng số item Không đạt (Failed):** 7
- **Tỉ lệ đạt:** 83.3%

---

## 2. Bảng Checklist Chi Tiết

|ID|Khía Cạnh (Interface Aspect)|Phân Loại (Classification)|Màn Hình Kiểm Thử (Tested Screen)|Mục Kiểm Thử (Checklist Item Description)|Trạng Thái (Passed/Failed/N/A)|Ghi Chú / Mô Tả Lỗi (Notes - Bắt buộc nếu Failed)|Minh chứng (Evidence)|
|---|---|---|---|---|---|---|---|
|IA-01-01|IA-01: General UI standards|Visual|Customer Profile|Phông chữ và kích thước chữ đồng nhất trên toàn bộ các trường nhập liệu, nhãn (labels) và các nút của trang cá nhân.|Passed||-|
|IA-01-02|IA-01: General UI standards|Visual|Customer Profile|Tông màu của nút "Cập nhật" và "Hủy đơn" tuân thủ theo bảng màu thương hiệu của hệ thống EShop.|Passed||-|
|IA-01-03|IA-01: General UI standards|Responsive|Customer Profile|Bố cục trang cá nhân hiển thị tương thích (responsive) trên màn hình di động mà không bị tràn ngang hoặc che khuất thông tin.|Passed||-|
|IA-01-04|IA-01: General UI standards|Visual|Customer Profile|Các tiêu đề cột trong bảng Lịch sử đơn hàng hiển thị đầy đủ, không bị xuống dòng ngắt quãng gây khó đọc.|Passed||-|
|IA-01-05|IA-01: General UI standards|Visual|Customer Profile|Giá trị tổng số tiền đơn hàng hiển thị đúng định dạng tiền tệ (VD: "₫" hoặc "VND" và có dấu phân cách hàng nghìn).|Passed|Hiển thị đúng định dạng dấu phẩy phân cách hàng nghìn và ký hiệu ₫|-|
|IA-01-06|IA-01: General UI standards|Visual|Customer Profile|Định dạng ngày tháng đặt hàng hiển thị thống nhất và dễ đọc (VD: DD/MM/YYYY).|Passed|Hiển thị ngày của trình duyệt|-|
|IA-01-07|IA-01: General UI standards|Visual|Admin User Management|Cột checkbox lựa chọn tại trang quản trị người dùng (Admin) thẳng hàng và có kích thước cân đối.|Passed||-|
|IA-01-08|IA-01: General UI standards|Visual|Admin User Management|Tiêu đề bảng và nội dung các ô trong trang quản lý người dùng sử dụng cùng một kiểu phông chữ.|Passed||-|
|IA-01-09|IA-01: General UI standards|Visual|Customer Profile / Admin User|Các nút thao tác ("Xóa", "Hủy đơn") căn lề gọn gàng và không đè lên các thành phần khác.|Passed||-|
|IA-01-10|IA-01: General UI standards|Visual|Customer Profile|Đường viền bảng và các phân chia hàng trong bảng lịch sử đơn hàng rõ ràng, thẩm mỹ.|Passed||-|
|IA-01-11|IA-01: General UI standards|Visual|Customer Profile / Admin User|Logo ứng dụng EShop hiển thị cân đối và rõ nét trên cả thanh tiêu đề người dùng và admin.|Passed||-|
|IA-01-12|IA-01: General UI standards|Visual|Customer Profile|Ô nhập Email bị vô hiệu hóa (disabled) hiển thị màu nền khác biệt (xám nhẹ) để biểu thị trạng thái chỉ đọc.|Passed|Trường email hiển thị màu xám và không cho phép chỉnh sửa|-|
|IA-02-01|IA-02: Forms|Usability|Customer Profile|Form cập nhật thông tin cá nhân hiển thị dấu sao đỏ ở field "Họ Tên".|Failed||-|
|IA-02-02|IA-02: Forms|Validation|Customer Profile|Thông báo lỗi hoặc cảnh báo của trình duyệt xuất hiện khi cố ý gửi form cập nhật thông tin mà để trống "Họ Tên".|Passed|Hiển thị bong bóng báo lỗi mặc định của HTML5|-|
|IA-02-03|IA-02: Forms|Validation|Customer Profile|Trường số điện thoại giới hạn định dạng và kiểm tra tính hợp lệ khi người dùng nhập sai số chữ số hoặc ký tự lạ.|Failed|Chặn tất cả số điện thoại Việt Nam bắt đầu bằng số 0|[bug_profile_phone.png](./screenshots/bug_profile_phone.png)|
|IA-02-04|IA-02: Forms|Usability|Customer Profile|Vị trí các thông báo lỗi biểu mẫu hiển thị gần với trường nhập liệu tương ứng để người dùng dễ nhận biết.|Failed|Lỗi định dạng SĐT chỉ hiển thị qua hàm alert() chung chung thay vì thông báo lỗi dưới chân trường nhập|[bug_profile_phone.png](./screenshots/bug_profile_phone.png)|
|IA-02-05|IA-02: Forms|Functional|Customer Profile|Nút submit "Cập nhật" hoạt động khi click, sau khi click thì thông tin được cập nhật.|Passed|Hoạt động tốt khi các dữ liệu đầu vào hợp lệ với  logic validate của hệ thống hiện tại|-|
|IA-02-06|IA-02: Forms|Accessibility|Customer Profile|Thứ tự di chuyển bằng phím Tab (Tab Order) trên biểu mẫu thông tin cá nhân đi theo trình tự logic (Họ tên -> Số điện thoại -> Địa chỉ -> Cập nhật).|Passed||-|
|IA-02-07|IA-02: Forms|Accessibility|Customer Profile|Các ô nhập liệu có chỉ báo tiêu điểm rõ ràng (focus ring/border outline) khi người dùng click hoặc tab vào.|Passed||-|
|IA-02-08|IA-02: Forms|Usability|Customer Profile|Vùng nhập "Địa chỉ giao hàng" (textarea) có kích thước mặc định hợp lý và cho phép co giãn hoặc có cuộn trang nếu văn bản quá dài.|Passed||-|
|IA-02-09|IA-02: Forms|Accessibility|Customer Profile|Trường Email bị vô hiệu hóa không nhận tiêu điểm (focus) khi nhấn Tab.|Passed||-|
|IA-02-10|IA-02: Forms|Usability|Customer Profile|Các văn bản gợi ý (placeholder) trong các ô nhập liệu mô tả đúng định dạng mong đợi (VD: "VD: 0912345678", "Nhập địa chỉ của bạn").|Passed||-|
|IA-03-01|IA-03: Navigation|Usability|Customer Profile|Liên kết điều hướng của "Hồ sơ" trên thanh menu người dùng được làm nổi bật khi đang ở trang cá nhân (khác với khi đang ở các trang khác).|Failed|Nút "Chào, Test User" khi ở trang `/` và trang `/profile` không có sự khác biệt|-|
|IA-03-02|IA-03: Navigation|Functional|Customer Profile|Bấm vào các liên kết trên thanh điều hướng (Home, Giỏ Hàng, Profile) chuyển hướng đúng trang mà không tải lại toàn bộ trang (do Tech Stack mô tả sử dụng ReactJS - Single Page App).|Passed|Chuyển hướng mượt mà không load lại trang|-|
|IA-03-03|IA-03: Navigation|Functional|Admin User Management|Thanh điều hướng bên (Sidebar) của Admin: bấm chọn "Người dùng" chuyển hướng sang đúng danh sách quản lý người dùng.|Passed||-|
|IA-03-04|IA-03: Navigation|Accessibility|Customer Profile|Khi bấm vào nút "Đăng xuất", tài khoản người dùng được đăng xuất và nội dung trang hiển thị "Vui lòng đăng nhập" trên nền trắng xóa.|Passed||-|
|IA-03-05|IA-03: Navigation|Feedback|Customer Profile|Nút "Back" của trình duyệt hoạt động chuẩn xác khi người dùng quay lại trang Home từ trang Profile.|Passed||-|
|IA-03-06|IA-03: Navigation|Functional|Customer Profile|Click vào logo EShop chuyển hướng người dùng về trang chủ.|Passed||-|
|IA-03-07|IA-03: Navigation|Usability|Admin User Management|Trạng thái active trên Sidebar của Admin thay đổi linh hoạt tương ứng với tab đang được chọn.|Passed||-|
|IA-03-09|IA-03: Navigation|Responsive|Customer Profile|Các mút điều hướng có kích thước đủ lớn để dễ tương tác bằng ngón tay.|Passed||-|
|IA-03-10|IA-03: Navigation|Usability|Customer Profile / Admin Dashboard|Tiêu đề của tab trình duyệt thay đổi tương ứng theo phân hệ (ví dụ: "Profile" hoặc "Admin Dashboard").|Failed|Tiêu đề tab trình duyệt luôn giữ nguyên mặc định là "frontend-web", "frontend-admin"|[customer_profile.png](./screenshots/customer_profile.png)|
|IA-04-01|IA-04: Feedback / state|Feedback|Customer Profile|Hiển thị thông báo thành công rõ ràng sau khi người dùng cập nhật hồ sơ cá nhân thành công.|Passed|Hiển thị alert "Cập nhật thành công!|-|
|IA-04-04|IA-04: Feedback / state|Feedback|Admin User Management|Xử lý trạng thái trống (Empty State): Khi danh sách người dùng trống, hiển thị thông báo thay thế phù hợp.|Failed|Nếu bảng người dùng Admin không có dữ liệu, giao diện chỉ hiển thị header bảng mà không có thông báo trống|[admin_users.png](./screenshots/admin_users.png)|
|IA-04-06|IA-04: Feedback / state|Visual|Customer Profile / Admin User|Các nút bấm thay đổi màu sắc hoặc độ mờ (opacity) khi di chuột qua (hover state).|Passed||-|
|IA-04-07|IA-04: Feedback / state|Visual|Admin User|Khi di chuột qua các hàng của bảng, hàng tương ứng được làm nổi bật (row hover highlight).|Failed|Không có hiệu ứng hover highlight dòng trên các bảng danh sách người dùng và đơn hàng|[admin_checkboxes.png](./screenshots/admin_checkboxes.png)|
|IA-04-08|IA-04: Feedback / state|Feedback|Customer Profile|Hiển thị thông báo lỗi cụ thể khi máy chủ gặp sự cố hoặc việc cập nhật thông tin thất bại.|Passed||-|
|IA-04-10|IA-04: Feedback / state|Usability|Admin User Management|Hiển thị hộp thoại xác nhận (Confirm Dialog) trước khi thực hiện xóa người dùng ở phân hệ Admin.|Failed|Click "Xóa" là người dùng bị xóa ngay lập tức khỏi DB mà không hỏi lại|[admin_users.png](./screenshots/admin_users.png)|

---

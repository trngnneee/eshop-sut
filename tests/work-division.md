# Phân chia Công việc Kiểm thử (Work Division)

Hệ thống EShop có tổng cộng **24 Yêu cầu chức năng (Functional Requirements - FRs)**.
* **Khoa (Bạn)** đã thực hiện kiểm thử: **FR-02** (Đăng nhập & Khóa tài khoản).
* Các FR còn lại (**23 FRs**) được chia đều cho **5 thành viên** trong nhóm (An, Bình, Chi, Dũng, Giang).
* Mỗi thành viên sẽ thực hiện **đúng 5 FRs**. Do có 23 FRs còn lại, các yêu cầu chung về giao diện (**FR-21** và **FR-22**) sẽ được chia sẻ cho 2 thành viên cùng kiểm thử nhằm tăng độ bao phủ.

---

## 1. Bảng phân chia chi tiết (Chi tiết theo Thành viên)

| Thành viên | Số lượng | Danh sách FR thực hiện | Vai trò / Phạm vi Kiểm thử |
| :--- | :---: | :--- | :--- |
| **An** | 5 | FR-01, FR-03, FR-04, FR-21, FR-22 | Đăng ký, Quên mật khẩu, Hồ sơ cá nhân & Tiêu chuẩn giao diện, Form |
| **Bình** | 5 | FR-05, FR-06, FR-07, FR-23, FR-24 | Xem danh sách, Chi tiết sản phẩm, Giỏ hàng & Điều hướng, Trạng thái phản hồi |
| **Chi** | 5 | FR-08, FR-09, FR-10, FR-11, FR-21 | Thanh toán, Áp mã coupon, Trạng thái đơn hàng, Lịch sử đơn hàng & Giao diện chung |
| **Dũng** | 5 | FR-12, FR-13, FR-14, FR-15, FR-22 | Admin Access, Dashboard, CRUD Danh mục, CRUD Sản phẩm & Form tiêu chuẩn |
| **Giang** | 5 | FR-16, FR-17, FR-18, FR-19, FR-20 | Import CSV, CRUD Coupon, Quản lý đơn hàng/user (Admin) & Tính năng Mobile |

---

## 2. Danh sách FR chi tiết được phân công

### **Thành viên 1: An**
1. **[FR-01](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L30-L37): Đăng ký tài khoản** (Họ tên, email, mật khẩu mạnh, xác nhận mật khẩu, redirect).
2. **[FR-03](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L46-L61): Quên mật khẩu & Đặt lại mật khẩu** (2 bước, OTP mẫu, Step Indicator, quay lại đăng nhập).
3. **[FR-04](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L62-L69): Quản lý hồ sơ cá nhân** (Cập nhật họ tên, SĐT 10-11 số, địa chỉ, không đổi email, không đổi role).
4. **[FR-21](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L242-L249): Tiêu chuẩn Giao diện Chung** *(Đồng kiểm thử)* (Tiếng Việt, màu sắc nút bấm, định dạng tiền `₫`, thẻ `<h1>`, Tab Order).
5. **[FR-22](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L250-L257): Form Requirements** *(Đồng kiểm thử)* (Ký hiệu `*` bắt buộc, type email/password, thông báo lỗi phía trên submit, Step indicator).

### **Thành viên 2: Bình**
1. **[FR-05](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L73-L82): Xem danh sách & Tìm kiếm sản phẩm** (Grid sản phẩm, hiển thị ảnh/tên/giá, tìm kiếm an toàn XSS, loading, empty state, đúng 1 thẻ `<h1>`).
2. **[FR-06](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L83-L88): Xem chi tiết sản phẩm** (Ảnh lớn, mô tả, số lượng nguyên dương, thêm giỏ hàng có feedback toast/badge).
3. **[FR-07](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L93-L101): Giỏ hàng (Shopping Cart)** (Thông tin sản phẩm, +/- số lượng, trùng sản phẩm tăng số lượng, confirm dialog xóa, nút mua tiếp, nhãn "Tổng cộng", empty state).
4. **[FR-23](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L258-L264): Navigation Requirements** (Highlight active nav, badge giỏ hàng, nhãn "Đăng xuất", breadcrumb).
5. **[FR-24](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L265-L271): Feedback & State Requirements** (Feedback thêm giỏ hàng, confirm xóa giỏ hàng, empty state icon, alt text của ảnh).

### **Thành viên 3: Chi**
1. **[FR-08](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L102-L109): Thanh toán (Checkout)** (Yêu cầu đăng nhập, tổng tiền tự động, backend tính lại tiền, xóa giỏ hàng sau checkout).
2. **[FR-09](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L110-L137): Mã Giảm Giá (Coupon)** (Áp dụng 5 điều kiện coupon, công thức tính giảm giá phần trăm/cố định).
3. **[FR-10](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L141-L163): Trạng thái Đơn hàng (Order State Machine)** (Chuyển đổi 5 trạng thái đơn hàng, final states, chặn user hủy khi shipping).
4. **[FR-11](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L164-L169): Xem lịch sử đơn hàng (User)** (Chỉ xem đơn của mình, thông tin đơn, dịch trạng thái sang tiếng Việt + màu sắc tương ứng).
5. **[FR-21](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L242-L249): Tiêu chuẩn Giao diện Chung** *(Đồng kiểm thử)* (Tiếng Việt, màu sắc nút bấm, định dạng tiền `₫`, thẻ `<h1>`, Tab Order).

### **Thành viên 4: Dũng**
1. **[FR-12](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L174-L180): Kiểm soát truy cập (Access Control)** (Chỉ cho phép `role = 'admin'` truy cập các API admin `/api/admin/*` và các API thay đổi dữ liệu).
2. **[FR-13](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L181-L185): Dashboard** (Tổng doanh thu chỉ tính các đơn `delivered`, tổng số đơn hàng).
3. **[FR-14](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L186-L190): Quản lý Danh mục (Category CRUD)** (Thêm/Xem/Xóa danh mục, tên danh mục bắt buộc).
4. **[FR-15](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L191-L199): Quản lý Sản phẩm (Product CRUD)** (Thêm/Xem/Sửa/Xóa sản phẩm, validate input dương, danh mục bắt buộc, sửa độc lập).
5. **[FR-22](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L250-L257): Form Requirements** *(Đồng kiểm thử)* (Ký hiệu `*` bắt buộc, type email/password, thông báo lỗi phía trên submit, Step indicator).

### **Thành viên 5: Giang**
1. **[FR-16](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L200-L212): Import Sản phẩm từ CSV** (File `.csv`, header, bọc nháy kép RFC 4180, validate trước import, transaction rollback all-or-nothing, report lỗi).
2. **[FR-17](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L213-L217): Quản lý Mã Giảm Giá (Coupon CRUD)** (Admin Thêm/Xem/Xóa mã giảm giá, validate các trường bắt buộc).
3. **[FR-18](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L218-L223): Quản lý Đơn hàng (Admin)** (Admin xem tất cả đơn hàng, đổi trạng thái đơn hàng theo đúng State Machine, hiển thị địa chỉ an toàn XSS).
4. **[FR-19](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L224-L228): Quản lý Người dùng (Admin)** (Admin xem list user không lộ mật khẩu, xóa user ngoại trừ chính tài khoản admin đang đăng nhập).
5. **[FR-20](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/README.md#L233-L238): Tính năng Mobile** (Các chức năng trên Mobile, hủy đơn theo đúng quy tắc State Machine).

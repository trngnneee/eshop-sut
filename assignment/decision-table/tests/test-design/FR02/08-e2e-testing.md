# 08 — End-to-End (E2E) Testing Design: FR02 — Đăng nhập & Khóa tài khoản

Tài liệu này thiết kế các luồng kiểm thử tích hợp đầu cuối (End-to-End - E2E) cho tính năng Đăng nhập & Khóa tài khoản (FR02). Các kịch bản này kiểm tra sự phối hợp đồng bộ giữa Giao diện (Frontend Web/Admin) $\rightarrow$ API Backend (Node.js/Express) $\rightarrow$ Cơ sở dữ liệu (SQLite).

---

## 1. Phạm vi Kiểm thử E2E (E2E Test Scope)

Các ca kiểm thử E2E kiểm chứng các khía cạnh:
- **UI/UX Flow:** Luồng chuyển đổi trang, hiển thị thông báo lỗi, trạng thái nút bấm (loading/disabled) và lưu trữ token phía Client.
- **API Integration:** Tính đúng đắn của các HTTP status codes, dữ liệu JSON trả về (JWT token, user object).
- **Database Integrity:** Sự thay đổi dữ liệu thực tế tại bảng `users` (`login_attempts`, `locked_until`, `password`, `reset_token`).
- **Authorization Guard:** Khả năng ngăn chặn truy cập trái phép của JWT token đối với các trang Dashboard (Admin) hoặc Giỏ hàng (User).

---

## 2. Các Kịch bản E2E Chi tiết

### 2.1. E2E-FLOW-01: Hành trình khách hàng đăng nhập & mua sắm thành công (Customer Journey)

- **Mục tiêu:** Kiểm chứng luồng đăng nhập thành công của User thường, nhận token và thực hiện tác vụ mua hàng hợp lệ.
- **Các thành phần tham gia:**
  - Frontend Web: Trang `/login`, Trang chủ sản phẩm, Navbar Badge, Trang `/cart`.
  - Backend: `POST /api/login`, `GET /api/cart`.
  - Database: Bảng `users`.

#### Các bước thực hiện:
1. **Chuẩn bị:** Có tài khoản `test@eshop.com` với mật khẩu `Test1234!` trong cơ sở dữ liệu.
2. **Thực hiện trên UI:**
   - Mở trình duyệt truy cập đường dẫn `/login`.
   - Nhập Email: `test@eshop.com` và Mật khẩu: `Test1234!`.
   - Nhấn nút "Đăng Nhập" (hoặc "Sign In").
3. **Kiểm tra tích hợp API & DB:**
   - Xác nhận API `/api/login` trả về HTTP `200 OK` cùng JWT token.
   - Kết nối DB và truy vấn: Xác nhận `login_attempts` đã được reset về `0` và `locked_until` là `NULL`.
4. **Kiểm tra UI hậu đăng nhập:**
   - Xác nhận người dùng được điều hướng về Trang chủ.
   - LocalStorage lưu trữ JWT token hợp lệ.
   - Navbar hiển thị thông tin người dùng (hoặc nút "Đăng xuất" thay vì "Đăng nhập").
5. **Tác vụ mua sắm liên quan:**
   - Thêm sản phẩm vào giỏ hàng $\rightarrow$ Xác nhận Badge giỏ hàng cập nhật tăng số lượng.
   - Truy cập trang `/cart` $\rightarrow$ Đọc giỏ hàng thành công (qua JWT xác thực trong Header).
6. **Đăng xuất:**
   - Nhấn nút "Đăng xuất".
   - Xác nhận JWT bị xóa khỏi LocalStorage.
   - Thử truy cập lại `/cart` $\rightarrow$ Phải bị chặn/redirect về `/login`.

---

### 2.2. E2E-FLOW-02: Hành trình Quản trị viên truy cập hệ thống (Admin Authorization Flow)

- **Mục tiêu:** Kiểm chứng luồng đăng nhập của Admin, phân quyền truy cập Dashboard và nạp dữ liệu thống kê doanh thu.
- **Các thành phần tham gia:**
  - Frontend Admin: Trang `/admin/login`, Trang `/admin/dashboard` (hoặc `/`).
  - Backend: `POST /api/admin/login`, các API thống kê `GET /api/admin/orders`, `GET /api/admin/users`.
  - Database: Bảng `users`, `orders`.

#### Các bước thực hiện:
1. **Chuẩn bị:** Có tài khoản Admin `admin@eshop.com` với mật khẩu `Admin123!`.
2. **Thực hiện trên UI:**
   - Truy cập trang đăng nhập admin `/admin/login` (hoặc phân hệ admin tương ứng).
   - Nhập Email: `admin@eshop.com` và Mật khẩu: `Admin123!`.
   - Nhấn nút "Đăng nhập".
3. **Kiểm tra API & DB:**
   - API trả về HTTP `200 OK`, payload chứa JWT token có `role: "admin"`.
   - DB ghi nhận `login_attempts = 0`.
4. **Kiểm tra UI hậu đăng nhập:**
   - Hệ thống chuyển hướng Admin về trang Dashboard.
   - Màn hình hiển thị các thẻ thống kê: Tổng doanh thu, Tổng số đơn hàng, Tổng số user.
   - Xác nhận phía Backend đã kiểm tra vai trò admin khi tải các API statistics (không trả về lỗi 403 Forbidden).
5. **Bảo mật:**
   - Thử sử dụng JWT token của user thường (từ E2E-FLOW-01) để gửi request tới API admin `/api/admin/orders`.
   - **Kết quả kỳ vọng:** API trả về HTTP `403 Forbidden` (SUT hiện tại có lỗi bảo mật nghiêm trọng **BUG-FR13-C-01** thiếu phân quyền ở API backend).

---

### 2.3. E2E-FLOW-03: Đăng nhập sai nhiều lần $\rightarrow$ Khóa tài khoản $\rightarrow$ Khôi phục bằng Đặt lại mật khẩu

- **Mục tiêu:** Kiểm chứng đầy đủ vòng đời bảo mật từ lỗi đăng nhập, cơ chế khóa tài khoản tạm thời đến khôi phục mật khẩu để tự động mở khóa.
- **Các thành phần tham gia:**
  - Frontend: Màn hình Login, Màn hình Quên mật khẩu, Màn hình Nhập mã reset & Mật khẩu mới.
  - Backend: `POST /api/login` (Check lock), `POST /api/forgot-password`, `POST /api/reset-password`.
  - Database: Cập nhật liên tục trường `login_attempts`, `locked_until`, `password`, `reset_token`.

#### Các bước thực hiện:
1. **Khởi động lỗi đăng nhập:**
   - Truy cập `/login` bằng email `test_e2e@eshop.com`.
   - Nhập mật khẩu sai liên tục 2 lần (đối với SUT thực tế có bug) hoặc 3 lần (đối với Spec kỳ vọng).
2. **Kiểm tra DB & UI khi bị khóa:**
   - Trên UI: Xuất hiện thông báo lỗi rõ ràng "Tài khoản đã bị khóa. Vui lòng thử lại sau." (HTTP `403 Forbidden`).
   - Trong DB: `login_attempts` tăng đạt ngưỡng, `locked_until` lưu timestamp tương lai (`NOW + 3 phút`).
3. **Thử thách Đăng nhập khi đang khóa:**
   - Thử đăng nhập lại bằng mật khẩu ĐÚNG.
   - **Kết quả:** Vẫn bị từ chối ngay lập tức với HTTP `403 Forbidden`. DB không tăng thêm số lần đăng nhập sai.
4. **Thực hiện khôi phục tài khoản (Forgot Password):**
   - Click vào link "Quên mật khẩu" trên UI (hoặc gọi API `/api/forgot-password`).
   - Nhập email `test_e2e@eshop.com`.
   - Hệ thống sinh mã OTP / Reset Token trong DB.
5. **Đặt lại mật khẩu mới (Reset Password):**
   - Nhập mã Reset Token nhận được và nhập Mật khẩu mới: `NewValidPass123!`.
   - Nhấn "Xác nhận đặt lại".
   - **Xác minh Database:**
     - Mật khẩu tại dòng user `test_e2e@eshop.com` chuyển sang giá trị mới.
     - `reset_token` được xóa (`NULL`).
     - **Spec kỳ vọng:** Trạng thái khóa phải tự động được xóa bỏ (`login_attempts = 0`, `locked_until = NULL`).
     - **Bug thực tế:** SUT gặp lỗi **BUG-FR02-A-17** (Không xóa trạng thái khóa khi reset mật khẩu thành công).
6. **Đăng nhập sau phục hồi:**
   - Tiến hành đăng nhập bằng mật khẩu mới `NewValidPass123!`.
   - **Kết quả kỳ vọng:** Đăng nhập thành công và được chuyển hướng vào hệ thống.

---

## 3. Ma trận kiểm chứng tích hợp E2E (E2E Integration Verification Matrix)

| E2E Flow ID | Trực quan UI (Frontend) | Nghiệp vụ API (Backend) | Dữ liệu CSDL (SQLite) | Trạng thái xác minh trên SUT |
|---|---|---|---|---|
| **E2E-FLOW-01** | Trực quan tốt: Đăng nhập $\rightarrow$ Điều hướng Trang chủ $\rightarrow$ Giỏ hàng hoạt động $\rightarrow$ Đăng xuất. | API `/api/login` trả về token JWT chuẩn, lưu vào Cookie/LocalStorage. | Reset `login_attempts = 0`, `locked_until = NULL`. | **Passed** |
| **E2E-FLOW-02** | Hiển thị Dashboard admin khi có token Admin. | API `/api/admin/orders` nạp dữ liệu thống kê thành công. | Đọc dữ liệu từ bảng orders để vẽ biểu đồ và tổng doanh thu. | **Failed** (Backend APIs admin không check role, lỗi bảo mật nghiêm trọng). |
| **E2E-FLOW-03** | Frontend hiển thị thông báo lỗi khóa tĩnh, thiếu thông tin thời gian khóa còn lại. | API trả về 403 khi đang khóa. Reset password trả về thành công. | DB cập nhật `locked_until`. Tuy nhiên, API reset-password không giải phóng các trường lock. | **Failed** (Lỗi khóa 2 lần thay vì 3 lần, lỗi không mở khóa khi reset password). |

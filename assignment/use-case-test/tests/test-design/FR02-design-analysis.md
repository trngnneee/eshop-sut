# Test Design Analysis: FR02 – Login & Account Lockout (Use Case Testing)

Tài liệu phân tích thiết kế kịch bản kiểm thử theo kỹ thuật Ca sử dụng (Use Case Testing) cho tính năng Đăng nhập và Khóa tài khoản (FR02) trong hệ thống EShop.

---

## 1. Mô Tả Use Case (Use Case Description)

* **Tên ca sử dụng**: Đăng nhập (Login)
* **Tác nhân (Actors)**: Khách hàng (Customer), Quản trị viên (Admin), Hệ thống (System), Backend API.
* **Điều kiện tiền quyết (Preconditions)**:
  1. Tài khoản của người dùng đã được đăng ký trong hệ thống.
  2. Tài khoản ở trạng thái hoạt động (không bị khóa trước đó).
* **Điều kiện sau (Postconditions)**:
  1. Người dùng đăng nhập thành công, nhận được mã JWT token lưu trữ tại trình duyệt.
  2. Người dùng được chuyển hướng đến trang thích hợp (Trang chủ cho Customer, Trang Dashboard cho Admin).
  3. Số lần đăng nhập sai (`login_attempts`) trong database được reset về `0`.

---

## 2. Luồng Nghiệp Vụ (Flow of Events)

### 2.1. Luồng Chính (Main Flow - Happy Path)
1. Người dùng truy cập trang Đăng nhập (`/login`).
2. Giao diện hiển thị biểu mẫu đăng nhập gồm ô nhập Email và Password.
3. Người dùng nhập Email và Password hợp lệ của tài khoản Khách hàng.
4. Người dùng click nút "Đăng nhập".
5. Hệ thống gửi yêu cầu xác thực (`POST /api/login`) kèm Email và Password.
6. Backend kiểm tra thông tin khớp, reset bộ đếm `login_attempts` trong CSDL về `0`.
7. Backend sinh mã JWT token và trả về thành công cho client.
8. Giao diện lưu token vào bộ nhớ trình duyệt và chuyển hướng người dùng về trang chủ (`/`).

### 2.2. Luồng Rẽ Nhánh (Alternate Flows - AF)
* **AF 1: Đăng nhập quyền Quản trị viên (Admin Login)**:
  - Tại bước 1, người dùng truy cập trang Đăng nhập Admin (`/login` trên giao diện Admin).
  - Tại bước 3, người dùng nhập tài khoản Admin hợp lệ (`admin@eshop.com` / `Admin123!`).
  - Hệ thống gọi API `POST /api/admin/login`, xác thực vai trò `admin` và chuyển hướng sang trang Dashboard (`/admin/dashboard`).

### 2.3. Luồng Ngoại Lệ (Exception Flows - EF)
* **EF 1: Nhập sai thông tin đăng nhập (Incorrect Credentials)**:
  - Tại bước 3, người dùng nhập sai Email hoặc Password.
  - Backend kiểm tra, tăng bộ đếm `login_attempts` thêm 1, lưu thời gian khóa nếu cần và trả về lỗi 401.
  - Giao diện hiển thị thông báo lỗi "Invalid email or password".
* **EF 2: Khóa tài khoản sau 3 lần sai liên tiếp (Account Lockout)**:
  - Người dùng đã đăng nhập sai 2 lần liên tiếp. Tại bước 3, người dùng tiếp tục nhập sai lần thứ 3.
  - Backend tăng bộ đếm `login_attempts` lên 3, cập nhật thời gian khóa `locked_until` (thêm 30s hoặc 180s trong DB) và trả về mã lỗi 403.
  - Giao diện báo lỗi tài khoản bị khóa tạm thời.
* **EF 3: Đăng nhập khi tài khoản đang bị khóa (Locked State Check)**:
  - Người dùng cố gắng đăng nhập lại khi tài khoản đang trong thời gian bị khóa tạm thời.
  - Backend kiểm tra thấy thời gian hiện tại nằm trong khoảng khóa `locked_until`, chặn ngay lập tức và trả về lỗi 403.
  - Giao diện hiển thị thông báo lỗi tài khoản đang bị khóa.
* **EF 4: Nhập sai định dạng Email (Invalid Email Format)**:
  - Tại bước 3, người dùng nhập email sai định dạng (ví dụ: `abc@com` hoặc `abc.com`).
  - Hệ thống (hoặc frontend validation) báo lỗi định dạng email ngay lập tức và chặn không gửi API lên backend.
* **EF 5: Để trống thông tin đăng nhập (Blank Fields)**:
  - Người dùng bỏ trống trường Email hoặc Password rồi bấm "Đăng nhập".
  - Hệ thống báo lỗi trường bắt buộc và chặn gửi request.

---

## 3. Các Kịch Bản Sử Dụng (Use Case Scenarios)

Dựa trên các luồng nghiệp vụ trên, chúng ta thiết kế các kịch bản kiểm thử (Use Case Scenarios):

| Scenario ID | Tên kịch bản (Scenario Name) | Luồng đi (Flow Path) | Kết quả mong đợi |
| :--- | :--- | :--- | :--- |
| **UC-SC-01** | Khách hàng đăng nhập thành công | Main Flow | Đăng nhập thành công, nhận JWT, chuyển hướng về Home. |
| **UC-SC-02** | Admin đăng nhập thành công | Main Flow + AF 1 | Đăng nhập thành công, nhận JWT, chuyển hướng về Dashboard. |
| **UC-SC-03** | Đăng nhập thất bại do thông tin sai | EF 1 | Báo lỗi thông tin sai, tăng attempts trong DB. |
| **UC-SC-04** | Bị khóa tài khoản khi nhập sai 3 lần liên tiếp | EF 2 | Báo lỗi tài khoản bị khóa tạm thời. |
| **UC-SC-05** | Chặn đăng nhập khi tài khoản đang bị khóa | EF 3 | Báo lỗi tài khoản đang bị khóa, chặn ngay lập tức. |
| **UC-SC-06** | Báo lỗi khi email sai định dạng | EF 4 | Báo lỗi định dạng email trên giao diện, chặn submit. |
| **UC-SC-07** | Báo lỗi khi để trống Email hoặc Password | EF 5 | Báo lỗi trường bắt buộc trên giao diện, chặn submit. |

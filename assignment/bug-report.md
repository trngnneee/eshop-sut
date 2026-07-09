# Báo Cáo Lỗi Kiểm Thử Chuyển Trạng Thái & Ca Sử Dụng (ST & UC Bug Report)

Báo cáo này tổng hợp chi tiết các lỗi (defects/bugs) phát hiện được trên hệ thống **EShop SUT** trong quá trình kiểm thử chức năng **FR02: Đăng nhập & Khóa tài khoản** bằng hai phương pháp **State Transition Testing (ST)** và **Use Case Testing (UC)**.

---

## 1. TÓM TẮT DANH SÁCH LỖI

| Mã Lỗi (Bug ID) | Tên Lỗi | Kỹ Thuật Phát Hiện | Mức Độ Nghiêm Trọng | Trạng Thái |
| :--- | :--- | :---: | :---: | :---: |
| **`BUG-FR02-ST-01`** | Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1 | ST | Major | Open |
| **`BUG-FR02-ST-02`** | Thời gian khóa tài khoản bị thiết lập sai thành 3 phút thay vì 30s | ST | Medium | Open |
| **`BUG-FR02-ST-03`** | Đặt lại mật khẩu thành công không giải phóng trạng thái khóa tài khoản | ST | Major | Open |
| **`BUG-FR02-UC-01`** | Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1 *(Trùng root cause)* | UC | Major | Open |
| **`BUG-FR02-UC-02`** | Đổi mật khẩu thành công không reset bộ đếm và mở khóa tài khoản *(Trùng root cause)* | UC | Major | Open |

---

## 2. CHI TIẾT BÁO CÁO LỖI (BUG DETAILS)

### 2.1. BUG-FR02-ST-01: Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-ST-01` |
| **Found by Test Case** | [TC-FR02-ST-002](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/state-transtition-test/tests/test-cases/FR02/TC-FR02-ST-002.md) |
| **Requirement Name** | FR02 – Đăng nhập & Khóa tài khoản |
| **Severity** | **Major** |
| **Priority** | **High** |
| **Preconditions** | Tài khoản `test@eshop.com` đang hoạt động bình thường (`login_attempts = 0`). |
| **Steps to reproduce** | 1. Truy cập giao diện đăng nhập EShop. <br> 2. Nhập email `test@eshop.com` và mật khẩu sai `Wrong123!`. <br> 3. Nhấp "Đăng nhập" để kích hoạt sự kiện `login_fail`. <br> 4. Kiểm tra trường `login_attempts` trong database SQLite (`backend/database.sqlite`). |
| **Expected Result** | Trường `login_attempts` phải có giá trị là `1` (tăng 1 đơn vị cho mỗi lần sai). |
| **Actual Result** | Trường `login_attempts` có giá trị là `2` (tăng 2 đơn vị). Tài khoản sẽ bị khóa ở lần nhập sai thứ 2 thay vì thứ 3. |
| **Suggested Fix** | Trong file `backend/server.js` (dòng 54), sửa công thức tăng attempts từ `user.login_attempts + 2` thành `user.login_attempts + 1`. |
| **Date** | 2026-07-06 |

---

### 2.2. BUG-FR02-ST-02: Thời gian khóa tài khoản bị thiết lập sai thành 3 phút

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-ST-02` |
| **Found by Test Case** | [TC-FR02-ST-005](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/state-transtition-test/tests/test-cases/FR02/TC-FR02-ST-005.md) |
| **Requirement Name** | FR02 – Đăng nhập & Khóa tài khoản |
| **Severity** | **Medium** |
| **Priority** | **High** |
| **Preconditions** | Tài khoản `test@eshop.com` đang hoạt động bình thường. |
| **Steps to reproduce** | 1. Thực hiện đăng nhập sai liên tiếp 3 lần để kích hoạt trạng thái `Locked`. <br> 2. Kiểm tra trường `locked_until` trong database. <br> 3. Đo khoảng thời gian từ lúc bị khóa đến lúc trường `locked_until` hết hạn. |
| **Expected Result** | Thời gian khóa trong môi trường thử nghiệm/demo phải là 30 giây kể từ thời điểm khóa. |
| **Actual Result** | Thời gian khóa bị cấu hình thành `180000` ms (3 phút), khiến tài khoản bị khóa quá lâu so với đặc tả kiểm thử. |
| **Suggested Fix** | Trong file `backend/server.js` (dòng 57), thay đổi cấu hình thời gian khóa từ `180000` (3 phút) thành `30000` (30 giây) để đúng đặc tả môi trường thử nghiệm. |
| **Date** | 2026-07-06 |

---

### 2.3. BUG-FR02-ST-03: Đặt lại mật khẩu thành công không giải phóng trạng thái khóa

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-ST-03` |
| **Found by Test Case** | [TC-FR02-ST-006](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/state-transtition-test/tests/test-cases/FR02/TC-FR02-ST-006.md) |
| **Requirement Name** | FR02 – Đăng nhập & Khóa tài khoản |
| **Severity** | **Major** |
| **Priority** | **High** |
| **Preconditions** | Tài khoản `test@eshop.com` đang bị khóa (`login_attempts = 3`, `locked_until` ở tương lai). |
| **Steps to reproduce** | 1. Thực hiện yêu cầu đặt lại mật khẩu mới thông qua endpoint `/api/reset-password`. <br> 2. Sử dụng mật khẩu mới để tiến hành đăng nhập lại ngay lập tức. |
| **Expected Result** | 1. Đặt lại mật khẩu thành công. <br> 2. Tài khoản tự động được mở khóa (reset bộ đếm và xóa thời gian khóa trong DB), người dùng đăng nhập thành công. |
| **Actual Result** | Hệ thống cho phép đặt lại mật khẩu thành công, nhưng giữ nguyên giá trị `login_attempts = 3` và `locked_until` trong DB. Người dùng đăng nhập bằng mật khẩu mới vẫn bị chặn và báo lỗi tài khoản bị khóa. |
| **Suggested Fix** | Trong endpoint `/api/reset-password` của backend, bổ sung câu lệnh cập nhật CSDL để đặt lại `login_attempts = 0` và `locked_until = NULL` sau khi cập nhật mật khẩu mới thành công. |
| **Date** | 2026-07-06 |

---

### 2.4. BUG-FR02-UC-01: Bộ đếm đăng nhập sai tăng thêm 2 đơn vị thay vì 1 (Use Case)

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-UC-01` |
| **Found by Test Case** | [TC-FR02-UC-003](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/use-case-test/tests/test-cases/FR02/TC-FR02-UC-003.md) |
| **Requirement Name** | FR02 – Đăng nhập & Khóa tài khoản |
| **Severity** | **Major** |
| **Priority** | **High** |
| **Preconditions** | Tài khoản user đang hoạt động bình thường. |
| **Steps to reproduce** | 1. Gọi API đăng nhập `/api/login` với email đúng nhưng mật khẩu sai. <br> 2. Kiểm tra giá trị `login_attempts` trong database. |
| **Expected Result** | Bộ đếm `login_attempts` tăng từ 0 lên 1. |
| **Actual Result** | Bộ đếm `login_attempts` nhảy vọt từ 0 lên 2. Lỗi này làm tài khoản bị khóa sai quy tắc ở lần nhập sai thứ 2. |
| **Suggested Fix** | Sửa logic tăng attempts trong file `backend/server.js`. *(Xem chi tiết tại BUG-FR02-ST-01)* |
| **Date** | 2026-07-06 |

---

### 2.5. BUG-FR02-UC-02: Đổi mật khẩu thành công không reset bộ đếm và mở khóa (Use Case)

| Tên trường (Field) | Giá trị (Value) |
| :--- | :--- |
| **BugID** | `BUG-FR02-UC-02` |
| **Found by Test Case** | [TC-FR02-UC-007](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/assignment/use-case-test/tests/test-cases/FR02/TC-FR02-UC-007.md) |
| **Requirement Name** | FR02 – Đăng nhập & Khóa tài khoản |
| **Severity** | **Major** |
| **Priority** | **High** |
| **Preconditions** | Tài khoản đang bị khóa do nhập sai 3 lần. |
| **Steps to reproduce** | 1. Thực hiện quy trình đặt lại mật khẩu mới. <br> 2. Gọi API đăng nhập `/api/login` bằng mật khẩu mới vừa đổi. |
| **Expected Result** | Đăng nhập thành công, tài khoản được mở khóa. |
| **Actual Result** | API báo lỗi tài khoản đang bị khóa tạm thời. Database vẫn lưu `login_attempts = 3` và `locked_until` ở tương lai, không được đặt lại sau khi khôi phục mật khẩu. |
| **Suggested Fix** | Bổ sung logic reset bộ đếm khóa và mở khóa tài khoản khi đổi mật khẩu thành công ở backend. *(Xem chi tiết tại BUG-FR02-ST-03)* |
| **Date** | 2026-07-06 |

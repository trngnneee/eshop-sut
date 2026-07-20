# Báo cáo Tổng kết Kết quả Kiểm thử (HW02)

## 1. Tổng quan Dự án & Phạm vi kiểm thử

Tài liệu này tổng hợp kết quả kiểm thử hệ thống thương mại điện tử **EShop** cho bài tập lớn **HW02_Testing**. Báo cáo thống kê chi tiết số lượng test case, độ phủ yêu cầu, trạng thái chạy test thực tế và thông tin các lỗi (bugs) được phát hiện qua 5 nhóm kỹ thuật kiểm thử cốt lõi.

---

## 2. Thống kê Test Cases & Trạng thái Thực thi

Dưới đây là bảng tổng hợp số lượng test case và kết quả thực thi chia theo từng nhóm bài tập (Kỹ thuật kiểm thử):

| Bài tập / Kỹ thuật | Chức năng kiểm thử | Requirement | Số Test Case | PASSED | FAILED | Tỷ lệ PASS |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **EP & BVA** (Domain Testing) | - Xem danh sách & Tìm kiếm sản phẩm<br>- Xem lịch sử đơn hàng<br>- Quản lý người dùng (Admin)<br>- Hủy đơn hàng trên Mobile | FR-05<br>FR-11<br>FR-19<br>FR-10, FR-20 | **72** | **51** | **21** | 70.8% |
| **DT & PT** (Decision Table & Pair-wise) | - Quản lý trạng thái đơn hàng (API) | FR-10 | **19** | **15** | **4** | 78.9% |
| **ST** (State Transition Testing) | - Quản lý Quên mật khẩu & Đặt lại mật khẩu (2 bước) | FR-03 | **20** | **5** | **15** | 25.0% |
| **UC** (Use Case Testing) | - Luồng Quên mật khẩu & Đặt lại mật khẩu (2 bước) | FR-03 | **7** | **2** | **5** | 28.6% |
| **TỔNG CỘNG** | | | **118** | **73** | **45** | **61.9%** |

### Chi tiết phân rã nhóm EP & BVA (Domain Testing):
- **Xem danh sách & Tìm kiếm sản phẩm (FR-05):** 14 Test Cases (6 PASSED, 8 FAILED)
- **Xem lịch sử đơn hàng (FR-11):** 14 Test Cases (12 PASSED, 2 FAILED)
- **Quản lý người dùng (FR-19):** 22 Test Cases (13 PASSED, 9 FAILED)
- **Trạng thái đơn hàng trên Mobile (FR-10, FR-20):** 22 Test Cases (20 PASSED, 2 FAILED)

---

## 3. Độ phủ Kiểm thử của Test Cases (Test Case Coverage)

### Theo Kỹ thuật Kiểm thử (Test Design Technique):
- **Equivalence Partitioning (EP) & Boundary Value Analysis (BVA):** Phủ 100% các phân vùng tương đương hợp lệ/không hợp lệ và các điểm biên của tham số đầu vào cũng như biên trạng thái (trạng thái hủy đơn trên Mobile).
- **Decision Table Testing (DT):** Bao phủ toàn bộ 28 luật kết hợp điều kiện chuyển đổi trạng thái đơn hàng.
- **Pair-wise Testing (PT):** Áp dụng thuật toán giảm số lượng test case từ 28 luật xuống 19 test case nhưng vẫn đảm bảo bao phủ mọi cặp yếu tố (Current State, Target State, Role).
- **State Transition Testing (ST):** Đạt độ phủ 100% cho:
  - State Coverage (4/4 states)
  - Transition Coverage (9/9 transitions gồm 4 valid và 5 invalid)
  - 1-switch Coverage (4 sequences)
  - n-switch Coverage (n=2, 4 sequences)
  - End-to-End Test (2 paths)
  - Final State Test (1 final state)
- **Use Case Testing (UC):** Đạt độ phủ 100% cho Main Flow (luồng chính), Alternative Flow (luồng thay thế) và Exception Flows (luồng ngoại lệ).

### Theo Yêu cầu Chức năng (Feature Requirement):
- **FR-03 (Quên mật khẩu):** Phủ đầy đủ cả 2 bước (Lấy OTP & Đặt lại mật khẩu), bao gồm kiểm tra tính hợp lệ của email, kiểm tra độ mạnh mật khẩu và logic xác thực mã OTP.
- **FR-05 (Tìm kiếm & Sản phẩm):** Phủ hiển thị dạng lưới, định dạng giá, hiển thị hình ảnh, thanh tìm kiếm và xử lý bảo mật (SQLi, XSS).
- **FR-10 (Order State Machine):** Phủ toàn bộ logic chuyển đổi giữa 5 trạng thái đơn hàng và phân quyền tương ứng cho Admin/User.
- **FR-11 (Lịch sử đơn hàng):** Phủ quyền sở hữu đơn hàng của chính mình, hiển thị tiếng Việt, hiển thị màu sắc và tính năng phân trang.
- **FR-19 (Quản lý người dùng):** Phủ phân quyền truy cập API Admin, tính năng xóa người dùng (bao gồm chặn tự xóa chính mình, kiểm tra tham số hợp lệ, kiểm tra ID không tồn tại và xử lý liên kết dữ liệu).
- **FR-20 (Mobile Order):** Phủ các đặc thù UI trên Mobile như hiển thị/ẩn nút Hủy đơn đỏ, hiển thị dialog xác nhận và cập nhật trạng thái ngay trên ứng dụng Mobile.

---

## 4. Báo cáo & Phân loại Lỗi (Bug Report & Severity)

Tổng số lỗi được phát hiện và lập báo cáo chi tiết: **26 lỗi (bugs)**.

### Phân phối Lỗi theo Yêu cầu Chức năng (Feature Requirement):
- **FR-05 (Sản phẩm & Tìm kiếm):** 8 bugs
- **FR-11 (Lịch sử đơn hàng):** 2 bugs
- **FR-19 (Quản lý người dùng):** 7 bugs
- **FR-10 & FR-20 (Đơn hàng & Mobile):** 4 bugs
- **FR-03 (Quên mật khẩu):** 5 bugs

### Phân loại Lỗi theo Mức độ Nghiêm trọng (Severity):

#### A. Critical (Nghiêm trọng / Bảo mật / Leo quyền) — 6 Bugs
1. **[Search]** Chức năng tìm kiếm không sanitize input dẫn đến lỗi bảo mật **Cross-Site Scripting (XSS)**.
2. **[Search]** Chức năng tìm kiếm không xử lý ký tự đặc biệt dẫn đến lỗi **SQL Injection**.
3. **[Order History]** API xem chi tiết đơn hàng không yêu cầu token xác thực, cho phép khách vãng lai xem chi tiết đơn hàng của người khác nếu biết ID đơn.
4. **[User Management]** Tài khoản user thường vẫn gọi được API Admin để lấy danh sách toàn bộ người dùng trong hệ thống.
5. **[User Management]** Tài khoản user thường có thể gọi API Admin để xóa tài khoản của người dùng khác (Leo quyền).
6. **[Order State Machine]** API cập nhật trạng thái đơn hàng của Admin không kiểm tra phân quyền role, cho phép user thường tự chuyển trạng thái đơn sang confirmed, shipping, delivered.

#### B. High (Lỗi Logic / Nghiệp vụ / Sai thông số chính) — 7 Bugs
7. **[User Management]** Admin có thể tự xóa chính tài khoản đang đăng nhập của mình, làm mất quyền quản trị.
8. **[User Management]** Xóa người dùng có đơn hàng liên quan nhưng không cascade xóa hoặc xử lý dữ liệu liên kết, dẫn đến các đơn hàng mồ côi (Orphan Data).
9. **[Order State Machine]** Khách hàng có thể tự hủy đơn hàng khi đơn đã chuyển sang trạng thái `shipping` (Đặc tả cấm tự hủy khi đang giao).
10. **[Forgot Password]** Mã OTP sinh ra ở backend chỉ có 4 chữ số thay vì 6 chữ số theo đặc tả.
11. **[Forgot Password]** Backend chấp nhận đặt lại mật khẩu với mật khẩu cực kỳ yếu (ví dụ: `abc`), bỏ qua quy tắc mật khẩu mạnh.
12. **[Forgot Password]** Biểu thức chính quy (Regex) validator độ mạnh mật khẩu ở frontend viết sai, bắt buộc có khoảng trắng và không cho phép ký tự đặc biệt, chặn toàn bộ mật khẩu mạnh tiêu chuẩn như `NewPass123!`.
13. **[Forgot Password]** Giao diện màn hình đặt lại mật khẩu thiếu hoàn toàn trường nhập "Xác nhận mật khẩu mới".

#### C. Medium (Lỗi hiển thị UI/UX / Phân trang / Thiết kế thiếu) — 10 Bugs
14. **[Product]** Giá sản phẩm không hiển thị đúng định dạng tiền tệ Việt Nam (thiếu ký hiệu `₫` và dấu phân cách hàng nghìn).
15. **[Product]** Trang hiển thị màn hình trắng trơn khi đang tải dữ liệu (không có thông báo Loading).
16. **[Product]** Không hiển thị thông báo Empty State phù hợp khi kết quả tìm kiếm không tìm thấy sản phẩm.
17. **[Order History]** API lịch sử đơn hàng bỏ qua tham số phân trang, luôn trả về toàn bộ dữ liệu.
18. **[User Management]** API xóa người dùng trả về `200 OK` (thành công giả) khi `user_id` không tồn tại.
19. **[User Management]** API xóa người dùng trả về `200 OK` khi `user_id` sai định dạng (ví dụ: `"abc"`).
20. **[User Management]** Trang quản lý người dùng của Admin không hỗ trợ phân trang khi số lượng người dùng lớn.
21. **[Mobile Order]** Các trạng thái đơn hàng hiển thị trên ứng dụng Mobile không có màu sắc phân biệt.
22. **[Mobile Order]** Không hiển thị dialog xác nhận trước khi hủy đơn hàng trên ứng dụng Mobile.
23. **[Forgot Password]** Không hiển thị chỉ báo bước ("Bước 1 / 2") và nút "Quay lại đăng nhập" ở màn hình nhập email.

#### D. Low (Lỗi hiển thị nhỏ / Tiêu chuẩn SEO) — 3 Bugs
24. **[Product]** Khi ảnh sản phẩm bị lỗi không tải được, thẻ ảnh không hiển thị văn bản thay thế `alt` mô tả sản phẩm.
25. **[Product]** Trang chủ chứa nhiều hơn một thẻ `<h1>` (Vi phạm quy tắc cấu trúc HTML).
26. **[Search]** Trang kết quả tìm kiếm sản phẩm chứa nhiều hơn một thẻ `<h1>`.

---

Báo cáo tổng kết được biên soạn nhằm phục vụ đánh giá tính tuân thủ đặc tả và chất lượng sản phẩm phần mềm của hệ thống **EShop**.

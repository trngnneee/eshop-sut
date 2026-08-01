# Báo Cáo Lỗi Giao Diện & Trải Nghiệm Người Dùng (GUI & Usability Bug Report)

Tài liệu này tổng hợp toàn bộ các lỗi phát hiện được trong quá trình thực hiện kiểm thử GUI Checklist (Task 1) và Đánh giá Usability (Task 2) đối với các chức năng FR-04: Personal profile management, FR-11: Order history view (user), và FR-19: User management (admin). Tất cả lỗi được phát hiện phải được log lên GitHub Issues của dự án và đính kèm liên kết kiểm chứng ở dưới.

---

## 1. Tóm Tắt Kết Quả Phát Hiện Lỗi

- **Tổng số lỗi phát hiện:** 5
- **Phân loại theo mức độ nghiêm trọng (Severity):**
  - **Nghiêm trọng / Chặn (Critical/Blocker):** 0
  - **Trung bình (Medium/Major):** 5
  - **Thấp / Thẩm mỹ (Low/Minor):** 0

---

## 2. Danh Sách Lỗi Chi Tiết (Bug Details)

### BUG-01: Ràng buộc Regex số điện thoại tại form cập nhật hồ sơ chặn các số điện thoại Việt Nam bắt đầu bằng '0'
- **Mô tả lỗi:** Biểu mẫu cập nhật hồ sơ cá nhân có kiểm tra tính hợp lệ của trường Số điện thoại bằng biểu thức chính quy `/^[1-9][0-9]{8,9}$/`. Điều này bắt buộc số điện thoại phải bắt đầu bằng chữ số từ 1 đến 9, vô tình loại bỏ tất cả số điện thoại Việt Nam hợp lệ bắt đầu bằng chữ số `0` (ví dụ: `0987654321`), dẫn đến người dùng không thể lưu số điện thoại của mình.
- **Các bước tái hiện (Steps to Reproduce):**
  1. Đăng nhập cổng người dùng bằng tài khoản `test@eshop.com` / `Test1234!`.
  2. Bấm vào tên người dùng ở góc trên bên phải để vào trang Hồ sơ cá nhân (`http://localhost:5173/profile`).
  3. Nhập số điện thoại `0987654321` vào trường "Số điện thoại".
  4. Bấm nút "Cập nhật".
- **Kết quả thực tế (Actual Result):** Hiển thị hộp thoại cảnh báo (alert): "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số." và ngăn không gửi yêu cầu lưu lên backend.
- **Kết quả mong đợi (Expected Result):** Cho phép nhập và lưu số điện thoại Việt Nam hợp lệ bắt đầu bằng số `0` (regex nên là `/^0[0-9]{8,9}$/` hoặc `/^[0-9]{9,10}$/`).
- **Mức độ nghiêm trọng (Severity):** Medium/Major (Lỗi chức năng quan trọng làm người dùng thực tế không thể khai báo số điện thoại liên lạc của họ).
- **Nền tảng phát hiện:** Trình duyệt Chrome / Edge trên Windows 11.
- **Link GitHub Issue:** `https://github.com/trngnneee/eshop-sut/issues/1`
- **Ảnh chụp màn hình lỗi (Có chứa email pqthinh231@clc.fitus.edu.vn watermark):**
  `![BUG-01 Screenshot](./screenshots/bug_profile_phone.png)`

---

### BUG-02: Form cập nhật thông tin cá nhân bị ghi đè hoàn tác dữ liệu cũ do không cập nhật React Context
- **Mô tả lỗi:** Sau khi thực hiện cập nhật thông tin cá nhân hợp lệ (ví dụ: đổi tên và nhập SĐT không bắt đầu bằng 0), form gửi yêu cầu thành công nhưng giao diện form lập tức bị xóa sạch dữ liệu vừa nhập, khôi phục lại các giá trị rỗng/cũ. Nguyên nhân do `useEffect` đồng bộ dữ liệu từ `AuthContext.user` (vẫn lưu thông tin cũ trên bộ nhớ client) đè lên các state cục bộ của form mà không có cơ chế tải lại dữ liệu mới từ server.
- **Các bước tái hiện (Steps to Reproduce):**
  1. Vào trang Hồ sơ cá nhân (`http://localhost:5173/profile`).
  2. Thay đổi Họ tên thành "Test User Updated", Số điện thoại thành "987654321", Địa chỉ thành "123 Nguyen Van Cu".
  3. Bấm nút "Cập nhật" -> hiển thị thông báo "Cập nhật thành công!".
  4. Chuyển sang trang Home rồi quay lại Profile hoặc refresh nhẹ trang.
- **Kết quả thực tế (Actual Result):** Các trường nhập liệu quay trở lại giá trị trống/cũ ban đầu do context không được đồng bộ.
- **Kết quả mong đợi (Expected Result):** Sau khi lưu thành công, thông tin mới cần được đồng bộ vào `AuthContext` hoặc tải lại từ server để hiển thị chính xác dữ liệu vừa cập nhật.
- **Mức độ nghiêm trọng (Severity):** Medium (Lỗi trải nghiệm/logic dữ liệu làm người dùng bối rối vì nghĩ rằng cập nhật không thành công).
- **Nền tảng phát hiện:** Trình duyệt Chrome / Edge trên Windows 11.
- **Link GitHub Issue:** `https://github.com/trngnneee/eshop-sut/issues/2`
- **Ảnh chụp màn hình lỗi (Có chứa email pqthinh231@clc.fitus.edu.vn watermark):**
  `![BUG-02 Screenshot](./screenshots/customer_profile.png)`

---

### BUG-03: Chức năng hủy đơn hàng thực thi lập tức mà không hiển thị hộp thoại xác nhận (Confirm Dialog)
- **Mô tả lỗi:** Khi click nút "Hủy đơn" trong Lịch sử đơn hàng, hệ thống lập tức thực hiện cập nhật trạng thái đơn hàng thành "Đã hủy" (canceled) trên server mà không hiển thị bất kỳ hộp thoại hoặc modal nào hỏi ý kiến người dùng trước.
- **Các bước tái hiện (Steps to Reproduce):**
  1. Tiến hành mua sắm một sản phẩm và checkout thành công để tạo đơn hàng.
  2. Vào trang Profile để xem Lịch sử đơn hàng.
  3. Nhấn vào nút "Hủy đơn" ở cột Thao tác.
- **Kết quả thực tế (Actual Result):** Đơn hàng lập tức đổi trạng thái sang "Đã hủy" và nút biến mất mà không có bước xác nhận.
- **Kết quả mong đợi (Expected Result):** Hệ thống cần hiển thị một thông báo xác nhận như "Bạn có chắc chắn muốn hủy đơn hàng này không?" để tránh người dùng click nhầm.
- **Mức độ nghiêm trọng (Severity):** Medium/Usability (Dễ xảy ra thao tác sai ngoài ý muốn của khách hàng).
- **Nền tảng phát hiện:** Trình duyệt Chrome / Edge trên Windows 11.
- **Link GitHub Issue:** `https://github.com/trngnneee/eshop-sut/issues/3`
- **Ảnh chụp màn hình lỗi (Có chứa email pqthinh231@clc.fitus.edu.vn watermark):**
  `![BUG-03 Screenshot](./screenshots/customer_profile.png)`

---

### BUG-04: Trang Admin - Xóa tài khoản người dùng trực tiếp mà không có hộp thoại xác nhận
- **Mô tả lỗi:** Tại trang quản lý người dùng của Admin, khi nhấn nút "Xóa" bên cạnh tài khoản người dùng, hệ thống lập tức gửi yêu cầu API DELETE và xóa người dùng khỏi cơ sở dữ liệu mà không có cảnh báo hay xác nhận.
- **Các bước tái hiện (Steps to Reproduce):**
  1. Đăng nhập Admin (`admin@eshop.com` / `Admin123!`) tại `http://localhost:5174/`.
  2. Chọn tab "Người dùng" trên thanh sidebar để xem danh sách.
  3. Nhấn vào nút "Xóa" tại hàng của một người dùng bất kỳ.
- **Kết quả thực tế (Actual Result):** Người dùng bị xóa ngay lập tức khỏi bảng danh sách.
- **Kết quả mong đợi (Expected Result):** Phải hiển thị hộp thoại xác nhận (Confirm Dialog) để xác thực hành động xóa tài khoản.
- **Mức độ nghiêm trọng (Severity):** Medium (Rủi ro mất dữ liệu người dùng do click nhầm).
- **Nền tảng phát hiện:** Trình duyệt Chrome / Edge trên Windows 11.
- **Link GitHub Issue:** `https://github.com/trngnneee/eshop-sut/issues/4`
- **Ảnh chụp màn hình lỗi (Có chứa email pqthinh231@clc.fitus.edu.vn watermark):**
  `![BUG-04 Screenshot](./screenshots/admin_users.png)`

---

### BUG-05: Trang Admin - Cột checkbox trong danh sách người dùng là tĩnh và không thực hiện bất kỳ hành động hàng loạt nào
- **Mô tả lỗi:** Bảng quản lý người dùng Admin hiển thị các checkbox ở đầu mỗi hàng và ở tiêu đề cột, cho phép click chọn. Tuy nhiên, các checkbox này là tĩnh (không liên kết với state) và trang web hoàn toàn không có nút hành động hàng loạt (ví dụ: "Xóa các mục đã chọn").
- **Các bước tái hiện (Steps to Reproduce):**
  1. Vào tab "Người dùng" của phân hệ Admin (`http://localhost:5174/`).
  2. Click vào checkbox ở header hoặc từng hàng người dùng.
- **Kết quả thực tế (Actual Result):** Checkbox thay đổi trạng thái chọn/bỏ chọn trực quan nhưng không có bất kỳ nút xử lý hay logic nghiệp vụ nào đi kèm.
- **Kết quả mong đợi (Expected Result):** Nếu đã hiển thị cột checkbox thì phải đi kèm với các chức năng xử lý hàng loạt (bulk actions) như xóa hàng loạt hoặc thay đổi vai trò hàng loạt, hoặc ẩn cột checkbox nếu không có chức năng này.
- **Mức độ nghiêm trọng (Severity):** Low/Minor (Tính năng thừa, chưa hoàn thiện trên giao diện).
- **Nền tảng phát hiện:** Trình duyệt Chrome / Edge trên Windows 11.
- **Link GitHub Issue:** `https://github.com/trngnneee/eshop-sut/issues/5`
- **Ảnh chụp màn hình lỗi (Có chứa email pqthinh231@clc.fitus.edu.vn watermark):**
  `![BUG-05 Screenshot](./screenshots/admin_checkboxes.png)`

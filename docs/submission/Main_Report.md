# Báo Cáo Chính: GUI & Usability Testing Report

Tài liệu này là Báo cáo chính cho bài tập HW03, bao gồm tóm tắt quá trình thực thi kiểm thử GUI Checklist (Task 1) cho các chức năng FR-04: Personal profile management, FR-11: Order history view (user), và FR-19: User management (admin).

---

## 1. Báo Cáo Kiểm Thử GUI (GUI Checklist Report)

### 1.1. Phạm Vi Kiểm Thử (Scope Selected)
- **Màn hình được chọn để xây dựng checklist:**
  1. **Màn hình Hồ sơ cá nhân người dùng (Customer Profile Page)**: Chứa biểu mẫu thông tin cá nhân (FR-04) và danh sách Lịch sử đơn hàng của người dùng (FR-11).
  2. **Màn hình Quản lý người dùng của Admin (Admin User Management Page)**: Chứa bảng hiển thị và các thao tác quản lý danh sách người dùng (FR-19).
- **Lý do lựa chọn:** Đây là các màn hình đại diện cho hai nhóm người dùng chính của hệ thống (Customer và Administrator) và tập trung nhiều tương tác biểu mẫu (Form), bảng dữ liệu (Table), nút hành động (Button) và kiểm tra xác thực (Validation) phức tạp.

### 1.2. Phương Pháp Thực Hiện (Methodology)
- Phân tích mã nguồn frontend và tài liệu yêu cầu hệ thống để định vị các phần tử giao diện chính.
- Sử dụng AI hỗ trợ sinh danh sách 44 mục kiểm thử chi tiết bao phủ 4 khía cạnh tiêu chuẩn giao diện:
  - **IA-01: General UI standards** (Phông chữ, định dạng, căn chỉnh, màu sắc, responsive).
  - **IA-02: Forms** (Ràng buộc, thông báo lỗi, nút bấm, Tab order).
  - **IA-03: Navigation** (Menu, thanh bên sidebar, chuyển hướng link, nút quay lại).
  - **IA-04: Feedback / state** (Thông báo, trạng thái rỗng empty state, màu sắc trạng thái, hover).
- Tiến hành thực thi kiểm thử trực tiếp trên trình duyệt, ghi nhận kết quả và chụp ảnh màn hình minh chứng lỗi có watermark MSSV/Email.

### 1.3. Kết Quả Tổng Quan (General Results)
- Xem bảng chi tiết tại: [GUI_Checklist.md](./GUI_Checklist.md)
- **Tổng số checklist item đã thiết kế:** 43
- **Tổng số item Đạt (Passed):** 34
- **Tổng số item Không đạt (Failed):** 9
- **Tỉ lệ đạt:** 79.1%
- **Phân tích các khía cạnh lỗi:**
  - **Khía cạnh Forms (IA-02)** và **Feedback / state (IA-04)** gặp nhiều lỗi nhất (mỗi nhóm có 3-4 lỗi). Điển hình là lỗi ràng buộc biểu thức chính quy (Regex) của số điện thoại chặn các số bắt đầu bằng `0`, thiếu hộp thoại xác nhận khi thực hiện hành động hủy đơn hoặc xóa người dùng trực tiếp, và các checkbox trong danh sách Admin là checkbox tĩnh không có chức năng bulk actions.
  - **Khía cạnh General UI (IA-01)** là khía cạnh tốt nhất khi hầu hết phông chữ, định dạng tiền tệ, và thiết kế responsive cho màn hình di động hoạt động đúng tiêu chuẩn hiển thị.

---

## 2. Báo Cáo Đánh Giá Usability (Usability Evaluation Report)

*(Nội dung phần này được ghi nhận chi tiết riêng trong các tài liệu khảo sát trải nghiệm người dùng thực tế và ghi chép Usability Session)*

- Xem chi tiết tại: [Usability_Session_Evidence.md](./Usability_Session_Evidence.md)

---

## 3. Kiểm Thử Đa Nền Tảng (Cross-Browser / Cross-Platform)

- **Các trình duyệt/nền tảng đã kiểm thử:**
  1. **Chrome 127 (Windows 11)** - Nền tảng chính cho việc thực thi kiểm thử và tìm lỗi.
  2. **Microsoft Edge 127 (Windows 11)** - Dùng để xác minh tính tương thích chéo của các form và bảng dữ liệu.
  3. **Mobile Responsive Mode (Chrome DevTools - iPhone 12 Pro & Pixel 7)** - Kiểm tra khả năng co giãn responsive của trang Cá nhân và bảng lịch sử đơn hàng.
- Xem chi tiết danh sách ảnh chụp màn hình kiểm chứng tại: [Cross_Platform_Evidence.md](./Cross_Platform_Evidence.md)

---

## 4. Kỹ Năng Agent (Agent Skills)

### 4.1. Mô Tả Kỹ Năng Đã Xây Dựng
- **Tên kỹ năng:** `gui_testing`
- **Chức năng chính:** Kỹ năng hỗ trợ thiết kế danh sách kiểm thử giao diện (GUI Checklist), tự động hóa các bước kiểm thử Black-box trên trình duyệt thông qua Playwright, phát hiện các hành vi sai lệch giao diện và tự động cập nhật đồng bộ các báo cáo tài liệu bàn giao (`GUI_Checklist.md`, `Bug_Report.md`, `Main_Report.md`).
- **Cách thức hoạt động:**
  1. Agent đọc cấu hình và hướng dẫn kỹ năng tại `c:\Users\Public\Projects\Testing_HCMUS\HW3\eshop-sut\.agents\skills\gui_testing\SKILL.md`.
  2. Dựa vào các khía cạnh kiểm thử GUI tiêu chuẩn (IA-01 đến IA-04) và các mô tả màn hình, Agent sinh danh sách checklist trống gồm hơn 40 mục cụ thể.
  3. Agent sử dụng Browser Subagent để duyệt qua các màn hình SUT, điền thông tin biểu mẫu và tương tác các nút bấm để kiểm thử.
  4. Từ các lỗi giao diện phát hiện được, Agent viết kịch bản Python chụp và đánh watermark MSSV lên ảnh chụp màn hình, sau đó cập nhật kết quả tự động vào các báo cáo.

### 4.2. Minh Chứng Video (Demo Video Links)
- **Link YouTube:** `[Chèn liên kết video Youtube chứng minh chạy Agent Skill từ đầu đến cuối]`
- **Mô tả nội dung video:** Video dài mô tả quá trình Agent khởi chạy các server SUT, thiết kế checklist, chạy browser subagent để thực thi kiểm thử trên trang Hồ sơ cá nhân (khách hàng) và trang Quản trị (Admin), phát hiện lỗi validate SĐT và xóa tài khoản không có cảnh báo, sau đó tự động chèn watermark và xuất bản báo cáo lỗi.

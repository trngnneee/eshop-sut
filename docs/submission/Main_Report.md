# Báo Cáo Chính: GUI & Usability Testing Report

Tài liệu này là Báo cáo chính cho bài tập HW03, bao gồm tóm tắt quá trình thực thi kiểm thử GUI Checklist, đánh giá trải nghiệm người dùng (Usability Evaluation) và Kỹ năng Agent (Agent Skills).

---

## 1. Báo Cáo Kiểm Thử GUI (GUI Checklist Report)

### 1.1. Phạm Vi Kiểm Thử (Scope Selected)
- **Màn hình được chọn để xây dựng checklist:** `[Liệt kê các màn hình, ví dụ: Trang chủ (Home), Giỏ hàng (Cart), Đăng ký (Register)]`
- **Lý do lựa chọn:** `[Giải thích lý do lựa chọn các màn hình này cho việc đánh giá chuẩn GUI]`

### 1.2. Phương Pháp Thực Hiện (Methodology)
- Sử dụng AI để sinh danh sách checklist ban đầu dựa trên các khía cạnh giao diện (IA-01 đến IA-04).
- Rà soát thủ công, bổ sung các phần AI bỏ sót (như Accessibility, Dark mode, RTL layout, responsive,...).
- Tiến hành chạy thử nghiệm (test execution) trên hệ thống SUT và ghi nhận trạng thái Đạt (Passed)/Không đạt (Failed).

### 1.3. Kết Quả Tổng Quan (General Results)
- Xem bảng chi tiết tại: [GUI_Checklist.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/GUI_Checklist.md)
- Phân tích các khía cạnh bị lỗi nhiều nhất: `[Phân tích khía cạnh nào như biểu mẫu, điều hướng, trạng thái phản hồi gặp nhiều lỗi nhất]`

---

## 2. Báo Cáo Đánh Giá Usability (Usability Evaluation Report)

### 2.1. Mục Tiêu Kiểm Thử (Objectives)
- Xác định các điểm nghẽn (bottlenecks) trong luồng thao tác của người dùng.
- Đo lường mức độ dễ sử dụng và mức độ hài lòng của người dùng thông qua chỉ số SUS / UEQ-S.
- Thu thập phản hồi định tính để cải thiện giao diện.

### 2.2. Kịch Bản Nhiệm Vụ (Task Scenario)
- **Luồng kiểm thử đầu-cuối được chọn:** `[Mô tả luồng, ví dụ: Đăng ký -> Chọn sản phẩm -> Áp dụng mã giảm giá -> Thanh toán]`
- **Kịch bản giao cho người dùng:** `[Mô tả kịch bản thực tế không chứa các bước hướng dẫn cụ thể từng click chuột]`

### 2.3. Kết Quả Đo Lường Định Lượng (Quantitative Analysis)
- **Điểm số SUS / UEQ-S trung bình:** `[Điểm số]`
- **Nhận xét kết quả:** `[Đánh giá hệ thống đạt mức Excellent, Good, OK, hay Poor dựa trên thang đo chuẩn]`

### 2.4. Tổng Hợp & Phân Tích Định Tính (Qualitative Analysis & Synthesis)
- **Các điểm nghẽn/vấn đề chung (Friction points):** `[Mô tả các hành vi ngập ngừng, bối rối của người dùng]`
- **Phân loại lỗi theo mức độ nghiêm trọng (Severity):**
  - **Blockers (Lỗi chặn dòng tác vụ):** `[Mô tả]`
  - **Major (Lỗi lớn gây khó khăn lớn):** `[Mô tả]`
  - **Minor (Lỗi nhỏ/thẩm mỹ):** `[Mô tả]`

---

## 3. Kiểm Thử Đa Nền Tảng (Cross-Browser / Cross-Platform)

- **Các trình duyệt/nền tảng đã kiểm thử:**
  1. Trình duyệt 1: Chrome (Windows/macOS)
  2. Trình duyệt 2: Firefox / Safari (macOS/iOS)
  3. Trình duyệt 3 (hoặc Mobile): Android Chrome / Expo Go trên điện thoại thực tế.
- Xem chi tiết danh sách ảnh chụp màn hình kiểm chứng tại: [Cross_Platform_Evidence.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/Cross_Platform_Evidence.md)

---

## 4. Kỹ Năng Agent (Agent Skills)

### 4.1. Mô Tả Kỹ Năng Đã Xây Dựng
- **Tên kỹ năng:** `[Tên kỹ năng, ví dụ: GUI_Checklist_Generator hoặc Usability_Session_Analyzer]`
- **Chức năng chính:** Kỹ năng giúp tự động hóa việc sinh các kịch bản kiểm thử giao diện hoặc phân tích phản hồi người dùng sau buổi test.
- **Cách thức hoạt động:** `[Mô tả ngắn gọn quy trình hoạt động của skill]`

### 4.2. Minh Chứng Video (Demo Video Links)
- **Link YouTube:** `[Chèn liên kết video Youtube chứng minh chạy Agent Skill từ đầu đến cuối]`
- **Mô tả nội dung video:** `[Tóm tắt những gì được thể hiện trong video]`

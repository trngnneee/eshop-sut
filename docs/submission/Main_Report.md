# Báo Cáo Chính: GUI & Usability Testing Report

| Student name (printed): | Phan Quốc Thịnh |
| :---- | :---- |
| **Student ID:** | 23127486 |
| **Class / Cohort:** | 23CLC3 |
| **Course:** | CS423 / CSC13003 – Software Testing |
| **Instructor:** | Dr. Lam Quang Vu / Dr. Tran Duy Hoang |
| **Date:** | 01/08/2026 |
| **Signature:** | Phan Quốc Thịnh |

---

## 1. Báo Cáo Kiểm Thử GUI (GUI Checklist Report)

### 1.1. Phạm Vi Kiểm Thử (Scope Selected)
- **Màn hình được chọn để xây dựng checklist:**
  1. **Màn hình Hồ sơ cá nhân người dùng (Customer Profile Page)**: Chứa biểu mẫu thông tin cá nhân (FR-04) và danh sách Lịch sử đơn hàng của người dùng (FR-11).
  2. **Màn hình Quản lý người dùng của Admin (Admin User Management Page)**: Chứa bảng hiển thị và các thao tác quản lý danh sách người dùng (FR-19).
- **Lý do lựa chọn:** Đây là các màn hình đại diện cho hai nhóm người dùng chính của hệ thống (Customer và Administrator) và tập trung nhiều tương tác biểu mẫu (Form), bảng dữ liệu (Table), nút hành động (Button) và kiểm tra xác thực (Validation) phức tạp.

### 1.2. Phương Pháp Thực Hiện (Methodology)
- Phân tích tài liệu yêu cầu hệ thống để định vị các phần tử giao diện chính.
- Sử dụng AI hỗ trợ sinh danh sách 44 mục kiểm thử chi tiết bao phủ 4 khía cạnh tiêu chuẩn giao diện:
  - **IA-01: General UI standards** (Phông chữ, định dạng, căn chỉnh, màu sắc, responsive).
  - **IA-02: Forms** (Ràng buộc, thông báo lỗi, nút bấm, Tab order).
  - **IA-03: Navigation** (Menu, thanh bên sidebar, chuyển hướng link, nút quay lại).
  - **IA-04: Feedback / state** (Thông báo, trạng thái rỗng empty state, màu sắc trạng thái, hover).
- Tiến hành thực thi kiểm thử trực tiếp trên trình duyệt, ghi nhận kết quả và chụp ảnh màn hình minh chứng lỗi có watermark MSSV/Email.

### 1.3. Kết Quả Tổng Quan (General Results)
- Xem bảng chi tiết tại: [GUI_Checklist.md](./GUI_Checklist.md)
- **Tổng số màn hình kiểm thử:** 2 (Web Customer Profile, Web Admin User Management)
- **Tổng số checklist item đã thiết kế:** 41 (Sau khi đã kiểm chứng)
- **Tổng số item Đạt (Passed):** 32
- **Tổng số item Không đạt (Failed):** 9
- **Tỉ lệ đạt:** 78.0%
- **Phân tích các khía cạnh lỗi:**
  - **Khía cạnh Forms (IA-02)** và **Feedback / state (IA-04)** gặp nhiều lỗi nhất (mỗi nhóm có 3-4 lỗi). Điển hình là lỗi của ô nhập số điện thoại ở trang profile chặn các số bắt đầu bằng `0`, thông báo lỗi Số điện thoại chỉ hiển thị qua popup `alert()`, thiếu dấu sao đỏ bắt buộc cho trường Họ tên, thiếu chỉ báo tải dữ liệu (loading indicator) khi tải Lịch sử đơn hàng, và trang quản trị Admin xóa tài khoản người dùng trực tiếp mà không hiển thị hộp thoại xác nhận.
  - **Khía cạnh General UI (IA-01)** là khía cạnh tốt nhất khi hầu hết phông chữ, định dạng tiền tệ, và thiết kế responsive cho màn hình di động hoạt động đúng tiêu chuẩn hiển thị.

*Xem thêm bảng chi tiết lỗi Usability trong [Bug_Report.md#2-danh-sach-loi-chi-tiet-bug-details](./Bug_Report.md#2-danh-sach-loi-chi-tiet-bug-details) (từ BUG-01 đến BUG-09).*

---

## 2. Báo Cáo Đánh Giá Usability (Usability Evaluation Report)

Quá trình đánh giá Usability (Task 2) được thực hiện với **7 người tham gia thực tế** nhằm khảo sát trải nghiệm người dùng đối với tính năng nhập liệu sản phẩm hàng loạt bằng file CSV ở phân hệ Web Admin.

### 2.1. Giới thiệu & Đối tượng tham gia
Nghiên cứu tuyển chọn thành công 7 người dùng thực tế với sự đa dạng cao về đối tượng và nền tảng công nghệ:
- **IT (5 người):** Võ Ngọc Bích Trâm (P1 - Pilot), Nguyễn Thanh Gia Bảo (P2), Đặng Trường Nguyên (P4), Trương Lý Khải (P5), Lê Trương Bảo Ngọc (P7). Cả 5 người tham gia đều thuộc khối ngành Công nghệ thông tin (IT) từ Trường Đại học Khoa học Tự nhiên (HCMUS).
- **Non-IT (2 người):** Phan Yến Anh (P3) và Nguyễn Vũ Thiên Tú (P6). Cả 2 người tham gia đều thuộc khối ngành ngoài CNTT (Non-IT) từ Trường Đại học Kinh tế TP.HCM (UEH).
- Thông tin chi tiết về danh sách người tham gia được ghi nhận đầy đủ tại [Usability_Session_Evidence.md#2-bang-danh-sach-7-nguoi-tham-gia-table-of-7-participants](./Usability_Session_Evidence.md#2-bang-danh-sach-7-nguoi-tham-gia-table-of-7-participants).

### 2.2. Kịch Bản Nhiệm Vụ (Task Scenario)
Người tham gia đóng vai trò là một Quản trị viên (Admin) mới của EShop và được giao chuỗi nhiệm vụ:
1. Đăng nhập vào tài khoản admin được cấp sẵn.
2. Thực hiện nhập liệu hàng loạt từ tệp chứa lỗi `import_i.csv` (thiếu tên sản phẩm ở dòng 2) và kiểm tra danh sách sản phẩm bên dưới xem hệ thống có rollback toàn bộ giao dịch hay không.
3. Thực hiện nhập liệu hàng loạt từ tệp hợp lệ `import_v.csv` và kiểm tra lại danh sách sản phẩm xem các sản phẩm mới đã được chèn đầy đủ chưa.

### 2.3. Nhận Xét Định Lượng (Quantitative Analysis)
- **Điểm SUS Trung Bình:** **67.8 / 100**
- **Xếp Loại:** **OK (Trung bình)**
  - Theo thang đo System Usability Scale (SUS) chuẩn:
    - *Excellent:* > 80.3
    - *Good:* 68 - 80.3
    - *OK:* 51 - 67.9
    - *Poor:* < 51
  - Với điểm số 67.8, hệ thống dừng ở mức độ trung bình (cận trên của mức OK, sát mức Good), người dùng có thể học và thực hiện tác vụ tương đối nhanh nhưng chưa hoàn toàn thỏa mãn về cách phản hồi và xử lý lỗi của hệ thống.
- **Chi tiết điểm SUS từng cá nhân:** P4 (IT) chấm điểm cao nhất (85.0), trong khi P5 (IT) gặp nhiều khó khăn nhất chấm điểm thấp nhất (50.0). Các người tham gia còn lại chấm quanh mức 57.5 - 72.5. Xem chi tiết bảng điểm tại [Usability_Session_Evidence.md#4-ket-qua-thang-do-usability-sus--ueq-s-score-sheet](./Usability_Session_Evidence.md#4-ket-qua-thang-do-usability-sus--ueq-s-score-sheet).

### 2.4. Phân Tích Định Tính (Qualitative Analysis)
#### Gom nhóm các khó khăn và điểm nghẽn chính (Friction Points):
1. **Lỗi logic/Tính toàn vẹn dữ liệu:** Không thực hiện rollback khi import file lỗi. Sản phẩm hợp lệ ở dòng đầu vẫn bị chèn dở dang vào backend.
2. **Bất nhất thị giác:** Hộp thông báo màu xanh lá (thành công) hiển thị chi tiết dòng lỗi màu đỏ gây bối rối.
3. **Tiện ích giao diện:** Thiếu các nút hành động dọn dẹp như xóa thông báo lỗi hoặc hủy file đã chọn.
4. **Hiển thị & Bố cục:** Phông chữ xem trước (preview table) quá nhỏ khó đọc; khu vực Import sản phẩm nằm ở vị trí khuất, chưa đủ nổi bật.
5. **Chỉnh sửa dữ liệu:** Bảng xem trước ở trạng thái chỉ đọc (Read-only), không cho phép chỉnh sửa dữ liệu lỗi tại chỗ.
6. **Hiệu năng:** Gặp hiện tượng giật/lag nhẹ khi cuộn danh sách xem trước dài.

#### Phân loại lỗi Usability theo mức độ nghiêm trọng:
- **Blockers (Lỗi chặn dòng tác vụ):** 0
- **Major Usability Issues (Lỗi lớn gây cản trở/hiểu nhầm):** 2 lỗi
  - *Không rollback giao dịch khi có dòng dữ liệu lỗi* (BUG-10)
  - *Hộp cảnh báo hiển thị mâu thuẫn trực quan xanh/đỏ* (BUG-11)
- **Minor Usability Issues (Lỗi nhỏ / Trải nghiệm kém):** 5 lỗi (Vùng import chưa nổi bật - BUG-12, thiếu nút hủy file/kết quả - BUG-13, font chữ preview nhỏ - BUG-14, preview read-only - BUG-15; và 1 vấn đề nhỏ về hiệu năng cuộn lag nhẹ không đưa vào bug report).

*Xem thêm bảng chi tiết lỗi Usability trong [Bug_Report.md#2-danh-sach-loi-chi-tiet-bug-details](./Bug_Report.md#2-danh-sach-loi-chi-tiet-bug-details) (từ BUG-10 đến BUG-15).*

---

## 3. Kiểm Thử Đa Nền Tảng (Cross-Browser / Cross-Platform)

- **Các trình duyệt/nền tảng đã kiểm thử:**
  1. **Google Chrome v127 (Windows 11)** - Nền tảng chính cho việc thực thi kiểm thử và tìm lỗi (chạy cục bộ).
  2. **Mozilla Firefox v127 (Windows 11)** - Dùng để xác minh tính tương thích chéo của giao diện trên trình duyệt khác (chạy cục bộ).
  3. **Mobile - Expo Go (Mobile App)** - Chạy ứng dụng di động thực tế hoặc giả lập qua Expo Go kết nối với máy chủ phát triển cục bộ.
- Xem chi tiết danh sách ảnh chụp màn hình kiểm chứng tại: [Cross_Platform_Evidence.md](./Cross_Platform_Evidence.md)

---

## 4. Kỹ Năng Agent (Agent Skills)

### 4.1. Mô Tả Kỹ Năng Đã Xây Dựng
1. **`gui_testing`**
   - **Chức năng chính:** Kỹ năng hỗ trợ thiết kế danh sách kiểm thử giao diện (GUI Checklist), tự động hóa các bước kiểm thử Black-box trên trình duyệt thông qua Playwright, phát hiện các hành vi sai lệch giao diện và tự động cập nhật đồng bộ các báo cáo tài liệu bàn giao (`GUI_Checklist.md`, `Bug_Report.md`, `Main_Report.md`).
   - **Cách thức hoạt động:**
     - Agent đọc hướng dẫn kỹ năng tại [GUI Testing Skill](./.agents/skills/gui_testing/SKILL.md).
     - Dựa vào các khía cạnh kiểm thử GUI tiêu chuẩn (IA-01 đến IA-04), Agent sinh danh sách checklist ban đầu gồm hơn 40 mục cụ thể.
     - Agent sử dụng Browser Subagent để duyệt qua các màn hình SUT, tương tác với giao diện để thực thi kiểm thử. 
     - Ghi nhận lỗi và chạy script chèn watermark MSSV/Email lên ảnh chụp màn hình và xuất bản báo cáo lỗi.

2. **`usability_testing_plan`**
   - **Chức năng chính:** Hướng dẫn thiết kế kịch bản tác vụ hướng mục tiêu (goal-oriented), chuẩn bị công cụ đo lường trải nghiệm (thang đo SUS, câu hỏi phỏng vấn đào sâu Probe Questions), lập kế hoạch tuyển chọn 7 người tham gia thực tế (bảo mật thông tin cá nhân) và dựng sẵn cấu trúc ghi chép (Session Notes) cho Usability Testing.
   - **Cách thức hoạt động:**
     - Agent đọc hướng dẫn kỹ năng tại [Usability Testing Plan](./.agents/skills/usability_testing_plan/SKILL.md).
     - Thiết lập kịch bản đóng vai trò thực tế (ví dụ: Admin import CSV).
     - Tạo cấu trúc bảng biểu danh sách người tham gia, mẫu khảo sát SUS và dựng sẵn các khung ghi chép quan sát trống cho 7 buổi test tại `Usability_Session_Evidence.md`.

3. **`usability_testing_analysis`**
   - **Chức năng chính:** Hướng dẫn xử lý dữ liệu định lượng (tính điểm quy đổi thang đo SUS của từng cá nhân và điểm trung bình hệ thống), tổng hợp định tính (gom nhóm các điểm nghẽn Friction Points của người dùng), phân loại lỗi usability theo mức độ nghiêm trọng (Blocker, Major, Minor) và đồng bộ kết quả vào các báo cáo.
   - **Cách thức hoạt động:**
     - Agent đọc hướng dẫn kỹ năng tại [Usability Testing Analysis](./.agents/skills/usability_testing_analysis/SKILL.md).
     - Áp dụng công cụ tính toán quy đổi điểm SUS chuẩn cho từng người dùng dựa trên phản hồi của họ.
     - Tổng hợp các lỗi usability và log chi tiết vào `Bug_Report.md` (từ BUG-10 đến BUG-15).
     - Cập nhật và đồng bộ hóa báo cáo tổng hợp tại `Main_Report.md` và `README.md`.

### 4.2. Minh Chứng Video (Demo Video Links)
- **Link YouTube:** [Link Youtube](https://youtu.be/dDhML8fNRlY)
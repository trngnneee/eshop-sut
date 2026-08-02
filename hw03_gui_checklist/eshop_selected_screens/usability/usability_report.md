# Usability Evaluation Report (Task 2)
## EShop Admin — Quản lý Sản phẩm

| Thông tin đánh giá | Chi tiết |
|---|---|
| **Flow được đánh giá** | Admin Login → Product Management → Add Product → Edit Product → Delete Product |
| **Phương pháp** | Moderated Usability Evaluation (Đánh giá tính dễ sử dụng có người điều phối) |
| **Thang đo định lượng** | SUS (System Usability Scale - 10 câu hỏi Likert 5 mức độ) |
| **Số người tham gia** | 7 người (100% người dùng thật, ngoài ngành IT/sinh viên) |
| **Môi trường thử nghiệm** | Frontend Admin Web (http://localhost:5174/ - Tab Sản phẩm) |
| **Ngày hoàn tất thử nghiệm** | 01/08/2026 |

---

## 1. Tổng quan & Mục tiêu Đánh giá (Objectives & Task Scenario)

### 1.1. Mục tiêu kiểm thử
1. **Clarity (Sự rõ ràng):** Đánh giá xem người dùng có hiểu ngay luồng thao tác quản lý sản phẩm (Thêm, Sửa, Xóa) mà không cần hướng dẫn hay trợ giúp kỹ thuật hay không.
2. **Efficiency (Hiệu quả & Tốc độ):** Đo lường mức độ thuận lợi và thời gian thực hiện tác vụ từ khi đăng nhập đến khi hoàn thành các thao tác CRUD.
3. **Error Recovery (Phục hồi lỗi & Phản hồi):** Đánh giá khả năng tự nhận biết, xử lý lỗi nhập liệu và sự hoang mang của người dùng khi gặp lỗi giao diện/hệ thống.
4. **Trust (Sự tin tưởng & An toàn dữ liệu):** Đánh giá mức độ tự tin và an tâm của người dùng khi thực hiện các thao tác quan trọng (đặc biệt là chỉnh sửa và xóa sản phẩm).

### 1.2. Kịch bản Tác vụ (Task Scenario)
Đã cung cấp Task Scenario A nguyên văn cho 7 người tham gia:
> *"EShop cần cập nhật kho hàng. Bạn là người quản trị — hãy đăng nhập và thêm một sản phẩm mới bất kỳ (tên, giá, danh mục tự chọn). Sau đó cập nhật lại giá của sản phẩm vừa tạo, rồi xóa 1 sản phẩm khỏi danh sách vì hàng hết."*

---

## 2. Thông tin Người tham gia (Participants Summary)

| Mã | Họ tên | Giới tính | Tuổi | Nghề nghiệp | IT Background | Liên hệ (masked) | Kết quả Tác vụ |
|---|---|---|---|---|---|---|---|
| **P01** | Nguyễn Phạm Quỳnh Như | Nữ | 20 | Sinh viên | Không | `058****545` | Hoàn thành (có ngập ngừng) |
| **P02** | Nguyễn Minh Kha | Nam | 21 | Sinh viên | Có | `032****338` | Hoàn thành (có ngập ngừng) |
| **P03** | Trần Thành Thịnh | Nam | 21 | Sinh viên | Không | `081****668` | Hoàn thành (có ngập ngừng) |
| **P04** | Đặng Trường Nguyên | Nam | 21 | Sinh viên | Có | `091****029` | Hoàn thành (có ngập ngừng) |
| **P05** | Nguyễn Trần Quốc Duy | Nam | 21 | Sinh viên | Có | `ntqduy23@clc...` | Hoàn thành (có ngập ngừng) |
| **P06** | Lê Trương Bảo Ngọc | Nữ | 21 | Sinh viên | Có | `084****506` | Hoàn thành (có ngập ngừng) |
| **P07** | Nguyễn Thanh Tiến | Nam | 21 | Sinh viên | Có | `093****577` | Hoàn thành (có ngập ngừng) |

*Ghi chú: 100% (7/7) người tham gia hoàn thành được flow nhưng đều gặp sự ngập ngừng/hoang mang (hesitation) ở bước Chỉnh sửa sản phẩm.*

---

## 3. Kết quả Thang đo Định lượng SUS (System Usability Scale)

### 3.1. Bảng dữ liệu câu trả lời thô (Raw SUS Responses)
Mỗi câu hỏi được chấm trên thang Likert 1 (Hoàn toàn không đồng ý) đến 5 (Hoàn toàn đồng ý).
*Lưu ý: Các câu lẻ (Q1, Q3, Q5, Q7, Q9) mang ý nghĩa tích cực; Các câu chẵn (Q2, Q4, Q6, Q8, Q10) mang ý nghĩa tiêu cực.*

| Mã P | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Điểm SUS (0-100) | Xếp loại Benchmark |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **P01** | 3 | 2 | 3 | 5 | 2 | 5 | 3 | 3 | 1 | 5 | **30.0** | F / Kém (Poor) |
| **P02** | 2 | 3 | 2 | 4 | 1 | 5 | 4 | 5 | 2 | 3 | **27.5** | F / Kém (Poor) |
| **P03** | 3 | 2 | 4 | 2 | 4 | 3 | 4 | 3 | 3 | 2 | **65.0** | D / Dưới trung bình |
| **P04** | 3 | 1 | 4 | 1 | 3 | 4 | 5 | 2 | 3 | 1 | **72.5** | B-C / Trên trung bình |
| **P05** | 1 | 2 | 4 | 1 | 2 | 5 | 5 | 2 | 2 | 3 | **52.5** | D / Dưới trung bình |
| **P06** | 1 | 2 | 4 | 1 | 2 | 5 | 5 | 2 | 2 | 3 | **52.5** | D / Dưới trung bình |
| **P07** | 1 | 2 | 4 | 1 | 2 | 5 | 5 | 2 | 2 | 3 | **52.5** | D / Dưới trung bình |
| **Trung bình** | - | - | - | - | - | - | - | - | - | - | **50.4** | **F / Kém (Poor)** |

### 3.2. Phân tích kết quả SUS
- **Điểm SUS Trung bình:** **50.4 / 100**
- **Đánh giá theo Benchmark ngành:** Ngưỡng trung bình chuẩn (Average SUS Benchmark) của ứng dụng web là **68.0 điểm**. Với điểm số **50.4**, tính dễ sử dụng của phân hệ Admin EShop xếp mức **F / Poor (Dưới trung bình / Kém)**.
- **Nguyên nhân chính khiến điểm SUS thấp:**
  1. **Q6 (Sự mâu thuẫn/Inconsistency) đạt điểm 5/5 ở 5/7 người dùng:** Lỗi hiển thị ghi đè tên của toàn bộ danh sách sản phẩm khi sửa 1 sản phẩm khiến người dùng nhận thấy sự thiếu đồng nhất nghiêm trọng trong phản hồi hệ thống.
  2. **Q9 (Độ tự tin khi sử dụng/Confidence) bị kéo xuống mức 1-2/5:** Sau khi chứng kiến toàn bộ danh sách sản phẩm bị đổi tên, người dùng hoàn toàn mất niềm tin vào việc dữ liệu có đang bị hư hỏng hay không.
  3. **Thiếu phản hồi xác nhận (Q5, Q8):** Việc không có Toast thông báo khi Thêm/Sửa và thiếu popup xác nhận khi Xóa khiến người dùng cảm thấy hệ thống cồng kềnh và khó kiểm soát.

---

## 4. Phân nhóm Vấn đề Trải nghiệm (Thematic Pain Points & Synthesis)

Qua tổng hợp quan sátThink-Aloud và câu hỏi Probe từ 7 phiên kiểm thử, các vấn đề được phân thành 4 nhóm chủ đề chính:

### Theme 1: Lỗi đồng bộ dữ liệu giao diện khi Sửa sản phẩm (Global State Mutation)
- **Tần suất:** 7/7 người tham gia (100%)
- **Mô tả:** Khi chọn nút "Sửa" ở một sản phẩm và bấm "Lưu", toàn bộ tên các sản phẩm khác trong danh sách Admin ngay lập tức bị ghi đè hiển thị bằng tên sản phẩm vừa sửa.
- **Tác động:** Tạo ra tâm lý hoang mang tột độ cho người dùng. Người dùng P01, P02, P03 tưởng mình làm hỏng toàn bộ cơ sở dữ liệu. P04 phải thử chuyển trang sang Dashboard rồi quay lại để kiểm tra; P05 thấy tên bị đổi nhưng giá giữ nguyên gây mâu thuẫn dữ liệu.

### Theme 2: Thiếu phản hồi xác nhận & Nhận biết trạng thái Form (Feedback & State Visibility)
- **Tần suất:** 5/7 người tham gia (71.4%)
- **Mô tả:**
  1. **Thiếu thông báo thành công:** Khi bấm "Thêm sản phẩm" hoặc "Lưu", hệ thống không có bất kỳ Toast/Banner thông báo nào xác nhận "Thao tác thành công". P02 và P06 hoang mang không biết nút bấm có ăn hay không, dẫn đến việc P06 nhấp lưu liên tục nhiều lần.
  2. **Nhập nhằng giữa Mode Thêm và Mode Sửa:** Nút "Sửa" nạp dữ liệu lên Form ở trên nhưng tiêu đề Form vẫn ghi "Thêm sản phẩm", không có nút "Hủy" và không tự động cuộn màn hình. P06 tưởng không có chức năng sửa vì chờ popup xuất hiện.

### Theme 3: Rủi ro An toàn dữ liệu khi Xóa (Data Safety & Confirmation)
- **Tần suất:** 7/7 người tham gia (100% quan sát & phản hồi Probe)
- **Mô tả:** Khi nhấp nút "Xóa", hệ thống lập tức xóa sản phẩm khỏi danh sách mà không có Hộp thoại xác nhận (Confirmation Dialog).
- **Tác động:** Mặc dù thao tác diễn ra nhanh, người dùng cho biết cảm thấy "lo sợ" và "không an toàn" nếu bấm nhầm nút Xóa trong thực tế quản trị kho hàng.

### Theme 4: Trải nghiệm Nhập liệu & Định dạng Giá tiền (Input & Formatting)
- **Tần suất:** 3/7 người tham gia (42.8%)
- **Mô tả:**
  1. **Xử lý khoảng trắng ở ô Giá tiền:** P05 nhập số tiền có khoảng trắng (`40 000 000`) bị báo lỗi tiếng Anh chung chung `"Please enter a number."` mà không tự động trim hoặc hướng dẫn định dạng.
  2. **Thiếu phân cách hàng nghìn:** P07 nhận xét ô nhập giá và hiển thị giá trong bảng thiếu dấu chấm/phẩy phân cách hàng nghìn, gây khó đọc và dễ nhầm lẫn số lượng chữ số 0.

---

## 5. Phân loại Mức độ Nghiêm trọng (Severity Classification Matrix)

Các vấn đề được phân cấp theo 3 mức độ chuẩn: **Blocker/Critical** (Chặn tác vụ/Gây hỏng dữ liệu), **Major** (Gây trở ngại lớn/Gây hoang mang), **Minor** (Lỗi thẩm mỹ/Nhỏ).

| Mã Vấn đề | Tóm tắt Vấn đề | Tần suất | Mức độ Nghiêm trọng (Severity) | Độ ưu tiên Fix (Priority) | Phân loại |
|---|---|---|---|---|---|
| **ISSUE-01** | Khi sửa 1 sản phẩm, danh sách admin cập nhật đè tên của tất cả sản phẩm khác | 7/7 (100%) | **Critical** | **P0** | System Bug |
| **ISSUE-02** | Xóa sản phẩm lập tức mà không hiển thị Hộp thoại xác nhận (Confirmation Modal) | 7/7 (100%) | **Major** | **P1** | Design & Safety Issue |
| **ISSUE-03** | Form Admin thiếu thông báo phản hồi (Toast/Alert) khi Thêm/Sửa thành công | 5/7 (71.4%) | **Major** | **P2** | Feedback / UX Issue |
| **ISSUE-04** | Giao diện không đổi tiêu đề và thiếu chỉ báo trạng thái Chế độ Sửa (Edit Mode) | 4/7 (57.1%) | **Major** | **P2** | State Visibility Issue |
| **ISSUE-05** | Ô nhập Giá sản phẩm không tự động loại bỏ khoảng trắng và thiếu phân cách hàng nghìn | 3/7 (42.8%) | **Minor** | **P3** | Input Formatting Issue |

---

## 6. Báo cáo Lỗi & Quản lý Bug (Bug Reports Summary)

Tuân thủ nguyên tắc: **Ưu tiên báo cáo bug mới, không tạo trùng lặp các bug đã được ghi nhận từ trước**.

### 6.1. Bảng tổng hợp các Bug Report liên quan đến Task 2

| Bug ID | Tóm tắt Bug Report | Trạng thái File Bug Report | Đường dẫn File Bug Report |
|---|---|---|---|
| **BUG-01** | `[BUG][Admin] Khi sửa một sản phẩm, danh sách admin cập nhật đè tên của tất cả sản phẩm khác` | Đã tồn tại từ trước (GUI Checklist) | [bug_admin_fake_mass_update.md](../bugs/bug_admin_fake_mass_update.md) |
| **BUG-02** | `[BUG][Admin] Không có hộp thoại xác nhận trước khi xóa sản phẩm` | Đã tồn tại từ trước (GUI Checklist) | [bug_admin_no_delete_confirm.md](../bugs/bug_admin_no_delete_confirm.md) |
| **BUG-03** *(MỚI)* | `[BUG][Admin] Form Admin thiếu thông báo phản hồi (Toast/Alert) sau khi Thêm hoặc Sửa sản phẩm thành công` | **MỚI tạo từ Usability Test** | [bug_admin_form_success_feedback.md](../bugs/bug_admin_form_success_feedback.md) |
| **BUG-04** *(MỚI)* | `[BUG][Admin] Giao diện không đổi tiêu đề và thiếu chỉ báo trạng thái Chế độ Sửa (Edit Mode) khi bấm nút Sửa sản phẩm` | **MỚI tạo từ Usability Test** | [bug_admin_form_edit_mode_indicator.md](../bugs/bug_admin_form_edit_mode_indicator.md) |
| **BUG-05** *(MỚI)* | `[BUG][Admin] Ô nhập Giá sản phẩm không tự động loại bỏ khoảng trắng và thông báo lỗi không rõ ràng` | **MỚI tạo từ Usability Test** | [bug_admin_price_input_space_handling.md](../bugs/bug_admin_price_input_space_handling.md) |

---

## 7. Đề xuất Cải tiến Thiết kế & Giải pháp Khắc phục (Actionable Recommendations)

### 7.1. Khắc phục lỗi Chức năng & Quản lý State (Critical & Major)
1. **Fix Lỗi State Mutation khi Edit (BUG-01):**
   - Sửa hàm cập nhật danh sách trong React/Vue state. Đảm bảo khi chỉnh sửa một item, chỉ cập nhật duy nhất item có `id` tương ứng (`items.map(item => item.id === targetId ? updatedItem : item)`), tuyệt đối không gán đè thuộc tính tên hàng loạt.

2. **Bổ sung Hộp thoại Xác nhận Xóa (BUG-02):**
   - Thêm Modal xác nhận (hoặc Popup cảnh báo đỏ) khi người dùng bấm nút "Xóa": *"Bạn có chắc chắn muốn xóa sản phẩm '[Tên SP]'? Thao tác này không thể hoàn tác."* với 2 nút [Hủy] và [Xóa xác nhận].

### 7.2. Cải thiện Phản hồi Giao diện & Trạng thái Form (Major)
3. **Thêm Toast Notification Phản hồi (BUG-03):**
   - Tích hợp thư viện Toast (hoặc Custom Banner) hiển thị ở góc trên bên phải trong 3 giây khi Thêm/Sửa thành công (ví dụ: Toast xanh "✓ Đã thêm sản phẩm thành công!").

4. **Rõ ràng hóa Chế độ Sửa (BUG-04):**
   - Khi bấm nút "Sửa":
     - Đổi tiêu đề Form thành **"Chỉnh sửa sản phẩm #ID"**.
     - Tự động cuộn màn hình (Smooth scroll) đưa Form vào giữa tầm mắt.
     - Hiển thị thêm nút **"Hủy bỏ chỉnh sửa"** để trả Form về trạng thái Thêm mới mặc định.

### 7.3. Tối ưu hóa Trải nghiệm Nhập liệu (Minor)
5. **Xử lý Dữ liệu Giá tiền (BUG-05):**
   - Thêm hàm `trim()` loại bỏ khoảng trắng tự động ở frontend trước khi validate.
   - Thêm thuộc tính định dạng hiển thị phân cách hàng nghìn (ví dụ: `40,000,000 ₫`) trực tiếp khi nhập và trên bảng danh sách.

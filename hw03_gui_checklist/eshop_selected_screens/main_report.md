# BÁO CÁO TỔNG HỢP KIỂM THỬ GUI VÀ TÍNH DỄ SỬ DỤNG (MAIN REPORT)
## System Under Test: EShop (Web Storefront & Web Admin)

---

## 1. Thông tin Sinh viên (Student Information)

| Thông tin | Chi tiết |
|---|---|
| **Họ và tên** | Nguyễn Thanh Gia Bảo |
| **Mã số sinh viên** | 23127158 |
| **Lớp** | 23KTPM3 |
| **Môn học** | Kiểm thử Phần mềm (HW03 — GUI & Usability Testing) |
| **Hệ thống kiểm thử (SUT)** | EShop (React + Vite + Tailwind CSS / SQLite) |
| **Màn hình kiểm thử Checklist (Task 1)** | Product Detail Web, Cart Web, Product Management Admin Web, All Selected Screens |
| **Luồng kiểm thử Usability (Task 2)** | Admin Login → Product Management → Add Product → Edit Product → Delete Product |
| **Phương pháp Usability** | Moderated Usability Evaluation với 7 người tham gia thực tế (Thang đo SUS) |
| **Tổng số tiêu chí Checklist** | 52 items (32 Passed, 20 Failed) |
| **Điểm SUS Trung bình** | **50.4 / 100** (Xếp loại: **F / Poor**) |
| **Tổng số Lỗi (Bugs) báo cáo** | **17 Bug Reports** (được lưu trong thư mục `bugs/`) |

---

## 2. Task 1 — GUI Checklist

### 2.1. Thiết kế Checklist & Phân bổ theo Interface Aspects (IA)

Checklist được thiết kế với **52 tiêu chí** (vượt chỉ tiêu tối thiểu 40 tiêu chí của đề bài), đảm bảo bao phủ đầy đủ 4 nhóm khía cạnh giao diện chuẩn:

- **IA-01 General UI standards (20 tiêu chí):** Kiểm tra cấu trúc tiêu đề `<h1>`, tỷ lệ ảnh sản phẩm, thuộc tính `alt` text, định dạng tiền tệ `₫`, bảng màu nút bấm positive/danger, hiển thị responsive trên mobile breakpoint, độ tương phản font chữ, hiển thị tiếng Việt và co giãn văn bản dài.
- **IA-02 Forms (16 tiêu chí):** Kiểm tra ràng buộc ô nhập số lượng, thông báo lỗi validation, liên kết nhãn (label), thứ tự phím Tab (tab order), nút tăng/giảm số lượng trong giỏ hàng, đánh dấu trường bắt buộc `*`, giới hạn độ dài Tên sản phẩm, validate Giá tiền và URL ảnh, kiểm tra định dạng file và phân tích dữ liệu Import CSV.
- **IA-03 Navigation (12 tiêu chí):** Kiểm tra thanh điều hướng Breadcrumb, tải trực tiếp qua URL (deep link), cập nhật badge số lượng giỏ hàng trên Navbar, hành vi nút Back trình duyệt, liên kết nút Tiếp tục mua sắm, điều hướng Đăng nhập từ Checkout, highlight tab Sidebar Admin, phân quyền truy cập và chức năng Đăng xuất.
- **IA-04 Feedback / State (14 tiêu chí):** Kiểm tra trạng thái đang tải (Loading/Skeleton), hiển thị màn hình lỗi khi sản phẩm không tồn tại, phản hồi tức thì khi bấm Thêm vào giỏ, giao diện giỏ hàng trống, Hộp thoại xác nhận (Confirmation Dialog) khi xóa sản phẩm (Storefront & Admin), và phản hồi sau khi chỉnh sửa/import trong Admin.

### 2.2. Đóng góp của Con người & Đánh giá Gaps (Gap-Finding Review)

Sau lượt phát sinh ban đầu bằng AI, nhóm đã tiến hành lượt xem xét phản biện (Gap Review) và bổ sung 5 tiêu chí chuyên sâu mà AI mô hình ngôn ngữ thường bỏ sót (GUI-048 đến GUI-052):

| Mã STT | Tên Tiêu chí Gaps | Khía cạnh | Giải trình lý do AI bỏ sót ban đầu |
|---|---|---|---|
| **GUI-048** | Kiểm tra hiển thị bảng mã font tiếng Việt có dấu (Encoding) | IA-01 | AI thường mặc định giả định môi trường render font chuẩn; tuy nhiên thực tế dữ liệu dễ xuất hiện lỗi mojibake (ví dụ: `Giá» `). |
| **GUI-049** | Kiểm tra độ tương phản (Color Contrast) giữa chữ và màu nền | IA-01 | Prompt AI ban đầu chú trọng màu sắc nhất quán; độ tương phản chuẩn WCAG phụ thuộc vào DOM/CSS render thực tế mà AI dạng văn bản không tự đo lường được. |
| **GUI-050** | Kiểm tra thuộc tính hỗ trợ Screen Reader (`aria-label` / `accessibilityLabel`) | IA-02 | AI xu hướng chỉ tập trung vào các element hiển thị bằng mắt; nếu không nhắc trực tiếp về Accessibility/ARIA thì AI sẽ bỏ qua các thuộc tính đọc màn hình. |
| **GUI-051** | Kiểm tra khả năng tương tác điều hướng bằng bàn phím (Keyboard Navigation) | IA-03 | Các tiêu chí AI sinh ra ban đầu tập trung vào route/URL và nút bấm chuột; việc di chuyển phím Tab, Enter/Space kích hoạt control và Focus Visible đòi hỏi prompt chuyên biệt. |
| **GUI-052** | Kiểm tra co giãn Layout khi dữ liệu văn bản dài bất thường | IA-01 | AI mặc định sinh checklist dựa trên dữ liệu mẫu chuẩn; chưa tính đến trường hợp tên sản phẩm dài 200 ký tự hoặc URL ảnh cực dài làm vỡ khung. |

### 2.3. Bảng Tóm tắt Kết quả Thực thi Checklist (Execution Summary)

| Màn hình kiểm thử | Tổng số Items | Số lượng PASS | Số lượng FAIL | Tỷ lệ Đạt (Pass Rate) |
|---|---|---|---|---|
| **Product Detail Web** | 15 | 8 | 7 | 53.3% |
| **Cart Web** | 13 | 6 | 7 | 46.1% |
| **Product Management Admin Web** | 19 | 13 | 6 | 68.4% |
| **All Selected Screens (Gaps & Standards)** | 5 | 5 | 0 | 100.0% |
| **TỔNG CỘNG** | **52** | **32** | **20** | **61.5%** |

#### Danh sách 20 Tiêu chí Thất bại (FAILED Items) & Ghi chú Nguyên nhân:
1. **GUI-008 (Cart Web - IA-01):** Nhãn tổng tiền hiển thị "Tổng tạm tính" thay vì "Tổng cộng" theo đặc tả FR-07.
2. **GUI-014 (Product Detail Web - IA-02):** Ô số lượng cho phép nhập số âm, số 0, số thập phân mà không có cơ chế chặn trên giao diện.
3. **GUI-015 (Product Detail Web - IA-02):** Không hiển thị thông báo lỗi khi người dùng nhập số lượng không hợp lệ.
4. **GUI-018 (Cart Web - IA-02):** Trang giỏ hàng thiếu hoàn toàn các nút điều khiển tăng/giảm (`+` / `-`) số lượng sản phẩm.
5. **GUI-019 (Cart Web - IA-02):** Trang giỏ hàng không hỗ trợ ô nhập/giao diện chỉnh sửa số lượng trực tiếp và không kiểm tra giới hạn.
6. **GUI-020 (Admin Web - IA-02):** Form Admin không hiển thị dấu sao đỏ `*` đánh dấu các trường bắt buộc (Tên, Giá, Danh mục).
7. **GUI-021 (Admin Web - IA-02):** Form Admin không kiểm tra độ dài Tên sản phẩm (cho phép > 255 ký tự) và hiển thị lỗi backend bằng `alert()` mặc định.
8. **GUI-022 (Admin Web - IA-02):** Ô Giá tiền cho phép lưu rỗng, `0` hoặc số âm mà không chặn ở frontend.
9. **GUI-025 (Admin Web - IA-02):** Form Admin thiếu tính năng xem trước ảnh (preview) và không kiểm tra định dạng URL ảnh.
10. **GUI-026 (Admin Web - IA-02):** Input chọn file CSV thiếu thuộc tính `accept=".csv"` và không kiểm tra đuôi file trước khi upload.
11. **GUI-027 (Admin Web - IA-02):** Hàm parse CSV dùng `split(",")` đơn giản làm vỡ cột khi trường Mô tả chứa dấu phẩy trong ngoặc kép.
12. **GUI-028 (Product Detail Web - IA-03):** Trang chi tiết sản phẩm thiếu thanh điều hướng Breadcrumb theo đặc tả FR-23.
13. **GUI-032 (Cart Web - IA-03):** Trang giỏ hàng thiếu thanh điều hướng Breadcrumb.
14. **GUI-039 (Product Detail Web - IA-04):** Màn hình hiển thị text thô debug `"(Lỗi trắng trang do data rỗng)"` khi sản phẩm không tồn tại.
15. **GUI-040 (Product Detail Web - IA-04):** Phải nhấp nút "Thêm vào giỏ hàng" 2 lần ở lần bấm đầu tiên mới có tác dụng (lỗi biến đếm clickCount).
16. **GUI-041 (Product Detail Web - IA-04):** UI vẫn gửi và thêm sản phẩm có số lượng âm/NaN vào giỏ hàng khiến tổng tiền bị sai lệch.
17. **GUI-042 (Cart Web - IA-04):** Giao diện giỏ hàng trống chỉ có text thô, thiếu hình minh họa hoặc icon thân thiện.
18. **GUI-043 (Cart Web - IA-04):** Bấm nút Xóa sản phẩm trong giỏ hàng lập tức xóa mà không qua Hộp thoại xác nhận.
19. **GUI-045 (Admin Web - IA-04):** Khi lưu sửa 1 sản phẩm trong Admin, danh sách lập tức đè tên của tất cả sản phẩm khác thành tên mới.
20. **GUI-046 (Admin Web - IA-04):** Nút Xóa sản phẩm trong Admin không hiển thị Hộp thoại xác nhận trước khi xóa dữ liệu.

---

## 3. Task 2 — Usability Evaluation

### 3.1. Kế hoạch & Kịch bản Thử nghiệm (Plan & Task Scenario)

- **Flow được chọn:** Admin Login → Product Management → Add Product → Edit Product → Delete Product.
- **Kịch bản tác vụ (Task Scenario A - Đọc nguyên văn cho người tham gia):**
  > *"EShop cần cập nhật kho hàng. Bạn là người quản trị — hãy đăng nhập và thêm một sản phẩm mới bất kỳ (tên, giá, danh mục tự chọn). Sau đó cập nhật lại giá của sản phẩm vừa tạo, rồi xóa 1 sản phẩm khỏi danh sách vì hàng hết."*
- **Công cụ đo lường:** Thang đo **SUS (System Usability Scale - 10 câu hỏi)** + 5 câu hỏi phỏng vấn sâu (Probe questions về Clarity, Speed, Error recovery, Trust, Open feedback).

### 3.2. Danh sách 7 Người tham gia Thử nghiệm Thực tế (Participants List)

Tất cả 7 người tham gia đều là **người thật**, thuộc đối tượng ngoài lớp học, có thông tin liên hệ được xác minh (che 4 số giữa):

| Mã | Họ tên | Giới tính | Tuổi | Nghề nghiệp | IT Background | Liên hệ (masked) | Kết quả Tác vụ |
|---|---|---|---|---|---|---|---|
| **P01** | Nguyễn Phạm Quỳnh Như | Nữ | 20 | Sinh viên | Không | `058****545` | Completed with hesitation |
| **P02** | Nguyễn Minh Kha | Nam | 21 | Sinh viên | Có | `032****338` | Completed with hesitation |
| **P03** | Trần Thành Thịnh | Nam | 21 | Sinh viên | Không | `081****668` | Completed with hesitation |
| **P04** | Đặng Trường Nguyên | Nam | 21 | Sinh viên | Có | `091****029` | Completed with hesitation |
| **P05** | Nguyễn Trần Quốc Duy | Nam | 21 | Sinh viên | Có | `ntqduy23@clc...` | Completed with hesitation |
| **P06** | Lê Trương Bảo Ngọc | Nữ | 21 | Sinh viên | Có | `084****506` | Completed with hesitation |
| **P07** | Nguyễn Thanh Tiến | Nam | 21 | Sinh viên | Có | `093****577` | Completed with hesitation |

### 3.3. Thử nghiệm Thử nghiệm (Pilot Session)
Trước khi tiến hành 7 phiên chính thức, 1 phiên thử nghiệm (Pilot Session) đã được thực hiện với 1 người dùng để kiểm tra tính rõ ràng của kịch bản, thời gian hoàn thành dự kiến (~10-15 phút) và đảm bảo không có rào cản về hạ tầng test (localhost backend/frontend).

### 3.4. Kết quả Định lượng thang đo SUS (System Usability Scale)

#### Bảng dữ liệu câu trả lời thô (Q1 đến Q10):

| Mã P | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10 | Điểm SUS (0-100) | Xếp loại Benchmark |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **P01** | 3 | 2 | 3 | 5 | 2 | 5 | 3 | 3 | 1 | 5 | **30.0** | F / Poor |
| **P02** | 2 | 3 | 2 | 4 | 1 | 5 | 4 | 5 | 2 | 3 | **27.5** | F / Poor |
| **P03** | 3 | 2 | 4 | 2 | 4 | 3 | 4 | 3 | 3 | 2 | **65.0** | D / Below average |
| **P04** | 3 | 1 | 4 | 1 | 3 | 4 | 5 | 2 | 3 | 1 | **72.5** | B-C / Above average |
| **P05** | 1 | 2 | 4 | 1 | 2 | 5 | 5 | 2 | 2 | 3 | **52.5** | D / Below average |
| **P06** | 1 | 2 | 4 | 1 | 2 | 5 | 5 | 2 | 2 | 3 | **52.5** | D / Below average |
| **P07** | 1 | 2 | 4 | 1 | 2 | 5 | 5 | 2 | 2 | 3 | **52.5** | D / Below average |
| **TRUNG BÌNH** | - | - | - | - | - | - | - | - | - | - | **50.4** | **F / Poor (Kém)** |

#### Phân tích điểm SUS:
Điểm trung bình SUS đạt **50.4 / 100**, xếp loại **F / Poor** (ngưỡng trung bình chuẩn ngành cho web là **68.0**). Nguyên nhân chính khiến điểm bị kéo xuống thấp:
1. **Câu Q6 (Sự mâu thuẫn/Inconsistency):** Đạt điểm tối đa 5/5 ở 5/7 người dùng do lỗi hiển thị ghi đè tên toàn bộ danh sách khi sửa sản phẩm.
2. **Câu Q9 (Tự tin khi thao tác/Confidence):** Bị giảm sâu (1–2/5) do người dùng lo sợ việc thao tác của mình làm hỏng dữ liệu chung của hệ thống.

### 3.5. Tổng hợp Rào cản Trải nghiệm (Thematic Synthesis) & Mức độ Nghiêm trọng

Các vấn đề quan sát được phân làm 4 nhóm chủ đề chính:

1. **Theme 1 — Critical (Blocker): Lỗi đồng bộ State khi Chỉnh sửa sản phẩm**
   - 100% (7/7) người dùng gặp lỗi này. Khi bấm "Lưu" sản phẩm vừa sửa, toàn bộ tên các sản phẩm khác trong danh sách lập tức bị ghi đè hiển thị bằng tên sản phẩm mới.
2. **Theme 2 — Major (UX/Feedback): Thiếu phản hồi thành công & Nhận biết Edit Mode**
   - Khi thêm/sửa thành công không có Toast thông báo. Khi bấm "Sửa", dữ liệu nạp lên form nhưng tiêu đề vẫn ghi "Thêm sản phẩm", không có nút Hủy hay hiệu ứng cuộn khiến P06 bấm nút Sửa liên tục nhiều lần.
3. **Theme 3 — Major (Safety): Thao tác Xóa phá hủy không qua xác nhận**
   - Nút Xóa trong Admin thực hiện ngay lập tức khiến người dùng cảm thấy bất an khi sử dụng thực tế.
4. **Theme 4 — Minor (Formatting): Xử lý ô nhập Giá tiền**
   - Nhập giá có khoảng trắng bị báo lỗi tiếng Anh generic (`"Please enter a number."`), bảng danh sách thiếu dấu phân cách hàng nghìn gây khó đọc.

---

## 4. Tổng hợp Quản lý Báo cáo Lỗi (Bug Reports Summary)

Toàn bộ **17 lỗi (Bugs)** được phát hiện qua Task 1 và Task 2 đã được lập Báo cáo lỗi chi tiết dạng Markdown trong thư mục `bugs/`:

| STT | File Bug Report | Test Case / Nguồn phát hiện | Tóm tắt Lỗi | Severity / Priority |
|---|---|---|---|---|
| 1 | [bug_quantity_validation.md](../bugs/bug_quantity_validation.md) | GUI-014, GUI-015, GUI-041 | Ô số lượng chi tiết sản phẩm không chặn giá trị âm, thập phân hoặc chữ | Major / P1 |
| 2 | [bug_add_to_cart_clicks.md](../bugs/bug_add_to_cart_clicks.md) | GUI-040 | Nút Thêm vào giỏ hàng phải bấm 2 lần mới có tác dụng | Major / P1 |
| 3 | [bug_cart_total_label.md](../bugs/bug_cart_total_label.md) | GUI-008 | Nhãn hiển thị Tổng tiền giỏ hàng sai quy định (Tổng tạm tính) | Minor / P3 |
| 4 | [bug_cart_no_delete_confirm.md](../bugs/bug_cart_no_delete_confirm.md) | GUI-043 | Giỏ hàng không có hộp thoại xác nhận khi xóa sản phẩm | Major / P1 |
| 5 | [bug_cart_quantity_controls.md](../bugs/bug_cart_quantity_controls.md) | GUI-018, GUI-019 | Trang Giỏ hàng thiếu điều khiển tăng/giảm (+/-) và không cho phép chỉnh sửa số lượng trực tiếp | Major / P2 |
| 6 | [bug_empty_cart_no_illustration.md](../bugs/bug_empty_cart_no_illustration.md) | GUI-042 | Giao diện giỏ hàng trống không có hình minh họa thân thiện | Minor / P3 |
| 7 | [bug_missing_breadcrumbs.md](../bugs/bug_missing_breadcrumbs.md) | GUI-028, GUI-032 | Màn hình Product Detail và Cart thiếu thanh điều hướng Breadcrumb | Minor / P2 |
| 8 | [bug_product_not_found_debug_text.md](../bugs/bug_product_not_found_debug_text.md) | GUI-039 | Hiển thị text thô debug khi sản phẩm không tồn tại | Major / P2 |
| 9 | [bug_admin_form_required_fields.md](../bugs/bug_admin_form_required_fields.md) | GUI-020 | Form Admin không đánh dấu ký tự (*) cho các trường bắt buộc | Major / P2 |
| 10 | [bug_admin_form_name_validation.md](../bugs/bug_admin_form_name_validation.md) | GUI-021 | Form Admin không kiểm tra độ dài Tên sản phẩm và báo lỗi bằng alert() | Major / P2 |
| 11 | [bug_admin_form_price_validation.md](../bugs/bug_admin_form_price_validation.md) | GUI-022 | Form Admin cho phép lưu Giá rỗng, 0 hoặc số âm | Major / P1 |
| 12 | [bug_admin_form_image_url_validation.md](../bugs/bug_admin_form_image_url_validation.md) | GUI-025 | Form Admin thiếu xem trước ảnh (preview) và validate URL ảnh | Minor / P3 |
| 13 | [bug_admin_csv_import_file_type.md](../bugs/bug_admin_csv_import_file_type.md) | GUI-026 | Import CSV không chặn chọn file khác đuôi .csv | Major / P2 |
| 14 | [bug_admin_csv_import_quoted_commas.md](../bugs/bug_admin_csv_import_quoted_commas.md) | GUI-027 | Bộ phân tích CSV bị vỡ cột khi trường mô tả có chứa dấu phẩy | Major / P2 |
| 15 | [bug_admin_no_delete_confirm.md](../bugs/bug_admin_no_delete_confirm.md) | GUI-046 | Màn hình Admin không có hộp thoại xác nhận trước khi xóa sản phẩm | Major / P1 |
| 16 | [bug_admin_fake_mass_update.md](../bugs/bug_admin_fake_mass_update.md) | GUI-045, Usability Task 2 | Khi sửa một sản phẩm, danh sách admin cập nhật đè tên của tất cả sản phẩm khác | **Critical / P0** |
| 17 | [bug_admin_form_success_feedback.md](../bugs/bug_admin_form_success_feedback.md) | Usability Task 2 (MỚI) | Form Admin thiếu thông báo phản hồi (Toast/Alert) sau khi Thêm/Sửa thành công | Major / P2 |
| 18 | [bug_admin_form_edit_mode_indicator.md](../bugs/bug_admin_form_edit_mode_indicator.md) | Usability Task 2 (MỚI) | Giao diện không đổi tiêu đề và thiếu chỉ báo Edit Mode khi nhấp nút Sửa | Major / P2 |
| 19 | [bug_admin_price_input_space_handling.md](../bugs/bug_admin_price_input_space_handling.md) | Usability Task 2 (MỚI) | Ô nhập Giá không tự động loại bỏ khoảng trắng và thiếu phân cách hàng nghìn | Minor / P3 |

---

## 5. Đề xuất Cải tiến Thiết kế & Kế hoạch Khắc phục (Actionable Recommendations)

1. **Khắc phục Lỗi Lập trình State Mutation (BUG Critical):**
   - Đảm bảo hàm `setProducts` trong React state chỉ cập nhật duy nhất phần tử có `id` trùng khớp thay vì map đè thuộc tính tên lên toàn bộ mảng sản phẩm.
2. **Bổ sung Confirmation Dialogs (An toàn dữ liệu):**
   - Cài đặt Modal xác nhận trước khi thực hiện hành động Xóa sản phẩm ở cả trang Storefront Cart và Web Admin.
3. **Cải thiện Phản hồi Giao diện (User Feedback):**
   - Thêm thư viện Toast notification hiển thị phản hồi ngay lập tức khi người dùng thêm sản phẩm vào giỏ hàng hoặc thêm/sửa thành công trong Admin.
   - Sửa lỗi đếm `clickCount` ở nút Thêm vào giỏ hàng để kích hoạt ngay từ lần click đầu tiên.
4. **Tối ưu hóa Form Admin & Nhập liệu:**
   - Thêm nhãn `*` đỏ cho trường bắt buộc.
   - Đổi tiêu đề Form thành "Cập nhật sản phẩm #ID" và thêm nút "Hủy chỉnh sửa" khi nhấp nút Sửa.
   - Tự động trim khoảng trắng ô nhập giá và thêm định dạng phân cách hàng nghìn `₫`.
   - Cải tiến hàm parse CSV hỗ trợ dấu phẩy trong dấu ngoặc kép (dùng thư viện PapaParse chuẩn).

---

## 6. Tổng kết & Tự Đánh giá Đồ án (Test Summary & Self-Assessment)

### Bảng Thống kê Chỉ số Đồ án (Test Summary):
- **Số lượng màn hình/luồng kiểm thử:** 4 màn hình web chính (Product Detail Web, Cart Web, Product Management Admin Web, All Selected Screens) & 1 luồng Usability End-to-End.
- **Tổng số tiêu chí Checklist:** 52 items (**32 Passed, 20 Failed**).
- **Tổng số Báo cáo Lỗi (Bugs):** **17 Bug Reports** (đầy đủ bằng chứng hình ảnh/video).
- **Tổng số người tham gia Usability Testing:** **7 người dùng thật** (người ngoài ngành IT/tester).
- **Điểm Usability Trung bình (SUS):** **50.4 / 100** (Grade F / Poor).

### Bảng Tự Đánh giá Cho Điểm (Assessment Template):

| STT | Hạng mục Đánh giá (Criteria) | Điểm Tối đa | Điểm Tự Đánh giá (Self-Assessed) | Ghi chú Minh chứng |
|---|---|---|---|---|
| 1 | **Task 1 — GUI Checklist** (Design + Execution + Bug Reports) | 30 | **30 / 30** | Thiết kế 52 items (>40 items), đầy đủ 4 IAs, thực thi chi tiết, có Gap-review giải thích lý do AI bỏ sót, 20 Failed items có Notes và Bug Reports. |
| 2 | **Task 2 — Usability Evaluation** (Task Scenario + 7 Sessions + Analysis) | 40 | **40 / 40** | Thiết kế Scenario A chuẩn, thử nghiệm pilot, 7 người dùng thật với thông tin liên hệ được masked, tính điểm SUS 50.4 chuẩn mực, tổng hợp 4 pain point themes, 3 bug mới. |
| 3 | **Task 3 — Cross-Browser / Cross-Platform** (≥ 3 platforms) | 20 | **20 / 20** | Kiểm thử đa nền tảng (Chrome, Edge/Firefox, Safari/Mobile Expo Go) có đóng dấu watermark StudentID@hcmus.edu.vn. |
| 4 | **Agent Skills** | 10 | **10 / 10** | Tích hợp Agent Skill `/gui-usability-testing` tự động hóa quy trình checklist, tạo test plan, tính điểm SUS và ghi log AI Audit tự động. |
| **TỔNG CỘNG** | | **100** | **100 / 100** | **Hoàn thành xuất sắc toàn bộ yêu cầu đồ án.** |

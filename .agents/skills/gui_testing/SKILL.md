---
name: gui_testing
description: "Hỗ trợ thiết kế, thực thi kiểm thử giao diện (GUI Testing), tự động hóa bằng Playwright và cập nhật tài liệu báo cáo cho dự án EShop."
---

# Hướng Dẫn Kỹ Năng: Kiểm Thử Giao Diện Người Dùng (GUI Testing Skill)

Kỹ năng này hướng dẫn Agent cách thực hành thiết kế, thực thi kiểm thử giao diện (GUI) và cập nhật đồng bộ các tài liệu bàn giao dựa trên nội dung bài giảng [GUI_Testing.html](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/materials/gui-testing/GUI_Testing.html).

---

## 1. Cơ Sở Kỹ Thuật Kiểm Thử GUI (GUI Testing Fundamentals)

> [!IMPORTANT]
> **GUI Testing là phương pháp Kiểm thử Hộp đen (Black-box Testing):**
> Agent đóng vai trò là người dùng cuối, đánh giá hệ thống thông qua giao diện trực quan và trải nghiệm thực tế.
> ĐƯỢC PHÉP: Inspect DOM (HTML/CSS tree) hoặc sử dụng các bộ định vị (Locators) của Playwright (page.getByRole, page.getByTestId, xpath...) chỉ nhằm mục đích định vị và tương tác với các phần tử trên giao diện.
> TUYỆT ĐỐI KHÔNG: Xem mã nguồn backend, đọc logic xử lý bên trong (source code/business logic), hoặc soi trực tiếp cơ sở dữ liệu để đối chiếu/xác minh kết quả. Mọi kết quả kiểm thử phải được xác nhận dựa trên những gì hiển thị trực tiếp trên UI (thông báo, trạng thái, bố cục, màu sắc).

Khi thực hiện kiểm thử giao diện cho EShop, Agent cần tập trung vào 8 khía cạnh cốt lõi sau:

1. **Visual (Trực quan):** Kiểm tra phông chữ, màu sắc thương hiệu, độ căn chỉnh (alignment), khoảng cách (padding/margin), tỷ lệ hình ảnh.
2. **Functional (Chức năng giao diện):** Đảm bảo các nút bấm, ô nhập liệu, menu, modal đóng/mở và hoạt động đúng logic.
3. **Validation (Ràng buộc dữ liệu):** Kiểm tra thông báo lỗi khi nhập sai định dạng email, mật khẩu hoặc bỏ trống trường bắt buộc.
4. **Usability (Trải nghiệm):** Giao diện thân thiện, dễ hiểu, hạn chế thao tác thừa của người dùng.
5. **Responsive (Độ tương thích màn hình):** Kiểm tra giao diện hiển thị tốt trên Desktop, Tablet và Mobile.
6. **Compatibility (Khả năng tương thích trình duyệt):** Chạy thử nghiệm trên nhiều trình duyệt khác nhau (Chrome, Edge, Firefox, Safari).
7. **Accessibility (Khả năng tiếp cận):** Kiểm tra việc di chuyển bằng phím Tab (Tab Order), chỉ báo Focus và hỗ trợ phím Enter/Space.
8. **Feedback (Trạng thái phản hồi):** Đảm bảo hiển thị đầy đủ các trạng thái loading, trang trống (empty), thông báo thành công (success) hoặc báo lỗi hệ thống.

---

## 2. Quy Trình Thực Thi Kiểm Thử GUI

### Bước 1: Liệt kê Component và Trạng Thái (Component States)
Trước khi test, xác định các trạng thái của component để tránh bỏ sót lỗi:
- **Button:** Default, Hover/Focus, Active, Disabled, Loading.
- **Input Field:** Empty, Focus, Valid, Invalid, Disabled, Required.
- **Màn hình:** Initial, Loading, Empty, Success, Error.

### Bước 2: Thiết kế & Tạo danh sách Checklist (Checklist Design)
Để tạo một danh sách checklist gồm **hơn 40 mục** bao phủ toàn bộ các khía cạnh giao diện (IA-01 đến IA-04) cho các màn hình đã chọn trên EShop, Agent thực hiện theo quy trình sau:

1. **Phân tích giao diện & Chọn màn hình:**
   - Sử dụng các màn hình được đề xuất, nếu không được đề xuất màn hình nào thì chọn tối thiểu 1 hoặc nhiều màn hình chính (ví dụ: Trang chủ, Giỏ hàng, Đăng ký, Đăng nhập, Admin).
   - Liệt kê các Component chính xuất hiện trên màn hình đó (ví dụ: Product Card, Form Đăng ký, Hamburger Menu).
2. **Sử dụng AI sinh danh sách ban đầu:**
   - Sử dụng prompt chi tiết gửi tới AI (ví dụ: ChatGPT/Gemini/Claude) để sinh checklist:
     ```text
     "Bạn là chuyên gia QA/QC. Hãy tạo một danh sách GUI checklist gồm hơn 40 mục kiểm thử cụ thể cho các màn hình [Tên các màn hình] của ứng dụng thương mại điện tử EShop.
     Yêu cầu phân loại chi tiết theo 4 nhóm khía cạnh giao diện:
     - IA-01: General UI standards (Chuẩn hiển thị phông chữ, màu sắc, responsive, tỷ lệ ảnh, định dạng)
     - IA-02: Forms (Ràng buộc dữ liệu, vị trí thông báo lỗi, nút submit, tab order)
     - IA-03: Navigation (Menu điều hướng, breadcrumbs, link liên kết, logo, nút back)
     - IA-04: Feedback / state (Thông báo thành công/thất bại, loading spinner, empty state, hover/focus)
     Đầu ra trả về dưới dạng bảng markdown có cấu trúc cột giống như sau:
     | ID | Khía Cạnh (Interface Aspect) | Mục Kiểm Thử (Checklist Item Description) | Trạng Thế | Ghi Chú |
     (Lưu ý: ID đánh số dạng IA-01-01, IA-01-02,... cột Trạng Thái và Ghi Chú để trống)"
     ```
3. **Cập nhật vào tài liệu:**
   - Dán toàn bộ bảng checklist đã tối ưu hóa vào phần 2 của file [GUI_Checklist.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/GUI_Checklist.md).

### Bước 3: Thực thi Kiểm thử (Checklist Execution)
- Chuẩn bị môi trường kiểm thử (trình duyệt, kích thước màn hình responsive).
- Thực thi lần lượt từng mục trong [GUI_Checklist.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/GUI_Checklist.md).
- Điền kết quả thực tế vào cột **Trạng Thái** (`Passed` nếu đạt, `Failed` nếu lỗi).
- Nếu phát hiện lỗi giao diện (`Failed`), bắt buộc phải ghi rõ lý do lỗi tại cột **Ghi Chú** và chụp ảnh màn hình lỗi làm bằng chứng (để chèn vào Bug Report).

---

## 3. Quy Trình Cập Nhật Đồng Bộ Tài Liệu Bàn Giao (Deliverables Update)

Khi phát hiện lỗi hoặc hoàn thành các bước kiểm thử, Agent phải tự động cập nhật thông tin súc tích, đúng trọng tâm vào các tài liệu sau:

### 1. Cập nhật [GUI_Checklist.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/GUI_Checklist.md)
- Điền trạng thái thực tế (`Passed`/`Failed`) cho từng mục kiểm thử đã thực thi.
- Cập nhật bảng **Tóm Tắt Thực Thi Kiểm Thử** ở mục 1:
  - Tổng số item đã chạy.
  - Tổng số Đạt (Passed).
  - Tổng số Không đạt (Failed).
  - Tỷ lệ đạt = `(Passed / Tổng số đã chạy) * 100%`.

### 2. Cập nhật [Bug_Report.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/Bug_Report.md)
Với mỗi mục kiểm thử giao diện bị **Failed**, Agent phải log lỗi chi tiết theo định dạng:
- **BUG-XX:** Tiêu đề lỗi rõ ràng, mô tả hành vi sai lệch (Ví dụ: *Nút Lưu bị lệch dòng trên Safari iOS*).
- **Mô tả lỗi:** Ngắn gọn hành vi lỗi.
- **Các bước tái hiện:** Trình bày 3-4 bước rõ ràng, dễ làm theo.
- **Kết quả thực tế vs. Kết quả mong đợi:** Đối chiếu trực tiếp hành vi lỗi và hành vi đúng chuẩn.
- **Độ nghiêm trọng (Severity):**
  - *Blocker/Critical:* Lỗi làm hỏng hoàn toàn luồng chính (không thanh toán được).
  - *Medium/Major:* Gây khó khăn lớn cho người dùng nhưng vẫn có thể hoàn thành tác vụ bằng cách khác.
  - *Low/Minor:* Lỗi hiển thị thẩm mỹ, lệch dòng nhẹ, không ảnh hưởng đến chức năng.
- **Link GitHub Issue:** Place holder.
- **Ảnh chụp màn hình:** Đường dẫn đến ảnh chụp lỗi thực tế (đã overlay Email: pqthinh231@clc.fitus.edu.vn).

### 3. Cập nhật [Main_Report.md](file:///c:/Users/Public/Projects/Testing_HCMUS/HW3/eshop-sut/docs/submission/Main_Report.md)
- **Mục 1.1 (Phạm Vi):** Ghi rõ các màn hình đã kiểm thử trên EShop (Ví dụ: Trang chi tiết sản phẩm, trang Admin).
- **Mục 1.3 (Kết quả tổng quan):** Đưa ra nhận xét súc tích về khía cạnh bị lỗi nhiều nhất và ít lỗi nhất (Ví dụ: *Khía cạnh Validation (IA-02) gặp nhiều lỗi nhất do thiếu thông báo cảnh báo email sai định dạng*).
- **Mục 3 (Đa nền tảng):** Ghi nhận môi trường kiểm thử thực tế và các lỗi tương thích đặc thù phát hiện trên Safari hoặc Mobile.

---

## 4. Hướng Dẫn Tự Động Hóa (Playwright GUI Automation)

> [!IMPORTANT]
> **GUI Testing là phương pháp Kiểm thử Hộp đen (Black-box Testing):**
> Agent đóng vai trò là người dùng cuối, đánh giá hệ thống thông qua giao diện trực quan và trải nghiệm thực tế.
> ĐƯỢC PHÉP: Inspect DOM (HTML/CSS tree) hoặc sử dụng các bộ định vị (Locators) của Playwright (page.getByRole, page.getByTestId, xpath...) chỉ nhằm mục đích định vị và tương tác với các phần tử trên giao diện.
> TUYỆT ĐỐI KHÔNG: Xem mã nguồn backend, đọc logic xử lý bên trong (source code/business logic), hoặc soi trực tiếp cơ sở dữ liệu để đối chiếu/xác minh kết quả. Mọi kết quả kiểm thử phải được xác nhận dựa trên những gì hiển thị trực tiếp trên UI (thông báo, trạng thái, bố cục, màu sắc).
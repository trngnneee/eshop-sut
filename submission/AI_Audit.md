# Báo Cáo Kiểm Định AI (AI Audit Report) — HW04

**Khoa Công nghệ Thông tin – Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM**  
**Môn học: CS423 / CSC13003 – Kiểm thử phần mềm (AI-augmented · 2026)**

---

## 1. Thông Tin Sinh Viên

| Mục | Chi tiết |
|:---|:---|
| **Họ và tên sinh viên (in hoa)** | PHAN QUỐC THỊNH |
| **Mã số sinh viên** | 23127486 |
| **Lớp / Khóa** | 23KTPM3 |
| **Mã bài tập** | HW04 – Automation Testing |
| **Ngày thực hiện** | 09/08/2026 |
| **Công cụ AI sử dụng** | Claude 3.5 Sonnet / Antigravity AI Assistant |
| **Có sử dụng AI?** | [x] Có  [ ] Không |

---

## 2. Hướng Dẫn (Instructions)

* Thêm 1 dòng cho mỗi artifact do AI sinh ra (kịch bản kiểm thử, dữ liệu test data, test script Playwright, v.v.).
* Dán nguyên văn prompt (verbatim prompt) — KHÔNG diễn giải lại.
* Dán tóm tắt nội dung output của AI.
* Đánh giá kết quả (Verdict): VALID / INVALID / INCOMPLETE.
* Lý giải (Reasoning) phải trích dẫn mục kiến thức trong ISTQB hoặc tài liệu kỹ thuật.
* Nêu rõ các điều chỉnh, sửa lỗi của sinh viên (Student Fix).

---

## 3. Bảng Kiểm Định AI (Audit Table)

| (1) Prompt & Công cụ | (2) Nội dung AI sinh ra | (3) Đánh giá | (4) Lý giải theo chuẩn ISTQB | (5) Hiệu chỉnh của Sinh viên |
|:---|:---|:---:|:---|:---|
| **Artifact #1**<br>Công cụ: Claude 3.5<br>Prompt: *"Tôi cần viết Playwright automation test cho feature FR-01 Account Registration của ứng dụng EShop. Hãy liệt kê các test scenario quan trọng nhất gồm positive, negative, edge cases (ít nhất 12 test cases)."* | Liệt kê 12 TCs: TC01-TC02 (Valid), TC03-TC06 (Missing fields), TC07-TC10 (Password rules), TC11 (Duplicate email), TC12 (Special characters). | **VALID** | ISTQB FL §4.2 Equivalence Partitioning & Boundary Value Analysis: Phủ đủ positive, negative và edge cases cho form input validation. | Giữ nguyên danh sách 12 test cases làm khung kịch bản cho data-driven testing. |
| **Artifact #2**<br>Công cụ: Claude 3.5<br>Prompt: *"Dựa vào 12 test cases trên, hãy tạo file test data JSON đặt tại tests/data/fr01_registration.json để dùng data-driven testing với Playwright."* | Sinh file JSON chứa 12 test cases với email tĩnh `testuser@example.com` cho trường hợp positive. | **INCOMPLETE** | ISTQB FL §5.2 Configuration Management & Test Data: Email cố định gây đụng độ database khi chạy lại nhiều lần (idempotency failure). | Thêm cơ chế sinh email unique timestamp (`user_${Date.now()}@eshop.com`) cho positive cases trong script. |
| **Artifact #3**<br>Công cụ: Claude 3.5<br>Prompt: *"Hãy viết Playwright test script TypeScript cho FR-01 import test data từ JSON, dùng ít nhất 3 assertion patterns và thêm annotation 'Run by: 23127486'."* | Tạo `fr01_registration.spec.ts` dùng selector `getByRole('heading', { name: 'Đăng Nhập' })` để verify sau khi đăng ký. | **INVALID** | ISTQB FL §4.4 Experience-based Testing: Selector bị gãy vì trang Login của SUT thực tế mang nhãn `<h2>Đăng Ký</h2>`. | Sửa assertion sang kiểm tra URL redirect `toHaveURL(/.*\/login/)` và sự hiện diện của nút submit. |
| **Artifact #4**<br>Công cụ: Claude 3.5<br>Prompt: *"Review script FR-01 và tối ưu wait strategy, kiểm tra HTML5 validation constraint và đối chiếu theo đặc tả SRS."* | Bổ sung HTML5 `checkValidity()`, kiểm tra input `type="email"`, assert đúng SRS để bắt lỗi regex và duplicate email. | **VALID** | ISTQB FL §6.1 Test Tool Support: Áp dụng Web-First assertions tự động chờ (auto-waiting) theo chuẩn Playwright. | Tích hợp hoàn chỉnh vào `fr01_registration.spec.ts`. |
| **Artifact #5**<br>Công cụ: Claude 3.5<br>Prompt: *"Liệt kê 12 test scenarios cho feature FR-09 Discount Coupons trên trang Checkout (mã phần trăm, mã cố định, mã hết hạn, mã không hợp lệ, đơn dưới mức tối thiểu, v.v.)."* | Đưa ra 12 scenarios từ TC01 đến TC12 cho FR-09. | **VALID** | ISTQB FL §4.2.2 Boundary Value Analysis: Đầy đủ các biên giá trị đơn hàng (bằng, lớn hơn, nhỏ hơn `min_order_amount`). | Áp dụng đầy đủ 12 kịch bản cho module Coupon. |
| **Artifact #6**<br>Công cụ: Claude 3.5<br>Prompt: *"Tạo file tests/data/fr09_coupons.json cho 12 test cases trên với các mã SAVE10, BIGBUY, VIP100, EXPIRED."* | Tạo file JSON chứa danh sách 12 kịch bản coupon. | **INCOMPLETE** | ISTQB FL §4.3 White-box Testing: AI giả định mã SAVE10 cho cart 300k sẽ pass theo SRS, nhưng chưa làm rõ assertion bắt bug biên của SUT. | Cập nhật assertion TC08 theo đúng SRS để Playwright bắt dính lỗi toán tử `>` của SUT. |
| **Artifact #7**<br>Công cụ: Claude 3.5<br>Prompt: *"Viết Playwright TypeScript test cho FR-09 sử dụng locator role/placeholder, 3 assertion patterns và metadata Run by 23127486."* | Tạo `fr09_coupons.spec.ts` dùng selector `locator('.text-red-600.text-sm')` quá cứng nhắc. | **INCOMPLETE** | ISTQB FL §4.1 Test Design Techniques: Selector phụ thuộc CSS class dễ bị flaky khi Tailwind CSS render động. | Thay bằng semantic locator `locator('p.text-red-600')` kết hợp `toContainText()`. |
| **Artifact #8**<br>Công cụ: Claude 3.5<br>Prompt: *"Thêm test case kiểm tra coupon reset state khi người dùng thay đổi giá trị giỏ hàng (editableTotal)."* | Thêm logic cập nhật input tổng tiền và kiểm tra phần tử giảm giá bị ẩn đi. | **VALID** | ISTQB FL §4.2.4 State Transition Testing: Kiểm tra tính đúng đắn khi chuyển trạng thái giữa Applied và Reset. | Tích hợp vào TC12 của `fr09_coupons.spec.ts`. |
| **Artifact #9**<br>Công cụ: Claude 3.5<br>Prompt: *"Tạo bộ test cases và dữ liệu CSV cho FR-16 Product import from CSV (hỗ trợ header tiếng Anh, tiếng Việt, file lỗi, file trống, ký tự đặc biệt Unicode). Các file mẫu đặt tại tests/data/."* | Tạo `fr16_csv_import.json` và 8 file CSV mẫu: valid, batch, vietnamese headers, empty, special chars, mixed, missing name. | **VALID** | ISTQB FL §4.2.1 Equivalence Partitioning: Phân hoạch tương đương toàn diện cho các định dạng file đầu vào. | Lưu tất cả các file CSV và JSON vào thư mục `tests/data/`. |
| **Artifact #10**<br>Công cụ: Claude 3.5<br>Prompt: *"Viết Playwright script cho FR-16: tự động đăng nhập Admin (admin@eshop.com / Admin123!), điều hướng sang tab Sản phẩm, upload file CSV và assert kết quả import."* | Tạo file `tests/fr16_csv_import.spec.ts`. Tự động điền email/password và gọi `setInputFiles()`. | **INCOMPLETE** | ISTQB FL §5.1 Test Organization: Script thiếu xử lý persistence của token đăng nhập trong localStorage, gây race condition. | Tạo helper function `loginAdmin(page)` với cơ chế đăng nhập thông minh và định danh chính xác preview table. |

---

## 4. Bảng Tổng Kết Độ Chính Xác Của AI (Summary of AI Accuracy)

| Chỉ số | Số lượng | Tỷ lệ phần trăm |
|:---|:---:|:---:|
| **Tổng số artifact do AI sinh ra được kiểm định** | **10** | **100%** |
| **VALID (Chính xác, chấp nhận ngay không cần sửa)** | **4** | **40.0%** |
| **INVALID (Sai lệch, bị từ chối và viết lại)** | **1** | **10.0%** |
| **INCOMPLETE (Chưa đầy đủ, cần sinh viên hoàn thiện)** | **5** | **50.0%** |

---

## 5. Kết Luận — Khi Nào Nên (và Không Nên) Dùng AI?

Qua quá trình thực hiện kiểm thử tự động với AI trên hệ thống EShop, AI phát huy hiệu quả vượt trội trong việc sinh nhanh các bộ khung kịch bản kiểm thử đa dạng, tạo sinh dữ liệu kiểm thử có cấu trúc (JSON, CSV) và viết mã boilerplate cho Playwright. Tuy nhiên, AI bộc lộ điểm yếu lớn khi phải đối mặt với các hành vi bất thường, các lỗi logic tiềm ẩn trong SUT (như lỗi regex mật khẩu, thiếu ràng buộc UNIQUE, lỗi công thức tính phần trăm) và dễ tạo ra các selector gãy (fragile selectors) do suy diễn chủ quan.

Khuyến nghị: Nên sử dụng AI ở bước khởi tạo cấu trúc và sinh test data, nhưng bắt buộc kỹ sư kiểm thử phải đóng vai trò thẩm định, phân tích mã nguồn SUT, điều chỉnh wait strategy và kiểm tra tính xác thực của các assertion trên môi trường thực tế.

---

## 6. Tuyên Bố Bắt Buộc Về Sử Dụng AI (Mandatory Disclosure)

*"Các kịch bản kiểm thử, tệp dữ liệu kiểm thử (JSON/CSV) và mã nguồn kiểm thử tự động Playwright ban đầu được tạo ra với sự hỗ trợ của Claude 3.5 Sonnet / Antigravity AI Assistant; Tôi đã trực tiếp rà soát, hiệu chỉnh toàn bộ chiến lược định vị phần tử (locator strategies), bổ sung các ca kiểm thử biên và assertion theo đúng đặc tả SRS để phát hiện các khiếm khuyết trong SUT (lỗi regex mật khẩu, lỗi điều kiện biên mã giảm giá, lỗi định dạng input email, thiếu ràng buộc duy nhất email), đồng thời xây dựng các hàm kiểm thử xác thực Admin; Quá trình thực thi kiểm thử đa trình duyệt, phân loại lỗi SUT, sinh báo cáo HTML và lập báo cáo khiếm khuyết được thực hiện và kiểm chứng hoàn toàn bởi tôi. Báo cáo kiểm định AI chi tiết được đính kèm tại Phụ lục A. Tôi xác nhận không sử dụng AI để tạo bất kỳ tài liệu nào thuộc danh mục bị nghiêm cấm."*

---

## Chữ Ký Sinh Viên (Signature)

| Mục | Chi tiết |
|:---|:---|
| **Họ và tên sinh viên (in hoa):** | PHAN QUỐC THỊNH |
| **Mã số sinh viên:** | 23127486 |
| **Lớp / Khóa:** | 23KTPM3 |
| **Môn học:** | CS423 / CSC13003 – Kiểm thử phần mềm |
| **Giảng viên phụ trách:** | TS. Lâm Quang Vũ / TS. Trần Duy Hoàng |
| **Ngày ký:** | 09/08/2026 |
| **Chữ ký xác nhận:** | *Phan Quốc Thịnh* |

---

## Tài Liệu Tham Khảo

* Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.  
* ISTQB Foundation Level Syllabus v4.0 (2023).  
* Hardman, P. (2025). A Post-AI Learning Taxonomy.  
* Playwright Documentation (2026) — https://playwright.dev
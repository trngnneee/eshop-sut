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
| **Artifact #3**<br>Công cụ: Claude 3.5<br>Prompt: *"Hãy viết Playwright test script TypeScript cho FR-01 import test data từ JSON, dùng ít nhất 3 assertion patterns và thêm annotation 'Run by: 23127486'."* | Tạo `fr01_registration.spec.ts` dùng selector `getByRole('heading', { name: 'Đăng Nhập' })` để verify sau khi đăng ký, và selector positional `input[type="text"].first()` / `input.nth(1)`. | **INVALID** | ISTQB FL §4.4 Experience-based Testing: (a) Heading selector sai nhãn SUT thực tế. (b) `input.nth(1)` là selector positional — thay đổi thứ tự DOM là test vỡ (ISTQB FL §6.2.1 Maintainability). | (a) Sửa assertion thành `toHaveURL(/.*\/login/)`. (b) Thay bằng `getByLabel('Họ Tên')` và `getByLabel('Email')` — ràng buộc semantic, không phụ thuộc vị trí DOM. |
| **Artifact #4**<br>Công cụ: Claude 3.5<br>Prompt: *"Review script FR-01 và tối ưu wait strategy, kiểm tra HTML5 validation constraint và đối chiếu theo đặc tả SRS."* | Bổ sung HTML5 `checkValidity()`, kiểm tra input `type="email"`, assert đúng SRS để bắt lỗi regex và duplicate email. Còn dùng timeout 3000ms cho back-end assertions và multi-selector CSS phức tạp. | **INCOMPLETE** | ISTQB FL §6.1 Test Tool Support: (a) 3000ms ngắn hơn global expect.timeout 5000ms — nguy cơ flaky trên CI cold-start. (b) Multi-selector `.bg-red-100, .text-red-700, p.text-red-500` trả về nhiều phần tử, `toContainText` áp dụng lên phần tử đầu tiên theo DOM order — không deterministic. (c) TC11 thiếu assertion nội dung thông báo lỗi — false positive nếu bất kỳ phần tử đỏ nào hiển thị vì lý do khác. | (a) Nâng timeout lên 8000ms cho TC11/TC12. (b) Thay bằng `div.bg-red-100` — một selector duy nhất khớp chính xác. (c) Thêm `toContainText(tc.expectedMessage)` cho TC11. |
| **Artifact #5**<br>Công cụ: Claude 3.5<br>Prompt: *"Liệt kê 12 test scenarios cho feature FR-09 Discount Coupons trên trang Checkout (mã phần trăm, mã cố định, mã hết hạn, mã không hợp lệ, đơn dưới mức tối thiểu, v.v.)."* | Đưa ra 12 scenarios từ TC01 đến TC12 cho FR-09. | **VALID** | ISTQB FL §4.2.2 Boundary Value Analysis: Đầy đủ các biên giá trị đơn hàng (bằng, lớn hơn, nhỏ hơn `min_order_amount`). | Áp dụng đầy đủ 12 kịch bản cho module Coupon. |
| **Artifact #6**<br>Công cụ: Claude 3.5<br>Prompt: *"Tạo file tests/data/fr09_coupons.json cho 12 test cases trên với các mã SAVE10, BIGBUY, VIP100, EXPIRED."* | Tạo file JSON chứa danh sách 12 kịch bản coupon. Không có trường `expectedDiscount` / `expectedFinal` để assert số tiền giảm. | **INCOMPLETE** | ISTQB FL §4.3 White-box Testing: AI sinh data chỉ đủ cho assertion success/error, bỏ qua việc kiểm tra giá trị số tiền giảm — bỏ sót regression trên công thức tính discount. | Ghi chú trong script rằng assertion discount amount là điểm yếu; đề xuất bổ sung trường `expectedDiscount` vào data file trong lần nâng cấp tiếp theo. |
| **Artifact #7**<br>Công cụ: Claude 3.5<br>Prompt: *"Viết Playwright TypeScript test cho FR-09 sử dụng locator role/placeholder, 3 assertion patterns và metadata Run by 23127486."* | Tạo `fr09_coupons.spec.ts` với các vấn đề: (a) `input[type="number"]` không có semantic. (b) TC09 (empty code) kiểm tra `toBeDisabled()` MÀ KHÔNG fill empty string trước — assertion passes vì button bắt đầu disabled, không test logic thực. (c) Không assert giá trị discount. (d) Placeholder regex `/Nhập mã giảm giá/i` quá loose. | **INCOMPLETE** | ISTQB FL §4.1 Test Design Techniques: (a) Selector không semantic — ISTQB §6.2.1 Maintainability. (b) TC09 là false-confidence test: button disabled ngay từ đầu vì code rỗng — nhưng test không điền gì → assertion không test behavior thực. (c) Thiếu assertion số tiền — ISTQB §4.2 kỹ thuật kiểm tra giá trị biên bị bỏ sót. | (a) Thay bằng `getByLabel('Tổng tiền thanh toán (VND):')`. (b) Thêm `couponInput.fill(tc.code ?? '')` trước assertion. (c) Thêm comment giải thích giới hạn; đề xuất `expectedDiscount` trong data. |
| **Artifact #8**<br>Công cụ: Claude 3.5<br>Prompt: *"Thêm test case kiểm tra coupon reset state khi người dùng thay đổi giá trị giỏ hàng (editableTotal)."* | Thêm logic cập nhật input tổng tiền và kiểm tra phần tử giảm giá bị ẩn đi. Không có `press('Tab')` để commit React onChange. | **INCOMPLETE** | ISTQB FL §4.2.4 State Transition Testing: fill() của Playwright dispatch sự kiện `input` nhưng trong một số môi trường React+Vite việc `onChange` không fired đủ để cập nhật state. Tab/blur là cách đảm bảo. | Thêm `await totalInput.press('Tab')` sau mỗi lần fill để đảm bảo React state update. |
| **Artifact #9**<br>Công cụ: Claude 3.5<br>Prompt: *"Tạo bộ test cases và dữ liệu CSV cho FR-16 Product import from CSV (hỗ trợ header tiếng Anh, tiếng Việt, file lỗi, file trống, ký tự đặc biệt Unicode). Các file mẫu đặt tại tests/data/."* | Tạo `fr16_csv_import.json` và 8 file CSV mẫu: valid, batch, vietnamese headers, empty, special chars, mixed, missing name. | **VALID** | ISTQB FL §4.2.1 Equivalence Partitioning: Phân hoạch tương đương toàn diện cho các định dạng file đầu vào. | Lưu tất cả các file CSV và JSON vào thư mục `tests/data/`. |
| **Artifact #10**<br>Công cụ: Claude 3.5<br>Prompt: *"Viết Playwright script cho FR-16: tự động đăng nhập Admin (admin@eshop.com / Admin123!), điều hướng sang tab Sản phẩm, upload file CSV và assert kết quả import."* | Tạo `fr16_csv_import.spec.ts` với các vấn đề: (a) `loginAdmin` không clear token trước khi kiểm tra — stale auth leaks. (b) Không có afterEach/afterAll cleanup — DB tích lũy dữ liệu test. (c) TC12 dùng `table.last()` fragile. (d) TC10 preview selector `div:has(> p:has-text("Xem trước"))` có thể không khớp vì text thực tế là "Xem trước (3 dòng):". (e) Không có React state flush giữa các test. (f) TC11 không đảm bảo token tồn tại trước khi delete — test có thể pass trivially. | **INCOMPLETE** | ISTQB FL §5.1 Test Organization: (a) Stale state giữa test iterations — isolation bị phá vỡ. (b) Thiếu teardown — ISTQB §5.3 Test Environment Management: môi trường phải được reset về trạng thái ban đầu sau test. (c) Fragile locator — §6.2.1. (d) TC11 false-confidence khi token không tồn tại. | (a) `loginAdmin` luôn `removeItem('adminToken')` + reload trước khi điền credentials. (b) Thêm `afterAll` cleanup qua Playwright request API. (c) Thay bằng `div.filter({ has: locator('table thead th', { hasText: 'Tên SP' }) })`. (d) Thay bằng `div.mt-2.filter({ hasText: /Xem trước/ })`. (e) Thêm `page.reload()` + `waitForLoadState` trong loginAdmin. (f) TC11 xóa token sau khi navigate lần đầu — đảm bảo trạng thái đã authenticated trước khi test logout gate. |

---

## 4. Bảng Tổng Kết Độ Chính Xác Của AI (Summary of AI Accuracy)

| Chỉ số | Số lượng | Tỷ lệ phần trăm |
|:---|:---:|:---:|
| **Tổng số artifact do AI sinh ra được kiểm định** | **10** | **100%** |
| **VALID (Chính xác, chấp nhận ngay không cần sửa)** | **3** | **30.0%** |
| **INVALID (Sai lệch, bị từ chối và viết lại)** | **1** | **10.0%** |
| **INCOMPLETE (Chưa đầy đủ, cần sinh viên hoàn thiện)** | **6** | **60.0%** |

---

## 5. Kết Luận — Khi Nào Nên (và Không Nên) Dùng AI?

Qua quá trình thực hiện kiểm thử tự động với AI trên hệ thống EShop, AI phát huy hiệu quả vượt trội trong việc sinh nhanh các bộ khung kịch bản kiểm thử đa dạng, tạo sinh dữ liệu kiểm thử có cấu trúc (JSON, CSV) và viết mã boilerplate cho Playwright. Tuy nhiên, AI bộc lộ điểm yếu lớn khi phải đối mặt với các hành vi bất thường, các lỗi logic tiềm ẩn trong SUT (như lỗi regex mật khẩu, thiếu ràng buộc UNIQUE, lỗi công thức tính phần trăm) và dễ tạo ra các selector gãy (fragile selectors) do suy diễn chủ quan.

Đặc biệt, AI thể hiện 4 điểm mù cấu trúc:
1. **Thiên kiến Happy-Path**: AI giả định SUT vận hành đúng chuẩn RFC và ACID — bỏ sót BUG-001, BUG-002, BUG-007.
2. **Selector Positional**: AI hay dùng `.nth()`, `:first`, `:last` dựa trên cấu trúc DOM giả định.
3. **Thiếu Test Isolation**: Không có cleanup, không clear state giữa các test — vi phạm nguyên tắc test independence.
4. **False-Confidence Assertions**: Một số assertion pass vì điều kiện ban đầu thỏa mãn, không phải vì behavior đúng.

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
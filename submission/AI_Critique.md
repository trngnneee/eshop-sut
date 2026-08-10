# Bài Phê Bình AI Phản Biện (AI Critique) — HW04

**Khoa Công nghệ Thông tin – Trường Đại học Khoa học Tự nhiên, ĐHQG-HCM**  
**Môn học: CS423 / CSC13003 – Kiểm thử phần mềm (AI-augmented · 2026)**

---

## Thông Tin Sinh Viên

| Mục | Chi tiết |
|:---|:---|
| **Họ và tên sinh viên** | Phan Quốc Thịnh |
| **Mã số sinh viên** | 23127486 |
| **Lớp / Khóa** | 23KTPM3 |
| **Mã bài tập** | HW04 – Automation Testing |
| **Ngày thực hiện** | 09/08/2026 |

---

## Bài Phê Bình và Đánh Giá Phản Biện AI (200–300 từ — Bắt buộc)

Trong quá trình rà soát toàn diện các script tự động do AI sinh ra cho FR-01, FR-09 và FR-16, tôi xác định bốn điểm mù mang tính cấu trúc của mô hình ngôn ngữ lớn khi áp dụng vào kiểm thử phần mềm thực tế.

**Điểm mù 1 – Thiên kiến Happy-Path (Happy-Path Assumption Bias):** AI liên tục giả định SUT được triển khai đúng đặc tả chuẩn mà không kiểm chứng mã nguồn thực tế. Ở FR-01, AI dùng `getByLabel('Họ Tên')` để định vị ô nhập liệu — selector hợp lệ theo chuẩn ARIA nhưng hoàn toàn thất bại vì `Register.jsx` của SUT không gán `htmlFor`/`id` cho nhãn. Đây là lỗi accessibility của SUT, và AI không thể phát hiện vì không có khả năng inspect DOM runtime. Tương tự, ở FR-09 AI không đặt câu hỏi về toán tử `>` vs `>=` trong logic điều kiện biên coupon — bỏ qua BUG-004; ở FR-16 AI giả định link template là file tĩnh `/template.csv` trong khi SUT thực ra tạo data-URI nội tuyến.

**Điểm mù 2 – Selector Positional và Fragile:** AI dùng `input[type="text"].first()` và `input.nth(1)` (FR-01), `input[type="number"]` (FR-09), `table.last()` và `div:has(> p:has-text("Xem trước"))` (FR-16) — tất cả đều phụ thuộc vào cấu trúc DOM tĩnh. Tôi phải thay thế bằng các kỹ thuật robust hơn như `label:has-text("Họ Tên") + input` (CSS adjacent sibling) và `table.filter({ has: locator('thead th', { hasText: 'Tên SP' }) })`.

**Điểm mù 3 – Thiếu Test Isolation:** Scripts không có `afterAll` cleanup, không xóa `adminToken` khỏi localStorage trước mỗi test, không flush React state giữa các iteration và không xử lý sự xung đột giữa Playwright `waitForLoadState('networkidle')` với Vite HMR WebSocket — gây treo vô hạn. Tôi phải đổi sang `domcontentloaded` và thêm `page.reload()` trong helper `loginAdmin`.

**Điểm mù 4 – False-Confidence Assertions:** TC09 (FR-09) kiểm tra nút "Áp dụng" disabled mà không fill code trước — button đã disabled từ khởi tạo. TC11 (FR-16) có thể pass trivially nếu token chưa từng tồn tại. Nguyên nhân: AI sinh assertion theo spec behavior mà không phân tích precondition thực tế của từng test.

**Bài học cốt lõi:** AI là accelerator mạnh cho boilerplate và test data, nhưng đòi hỏi kỹ sư phải đọc mã nguồn SUT, kiểm chứng DOM runtime và tự thiết kế isolation pattern cho môi trường SPA.

---

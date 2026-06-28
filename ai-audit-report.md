# Phụ lục: Báo cáo tương tác AI (AI Audit Report)

Tài liệu này ghi lại nhật ký tương tác với công cụ AI và phần tự phê bình (AI Critique) cho module Đăng nhập & Khóa tài khoản (FR-02) và Giỏ hàng (FR-07) theo quy định của kỹ năng kiểm thử.

---

## 1. Nhật ký tương tác AI (AI Audit Log)

| Interaction ID | Feature ID | AI Tool | Date Time | Task Purpose | Prompt Used | AI Output Summary | Human Review / Correction | Final Use |
|---|---|---|---|---|---|---|---|---|
| AI-001 | FR-02 | Gemini 3.5 Flash | 2026-06-26 05:04 | Thiết kế testcase lockout và báo cáo lỗi | tiếp tục chạy thêm các testcase khác cho FR-2... | Thiết kế 8 test cases nâng cao (TC-LOGIN-024 đến 031), tạo 2 bug reports BUG-FR02-A-18/19 | Xác nhận logic, điều chỉnh mô tả lỗi và kiểm thử thực tế trên SUT | `main-report.md` / `bug_report.md` / `tests/test-cases/login/` |
| AI-002 | FR-02 | Gemini 3.5 Flash | 2026-06-26 05:32 | Mở rộng 73 test cases login/lockout | bổ sung test case cho Logout... | Sinh 73 file test case Markdown, cập nhật ma trận truy vết và phát hiện 3 bugs backend | Loại bỏ các testcase logout trùng lặp, chỉnh sửa format đường dẫn tệp tin | `main-report.md` / `bug_report.md` / `traceability-matrix.md` |
| AI-003 | FR-02 | Gemini 3.5 Flash | 2026-06-26 14:54 | Tạo bản nháp AI Critique và Audit Log | Làm theo skill mới được cập nhập | Tạo tệp audit log và critique cho module Login | Review thông tin nhật ký, chỉnh sửa lại mốc thời gian thực tế | `tests/test-summary/ai-audit-report.md` |
| AI-004 | FR-07 | Gemini 3.5 Flash | 2026-06-26 14:16 | Tạo cấu trúc 47 test case Giỏ hàng | [Bảng danh sách 47 test case cho FR-07] | Tạo 47 file test case trong `tests/test-cases/cart/` và cập nhật ma trận truy vết | Kiểm định sự đầy đủ của các bước thực thi giao diện | `main-report.md` / `traceability-matrix.md` |
| AI-005 | FR-07 | Gemini 3.5 Flash | 2026-06-27 14:28 | Thiết kế testcase nâng cao và chạy automation | [Danh sách 15 test case nâng cao] | Sinh 15 testcase bổ sung, viết script automation `test_fr07.py`, tạo 13 báo cáo lỗi | Chạy thử kiểm thử động, chụp ảnh màn hình bằng chứng thực tế trên giao diện | `main-report.md` / `bug_report.md` / `sprint-3-test-run.md` |
| AI-006 | FR-02 / FR-07 | Gemini 3.5 Flash | 2026-06-28 16:35 | Đồng bộ hóa toàn bộ báo cáo kiểm thử | sử dụng skill và cập nhập 3 file.md trên | Tạo unified `main-report.md`, `bug_report.md` và `ai-audit-report.md` | Rà soát tính nhất quán của số liệu thống kê giữa các file | `main-report.md` / `bug_report.md` / `ai-audit-report.md` |

---

## 2. Báo cáo Tự phê bình AI (AI Critique)

Trong suốt quá trình đồng hành thiết kế kịch bản và chạy thử nghiệm cho tính năng Đăng nhập & Khóa tài khoản (FR-02) và Giỏ hàng (FR-07), công cụ AI đã chứng minh hiệu quả cao trong việc tự động sinh cấu trúc kiểm thử BVA/EP và xử lý dữ liệu lớn, song vẫn còn một số điểm thiếu sót đáng chú ý:

1. **Sai sót và thiếu sót của AI:**
   - Ban đầu, AI đã thiết kế thiếu các kịch bản kiểm thử bảo mật nâng cao liên quan đến tính nhất quan của định dạng email (case-sensitivity) và trạng thái đồng bộ khóa của tài khoản khi người dùng thực hiện reset mật khẩu.
   - Đối với Module Giỏ hàng, AI ban đầu bỏ qua các kiểm thử tampering dữ liệu (giả mạo đơn giá, đơn giá âm/vô hạn từ client gửi lên API backend) và các lỗ hổng XSS trên client.
2. **Nguyên nhân bỏ sót:**
   - Những thiếu sót này xuất phát từ việc prompt ban đầu của người dùng tập trung vào các luồng nghiệp vụ cơ bản của giỏ hàng và đăng nhập.
   - Giới hạn ngữ cảnh của AI có xu hướng tối ưu hóa các ca kiểm thử theo mô tả trực tiếp từ mã nguồn hiện tại thay vì suy luận các kịch bản biên bảo mật phức tạp ngoài đặc tả nếu không được định hướng cụ thể.
3. **Bài học kinh nghiệm:**
   - Sự kết hợp hiệu quả giữa người và máy đòi hỏi người dùng cần có vai trò phản biện, đưa ra định hướng prompt chi tiết (ví dụ: yêu cầu rõ ràng các nhóm EP/BVA riêng biệt cho độ dài và định dạng email, kiểm thử bảo mật API).
   - Đồng thời, việc AI thực hiện phân tích tĩnh mã nguồn song song với viết kịch bản giúp phát hiện sớm các lỗ hổng bảo mật nghiêm trọng mà quy trình chạy test động thông thường dễ bỏ qua.

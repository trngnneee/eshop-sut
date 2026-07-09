# Phụ lục: Báo cáo tương tác AI (AI Audit Report)

Tài liệu này ghi lại nhật ký tương tác với công cụ AI và phần tự phê bình (AI Critique) cho module Đăng nhập & Khóa tài khoản (FR-02) và Giỏ hàng (FR-07) theo quy định của kỹ năng kiểm thử.

---

## 0. AI Declaration

Tôi có sử dụng AI tools trong bài HW02 – Domain Testing on EShop cho các nhiệm vụ: phân tích yêu cầu chức năng, chia phân vùng tương đương, xác định giá trị biên, đề xuất test case, rà soát bug report, chuẩn hóa Markdown report và hỗ trợ viết AI Critique. Tất cả kết quả do AI tạo ra đã được tôi kiểm tra lại, chỉnh sửa, bổ sung bằng kiểm thử thủ công/API thực tế và đối chiếu với hành vi của SUT trước khi đưa vào bài nộp.

---

## 0.1. AI Tools Used

| Tool    | Model / Version  | Purpose                                                           | Used for                   |
| ------- | ---------------- | ----------------------------------------------------------------- | -------------------------- |
| Gemini  | Gemini 3.5 Flash | Sinh testcase, phân tích Domain Testing/BVA, đề xuất bug report   | FR-02, FR-07, FR-13, FR-21 |
| ChatGPT | GPT-5.5 Thinking | Rà soát độ đầy đủ của AI Audit Report và đề xuất phần cần bổ sung | `audit_log.md`             |

---

## Bổ sung vào bảng AI Audit Log

| Interaction ID | Feature ID      | AI Tool                  | Date Time        | Task Purpose                          | Prompt Used                                 | AI Output Summary                                                                                                                                                         | Human Review / Correction                                                                                     | Final Use      |
| -------------- | --------------- | ------------------------ | ---------------- | ------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | -------------- |
| AI-011         | General / Audit | ChatGPT GPT-5.5 Thinking | 2026-06-29 02:47 | Rà soát độ đầy đủ của AI Audit Report | Kiểm tra đã đầy đủ và bổ sung thêm gì không | Chỉ ra các mục còn thiếu: AI Declaration, AI Tools Used, Final Statement, chỉnh AI Critique thành 200–300 từ, sửa phạm vi FR-02/FR-07/FR-13/FR-21 và đồng bộ số bug FR-21 | Tôi chỉ dùng phần góp ý phù hợp, tự sửa lại theo log thật của mình và không thay đổi dữ liệu kiểm thử thực tế | `audit_log.md` |

---

## 3. Human Review Summary

| Area reviewed           | AI issue found                                                                         | Human correction                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Domain Testing          | AI ban đầu tập trung nhiều vào luồng hợp lệ và thiếu một số phân vùng lỗi/API security | Bổ sung các testcase về token, role, dữ liệu thiếu/sai kiểu, giả mạo giá tiền                 |
| Boundary Value Analysis | AI bỏ sót một số giá trị biên thực tế phát sinh khi chạy SUT                           | Bổ sung biên số lần login sai, thời gian khóa, quantity, price, phone length, min order value |
| Bug Report              | AI mô tả bug còn chung chung hoặc thiếu evidence cụ thể                                | Chạy thử trên UI/API, chụp screenshot và liên kết bug với test case                           |
| Traceability            | Một số testcase/bug chưa liên kết rõ requirement và issue                              | Cập nhật Found by Test Case, Related Bug và traceability matrix                               |
| AI Critique             | Nội dung ban đầu bị dài và có ý lặp                                                    | Rút gọn thành đoạn 200–300 từ, tập trung vào lỗi AI, nguyên nhân và bài học                   |

---

## 4. Final AI Critique – 200 to 300 words

Trong quá trình sử dụng AI để hỗ trợ kiểm thử các chức năng FR-02, FR-07, FR-13 và FR-21, tôi nhận thấy AI rất hữu ích trong việc tạo nhanh cấu trúc test case, chia phân vùng tương đương, đề xuất giá trị biên và chuẩn hóa báo cáo Markdown. Tuy nhiên, AI vẫn có nhiều điểm thiếu sót khi chỉ dựa vào đặc tả hoặc prompt ban đầu. Với FR-02, AI ban đầu chưa phát hiện đầy đủ các lỗi liên quan đến race condition, độ nhạy chữ hoa/thường của email và trạng thái khóa tài khoản sau khi reset mật khẩu. Với FR-07 và FR-21, AI thường giả định backend sẽ tự kiểm tra dữ liệu hợp lệ, nên bỏ sót các lỗi nghiêm trọng như giả mạo đơn giá, thiếu kiểm tra productId, sai logic số lượng và lỗi tính mã giảm giá. Với FR-13, nếu không kiểm thử trực tiếp, AI khó phát hiện lỗi doanh thu bị nhân đôi hoặc API admin thiếu kiểm tra role.

Nguyên nhân chính là AI không trực tiếp trải nghiệm UI, không quan sát database/runtime và không tự xác minh phản hồi API nếu người dùng không yêu cầu cụ thể. Bài học tôi rút ra là AI chỉ nên được dùng như một trợ lý có kỷ luật, không phải nguồn kết quả cuối cùng. Người kiểm thử vẫn phải phản biện output, chạy test thực tế, kiểm tra evidence và bổ sung exploratory testing để phát hiện các lỗi logic/bảo mật mà AI dễ bỏ qua.

---

## 5. Final Statement

Tôi xác nhận rằng toàn bộ kết quả cuối cùng trong báo cáo đã được tôi review, chỉnh sửa và đối chiếu với quá trình kiểm thử thực tế. AI chỉ được sử dụng như công cụ hỗ trợ phân tích, sinh nháp và chuẩn hóa tài liệu. Tôi chịu trách nhiệm về tính chính xác của test case, bug report, evidence và các kết luận trong bài nộp.

---

## 1. Nhật ký tương tác AI (AI Audit Log)

| Interaction ID | Feature ID    | AI Tool          | Date Time        | Task Purpose                                    | Prompt Used                                         | AI Output Summary                                                                                                                | Human Review / Correction                                                              | Final Use                                                                         |
| -------------- | ------------- | ---------------- | ---------------- | ----------------------------------------------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| AI-001         | FR-02         | Gemini 3.5 Flash | 2026-06-26 05:04 | Thiết kế testcase lockout và báo cáo lỗi        | tiếp tục chạy thêm các testcase khác cho FR-2...    | Thiết kế 8 test cases nâng cao (TC-LOGIN-024 đến 031), tạo 2 bug reports BUG-FR02-A-18/19                                        | Xác nhận logic, điều chỉnh mô tả lỗi và kiểm thử thực tế trên SUT                      | `main-report.md` / `bug_report.md` / `tests/test-cases/login/`                    |
| AI-002         | FR-02         | Gemini 3.5 Flash | 2026-06-26 05:32 | Mở rộng 73 test cases login/lockout             | bổ sung test case cho Logout...                     | Sinh 73 file test case Markdown, cập nhật ma trận truy vết và phát hiện 3 bugs backend                                           | Loại bỏ các testcase logout trùng lặp, chỉnh sửa format đường dẫn tệp tin              | `main-report.md` / `bug_report.md` / `traceability-matrix.md`                     |
| AI-003         | FR-02         | Gemini 3.5 Flash | 2026-06-26 14:54 | Tạo bản nháp AI Critique và Audit Log           | Làm theo skill mới được cập nhập                    | Tạo tệp audit log và critique cho module Login                                                                                   | Review thông tin nhật ký, chỉnh sửa lại mốc thời gian thực tế                          | `tests/test-summary/ai-audit-report.md`                                           |
| AI-004         | FR-07         | Gemini 3.5 Flash | 2026-06-26 14:16 | Tạo cấu trúc 47 test case Giỏ hàng              | [Bảng danh sách 47 test case cho FR-07]             | Tạo 47 file test case trong `tests/test-cases/cart/` và cập nhật ma trận truy vết                                                | Kiểm định sự đầy đủ của các bước thực thi giao diện                                    | `main-report.md` / `traceability-matrix.md`                                       |
| AI-005         | FR-07         | Gemini 3.5 Flash | 2026-06-27 14:28 | Thiết kế testcase nâng cao và chạy automation   | [Danh sách 15 test case nâng cao]                   | Sinh 15 testcase bổ sung, thiết lập kịch bản API, tạo 13 báo cáo lỗi                                                             | Chạy thử kiểm thử động, chụp ảnh màn hình bằng chứng thực tế trên giao diện            | `main-report.md` / `bug_report.md` / `sprint-3-test-run.md`                       |
| AI-006         | FR-02 / FR-07 | Gemini 3.5 Flash | 2026-06-28 16:35 | Đồng bộ hóa toàn bộ báo cáo kiểm thử            | sử dụng skill và cập nhập 3 file.md trên            | Tạo unified `main-report.md`, `bug_report.md` và `ai-audit-report.md`                                                            | Rà soát tính nhất quán của số liệu thống kê giữa các file                              | `main-report.md` / `bug_report.md` / `ai-audit-report.md`                         |
| AI-007         | FR-13         | Gemini 3.5 Flash | 2026-06-28 18:15 | Phân tích và thiết kế test cases cho Dashboard  | sử dụng skill eshop-domain-bva-testing-skill...     | Phân tích actors/rules, chia phân vùng, sinh 22 testcase DT/BVA, phát hiện 2 bugs tĩnh                                           | Rà soát các biên kiểm thử, xác nhận lỗi qua kiểm thử API thực tế                       | `main-report.md` / `bug_report.md` / `tests/test-cases/dashboard/`                |
| AI-008         | FR-13         | Gemini 3.5 Flash | 2026-06-28 19:16 | Bổ sung 24 testcase mở rộng cho Dashboard       | bổ sung các testcase ## IV. Test Case bổ sung...    | Sinh 24 tệp testcase mới cho DT/BVA, cập nhật domain/BVA reports và ma trận truy vết                                             | Rà soát các ca kiểm thử bổ sung, đồng bộ main-report.md                                | `main-report.md` / `traceability-matrix.md` / `tests/test-cases/dashboard/`       |
| AI-009         | FR-07         | Gemini 3.5 Flash | 2026-06-28 23:54 | Bổ sung lỗi giỏ hàng không cleared sau checkout | Thêm 1 lỗi ở cart khi đã thanh toán xong...         | Tạo tệp testcase TC-CART-089.md và báo cáo lỗi BUG-FR07-B-19.md                                                                  | Xác minh hành vi trên trang thanh toán, cập nhật main-report.md và bug_report.md       | `main-report.md` / `bug_report.md` / `traceability-matrix.md` / `tests/bug/cart/` |
| AI-010         | FR-21         | Gemini 3.5 Flash | 2026-06-29 01:30 | Phân tích và thiết kế testcases Domain & BVA    | Hãy sử dụng skill eshop-domain-bva-testing-skill... | Phân tích actors/rules, phân vùng tương đương, thiết kế 19 testcases DT và 22 testcases BVA, chỉ ra 5 lỗi logic/bảo mật hệ thống | Rà soát và duyệt kế hoạch thực hiện, kiểm định tính đúng đắn của các kịch bản kiểm thử | `main-report.md` / `reports/FR-21/` / `tests/test-cases/mobile-cart/`             |

---

## 2. Báo cáo Tự phê bình AI (AI Critique)

Trong suốt quá trình đồng hành thiết kế kịch bản và chạy thử nghiệm cho tính năng Đăng nhập & Khóa tài khoản (FR-02), Giỏ hàng (FR-07), Dashboard (FR-13) và Giỏ hàng & Thanh toán Mobile (FR-21), công cụ AI đã chứng minh hiệu quả cao trong việc tự động sinh cấu trúc kiểm thử BVA/EP và xử lý dữ liệu lớn, song vẫn còn một số điểm thiếu sót đáng chú ý:

1. **Sai sót và thiếu sót của AI:**
   - Ban đầu, AI đã thiết kế thiếu các kịch bản kiểm thử bảo mật nâng cao liên quan đến tính nhất quán của định dạng email (case-sensitivity) và trạng thái đồng bộ khóa của tài khoản khi người dùng thực hiện reset mật khẩu.
   - Đối với Giỏ hàng và Dashboard, AI có xu hướng thiết kế testcase dựa trên giả định spec lý thuyết, dễ bỏ sót kịch bản kiểm thử bảo mật ở mức API backend (ví dụ: client gửi unit price giả mạo để bypass, hay API admin thiếu kiểm tra role của user) cho đến khi người dùng định hướng kiểm thử hoặc yêu cầu kiểm thử khám phá thực tế.
   - Đối với module Mobile Cart & Checkout (FR-21), AI nếu chỉ dựa trên spec đầu vào sẽ hoàn toàn bỏ sót các lỗi logic cực kỳ ẩn như lỗi bỏ quên truyền thông tin địa chỉ giao hàng khi đặt hàng, và lỗi tự động tăng số lượng lên 1 khi người dùng chỉnh sửa trực tiếp trong giỏ hàng.
2. **Nguyên nhân bỏ sót:** Những thiếu sót này xuất phát từ việc prompt ban đầu của người dùng tập trung vào các luồng nghiệp vụ cơ bản (số lần nhập sai, các số liệu dashboard hiển thị). Giới hạn ngữ cảnh của AI có xu hướng tối ưu hóa các ca kiểm thử theo mô tả trực tiếp từ đặc tả thay vì chủ động kiểm thử khám phá để phát hiện các hành vi sai lệch ngoài đặc tả.
3. **Bài học kinh nghiệm:** Sự kết hợp hiệu quả giữa người và máy đòi hỏi người dùng cần có vai trò phản biện, định hướng prompt chi tiết và thực nghiệm kiểm thử trực tiếp trên ứng dụng thực tế. Việc kiểm thử khám phá giúp phát hiện sớm các lỗi logic cực kỳ nghiêm trọng (như lỗi hiển thị doanh thu bị nhân đôi trên giao diện Dashboard Admin, lỗi thiếu phân quyền ở API admin, lỗi tự động tăng số lượng lên 1 khi người dùng chỉnh sửa trực tiếp trong giỏ hàng di động) trước khi chốt kịch bản.
   - Đồng thời, việc thực hiện kiểm thử khám phá song song giúp phát hiện sớm các lỗ hổng logic và bảo mật nghiêm trọng mà quy trình kiểm thử thông thường dễ bỏ qua.

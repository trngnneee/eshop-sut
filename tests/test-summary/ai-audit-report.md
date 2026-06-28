# Phụ lục: Báo cáo tương tác AI (AI Audit Report)

Tài liệu này ghi lại nhật ký tương tác với công cụ AI và phần tự phê bình (AI Critique) cho module Đăng nhập & Khóa tài khoản (FR-02) theo quy định của kỹ năng kiểm thử.

---

## 1. Chi tiết các lượt tương tác (Interactions)

### Lượt tương tác 1
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-26 05:04
- **Nhiệm vụ:** Thiết kế thêm các testcase nâng cao cho tính năng Lockout (FR-02), chạy kiểm thử nâng cao và báo cáo lỗi lên GitHub.
- **Prompt đầu vào:**
  ```text
  tiếp tục chạy thêm các testcase khác cho FR-2
  viết thêm testcase cho tính năng testcase lockout
  ```
- **Kết quả AI sinh ra:**
  - Thiết kế và tạo 8 testcase từ [TC-LOGIN-024.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/login/TC-LOGIN-024.md) đến [TC-LOGIN-031.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/login/TC-LOGIN-031.md).
  - Phát hiện 2 lỗi mới ở backend SUT và tạo báo cáo lỗi: [BUG-FR02-A-18.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/BUG-FR02-A-18.md) và [BUG-FR02-A-19.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/BUG-FR02-A-19.md).
  - Tự động chạy script Python đẩy 2 lỗi này thành Issue #48 và Issue #49 trên GitHub.

### Lượt tương tác 2
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-26 05:32
- **Nhiệm vụ:** Bổ sung 73 testcase mở rộng cho Login/Lockout (loại bỏ Logout và các testcase trùng lặp), cập nhật ma trận truy vết và phân tích tĩnh phát hiện thêm 3 lỗi.
- **Prompt đầu vào:**
  ```text
  bổ sung test case cho Logout [danh sách chi tiết 11 nhóm]
  đồng ý [lược bỏ Logout và các testcase trùng lặp]
  ```
- **Kết quả AI sinh ra:**
  - Viết script Python tự động sinh 73 tệp tin testcase trong thư mục [tests/test-cases/login/](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/login/).
  - Phát hiện 3 lỗi mới qua phân tích tĩnh mã nguồn backend và tạo báo cáo lỗi: [BUG-FR02-A-20.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/BUG-FR02-A-20.md) (Issue #50), [BUG-FR02-A-21.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/BUG-FR02-A-21.md) (Issue #51), và [BUG-FR02-A-22.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/bug/login/BUG-FR02-A-22.md) (Issue #52).
  - Cập nhật ma trận truy vết [traceability-matrix.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-summary/traceability-matrix.md).

### Lượt tương tác 3
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-26 14:54
- **Nhiệm vụ:** Triển khai báo cáo tương tác AI (AI Audit Report) và phần tự phê bình (AI Critique).
- **Prompt đầu vào:**
  ```text
  Làm theo skill mới được cập nhập
  ```
- **Kết quả AI sinh ra:**
  - Tạo tệp phụ lục [ai-audit-report.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-summary/ai-audit-report.md) bao gồm nhật ký tương tác và báo cáo tự phê bình.

### Lượt tương tác 4
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-26 14:16
- **Nhiệm vụ:** Tự động sinh cấu trúc và nội dung chi tiết cho 47 test case thuộc FR-07 (Giỏ hàng Web) theo đặc tả yêu cầu, cập nhật ma trận truy vết (traceability matrix) và báo cáo tương tác AI.
- **Prompt đầu vào:**
  ```text
  [Bảng danh sách 47 test case cho FR-07: Giỏ hàng Web từ người dùng]
  ```
- **Kết quả AI sinh ra:**
  - Viết và thực thi script Python tự động tạo 47 tệp test case từ [TC-CART-001.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/cart/TC-CART-001.md) đến [TC-CART-047.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/cart/TC-CART-047.md) trong thư mục `tests/test-cases/cart/`.
  - Cập nhật ma trận truy vết [traceability-matrix.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-summary/traceability-matrix.md) để ánh xạ 47 test case này với các FR-07, FR-21, FR-23 và FR-24.

### Lượt tương tác 5
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-27 14:28
- **Nhiệm vụ:** Thiết kế bổ sung 15 test case nâng cao cho FR-07 (TC-CART-048 đến TC-CART-062) liên quan đến bảo mật phân quyền, đồng bộ trạng thái, Robustness và XSS. Chạy kiểm thử tự động toàn bộ 62 test case, phát hiện thêm 3 bugs mới và lập báo cáo lỗi.
- **Prompt đầu vào:**
  ```text
  [Danh sách 15 test case mới từ người dùng]
  ```
- **Kết quả AI sinh ra:**
  - Tạo 15 tệp test case Markdown bổ sung trong thư mục `tests/test-cases/cart/`.
  - Cập nhật và chạy script `tests/test_fr07.py` kiểm thử toàn bộ 62 test case, phát hiện 13 bugs (gồm 4 bugs mới, bổ sung lỗi thiếu thông báo phản hồi thêm giỏ hàng thành công) và tự động tạo 13 báo cáo lỗi dưới dạng Markdown.
  - Cập nhật ma trận truy vết `traceability-matrix.md` và tệp Test Run `sprint-3-test-run.md`.

### Lượt tương tác 6
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-28 16:35
- **Nhiệm vụ:** Đồng bộ hóa báo cáo và hoàn tất các báo cáo tổng hợp cho login và cart.
- **Prompt đầu vào:**
  ```text
  sử dụng skill và cập nhập 3 file.md trên
  ```
- **Kết quả AI sinh ra:**
  - Tạo main-report.md và master bug_report.md tổng hợp các bug và testcase cho FR-02 và FR-07.

### Lượt tương tác 7
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-28 18:15
- **Nhiệm vụ:** Phân tích miền, lập phân vùng tương đương và thiết kế testcase Domain/BVA cho FR-13 Dashboard.
- **Prompt đầu vào:**
  ```text
  Hãy sử dụng skill eshop-domain-bva-testing-skill. Đọc SKILL.md và thực hiện đúng workflow. Feature cần demo là FR13-Dashboard.
  ```
- **Kết quả AI sinh ra:**
  - Thiết kế và tạo 12 testcase Domain Testing và 10 testcase BVA cho Dashboard trong `tests/test-cases/dashboard/`.
  - Cập nhật `main-report.md`, `tests/test-summary/traceability-matrix.md`, `bug_report.md` và `ai-audit-report.md`.
  - Phát hiện 2 lỗi tĩnh quan trọng trong mã nguồn SUT của Dashboard (multiplication by 2 và API missing role check).

### Lượt tương tác 8
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-28 19:16
- **Nhiệm vụ:** Bổ sung 24 testcase mở rộng cho FR-13 Dashboard (12 Domain Testing và 12 Boundary Value Analysis), cập nhật tài liệu và ma trận truy vết.
- **Prompt đầu vào:**
  ```text
  bổ sung các testcase ## IV. Test Case bổ sung cho FR-13 – Dashboard ...
  ```
- **Kết quả AI sinh ra:**
  - Thiết kế và tạo 24 tệp testcase mới từ [TC-DASHBOARD-DT-013.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/dashboard/TC-DASHBOARD-DT-013.md) đến [TC-DASHBOARD-DT-024.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/dashboard/TC-DASHBOARD-DT-024.md) và [TC-DASHBOARD-BVA-011.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/dashboard/TC-DASHBOARD-BVA-011.md) đến [TC-DASHBOARD-BVA-022.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-cases/dashboard/TC-DASHBOARD-BVA-022.md) trong thư mục `tests/test-cases/dashboard/`.
  - Cập nhật các tài liệu thiết kế kịch bản [reports/FR-13/domain-testing.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/reports/FR-13/domain-testing.md) và [reports/FR-13/boundary-value-analysis.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/reports/FR-13/boundary-value-analysis.md).
  - Đồng bộ số liệu thống kê trong báo cáo chính [main-report.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/main-report.md) và bảng truy vết [traceability-matrix.md](file:///c:/My%20Workspace/HCMUS/Test/Week%203/Hw2/tests/test-summary/traceability-matrix.md).

### Lượt tương tác 9
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-28 23:54
- **Nhiệm vụ:** Bổ sung lỗi giỏ hàng không được xóa sạch sau khi thanh toán thành công (checkout success).
- **Prompt đầu vào:**
  ```text
  Thêm 1 lỗi ở cart khi đã thanh toán xong nhưng trong cart vẫn hiện lại những món đã thanh toán
  ```
- **Kết quả AI sinh ra:**
  - Tạo tệp testcase `TC-CART-089.md` và tệp báo cáo lỗi `BUG-FR07-B-19.md` trong thư mục `tests/bug/cart/`.
  - Cập nhật tài liệu `main-report.md`, `bug_report.md` và `tests/test-summary/traceability-matrix.md`.

---

## 2. Báo cáo Tự phê bình AI (AI Critique)

Trong suốt quá trình đồng hành thiết kế kịch bản và chạy thử nghiệm cho tính năng Đăng nhập & Khóa tài khoản (FR-02), Giỏ hàng (FR-07) và Dashboard (FR-13), công cụ AI đã chứng minh hiệu quả cao trong việc tự động sinh cấu trúc kiểm thử BVA/EP và xử lý dữ liệu lớn, song vẫn còn một số điểm thiếu sót đáng chú ý:

1. **Sai sót và thiếu sót của AI:** 
   - Ban đầu, AI đã thiết kế thiếu các kịch bản kiểm thử bảo mật nâng cao liên quan đến tính nhất quán của định dạng email (case-sensitivity) và trạng thái đồng bộ khóa của tài khoản khi người dùng thực hiện reset mật khẩu.
   - Đối với Giỏ hàng và Dashboard, AI có xu hướng thiết kế testcase dựa trên giả định spec lý thuyết, dễ bỏ sót kịch bản kiểm thử bảo mật ở mức API backend (ví dụ: client gửi unit price giả mạo để bypass, hay API admin thiếu kiểm tra role của user) cho đến khi người dùng định hướng kiểm thử hoặc yêu cầu kiểm tra code.
2. **Nguyên nhân bỏ sót:** Những thiếu sót này xuất phát từ việc prompt ban đầu của người dùng tập trung vào các luồng nghiệp vụ cơ bản (số lần nhập sai, các số liệu dashboard hiển thị). Giới hạn ngữ cảnh của AI có xu hướng tối ưu hóa các ca kiểm thử theo mô tả trực tiếp từ đặc tả thay vì chủ động phân tích tĩnh mã nguồn để chỉ ra các kịch bản biên hoặc bảo mật phức tạp ngoài đặc tả.
3. **Bài học kinh nghiệm:** Sự kết hợp hiệu quả giữa người và máy đòi hỏi người dùng cần có vai trò phản biện, định hướng prompt chi tiết và yêu cầu AI thực hiện phân tích tĩnh (static analysis) mã nguồn thực tế. Việc đối chiếu trực tiếp mã nguồn giúp phát hiện sớm các bugs logic cực kỳ nghiêm trọng (như bug nhân đôi doanh thu hiển thị ở App.jsx hay hỏng phân quyền ở server.js) trước khi chuyển qua chạy test động.


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

---

## 2. Báo cáo Tự phê bình AI (AI Critique)

Trong suốt quá trình đồng hành thiết kế kịch bản và chạy thử nghiệm cho tính năng Đăng nhập & Khóa tài khoản (FR-02), công cụ AI đã chứng minh hiệu quả cao trong việc tự động sinh cấu trúc kiểm thử BVA/EP và xử lý dữ liệu lớn, song vẫn còn một số điểm thiếu sót đáng chú ý:

1. **Sai sót và thiếu sót của AI:** Ban đầu, AI đã thiết kế thiếu các kịch bản kiểm thử bảo mật nâng cao liên quan đến tính nhất quan của định dạng email (case-sensitivity) và trạng thái đồng bộ khóa của tài khoản khi người dùng thực hiện reset mật khẩu. AI cũng bỏ qua việc phân vùng đầy đủ các lớp tương đương định dạng email (như subdomain, ký tự Unicode) cho đến khi người dùng yêu cầu bổ sung chi tiết.
2. **Nguyên nhân bỏ sót:** Những thiếu sót này xuất phát từ việc prompt ban đầu của người dùng tập trung vào các luồng nghiệp vụ cơ bản của lockout (số lần nhập sai, thời gian khóa). Giới hạn ngữ cảnh của AI có xu hướng tối ưu hóa các ca kiểm thử theo mô tả trực tiếp từ mã nguồn hiện tại thay vì suy luận các kịch bản biên bảo mật phức tạp ngoài đặc tả nếu không được định hướng cụ thể.
3. **Bài học kinh nghiệm:** Sự kết hợp hiệu quả giữa người và máy đòi hỏi người dùng cần có vai trò phản biện, đưa ra định hướng prompt chi tiết (ví dụ: yêu cầu rõ ràng các nhóm EP/BVA riêng biệt cho độ dài và định dạng email). Đồng thời, việc AI thực hiện phân tích tĩnh mã nguồn song song với viết kịch bản giúp phát hiện sớm các lỗ hổng bảo mật nghiêm trọng (như thiếu Refresh Token hay Remember Me) mà quy trình chạy test động thông thường dễ bỏ qua.

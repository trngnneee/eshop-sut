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
  - Thiết kế và tạo 8 testcase từ [TC-LOGIN-024.md](../test-cases/login/TC-LOGIN-024.md) đến [TC-LOGIN-031.md](../test-cases/login/TC-LOGIN-031.md).
  - Phát hiện 2 lỗi mới trên hệ thống SUT và tạo báo cáo lỗi: [BUG-FR02-A-18.md](../bug/login/BUG-FR02-A-18.md) và [BUG-FR02-A-19.md](../bug/login/BUG-FR02-A-19.md).
  - Tự động chạy script Python đẩy 2 lỗi này thành Issue #48 và Issue #49 trên GitHub.

### Lượt tương tác 2
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-26 05:32
- **Nhiệm vụ:** Bổ sung 73 testcase mở rộng cho Login/Lockout (loại bỏ Logout và các testcase trùng lặp), cập nhật ma trận truy vết và phát hiện thêm 3 lỗi.
- **Prompt đầu vào:**
  ```text
  bổ sung test case cho Logout [danh sách chi tiết 11 nhóm]
  đồng ý [lược bỏ Logout và các testcase trùng lặp]
  ```
- **Kết quả AI sinh ra:**
  - Viết script Python tự động sinh 73 tệp tin testcase trong thư mục [tests/test-cases/login/](../test-cases/login).
  - Phát hiện 3 lỗi mới qua kiểm thử API và logic hệ thống và tạo báo cáo lỗi: [BUG-FR02-A-20.md](../bug/login/BUG-FR02-A-20.md) (Issue #50), [BUG-FR02-A-21.md](../bug/login/BUG-FR02-A-21.md) (Issue #51), và [BUG-FR02-A-22.md](../bug/login/BUG-FR02-A-22.md) (Issue #52).
  - Cập nhật ma trận truy vết [traceability-matrix.md](traceability-matrix.md).

### Lượt tương tác 3
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-26 14:54
- **Nhiệm vụ:** Triển khai báo cáo tương tác AI (AI Audit Report) và phần tự phê bình (AI Critique).
- **Prompt đầu vào:**
  ```text
  Làm theo skill mới được cập nhập
  ```
- **Kết quả AI sinh ra:**
  - Tạo tệp phụ lục [ai-audit-report.md](ai-audit-report.md) bao gồm nhật ký tương tác và báo cáo tự phê bình.

### Lượt tương tác 4
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-26 14:16
- **Nhiệm vụ:** Tự động sinh cấu trúc và nội dung chi tiết cho 47 test case thuộc FR-07 (Giỏ hàng Web) theo đặc tả yêu cầu, cập nhật ma trận truy vết (traceability matrix) và báo cáo tương tác AI.
- **Prompt đầu vào:**
  ```text
  [Bảng danh sách 47 test case cho FR-07: Giỏ hàng Web từ người dùng]
  ```
- **Kết quả AI sinh ra:**
  - Viết và thực thi script Python tự động tạo 47 tệp test case từ [TC-CART-001.md](../test-cases/cart/TC-CART-001.md) đến [TC-CART-047.md](../test-cases/cart/TC-CART-047.md) trong thư mục `tests/test-cases/cart/`.
  - Cập nhật ma trận truy vết [traceability-matrix.md](traceability-matrix.md) để ánh xạ 47 test case này với các FR-07, FR-21, FR-23 và FR-24.

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
  - Phát hiện 2 lỗi logic và bảo mật quan trọng của Dashboard (doanh thu bị nhân đôi và lỗi phân quyền API).

### Lượt tương tác 8
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-28 19:16
- **Nhiệm vụ:** Bổ sung 24 testcase mở rộng cho FR-13 Dashboard (12 Domain Testing và 12 Boundary Value Analysis), cập nhật tài liệu và ma trận truy vết.
- **Prompt đầu vào:**
  ```text
  bổ sung các testcase ## IV. Test Case bổ sung cho FR-13 – Dashboard ...
  ```
- **Kết quả AI sinh ra:**
  - Thiết kế và tạo 24 tệp testcase mới từ [TC-DASHBOARD-DT-013.md](../test-cases/dashboard/TC-DASHBOARD-DT-013.md) đến [TC-DASHBOARD-DT-024.md](../test-cases/dashboard/TC-DASHBOARD-DT-024.md) và [TC-DASHBOARD-BVA-011.md](../test-cases/dashboard/TC-DASHBOARD-BVA-011.md) đến [TC-DASHBOARD-BVA-022.md](../test-cases/dashboard/TC-DASHBOARD-BVA-022.md) trong thư mục `tests/test-cases/dashboard/`.
  - Cập nhật các tài liệu thiết kế kịch bản [reports/FR-13/domain-testing.md](../../reports/FR-13/domain-testing.md) và [reports/FR-13/boundary-value-analysis.md](../../reports/FR-13/boundary-value-analysis.md).
  - Đồng bộ số liệu thống kê trong báo cáo chính [main-report.md](../../main-report.md) và bảng truy vết [traceability-matrix.md](traceability-matrix.md).

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

### Lượt tương tác 10
- **Tên công cụ AI:** Antigravity (Gemini-based AI Coding Assistant)
- **Thời gian thực hiện:** 2026-06-29 01:30
- **Nhiệm vụ:** Phân tích miền, lập phân vùng tương đương, thiết kế testcase Domain/BVA cho FR-21 Mobile Cart & Checkout.
- **Prompt đầu vào:**
  ```text
  Hãy sử dụng skill eshop-domain-bva-testing-skill. Đọc SKILL.md và thực hiện đúng workflow. Feature cần demo là FR-21 Giỏ hàng và thanh toán.
  ```
- **Kết quả AI sinh ra:**
  - Lập phân vùng tương đương và thiết kế 19 testcase Domain Testing và 22 testcase BVA cho Mobile Cart & Checkout trong `tests/test-cases/mobile-cart/`.
  - Tạo tài liệu phân tích [reports/FR-21/domain-testing.md](../../reports/FR-21/domain-testing.md) và [reports/FR-21/boundary-value-analysis.md](../../reports/FR-21/boundary-value-analysis.md).
  - Tạo báo cáo Gap Analysis [reports/FR-21/ai-gap-analysis.md](../../reports/FR-21/ai-gap-analysis.md).
  - Ph�    - Đối với module Mobile Cart & Checkout (FR-21), AI nếu chỉ dựa trên spec đầu vào sẽ hoàn toàn bỏ sót các lỗi logic cực kỳ ẩn như lỗi bỏ quên truyền thông tin địa chỉ giao hàng khi đặt hàng, và lỗi tự động tăng số lượng lên 1 khi người dùng chỉnh sửa trực tiếp trong giỏ hàng.
2. **Nguyên nhân bỏ sót:** Những thiếu sót này xuất phát từ việc prompt ban đầu của người dùng tập trung vào các luồng nghiệp vụ cơ bản (số lần nhập sai, các số liệu dashboard hiển thị). Giới hạn ngữ cảnh của AI có xu hướng tối ưu hóa các ca kiểm thử theo mô tả trực tiếp từ đặc tả thay vì chủ động kiểm thử khám phá để phát hiện các hành vi sai lệch ngoài đặc tả.
3. **Bài học kinh nghiệm:** Sự kết hợp hiệu quả giữa người và máy đòi hỏi người dùng cần có vai trò phản biện, định hướng prompt chi tiết và thực nghiệm kiểm thử trực tiếp trên ứng dụng thực tế. Việc kiểm thử khám phá giúp phát hiện sớm các lỗi logic cực kỳ nghiêm trọng (như lỗi hiển thị doanh thu bị nhân đôi trên giao diện Dashboard Admin, lỗi thiếu phân quyền ở API admin, lỗi tự động tăng số lượng lên 1 khi người dùng chỉnh sửa trực tiếp trong giỏ hàng di động) trước khi chốt kịch bản.��t ở mức API backend (ví dụ: client gửi unit price giả mạo để bypass, hay API admin thiếu kiểm tra role của user) cho đến khi người dùng định hướng kiểm thử hoặc yêu cầu kiểm thử khám phá thực tế.
   - Đối với module Mobile Cart & Checkout (FR-21), AI nếu chỉ dựa trên spec đầu vào sẽ hoàn toàn bỏ sót các lỗi logic cực kỳ ẩn như lỗi tự động loại bỏ sản phẩm cuối cùng khỏi đơn hàng khi thanh toán nhiều sản phẩm, lỗi bỏ quên truyền thông tin địa chỉ giao hàng khi đặt hàng, và lỗi tự động tăng số lượng lên 1 khi người dùng chỉnh sửa trực tiếp trong giỏ hàng.
2. **Nguyên nhân bỏ sót:** Những thiếu sót này xuất phát từ việc prompt ban đầu của người dùng tập trung vào các luồng nghiệp vụ cơ bản (số lần nhập sai, các số liệu dashboard hiển thị). Giới hạn ngữ cảnh của AI có xu hướng tối ưu hóa các ca kiểm thử theo mô tả trực tiếp từ đặc tả thay vì chủ động kiểm thử khám phá để phát hiện các hành vi sai lệch ngoài đặc tả.
3. **Bài học kinh nghiệm:** Sự kết hợp hiệu quả giữa người và máy đòi hỏi người dùng cần có vai trò phản biện, định hướng prompt chi tiết và thực nghiệm kiểm thử trực tiếp trên ứng dụng thực tế. Việc kiểm thử khám phá giúp phát hiện sớm các lỗi logic cực kỳ nghiêm trọng (như lỗi hiển thị doanh thu bị nhân đôi trên giao diện Dashboard Admin, lỗi thiếu phân quyền ở API admin, lỗi tự động cắt sản phẩm trong giỏ hàng di động) trước khi chốt kịch bản.
   - Đồng thời, việc thực hiện kiểm thử khám phá song song giúp phát hiện sớm các lỗ hổng logic và bảo mật nghiêm trọng mà quy trình kiểm thử thông thường dễ bỏ qua.



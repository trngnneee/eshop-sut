---
name: domain-testing-skill
description: Use this skill when you need to perform Domain Testing (Phân vùng tương đương & Phân tích giá trị biên), design and structure test cases, write automated test scripts, log test runs, report bugs, and maintain the Traceability Matrix on GitHub.
---
# Domain Testing Skill (EP + BVA + GitHub Management)

## Mục tiêu (Goal)
Kỹ năng này kết hợp toàn bộ quy trình kiểm thử miền (Domain Testing) bao gồm Phân vùng tương đương (EP) và Phân tích giá trị biên (BVA) với quy trình quản lý kiểm thử trên GitHub. AI sẽ đồng hành cùng sinh viên thiết kế test case có cấu trúc, tạo test script tự động, ghi nhận test run, báo cáo bug và duy trì bảng Traceability Matrix.

## Quy trình 7 bước Thực hiện (Instructions)

1. **Bước 1: Phân tích & Xác định Lớp tương đương (EP):**
   * Phân tích *đầy đủ* yêu cầu của chức năng đang xét, từ đó xác định *TẤT CẢ* các biến đầu vào/đầu ra của chức năng cụ thể trên EShop.
   * Với mỗi biến, xác định các lớp tương đương **Hợp lệ (Valid)** và **Không hợp lệ (Invalid)** của biến đó. 
   * Với mỗi biến, mỗi lớp tương đương của nó được xác định 1 giá trị đại diện.
2. **Bước 2: Phân tích Giá trị Biên (BVA):**
   * Với mỗi biến, từ các miền giá trị đã xác định ở bước 1, xác định các giá trị biên của các miền giá trị (sử dụng chiến lược biên 2 điểm hoặc 3 điểm).
3. **Bước 3: Thiết kế các Test Cases chi tiết:**
   * Viết các test case riêng biệt theo cấu trúc Markdown chuẩn của môn học.
   * Quy ước đặt mã test case: `TC-[MODULE]-[NUMBER]` (Ví dụ: `TC-CART-001`).
   * Cấu trúc file test case phải đầy đủ các trường: Requirement ID, Technique, Preconditions, Test data, Test steps, Expected result, Status/Related bugs.
   * **Lưu ý:**
     * Đối với các lớp hợp lệ: Chọn các test case sao cho bao phủ được càng nhiều lớp hợp lệ cùng lúc càng tốt.
     * Đối với các lớp không hợp lệ: Mỗi test case chỉ nên chứa **duy nhất một** giá trị thuộc lớp không hợp lệ để tránh hiện tượng lỗi này che lấp lỗi kia.
     * Tất cả các giá trị biên đã xác định.
     * **Cô lập lỗi**: Tại 1 thời điểm chỉ quan tâm đến miền giá trị đang xét của 1 biến, các biến khác lấy giá trị đại diện trong miền hợp lệ của nó
4. **Bước 4: Tạo Test Script tự động (Automated Test Script):**
   * **BẮT BUỘC:** Trước khi thực thi nghiệm thu, viết mã kịch bản kiểm thử tự động (ví dụ: Cypress, Playwright, hoặc Selenium) cho test case tương ứng để tích hợp chạy CI/CD.
5. **Bước 5: Ghi nhận Test Run:**
   * Cập nhật kết quả chạy test case vào file nhật ký `sprint-X-test-run.md`.
   * Ghi nhận các trường thông tin: Test Case ID, Module, Tester, Result (Pass/Fail/Blocked/Not Run), Related Bug, Note.
6. **Bước 6: Ghi nhận Lỗi (Create Bug Report):**
   * Nếu kết quả chạy kiểm thử là **Fail** hoặc **Blocked**, tạo 1 file bug report tương ứng định dạng Markdown và lưu vào thư mục `tests/bug-reports/` (Ví dụ: `tests/bug-reports/BUG-CART-001.md`).
   * Cấu trúc Bug Report gồm: Title `[BUG][Module] Description`, Found by Test Case, Requirement liên quan, Severity/Priority, Environment, Steps to reproduce, Expected/Actual result, Evidence.
   * Phần metadata của file bug report cần ghi rõ các nhãn (Labels): `type: bug`, `module: [module]`, `severity: [severity]`, `priority: [priority]`, `status: new`, `found-by: test-case` để sẵn sàng tạo Issue trên GitHub.
7. **Bước 7: Cập nhật Ma trận Truy vết (Traceability Matrix):**
   * Cập nhật file `traceability-matrix.md` để chứng minh độ bao phủ (coverage) và không bỏ sót lỗi.

## Tham chiếu (References)
* Xem ví dụ cụ thể và mẫu biểu chi tiết tại [domain_testing_guide.md](references/domain_testing_guide.md).

## Ràng buộc (Constraints)
* Đảm bảo liên kết hai chiều chặt chẽ: Bug Issue phải ghi rõ `Found by Test Case`, Test Case bị fail phải ghi rõ `Related bug #...`.
* Test case không được sửa trực tiếp trên nhánh `main`. Phải tạo nhánh (branch) mới và tạo Pull Request để review.
* Sau khi hoàn tất Domain Testing cho 1 chức năng, tiến hành ghi 3 bước đầu tiên (Phân tích & Xác định Lớp tương đương (EP), Phân tích Giá trị Biên (BVA), Thiết kế các Test Cases chi tiết) vào file MainReport.md vào đúng phần chức năng đã test. Cách trình bày tham khảo file [domain_testing_guide.md](references/domain_testing_guide.md), ưu tiên trình bày theo dạng bảng. Đồng thời, với mỗi bug tìm được, ghi vào phần ## 4. BÁO CÁO LỖI (BUG REPORT) trong MainReport.md theo đúng định dạng yêu cầu trong file (chừa phần ảnh chụp github issue, tôi sẽ chèn sau).

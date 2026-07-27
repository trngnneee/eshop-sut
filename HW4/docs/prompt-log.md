# AI Generation Prompt Log (Nhật ký Tương tác AI)

**Student ID**: `23127207`  
**Task**: HW4 - Single Test Case Login Automation Script  
**Date**: 2026-07-27

---

## Bước 1: Khảo sát Hệ thống SUT & Thu thập Locator

- **Thời gian**: `2026-07-27 14:45:30`
- **Mục tiêu**: Phân tích cấu trúc thư mục backend/frontend-web, tìm các trường đăng nhập, tài khoản mặc định và hành vi chuyển hướng sau khi đăng nhập thành công.
- **Prompt đã sử dụng**:
  > "Hãy kiểm tra cấu trúc repository EShop SUT, xác định URL trang đăng nhập, cách khởi động backend/frontend, tài khoản người dùng hợp lệ trong database.js và các thành phần DOM trang login.jsx để lập tài liệu system-analysis.md."
- **Kết quả AI tạo ra**: AI đã xác định đúng URL `http://localhost:5173/login`, tài khoản `test@eshop.com` / `Test1234!`, và cấu trúc giao diện trang login.
- **Thay đổi thực hiện sau review**: Phát hiện thẻ `<label>` không bọc ngoài `<input>` và không có `htmlFor`, do đó cập nhật locator từ `getByLabel` đơn thuần sang locator dựa trên container filter text để đảm bảo không bị time out.

---

## Bước 2: Xây dựng Schema & File Dữ liệu Kiểm thử (Test Data)

- **Thời gian**: `2026-07-27 14:48:40`
- **Mục tiêu**: Tạo file dữ liệu tách biệt `HW4/test-data/login-data.json` theo nguyên tắc Data-driven testing cho TC-LOGIN-001.
- **Prompt đã sử dụng**:
  > "Tạo file HW4/test-data/login-data.json chứa đúng 01 bộ dữ liệu kiểm thử cho TC-LOGIN-001 bao gồm email, password, expectedUrl, expectedVisibleText và expectedUserGreeting."
- **Kết quả AI tạo ra**: File JSON chuẩn hóa với đầy đủ các trường thông tin cần thiết.
- **Thay đổi thực hiện sau review**: Đã xác nhận không hardcode thông tin nhạy cảm hay expected result trong file code test, truyền đầy đủ primitive value từ JSON.

---

## Bước 3: Viết Kịch bản Automation Test Playwright (`login.spec.ts`)

- **Thời gian**: `2026-07-27 14:48:50`
- **Mục tiêu**: Tạo duy nhất 01 Playwright test trong `HW4/tests/login.spec.ts` đọc dữ liệu từ JSON, kiểm tra cấu trúc dữ liệu trước khi dùng và thực hiện 3 pattern assertion.
- **Prompt đã sử dụng**:
  > "Viết duy nhất 01 Playwright test case TC-LOGIN-001 trong file HW4/tests/login.spec.ts sử dụng TypeScript. Kiểm tra cấu trúc JSON bằng loadAndValidateLoginData(), thực hiện luồng đăng nhập và kiểm tra với toHaveURL(), toBeVisible(), toContainText()."
- **Kết quả AI tạo ra**: Mã nguồn Playwright với đầy đủ các bước điều hướng, điền thông tin, click button và 3 patterns assertion.
- **Thay đổi thực hiện sau review**: Thêm `testInfo.annotations.push` để ghi nhận `Run by: 23127207` trực tiếp vào metadata của test suite.

---

## Bước 4: Cấu hình Multi-Browser Matrix & Tách HTML Reports

- **Thời gian**: `2026-07-27 14:52:40`
- **Mục tiêu**: Cấu hình `playwright.config.ts`, 3 browser projects (Chromium, Firefox, WebKit), và tạo script inject Student ID `23127207` vào báo cáo HTML riêng biệt cho từng trình duyệt.
- **Prompt đã sử dụng**:
  > "Cấu hình playwright.config.ts cho 3 project Chromium, Firefox, WebKit. Tách riêng thư mục xuất HTML report theo biến môi trường BROWSER (reports/chromium, reports/firefox, reports/webkit) và đảm bảo dòng 'Run by: 23127207' xuất hiện trực tiếp trong title và banner của index.html."
- **Kết quả AI tạo ra**: File `playwright.config.ts` và script `HW4/scripts/inject-student-id.js` hoàn chỉnh.
- **Thay đổi thực hiện sau review**: Tích hợp lệnh `node scripts/inject-student-id.js` trực tiếp vào các npm scripts (`test:chromium`, `test:firefox`, `test:webkit`) trong `package.json` để tự động hóa hoàn toàn.

---

## Bước 5: Thực thi & Kiểm tra Báo cáo Bằng Chứng

- **Thời gian**: `2026-07-27 14:53:00`
- **Mục tiêu**: Chạy test trên cả 3 trình duyệt, kiểm tra kết quả pass/fail và xác nhận dòng `Run by: 23127207` có mặt trong cả 3 báo cáo HTML.
- **Prompt đã sử dụng**:
  > "Chạy toàn bộ test suite trên Chromium, Firefox và WebKit, kiểm tra trạng thái pass và verify sự tồn tại của dòng Student ID trong cả 3 file index.html."
- **Kết quả AI tạo ra**: Cả 3 trình duyệt đều chạy thành công 100% (Pass). Ba báo cáo HTML độc lập được sinh ra đầy đủ.
- **Thay đổi thực hiện sau review**: Kiểm tra bằng `grep_search` xác nhận dòng `<title>Run by: 23127207 | Playwright Test Report (...)</title>` đã có mặt ở cả 3 thư mục `HW4/reports/chromium/`, `HW4/reports/firefox/`, `HW4/reports/webkit/`.

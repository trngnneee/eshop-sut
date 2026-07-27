# Senior QA AI Review & Code Audit Report

**Student ID**: `23127207`  
**Reviewer Role**: Senior QA/QC Automation Engineer  
**Scope**: Verification of AI-generated Playwright automation artifacts for `TC-LOGIN-001`  
**Date**: 2026-07-27

---

## 1. AI-Generated Initial Approach (Cách tiếp cận ban đầu của AI)

AI đã thực hiện khởi tạo kịch bản automation với các định hướng chính:
- Sử dụng framework `@playwright/test` với ngôn ngữ TypeScript.
- Khai báo duy nhất 01 kịch bản test `TC-LOGIN-001` kiểm thử luồng đăng nhập thành công.
- Sử dụng locator chuẩn của Playwright như `getByLabel('Username')`, `getByLabel('Mật khẩu')`, `getByRole('button', { name: 'Sign In' })`.
- Đọc dữ liệu từ file JSON riêng biệt `HW4/test-data/login-data.json`.
- Thiết lập cấu hình `playwright.config.ts` hỗ trợ 3 trình duyệt Chromium, Firefox, WebKit.

---

## 2. Problems Found in AI Output (Các vấn đề phát hiện được qua Review)

Qua kiểm tra thực tế trên hệ thống SUT và mã nguồn sinh ra, Senior QA đã phát hiện 4 vấn đề kỹ thuật quan trọng:

### Vấn đề 1: Selector bị đơ (Timeout Error) do cấu trúc DOM thực tế
- **Chi tiết**: AI sử dụng `page.getByLabel('Username')` và `page.getByLabel('Mật khẩu')`. Tuy nhiên, trong `Login.jsx` của hệ thống SUT, thẻ `<label>` không có thuộc tính `htmlFor` và không bọc ngoài `<input>`.
- **Hậu quả**: Playwright không thể liên kết label với input trong Accessibility Tree, dẫn tới test bị `Timeout 30000ms` khi chờ locator.

### Vấn đề 2: Ghi đè HTML Report khi chạy liên tiếp các trình duyệt
- **Chi tiết**: Cấu hình reporter mặc định trong AI script ghi toàn bộ báo cáo vào một thư mục cố định (`playwright-report/` hoặc `reports/`).
- **Hậu quả**: Lần chạy trình duyệt sau (Firefox, WebKit) ghi đè lên báo cáo của trình duyệt trước (Chromium), làm mất bằng chứng kiểm thử độc lập.

### Vấn đề 3: Thiếu hiển thị Student ID `23127207` trong giao diện HTML Report
- **Chi tiết**: AI chỉ đặt Student ID trong file README mà không đưa thông tin Student ID vào trong HTML Report tĩnh được Playwright sinh ra.
- **Hậu quả**: Báo cáo HTML không hiển thị trực tiếp dòng `Run by: 23127207` ở tiêu đề hoặc trang báo cáo.

### Vấn đề 4: Thiếu hàm kiểm tra cấu trúc dữ liệu JSON (Runtime Validation)
- **Chi tiết**: Bản mã ban đầu dùng `require('../test-data/login-data.json')` trực tiếp mà không kiểm tra xem các trường `email`, `password`, `expectedUrl` có tồn tại và đúng kiểu dữ liệu hay không.
- **Hậu quả**: Nguy cơ crash không rõ nguyên nhân nếu file JSON bị thiếu trường dữ liệu hoặc rỗng.

---

## 3. Why AI Made or Missed Those Problems (Nguyên nhân AI mắc phải hoặc bỏ sót)

1. **Về Locator**: AI đưa ra giả định lý tưởng rằng giao diện Web luôn tuân thủ chuẩn WAI-ARIA accessibility (thẻ label luôn liên kết với input via `for/id`). AI không phân tích DOM tĩnh của file `Login.jsx` trước khi chọn locator.
2. **Về HTML Report**: Cấu hình HTML reporter mặc định của Playwright không tự động phân tách theo từng browser project nếu không có tham số `outputFolder` động hoặc script điều hướng runner.
3. **Về Student ID Branding**: AI sinh code theo mẫu chung (generic template) nên không tự động can thiệp vào file HTML report tĩnh sau khi Playwright build xong trừ khi được thiết lập script hậu xử lý.
4. **Về Validation**: AI thường tập trung vào happy path khi đọc file JSON bằng `import` hoặc `require` mà bỏ qua bước kiểm soát lỗi dữ liệu đầu vào (defensive programming).

---

## 4. Corrections Made by the Student (Các sửa đổi và cải tiến đã thực hiện)

1. **Cải tiến Locator**:
   - Thay `getByLabel('Username')` bằng `page.locator('div').filter({ hasText: /^Username$/ }).locator('input')`.
   - Thay `getByLabel('Mật khẩu')` bằng `page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input')`.
   - Giữ nguyên locator chuẩn `getByRole('button', { name: 'Sign In' })`.
2. **Phân tách HTML Report riêng biệt**:
   - Thiết lập `playwright.config.ts` nhận biến môi trường `process.env.BROWSER` để chỉ định `outputFolder: reports/${targetBrowser}`.
   - Kết quả sinh ra 3 thư mục báo cáo độc lập: `HW4/reports/chromium/`, `HW4/reports/firefox/`, `HW4/reports/webkit/`.
3. **Hiển thị trực tiếp Student ID `23127207`**:
   - Viết script `HW4/scripts/inject-student-id.js` tự động cập nhật `<title>Run by: 23127207 | Playwright Test Report (...)</title>` và thêm banner hiển thị `Run by: 23127207` ngay trên đầu trang HTML report.
   - Tích hợp vào tất cả các lệnh `npm run test:*`.
4. **Thêm Runtime Data Validation**:
   - Xây dựng hàm `loadAndValidateLoginData(filePath)` kiểm tra sự tồn tại của file và tính hợp lệ của tất cả các trường thuộc tính JSON trước khi test case khởi chạy.

---

## 5. Final Responsibility Statement (Tuyên bố Trách nhiệm Về Mã Nguồn)

Tất cả các tệp tin trong thư mục `HW4/` bao gồm mã nguồn test TypeScript, tệp dữ liệu JSON, cấu hình Playwright, tài liệu và các báo cáo HTML đã được kiểm tra, rà soát thủ công và chạy thực tế 100% trên cả 3 trình duyệt (Chromium, Firefox, WebKit) bởi học viên. Học viên chịu hoàn toàn trách nhiệm về tính chính xác, tính ổn định và tính trung thực của kết quả kiểm thử được báo cáo.

**Học viên thực hiện**:  
MSSV: `23127207`

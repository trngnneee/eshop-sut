# AI Audit Report - HW04 Automation Testing

I use AI tools for the following tasks:

## Interaction Log

### [1] FR-05 - Phân tích yêu cầu xem danh sách và tìm kiếm sản phẩm
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 22:50
- **Prompt:**
  > Hãy phân tích FR-05
- **Output:**
  AI đã đọc skill HW04 automation-testing, kiểm tra `feature_pools.md`, `README.md`, `api_specification.md`, `frontend-web/src/pages/Home.jsx`, `backend/server.js` và `backend/database.js`, sau đó tóm tắt phạm vi FR-05. Output ban đầu xác định luồng chính, các yêu cầu có thể kiểm thử và một số bug candidate: từ khóa tìm kiếm có nguy cơ render HTML không an toàn, ảnh sản phẩm thiếu `alt` mô tả, thiếu loading state, thiếu empty state, có thể có nhiều hơn một thẻ `<h1>`, và API tìm kiếm có rủi ro SQL injection.
- **Accepted as-is / Modified:** Modified after human review. Người review nhắc lại rằng test phải bám đặc tả FR-05 trong README, không bám code hiện tại. Các ghi chú review được giữ lại theo hướng “expected theo đặc tả; nếu code hiện tại khác thì xem là bug”.

### [2] FR-05 - Tạo các file Markdown cho test case
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 22:52
- **Prompt:**
  > Hãy tạo các file md cho các test case
- **Output:**
  AI đã tạo `hw04-automation/docs/test-cases/FR-05-test-cases.md` và các file Markdown riêng từ `TC-FR05-01.md` đến `TC-FR05-14.md`. Bộ test gồm 14 test case bao phủ luồng positive, edge case, negative/security, accessibility, semantic HTML và loading behavior. Tất cả test case đang có `Status = Not Run` vì chưa sinh và chạy automation script.
- **Accepted as-is / Modified:** Modified after human feedback. Yêu cầu chuyển nội dung các file sang tiếng Việt có dấu, đúng chính tả, và làm rõ expected result theo đặc tả. AI đã cập nhật lại toàn bộ file Markdown sang tiếng Việt và bổ sung ghi chú rằng giá mong đợi phải dùng đơn vị `₫`, không dùng `VND`.

### [3] FR-05 - Tạo file dữ liệu kiểm thử
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 22:57
- **Prompt:**
  > Tạo data file data/fr05.json từ các test case vừa thiết kế.
- **Output:**
  AI đã tạo `hw04-automation/data/fr05.json` với dữ liệu sản phẩm seed, input/expected cho tìm kiếm, payload negative, expectation về semantic HTML và dữ liệu delay API để kiểm tra loading cho TC-FR05-01 đến TC-FR05-14. AI cũng cập nhật các reference trong Markdown từ `data/fr05-product-search.json` sang `data/fr05.json`.
- **Accepted as-is / Modified:** Modified after human review. Phát hiện expected giá ban đầu đang bám code hiện tại (`VND`, dấu phẩy) thay vì bám đặc tả README. AI đã sửa `fr05.json` để expected giá dùng đơn vị `₫` và phân cách hàng nghìn theo dạng `30.000.000 ₫`; đồng thời chuyển mô tả trong data file sang tiếng Việt có dấu. JSON đã được validate lại bằng `ConvertFrom-Json`.

### [4] FR-05 - Step A tạo locator/page object
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:28
- **Prompt:**
  > Bước A: tạo locators/page object cho trang **Xem danh sách & Tìm kiếm sản phẩm (FR-05)**
- **Output:**
  AI đã tạo `hw04-automation/tests/pages/ProductListingPage.js` với page object cho trang danh sách và tìm kiếm sản phẩm. Page object gồm locator cho heading chính, tất cả thẻ `h1`, form tìm kiếm, ô tìm kiếm, nút submit, lưới sản phẩm, thẻ sản phẩm, ảnh, giá, link xem chi tiết, nút thêm vào giỏ, search summary và error panel. AI cũng tạo `hw04-automation/docs/locator-review/FR-05-locators.md` để review độ ổn định của selector và ghi chú các selector còn phụ thuộc CSS class do app chưa có `data-testid`.
- **Accepted as-is / Modified:** Accepted with selector review notes. Cú pháp JavaScript đã được kiểm tra bằng `node --check`. Các locator text tiếng Việt được hạn chế vì source UI hiện tại có dấu hiệu lỗi encoding; khi có thể cải thiện app, nên bổ sung `data-testid` cho product grid, product card, product price, search summary và error panel.

### [5] FR-05 - Step B sinh automation cho TC-FR05-01 và TC-FR05-02
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:30
- **Prompt:**
  > Bước B: sinh automation cho **TC-FR05-01**, **TC-FR05-02** dùng locator trên
- **Output:**
  AI đã tạo `hw04-automation/tests/fr05-listing.spec.js` dùng `ProductListingPage` và dữ liệu từ `hw04-automation/data/fr05.json`. Spec hiện chỉ có hai test: `TC-FR05-01` kiểm tra trang chủ hiển thị đủ số lượng và tên sản phẩm seed; `TC-FR05-02` kiểm tra mỗi product card có ảnh, tên, giá, link xem chi tiết và nút thêm vào giỏ. Helper `openProductListing` chờ response `GET /api/products` trước khi assert lưới sản phẩm.
- **Accepted as-is / Modified:** Accepted. Cú pháp JavaScript đã được kiểm tra bằng `node --check`. Exact price format theo đặc tả FR-05 chưa được assert trong TC-FR05-02 để tránh trộn với TC-FR05-03, case chuyên kiểm tra định dạng giá.

### [6] HW04 - Tạo package.json và Playwright config
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:35
- **Prompt:**
  > thêm file package.json trong thư mục hw4 và file config playwright
- **Output:**
  AI đã tạo `hw04-automation/package.json` với dependency `@playwright/test` và các script `test`, `report`, `stamp-report`. AI cũng tạo `hw04-automation/playwright.config.js` với `testDir: "./tests"`, HTML/list reporter, 3 browser projects Chromium/Firefox/WebKit, trace/screenshot khi fail, metadata `Run by` và ISO timestamp. `baseURL` được đặt mặc định là `http://localhost:5173` để chạy test web frontend; có thể override bằng biến môi trường `SUT_BASE_URL`.
- **Accepted as-is / Modified:** Accepted with note. `STUDENT_ID` đang để placeholder `CHANGE_ME_STUDENT_ID` vì người dùng chưa cung cấp MSSV; cần thay bằng MSSV thật trước khi chạy report chính thức. `node --check playwright.config.js` và parse `package.json` đều OK.

### [7] FR-05 - Step B sinh automation cho TC-FR05-03 và TC-FR05-04
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:42
- **Prompt:**
  > Bước B: sinh automation cho **TC-FR05-03**, **TC-FR05-04** dùng locator trên
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr05-listing.spec.js` để thêm `TC-FR05-03` và `TC-FR05-04`. `TC-FR05-03` dùng dữ liệu `price_format` trong `fr05.json` để assert exact text của giá theo đặc tả FR-05, ví dụ `30.000.000 ₫`. `TC-FR05-04` dùng dữ liệu `exact_match`, submit keyword `MacBook Pro M3`, chờ response search, kiểm tra số lượng card, sản phẩm hiển thị, sản phẩm bị ẩn và search summary.
- **Accepted as-is / Modified:** Accepted. `node --check` cho spec OK. Node đọc `fr05.json` cho thấy expected price dùng đúng ký tự `₫`; nếu app hiện trả `VND` thì TC-FR05-03 fail đúng theo đặc tả.

## Tool declaration summary

| Tool | Used for | # of interactions |
|---|---|---|
| Codex (GPT-5) | Phân tích FR-05, thiết kế test case Markdown, tạo dữ liệu kiểm thử, tạo locator/page object, review selector, sinh automation theo từng test case và scaffold Playwright config | 7 |

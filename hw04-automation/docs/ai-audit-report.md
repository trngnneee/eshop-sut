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
- **Accepted as-is / Modified:** Accepted by human review.

### [5] FR-05 - Step B sinh automation cho TC-FR05-01 và TC-FR05-02
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:30
- **Prompt:**
  > Bước B: sinh automation cho **TC-FR05-01**, **TC-FR05-02** dùng locator trên
- **Output:**
  AI đã tạo `hw04-automation/tests/fr05-listing.spec.js` dùng `ProductListingPage` và dữ liệu từ `hw04-automation/data/fr05.json`. Spec hiện chỉ có hai test: `TC-FR05-01` kiểm tra trang chủ hiển thị đủ số lượng và tên sản phẩm seed; `TC-FR05-02` kiểm tra mỗi product card có ảnh, tên, giá, link xem chi tiết và nút thêm vào giỏ. Helper `openProductListing` chờ response `GET /api/products` trước khi assert lưới sản phẩm.
- **Accepted as-is / Modified:** Accepted by human review.

### [6] HW04 - Tạo package.json và Playwright config
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:35
- **Prompt:**
  > thêm file package.json trong thư mục hw4 và file config playwright
- **Output:**
  AI đã tạo `hw04-automation/package.json` với dependency `@playwright/test` và các script `test`, `report`, `stamp-report`. AI cũng tạo `hw04-automation/playwright.config.js` với `testDir: "./tests"`, HTML/list reporter, 3 browser projects Chromium/Firefox/WebKit, trace/screenshot khi fail, metadata `Run by` và ISO timestamp. `baseURL` được đặt mặc định là `http://localhost:5173` để chạy test web frontend; có thể override bằng biến môi trường `SUT_BASE_URL`.
- **Accepted as-is / Modified:** Accepted by human review.

### [7] FR-05 - Step B sinh automation cho TC-FR05-03 và TC-FR05-04
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:42
- **Prompt:**
  > Bước B: sinh automation cho **TC-FR05-03**, **TC-FR05-04** dùng locator trên
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr05-listing.spec.js` để thêm `TC-FR05-03` và `TC-FR05-04`. `TC-FR05-03` dùng dữ liệu `price_format` trong `fr05.json` để assert exact text của giá theo đặc tả FR-05, ví dụ `30.000.000 ₫`. `TC-FR05-04` dùng dữ liệu `exact_match`, submit keyword `MacBook Pro M3`, chờ response search, kiểm tra số lượng card, sản phẩm hiển thị, sản phẩm bị ẩn và search summary.
- **Accepted as-is / Modified:** Accepted by human review.

### [8] FR-05 - Step B sinh automation cho TC-FR05-05 đến TC-FR05-08
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-08 23:52
- **Prompt:**
  > Bước B: sinh automation cho **TC-FR05-05**, **TC-FR05-06,**  **TC-FR05-07, TC-FR05-08** dùng locator trên
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr05-listing.spec.js` để thêm automation cho bốn test case tiếp theo. `TC-FR05-05` kiểm tra tìm kiếm partial keyword `Pro`; `TC-FR05-06` kiểm tra trường hợp không có kết quả và empty state; `TC-FR05-07` kiểm tra submit từ khóa rỗng hiển thị lại toàn bộ sản phẩm; `TC-FR05-08` kiểm tra từ khóa có khoảng trắng đầu/cuối không gây lỗi giao diện hoặc API. AI cũng bổ sung helper `emptyStateMessage(message)` trong `ProductListingPage.js` để locator empty state được tái sử dụng qua page object.
- **Accepted as-is / Modified:** Modified TC-FR05-08. Automation ban đầu chỉ kiểm tra grid visible và productCount >= 0, chưa thực sự kiểm tra behavior trim keyword. 
### [9] FR-05 - Step B sinh automation cho TC-FR05-09 đến TC-FR05-12
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 01:02
- **Prompt:**
  > Bước B: sinh automation cho **TC-FR05-09**, **TC-FR05-10,**  **TC-FR05-011, TC-FR05-12** dùng locator trên
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr05-listing.spec.js` để thêm automation cho `TC-FR05-09`, `TC-FR05-10`, `TC-FR05-11` và `TC-FR05-12`. `TC-FR05-011` trong prompt được hiểu là `TC-FR05-11` theo bộ ID test case đã thiết kế. TC09 kiểm tra payload HTML phải hiển thị như text và không render selector bị chèn; TC10 kiểm tra payload script không thực thi dialog và hiển thị như text; TC11 kiểm tra payload SQL injection không trả về toàn bộ sản phẩm hoặc lỗi database; TC12 kiểm tra ảnh sản phẩm có `alt` mô tả theo `seedProducts`.
- **Accepted as-is / Modified:** Accepted by human review.

### [10] FR-05 - Step B sinh automation cho TC-FR05-13 và TC-FR05-14
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 01:22
- **Prompt:**
  > Bước B: sinh automation cho **TC-FR05-13**, **TC-FR05-14** dùng locator trên
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr05-listing.spec.js` để thêm `TC-FR05-13` và `TC-FR05-14`. TC13 kiểm tra trang chủ chỉ có đúng một thẻ `h1` và heading chính chứa text mong đợi từ `data/fr05.json`. TC14 dùng `page.route` để delay request sản phẩm theo `delayed_api.delayMs`, sau đó kiểm tra loading indicator trong lúc dữ liệu đang tải và xác nhận danh sách sản phẩm xuất hiện sau khi response hoàn tất. AI cũng bổ sung helper `loadingIndicator(message)` trong `ProductListingPage.js`.
- **Accepted as-is / Modified:** Accepted by human review.

### [11] FR-11 - Phân tích yêu cầu xem lịch sử đơn hàng
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 14:10
- **Prompt:**
  > Phân tích FR-11
- **Output:**
  AI đã đọc skill HW04 automation-testing, `feature_pools.md`, `README.md`, `api_specification.md`, `frontend-web/src/App.jsx`, `frontend-web/src/pages/Profile.jsx`, `frontend-web/src/context/AuthContext.jsx`, `backend/server.js` và `backend/database.js`. AI xác định FR-11 thuộc Pool B, phạm vi chính là user đã đăng nhập xem lịch sử đơn hàng của chính mình qua trang `/profile` và API `GET /api/orders/my-orders`. Output cũng ghi rõ các trường bắt buộc cần hiển thị: mã đơn, ngày đặt, tổng tiền, trạng thái hiện tại; trạng thái phải dịch sang tiếng Việt và phân biệt màu. Các điểm mơ hồ được ghi lại gồm định dạng ngày/tiền, empty state, loading/error state và việc UI hiện có nút hủy đơn thuộc phạm vi liên quan FR-10 hơn là yêu cầu cốt lõi của FR-11.
- **Accepted as-is / Modified:** Accepted by human review.

### [12] FR-11 - Thiết kế test case và dữ liệu kiểm thử
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 14:14
- **Prompt:**
  > tiếp tục Stage 2: thiết kế ít nhất 12 test case + tạo data file cho FR-11
- **Output:**
  AI đã tạo `hw04-automation/docs/test-cases/FR-11-test-cases.md` với 14 test case cho FR-11, bao phủ luồng tích cực, tiêu cực, biên và bảo mật. Bộ test kiểm tra bảng lịch sử đơn hàng, các trường bắt buộc, định dạng mã đơn/tổng tiền, đủ 5 trạng thái đơn hàng bằng tiếng Việt và màu sắc, isolation giữa user chính và user khác, UI khi chưa đăng nhập, API không token/token sai, và empty state cho user chưa có đơn. AI cũng tạo `hw04-automation/data/fr11.json` chứa users, API routes, fixture đơn hàng, expected label/class trạng thái, expected amount text và mapping `TC-FR11-01` đến `TC-FR11-14`. JSON đã được validate bằng `ConvertFrom-Json`.
- **Accepted as-is / Modified:** Modified after human review. Thiếu artifact file riêng trong Stage 2 ban đầu.

### [13] FR-11 - Sửa Stage 2 để có file riêng từng test case
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 14:17
- **Prompt:**
  > Sao không có từng file md cho từng test case. Hãy cập nhật lại skill để ở stage 2 không chỉ sinh 1 file chung mà sinh riêng từng file test case nữa.
- **Output:**
  AI đã cập nhật `.agents/skills/hw04-automation-testing/SKILL.md` để Stage 2 bắt buộc sinh cả file tổng `docs/test-cases/FR-xx-test-cases.md` và từng file riêng `docs/test-cases/TC-FRxx-NN.md`. AI cũng bổ sung 14 file riêng cho FR-11 từ `TC-FR11-01.md` đến `TC-FR11-14.md`, mỗi file có metadata, bước thực hiện, expected result và assertion gợi ý. File tổng `FR-11-test-cases.md` và `docs/report.md` được cập nhật để tham chiếu các file riêng này.
- **Accepted as-is / Modified:** Accepted by human review.

### [14] FR-11 - Tạo locator/page object cho lịch sử đơn hàng
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 14:26
- **Prompt:**
  > tiếp tục Stage 3: tạo locators/page object cho FR-11
- **Output:**
  AI đã đọc `frontend-web/src/pages/Profile.jsx`, `hw04-automation/data/fr11.json` và page object FR-05 hiện có, sau đó tạo `hw04-automation/tests/pages/OrderHistoryPage.js`. Page object gồm locator/handler cho trang `/profile`, thông báo chưa đăng nhập, heading lịch sử đơn hàng, empty state, bảng đơn hàng, header, dòng đơn, cell mã đơn/ngày/tổng tiền/trạng thái/thao tác, badge trạng thái, nút hủy đơn và helper chờ response `GET /api/orders/my-orders`. AI cũng tạo `hw04-automation/docs/locator-review/FR-11-locators.md` để ghi rõ độ ổn định của từng selector và rủi ro do frontend chưa có `data-testid`. Cú pháp JS đã được kiểm tra bằng `node --check`.
- **Accepted as-is / Modified:** Accepted by human review.

### [15] FR-11 - Sinh automation cho TC-FR11-01 đến TC-FR11-04
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 14:35
- **Prompt:**
  > tiếp tục Stage 4: sinh automation script cho test case FR-11 từ 01->04
- **Output:**
  AI đã tạo `hw04-automation/tests/fr11-order-history.spec.js` với automation cho `TC-FR11-01` đến `TC-FR11-04`. Spec dùng `OrderHistoryPage` và `data/fr11.json`, có helper login qua API, tạo order qua `POST /api/checkout`, set token vào localStorage, mở `/profile`, chờ `GET /api/orders/my-orders`, rồi assert bảng lịch sử, header/cell bắt buộc, mã đơn dạng `#<id>` và format tổng tiền. Script hiện dùng nhiều assertion pattern: `toBeVisible`, `toHaveText`, `not.toContainText`, `toBeGreaterThanOrEqual`, và `expect.soft(...).not.toBe("")`. Cú pháp spec và page object đã được kiểm tra bằng `node --check`.
- **Accepted as-is / Modified:** Accepted by human review.

### [16] FR-11 - Sinh automation cho TC-FR11-05 đến TC-FR11-08
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 15:14
- **Prompt:**
  > tiếp tục Stage 4: sinh automation script cho test case FR-11 từ 05->08
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr11-order-history.spec.js` để thêm automation cho `TC-FR11-05` đến `TC-FR11-08`. Script bổ sung helper `updateOrderStatusViaApi`, `moveOrderToTargetStatus`, `primaryFixtureByKey`, `createPrimaryOrderForStatus` và `expectStatusBadge`. Các test mới tạo đơn cho user chính, dùng token admin để chuyển trạng thái theo state machine hợp lệ (`pending`, `confirmed`, `shipping`, `delivered`), mở `/profile`, rồi assert badge trạng thái có label tiếng Việt và class màu mong đợi từ `data/fr11.json`. Cú pháp spec đã được kiểm tra bằng `node --check`.
- **Accepted as-is / Modified:** Accepted by human review.

### [17] FR-11 - Sinh automation cho TC-FR11-09 đến TC-FR11-14
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 15:24
- **Prompt:**
  > Tôi chấp nhận sau khi review.
  > Tiếp tục Stage 4: sinh automation script cho test case FR-11 từ 09->14
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr11-order-history.spec.js` để thêm automation cho `TC-FR11-09` đến `TC-FR11-14`, hoàn tất đủ 14 test case FR-11. Script bổ sung helper đăng ký user động `registerViaApi`, `uniqueUser`, `createOrderForNewUser` và `openProfileWithoutToken`. Các test mới kiểm tra trạng thái `canceled`, isolation không thấy đơn user khác, UI chưa đăng nhập, API không token trả `401`, API token sai trả `403`, và empty state cho user mới chưa có đơn. Spec hiện có đủ 14 test case và cú pháp đã được kiểm tra bằng `node --check`.
- **Accepted as-is / Modified:** Pending human review.

### [18] FR-19 - Phân tích yêu cầu quản lý người dùng admin
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 16:16
- **Prompt:**
  > Phân tích FR-19
- **Output:**
  AI đã đọc skill HW04 automation-testing, `feature_pools.md`, `README.md`, `api_specification.md`, `frontend-admin/src/App.jsx`, `backend/server.js` và `backend/database.js`. AI xác định FR-19 thuộc Pool C, phạm vi chính là admin xem danh sách tất cả người dùng không lộ password và xóa người dùng, trừ trường hợp không được xóa chính tài khoản đang đăng nhập. Output cũng ghi rõ UI hiện tại nằm ở tab "Người dùng" của admin app, gọi `GET /api/admin/users` và `DELETE /api/admin/users/:id`; backend list user không select `password`. Các điểm cần đưa vào test security gồm request không token, token user thường, response không chứa password, xóa user thành công, và chặn self-delete. AI cũng ghi nhận lệch spec/code tiềm năng: middleware admin API hiện chỉ verify JWT, chưa kiểm tra `role = "admin"`, và delete user chưa chặn id của tài khoản đang đăng nhập.
- **Accepted as-is / Modified:** Pending human review.

### [19] FR-19 - Thiết kế test case và dữ liệu kiểm thử
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 16:21
- **Prompt:**
  > tiếp tục Stage 2 để thiết kế ít nhất 12 test case + tạo data file cho FR-19
- **Output:**
  AI đã tạo `hw04-automation/docs/test-cases/FR-19-test-cases.md` với 14 test case cho FR-19, bao phủ luồng tích cực, tiêu cực, biên và bảo mật. Bộ test kiểm tra admin xem bảng user, các cột bắt buộc, API/UI không lộ password, hiển thị user seed và role, xóa user thường, user đã xóa biến mất khỏi danh sách, chặn admin tự xóa chính mình, request không token/token sai, user thường không được list/xóa user, UI admin từ chối user thường, và xóa một user không ảnh hưởng user khác. AI cũng tạo `hw04-automation/data/fr19.json` chứa users, API routes, expectation theo từng dataRef và mapping `TC-FR19-01` đến `TC-FR19-14`. Mỗi test case có file riêng `TC-FR19-01.md` đến `TC-FR19-14.md`; JSON đã được validate bằng `ConvertFrom-Json`.
- **Accepted as-is / Modified:** Modified after human review. Người review yêu cầu các file vừa tạo phải dùng tiếng Việt có dấu.

### [20] FR-19 - Việt hóa có dấu artifact Stage 2
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 16:27
- **Prompt:**
  > Yêu cầu modify các file vừa tạo thành tiếng việt có dấu.
- **Output:**
  AI đã cập nhật `hw04-automation/docs/test-cases/FR-19-test-cases.md`, 14 file riêng từ `TC-FR19-01.md` đến `TC-FR19-14.md`, `hw04-automation/data/fr19.json`, và phần FR-19 trong `hw04-automation/docs/report.md` để chuyển phần mô tả, bước kiểm thử, expected result và dữ liệu người đọc thấy sang tiếng Việt có dấu. Các ID test case, JSON key, endpoint và field kỹ thuật được giữ ổn định để phục vụ Stage 3/4. JSON `fr19.json` đã được validate lại bằng `ConvertFrom-Json` và vẫn có đủ 14 mapping test case.
- **Accepted as-is / Modified:** Pending human review.

### [21] FR-19 - Tạo locator/page object cho quản lý người dùng admin
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 16:31
- **Prompt:**
  > tiếp tục Stage 3 để tạo locators/page object cho FR-19
- **Output:**
  AI đã đọc `frontend-admin/src/App.jsx`, `hw04-automation/data/fr19.json` và các page object hiện có, sau đó tạo `hw04-automation/tests/pages/AdminUserManagementPage.js`. Page object gồm locator/handler cho form admin login, input Email/Password, nút Login, admin shell, tab Người dùng, heading "Quản lý Người dùng", bảng user, header, dòng user, dòng theo email, cell ID/Email/Role/Số ĐT/Hành động, checkbox dòng và nút Xóa theo dòng. AI cũng tạo `hw04-automation/docs/locator-review/FR-19-locators.md` để ghi độ ổn định selector và rủi ro do frontend admin chưa có `data-testid`. Cú pháp JS đã được kiểm tra bằng `node --check`.
- **Accepted as-is / Modified:** Pending human review.

### [22] FR-19 - Sinh automation cho TC-FR19-01 đến TC-FR19-04
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 16:33
- **Prompt:**
  > tiếp tục Stage 4 để sinh automation script cho FR-19 từ TC-01 ->TC-04
- **Output:**
  AI đã tạo `hw04-automation/tests/fr19-user-management.spec.js` với automation cho `TC-FR19-01` đến `TC-FR19-04`, dùng `AdminUserManagementPage` và `data/fr19.json`. Spec bổ sung helper `loginViaApi`, `openAdminUserManagement` và `expectUserDoesNotExposeForbiddenFields`. Các test kiểm tra admin mở được bảng quản lý người dùng, bảng có các cột bắt buộc, API `GET /api/admin/users` không trả field `password`, và UI hiển thị user seed kèm role tương ứng. Script dùng nhiều assertion pattern: `toBeVisible`, `toHaveText`, `toBeGreaterThanOrEqual`, `response.status()`, `toHaveProperty` và `not.toHaveProperty`. Cú pháp spec và page object đã được kiểm tra bằng `node --check`.
- **Accepted as-is / Modified:** Pending human review.

### [23] FR-19 - Sinh automation cho TC-FR19-05 đến TC-FR19-08
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 16:52
- **Prompt:**
  > tiếp tục Stage 4 để sinh automation script cho FR-19 từ TC-05 ->TC-08
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr19-user-management.spec.js` để thêm automation cho `TC-FR19-05` đến `TC-FR19-08`. Script bổ sung helper `registerViaApi`, `uniqueUser`, `authHeaders`, `deleteEndpoint`, `getAdminUsersViaApi`, `findUserByEmail`, `createUserAndFindInAdminList`, `deleteUserViaApi` và `createTemporaryAdmin`. Các test mới kiểm tra admin xóa user thường, user đã xóa biến mất khỏi API/UI, admin không được tự xóa chính tài khoản đang đăng nhập, và API list user từ chối request không token. Riêng TC-FR19-07 dùng admin tạm thay vì seed admin để tránh phá dữ liệu seed nếu SUT có bug self-delete. AI cũng cập nhật `data/fr19.json` thêm route `userProfile` và user template `selfDeleteAdmin`. Cú pháp spec/page object đã được kiểm tra bằng `node --check` và JSON đã được validate lại bằng `ConvertFrom-Json`.
- **Accepted as-is / Modified:** Pending human review.

### [24] FR-19 - Sinh automation cho TC-FR19-09 đến TC-FR19-14
- **Tool:** Codex (GPT-5)
- **Date/time:** 2026-08-09 17:04
- **Prompt:**
  > Chấp nhận. Tiếp tục sinh automation cho TC-FR19-09 đến TC-FR19-14
- **Output:**
  AI đã cập nhật `hw04-automation/tests/fr19-user-management.spec.js` để thêm automation cho `TC-FR19-09` đến `TC-FR19-14`, hoàn tất đủ 14 test case FR-19. Các test mới kiểm tra token không hợp lệ bị từ chối, user thường không được list user, user thường không được xóa user, UI admin từ chối đăng nhập bằng user thường, xóa một user không ảnh hưởng user khác, và UI không hiển thị password. Spec hiện dùng dữ liệu từ `data/fr19.json`, page object `AdminUserManagementPage`, helper API dùng email unique, và nhiều assertion pattern gồm `toBeVisible`, `toHaveText`, `toHaveCount`, `toContainText` phủ định, `response.status()`, `body.error`, `toHaveProperty`/`not.toHaveProperty`, `toBeTruthy`, `toBeUndefined` và `Array.isArray`. Cú pháp spec/page object đã được kiểm tra bằng `node --check`; spec hiện có đủ 14 test case theo `Select-String`.
- **Accepted as-is / Modified:** Pending human review.

## Tool declaration summary

| Tool | Used for | # of interactions |
|---|---|---|
| Codex (GPT-5) | Phân tích FR-05/FR-11/FR-19, thiết kế test case Markdown, tạo dữ liệu kiểm thử, tạo locator/page object, review selector, sinh automation theo từng test case, cập nhật skill và scaffold Playwright config | 24 |

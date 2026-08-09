# HW04 - Automation Testing Report

**Student ID:** {{STUDENT_ID}}
**Repository:** {{GITHUB_REPO_URL}}
**Tool stack:** Playwright | Chromium/Firefox/WebKit | Playwright HTML reporter

## 1. Feature Selection

| Pool | Feature | Reused from HW02? |
|---|---|---|
| A | FR-05 - Product listing and search | {{Yes / No}} |
| B | FR-11 - Order history view (user) | {{Yes / No}} |
| C | FR-19 - User management (admin) | {{Yes / No}} |

---

## 2. Feature A - FR-05 Product Listing And Search

Các test case và automation hiện đang nằm trong `docs/test-cases/`, `data/fr05.json`, `tests/pages/ProductListingPage.js`, và `tests/fr05-listing.spec.js`.


### 2.1 Test Case Update After Review

Sau review, FR-05 được bổ sung thêm 3 edge/security test case, nâng tổng số case từ 14 lên 17:

| ID | Type | Description | Expected Result |
|---|---|---|---|
| TC-FR05-15 | Security/Edge | Tìm kiếm bằng payload `<image src=1 href=1 onerror="javascript:alert(1)"></image>` | Payload hiển thị như text, không tạo element `image`/`img[src="1"]`, không bật dialog `alert(1)` |
| TC-FR05-16 | Edge | Tìm kiếm bằng keyword rất dài | Không lỗi UI/API, không hiện error panel, summary hiển thị an toàn, không có kết quả phù hợp |
| TC-FR05-17 | Edge | Tìm kiếm bằng keyword Unicode/emoji | Không lỗi UI/API, summary giữ đúng Unicode/emoji, không có kết quả phù hợp nếu seed data không match |

### 2.5 Human Review - What The AI Got Wrong / Missed

| Issue | Category | Fix applied | Likely cause |
|---|---|---|---|
| Bộ test XSS ban đầu có HTML/script payload nhưng thiếu biến thể event-handler qua thẻ media/image như `<image onerror>` | Edge case/security | Bổ sung `TC-FR05-15`, data key `image_onerror_payload`, và automation assert không dialog, không element injected trong `searchSummary` | AI thường nghĩ đến `<script>` trước, nhưng XSS thực tế hay đi qua event handler như `onerror` |
| Chưa kiểm tra input tìm kiếm rất dài | Edge case | Bổ sung `TC-FR05-16` với keyword dài, assert không error panel và không vỡ search summary | Prompt ban đầu tập trung vào chức năng chính và security phổ biến, chưa ép boundary input length |
| Chưa kiểm tra ký tự Unicode/emoji trong keyword | Edge case/i18n | Bổ sung `TC-FR05-17`, assert summary giữ đúng Unicode/emoji và không lỗi API/UI | AI bỏ sót i18n vì seed data chủ yếu là tên sản phẩm ASCII/tiếng Việt có dấu đơn giản |
| Locator/test hiện phụ thuộc vào `searchSummary` vì frontend chưa có `data-testid` riêng cho keyword rendered text | Selector/assertion | Giữ locator hiện có nhưng scope kiểm tra element injected bên trong `searchSummary` để giảm đọc nhầm DOM ngoài vùng cần test | Ứng dụng chưa thiết kế sẵn testability hook cho search summary |

### 2.6 Execution Results

Playwright HTML report: `reports/html/index.html`. Run metadata trong report: `Run by: 23127158`, `Run at (ISO): 2026-08-09T11:29:27.604Z`.

| Browser | Total | Passed | Failed | Skipped |
|---|---:|---:|---:|---:|
| Chromium | 17 | 7 | 10 | 0 |
| Firefox | 17 | 7 | 10 | 0 |
| WebKit | 17 | 7 | 10 | 0 |
| **Unique test cases** | **17** | **7** | **10** | **0** |

Failed test cases: `TC-FR05-03`, `TC-FR05-06`, `TC-FR05-08`, `TC-FR05-09`, `TC-FR05-10`, `TC-FR05-11`, `TC-FR05-12`, `TC-FR05-13`, `TC-FR05-14`, `TC-FR05-15`.

### 2.7 Bugs Found

| Bug ID | Found by | Summary | Severity / Priority | Report |
|---|---|---|---|---|
| BUG-FR05-001 | TC-FR05-03 | Giá sản phẩm hiển thị `VND` thay vì `₫` | Major / P1 | `docs/bug/BUG-FR05-001-price-format.md` |
| BUG-FR05-002 | TC-FR05-06 | Không hiển thị empty state khi tìm kiếm không có kết quả | Major / P1 | `docs/bug/BUG-FR05-002-empty-state.md` |
| BUG-FR05-003 | TC-FR05-08 | Tìm kiếm không trim khoảng trắng đầu/cuối | Minor / P2 | `docs/bug/BUG-FR05-003-search-trim.md` |
| BUG-FR05-004 | TC-FR05-09, TC-FR05-10, TC-FR05-15 | Từ khóa tìm kiếm bị render thành HTML | Critical / P0 | `docs/bug/BUG-FR05-004-search-xss.md` |
| BUG-FR05-005 | TC-FR05-11 | API tìm kiếm nối chuỗi SQL trực tiếp | Critical / P0 | `docs/bug/BUG-FR05-005-sql-injection-search.md` |
| BUG-FR05-006 | TC-FR05-12 | Ảnh sản phẩm thiếu alt text mô tả | Minor / P2 | `docs/bug/BUG-FR05-006-image-alt.md` |
| BUG-FR05-007 | TC-FR05-13 | Trang chủ có nhiều hơn một thẻ h1 | Minor / P2 | `docs/bug/BUG-FR05-007-multiple-h1.md` |
| BUG-FR05-008 | TC-FR05-14 | Không hiển thị loading state khi tải sản phẩm | Minor / P2 | `docs/bug/BUG-FR05-008-loading-state.md` |

---

## 3. Feature B - FR-11 Order History View (User)

### Spec Summary

FR-11 cho phép người dùng đã đăng nhập xem lịch sử đơn hàng của chính mình. Dữ liệu lịch sử được lấy qua API `GET /api/orders/my-orders`, yêu cầu JWT hợp lệ, và backend lọc theo `user_id` từ token trước khi trả về danh sách đơn hàng theo thứ tự `id DESC`.

Luồng UI hiện tại nằm trong trang hồ sơ người dùng `/profile`, không có route riêng `/orders`. Khi người dùng chưa đăng nhập, trang hiển thị thông báo yêu cầu đăng nhập. Khi đã đăng nhập, trang Profile hiển thị khối "Lịch sử đơn hàng"; nếu không có đơn thì hiển thị empty state, nếu có đơn thì hiển thị bảng lịch sử.

Các thông tin bắt buộc theo đặc tả cần hiển thị cho mỗi đơn: mã đơn, ngày đặt, tổng tiền, trạng thái hiện tại. Code hiện tại cũng hiển thị thêm cột thao tác hủy đơn, nhưng đây là hành vi liên quan FR-10/API hủy đơn, không phải yêu cầu cốt lõi của FR-11.

Trạng thái đơn hàng gồm các giá trị chính từ FR-10: `pending`, `confirmed`, `shipping`, `delivered`, `canceled`. FR-11 yêu cầu trạng thái phải được dịch sang tiếng Việt rõ ràng và phân biệt bằng màu sắc. UI hiện tại ánh xạ lần lượt thành "Chờ xác nhận", "Đã xác nhận", "Đang giao", "Đã giao", "Đã hủy", với màu nền/chữ khác nhau cho từng nhóm trạng thái.

Ràng buộc quan trọng để thiết kế test: người dùng chỉ được thấy đơn hàng của chính mình; API `/api/orders/my-orders` phải bị chặn khi không có token hoặc token không hợp lệ; danh sách cần giữ thứ tự mới hơn trước theo `id DESC`; ngày đặt lấy từ `created_at`; tổng tiền lấy từ `total_amount` và cần hiển thị dưới dạng tiền tệ dễ đọc.

Điểm mơ hồ/ngoài đặc tả: README không nêu định dạng ngày chính xác, định dạng tiền chính xác, empty-state text, hành vi loading/error khi API lỗi, hoặc có cần hiển thị chi tiết sản phẩm trong từng đơn hay không. API `GET /api/orders/:id` trong code hiện không yêu cầu xác thực, nhưng đây là endpoint chi tiết đơn và không thuộc phạm vi chính của FR-11 trừ khi Stage 2 quyết định thêm kiểm thử bảo mật liên quan.

### 3.1 Test Cases (>=12)

Chi tiết đầy đủ: `docs/test-cases/FR-11-test-cases.md`. Mỗi test case cũng có file riêng từ `docs/test-cases/TC-FR11-01.md` đến `docs/test-cases/TC-FR11-14.md`.

| ID | Type | Description | Expected Result |
|---|---|---|---|
| TC-FR11-01 | Positive | User đã đăng nhập xem được bảng lịch sử đơn hàng | Bảng lịch sử hiển thị ít nhất 3 đơn của user chính |
| TC-FR11-02 | Positive | Mỗi dòng đơn hiển thị đủ trường bắt buộc | Có mã đơn, ngày đặt, tổng tiền, trạng thái; ô bắt buộc không rỗng |
| TC-FR11-03 | Positive | Mã đơn hiển thị theo đúng order id | Mã đơn có dạng `#<id>` và khớp API |
| TC-FR11-04 | Positive | Tổng tiền hiển thị theo định dạng tiền tệ dễ đọc | Có phân cách hàng nghìn và đơn vị `₫`; khớp `total_amount` |
| TC-FR11-05 | Positive | Trạng thái `pending` được dịch và có màu riêng | Hiển thị `Chờ xác nhận`, nhóm màu vàng |
| TC-FR11-06 | Positive | Trạng thái `confirmed` được dịch và có màu riêng | Hiển thị `Đã xác nhận`, nhóm màu indigo |
| TC-FR11-07 | Positive | Trạng thái `shipping` được dịch và có màu riêng | Hiển thị `Đang giao`, nhóm màu xanh dương |
| TC-FR11-08 | Positive | Trạng thái `delivered` được dịch và có màu riêng | Hiển thị `Đã giao`, nhóm màu xanh lá |
| TC-FR11-09 | Positive | Trạng thái `canceled` được dịch và có màu riêng | Hiển thị `Đã hủy`, nhóm màu đỏ |
| TC-FR11-10 | Security | User không thấy đơn hàng của user khác | Không có mã đơn/tổng tiền của user phụ trong lịch sử user chính |
| TC-FR11-11 | Negative | Chưa đăng nhập không xem được lịch sử qua UI | Hiển thị yêu cầu đăng nhập, không hiển thị bảng lịch sử |
| TC-FR11-12 | Negative | API lịch sử từ chối request không có token | Trả `401 Unauthorized`, không trả danh sách đơn |
| TC-FR11-13 | Negative | API lịch sử từ chối token không hợp lệ | Trả `403 Forbidden`, không trả danh sách đơn |
| TC-FR11-14 | Edge | User chưa có đơn hàng thấy empty state | Hiển thị `Bạn chưa có đơn hàng nào.` |

### 3.2 Test Data

Location: `data/fr11.json`.

Schema chính:
- `users`: tài khoản seed và tài khoản phụ dùng cho setup/permission checks.
- `orderFixtures`: các đơn cần tạo cho user chính và user phụ, gồm `total_amount`, `shipping_address`, `targetStatus`, `expectedAmountText`.
- `statusExpectations`: nhãn tiếng Việt và class màu mong đợi cho `pending`, `confirmed`, `shipping`, `delivered`, `canceled`.
- Các key theo từng test case như `primary_user_orders`, `required_columns`, `other_user_isolation`, `api_without_token`, `empty_order_history`.
- `testCases`: mapping ổn định từ `TC-FR11-01` đến `TC-FR11-14` sang `dataRef`.

### 3.3 AI-Driven Generation Process

Stage 1 phân tích đặc tả FR-11 từ README/API/frontend/backend. Stage 2 tạo `docs/test-cases/FR-11-test-cases.md`, các file riêng `TC-FR11-01.md` đến `TC-FR11-14.md`, và `data/fr11.json`. Stage 3 tạo page object `tests/pages/OrderHistoryPage.js` và locator review `docs/locator-review/FR-11-locators.md`.

Locator/page object chính:
- `goto()` và `gotoAndWaitForOrders()` mở `/profile` và chờ `GET /api/orders/my-orders`.
- `unauthenticatedMessage`, `orderHistoryHeading`, `emptyStateMessage` kiểm tra trạng thái chưa đăng nhập/empty state.
- `ordersTable`, `tableHeaders`, `orderRows` định vị bảng lịch sử.
- `headerByName(name)`, `rowByOrderId(orderId)`, `rowByAmountText(amountText)`, `rowByStatusLabel(statusLabel)` hỗ trợ assert theo dữ liệu API/data file.
- `orderIdCell(row)`, `orderDateCell(row)`, `orderAmountCell(row)`, `orderStatusCell(row)`, `orderStatusBadge(row)` hỗ trợ kiểm tra từng trường bắt buộc và badge trạng thái.
- `cancelButton(row)` được giữ để quan sát hành vi liên quan FR-10 nếu cần, nhưng không phải trọng tâm FR-11.

### 3.4 Assertion Patterns Used

Stage 4 generated for all FR-11 test cases, `TC-FR11-01` to `TC-FR11-14`, in `tests/fr11-order-history.spec.js`.

Assertion patterns currently used:
- `toBeVisible`: kiểm tra heading, bảng lịch sử và các dòng đơn hàng xuất hiện.
- `toHaveText`: kiểm tra mã đơn dạng `#<id>` và tổng tiền đúng expected text.
- `toContainText`: kiểm tra label trạng thái tiếng Việt trong badge.
- `toHaveClass`: kiểm tra class màu của badge trạng thái.
- `not.toContainText`: kiểm tra tổng tiền không dùng đơn vị cấm `VND`.
- `expect(...).toBeGreaterThanOrEqual(...)`: kiểm tra số dòng đơn tối thiểu.
- `expect.soft(...).not.toBe("")`: kiểm tra các cell bắt buộc không rỗng mà vẫn gom lỗi theo từng dòng.

Stage 4 script generation is complete. Test execution is pending after human review approval.

### 3.5 Human Review - What The AI Got Wrong / Missed

Không phát hiện fail sau execution. Bộ locator/API setup của FR-11 ổn định trên cả Chromium, Firefox và WebKit. Rủi ro còn lại là format ngày chưa được đặc tả chặt, nên automation chỉ kiểm tra ngày hiển thị và parse được thay vì ép một format cụ thể.

### 3.6 Execution Results

Playwright HTML report: `reports/html/index.html`. Run metadata trong report: `Run by: 23127158`, `Run at (ISO): 2026-08-09T11:29:27.604Z`.

| Browser | Total | Passed | Failed | Skipped |
|---|---:|---:|---:|---:|
| Chromium | 14 | 14 | 0 | 0 |
| Firefox | 14 | 14 | 0 | 0 |
| WebKit | 14 | 14 | 0 | 0 |
| **Unique test cases** | **14** | **14** | **0** | **0** |

### 3.7 Bugs Found (if any)

Không có bug được phát hiện từ run Playwright hiện tại.

### 3.8 Test Cases Not Automated (if any)

Không có.

---

## 4. Feature C - FR-19 Quản Lý Người Dùng Admin

### Spec Summary

FR-19 thuộc phân hệ Web Admin và yêu cầu admin quản lý danh sách người dùng. Theo README, admin phải xem được danh sách tất cả người dùng nhưng không được làm lộ mật khẩu. Admin có thể xóa người dùng, ngoại trừ trường hợp không được xóa chính tài khoản đang đăng nhập.

Luồng UI hiện tại nằm trong ứng dụng `frontend-admin`. Admin đăng nhập bằng form admin qua `POST /api/login`; UI chỉ lưu token nếu response trả về user có `role = "admin"`. Sau khi có token, app gọi `fetchData()` và lấy danh sách user qua `GET /api/admin/users`. Tab "Người dùng" hiển thị bảng quản lý với các cột checkbox, ID, Email, Role, Số ĐT và Hành động. Mỗi dòng user có nút "Xóa", nút này gọi `DELETE /api/admin/users/:id` rồi fetch lại dữ liệu.

API spec xác định nhóm Admin API yêu cầu `Authorization: Bearer <token>` và tài khoản phải có quyền admin. Riêng FR-19 gồm hai endpoint: `GET /api/admin/users` để lấy danh sách người dùng và `DELETE /api/admin/users/:id` để xóa người dùng. Backend hiện tại trả về các cột `id`, `name`, `email`, `role`, `login_attempts`, `locked_until`, `shipping_address`; không select cột `password`, đáp ứng yêu cầu không lộ mật khẩu ở API list user. Tuy nhiên UI admin hiện chỉ hiển thị `id`, `email`, `role`, `phone`; trường `phone` không có trong SELECT của endpoint list user, nên cột Số ĐT có khả năng rỗng dữ liệu.

Ràng buộc quan trọng cần đưa vào test design: danh sách user chỉ được truy cập bằng token hợp lệ của admin; user thường hoặc request không token không được xem/xóa user; response list không được chứa `password`; xóa user thành công phải làm user biến mất khỏi danh sách; admin không được tự xóa tài khoản đang đăng nhập. Điểm lệch spec/code đang nghi nhận: middleware `authenticateToken` chỉ verify JWT và không kiểm tra `role = "admin"` cho `/api/admin/*`, nên user thường có token hợp lệ có thể gọi admin API; `DELETE /api/admin/users/:id` không chặn id bằng `req.user.id`, nên có nguy cơ cho phép admin tự xóa chính mình. Các lệch này sẽ được thiết kế thành security/negative test và nếu automation xác nhận thất bại thì ghi bug.

### 4.1 Test Cases (>=12)

Chi tiết đầy đủ: `docs/test-cases/FR-19-test-cases.md`. Mỗi test case cũng có file riêng từ `docs/test-cases/TC-FR19-01.md` đến `docs/test-cases/TC-FR19-14.md`.

| ID | Type | Description | Expected Result |
|---|---|---|---|
| TC-FR19-01 | Positive | Admin xem được bảng quản lý người dùng | Heading/bảng user hiển thị, có ít nhất 2 dòng seed |
| TC-FR19-02 | Positive | Bảng user hiển thị các cột quản lý chính | Có các cột ID, Email, Role, Số ĐT, Hành động |
| TC-FR19-03 | Security | API list user không trả về password | Status 200 và không object user nào có field `password` |
| TC-FR19-04 | Positive | UI hiển thị user seed và role tương ứng | Admin seed có role admin, user seed có role user |
| TC-FR19-05 | Positive | Admin xóa được user thường | Delete thành công với status/message phù hợp |
| TC-FR19-06 | Positive | User đã xóa biến mất khỏi danh sách | Email user đã xóa không còn trong API/UI |
| TC-FR19-07 | Security | Admin không được tự xóa tài khoản đang đăng nhập | Request bị từ chối và admin vẫn tồn tại |
| TC-FR19-08 | Negative | API list user từ chối request không token | Trả 401 Unauthorized |
| TC-FR19-09 | Negative | API list user từ chối token không hợp lệ | Trả 403 Forbidden |
| TC-FR19-10 | Security | User thường không được lấy danh sách user | Trả 403 Forbidden, không trả list user |
| TC-FR19-11 | Security | User thường không được xóa user | Trả 403 Forbidden, target user vẫn tồn tại |
| TC-FR19-12 | Negative | UI admin từ chối đăng nhập bằng user thường | Báo không phải admin, không hiển thị dashboard |
| TC-FR19-13 | Edge | Xóa một user không ảnh hưởng user khác | Target bị xóa, protected user vẫn tồn tại |
| TC-FR19-14 | Security | UI không hiển thị password | Không có cột/text password trên bảng user |

### 4.2 Test Data

Location: `data/fr19.json`.

Schema chính:
- `users`: tài khoản seed admin/user và các user động dùng cho xóa, bảo vệ, và non-admin security checks.
- `api`: các route login, register, list user và delete user.
- `specification`: cột UI bắt buộc, field API bắt buộc, field cấm `password`, ràng buộc admin-only và self-delete forbidden.
- Các key theo từng test case như `ui_admin_user_list`, `api_list_excludes_password`, `self_delete_blocked`, `api_non_admin_list_forbidden`, `delete_one_user_preserves_others`, `ui_no_password_visible`.
- `testCases`: mapping ổn định từ `TC-FR19-01` đến `TC-FR19-14` sang `dataRef`.

### 4.3 AI-Driven Generation Process

Stage 1 phân tích đặc tả FR-19 từ README, API specification, admin frontend, backend auth/user endpoints và database seed/schema. Stage 2 tạo `docs/test-cases/FR-19-test-cases.md`, các file riêng `TC-FR19-01.md` đến `TC-FR19-14.md`, và `data/fr19.json`. Stage 3 tạo page object `tests/pages/AdminUserManagementPage.js` và locator review `docs/locator-review/FR-19-locators.md`.

Locator/page object chính:
- `goto()` mở trang admin `/`.
- `login(email, password)` và `loginAsAdminAndWaitForUsers(email, password)` thao tác form login và chờ `GET /api/admin/users`.
- `openUsersTab()` mở tab "Người dùng" và chờ heading "Quản lý Người dùng".
- `loginHeading`, `emailInput`, `passwordInput`, `loginButton`, `adminHeading`, `usersNavItem`, `logoutNavItem` hỗ trợ luồng đăng nhập/admin shell.
- `userManagementHeading`, `usersTable`, `tableHeaders`, `userRows` định vị khu vực quản lý người dùng.
- `headerByName(name)`, `rowByEmail(email)`, `rowCount()` hỗ trợ kiểm tra header, dòng user và số lượng user.
- `userIdCell(row)`, `userEmailCell(row)`, `userRoleCell(row)`, `userPhoneCell(row)`, `userActionCell(row)`, `deleteButton(row)` hỗ trợ kiểm tra dữ liệu từng dòng và thao tác xóa user.

### 4.4 Assertion Patterns Used

Stage 4 đã sinh automation cho toàn bộ `TC-FR19-01` đến `TC-FR19-14` trong `tests/fr19-user-management.spec.js`.

Assertion patterns hiện dùng:
- `toBeVisible`: kiểm tra heading quản lý user, bảng user, header bảng và dòng user seed hiển thị.
- `toHaveText`: kiểm tra heading, email cell và role cell khớp dữ liệu mong đợi.
- `expect(...).toBeGreaterThanOrEqual(...)`: kiểm tra số dòng user tối thiểu.
- `expect(response.status()).toBe(...)`: kiểm tra status API list user.
- `expect(...).toHaveProperty(...)` và `not.toHaveProperty(...)`: kiểm tra object user có field bắt buộc và không lộ field `password`.
- `expect(response.ok()).toBeTruthy()`: kiểm tra API setup/delete thành công ở các bước chuẩn bị.
- `toHaveCount`: kiểm tra user đã xóa không còn xuất hiện trong UI.
- `expect(body.error).toBe(...)`: kiểm tra lỗi API khi không token, token sai hoặc user thường gọi admin API.
- `toContainText` dạng phủ định qua `not.toContainText`: kiểm tra bảng user không hiển thị password seed.

Stage 4 script generation is complete. Test execution is pending after human review approval.

### 4.5 Human Review - What The AI Got Wrong / Missed

Execution xác nhận các nghi vấn đã nêu ở Stage 1: backend chỉ verify JWT nhưng chưa enforce `role = "admin"` cho `/api/admin/*`, và endpoint xóa user chưa chặn self-delete. Các fail lặp lại trên cả 3 browser vì đây là lỗi API, không phải lỗi selector hay timing.

### 4.6 Execution Results

Playwright HTML report: `reports/html/index.html`. Run metadata trong report: `Run by: 23127158`, `Run at (ISO): 2026-08-09T11:29:27.604Z`.

| Browser | Total | Passed | Failed | Skipped |
|---|---:|---:|---:|---:|
| Chromium | 14 | 11 | 3 | 0 |
| Firefox | 14 | 11 | 3 | 0 |
| WebKit | 14 | 11 | 3 | 0 |
| **Unique test cases** | **14** | **11** | **3** | **0** |

Failed test cases: `TC-FR19-07`, `TC-FR19-10`, `TC-FR19-11`.

### 4.7 Bugs Found (if any)

| Bug ID | Found by | Summary | Severity / Priority | Report |
|---|---|---|---|---|
| BUG-FR19-001 | TC-FR19-07 | Admin có thể tự xóa tài khoản đang đăng nhập | Critical / P0 | `docs/bug/BUG-FR19-001-self-delete.md` |
| BUG-FR19-002 | TC-FR19-10, TC-FR19-11 | User thường có token hợp lệ gọi được Admin API | Critical / P0 | `docs/bug/BUG-FR19-002-admin-role-bypass.md` |

### 4.8 Test Cases Not Automated (if any)

Không có.


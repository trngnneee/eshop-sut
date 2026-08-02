# GUI Bug Report — HW03 Task 1

**Traceability:** one reproducible record per failed checklist assertion; existing issues were fetched before reuse.

| Bug ID | Severity | Checklist ID | GitHub | Evidence |
|---|---|---|---|---|
| `BUG-GUI-WEB-LOGIN-001` | Medium | `GUI-WEB-LOGIN-001` | [Issue](https://github.com/trngnneee/eshop-sut/issues/199) | [PNG](evidence/executed-chrome/001-web-login-baseline.png) |
| `BUG-GUI-WEB-LOGIN-002` | Medium | `GUI-WEB-LOGIN-002` | [Issue](https://github.com/trngnneee/eshop-sut/issues/203) | [PNG](evidence/executed-chrome/001-web-login-baseline.png) |
| `BUG-GUI-WEB-LOGIN-003` | Critical | `GUI-WEB-LOGIN-003` | [Issue](https://github.com/trngnneee/eshop-sut/issues/37) | [PNG](evidence/executed-chrome/001-web-login-baseline.png) |
| `BUG-GUI-WEB-LOGIN-007` | Low | `GUI-WEB-LOGIN-007` | [Issue](https://github.com/trngnneee/eshop-sut/issues/230) | [PNG](evidence/executed-chrome/004-web-login-forgot-navigation.png) |
| `BUG-GUI-WEB-LOGIN-009` | Medium | `GUI-WEB-LOGIN-009` | [Issue](https://github.com/trngnneee/eshop-sut/issues/198) | [PNG](evidence/executed-chrome/001-web-login-baseline.png) |
| `BUG-GUI-WEB-LOGIN-010` | High | `GUI-WEB-LOGIN-010` | [Issue](https://github.com/trngnneee/eshop-sut/issues/238) | [PNG](evidence/executed-chrome/006-web-login-lockout-feedback.png) |
| `BUG-GUI-WEB-LOGIN-011` | Medium | `GUI-WEB-LOGIN-011` | [Issue](https://github.com/trngnneee/eshop-sut/issues/201) | [PNG](evidence/executed-chrome/007-web-login-keyboard-focus.png) |
| `BUG-GUI-WEB-REGISTER-006` | High | `GUI-WEB-REGISTER-006` | [Issue](https://github.com/trngnneee/eshop-sut/issues/117) | [PNG](evidence/executed-chrome/013-web-register-duplicate.png) |
| `BUG-GUI-ADMIN-LOGIN-002` | Medium | `GUI-ADMIN-LOGIN-002` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/018-admin-login-baseline.png) |
| `BUG-GUI-ADMIN-LOGIN-003` | Medium | `GUI-ADMIN-LOGIN-003` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/019-admin-login-invalid-dialog.png) |
| `BUG-GUI-ADMIN-LOGIN-004` | Medium | `GUI-ADMIN-LOGIN-004` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/020-admin-login-nonadmin-dialog.png) |
| `BUG-GUI-ADMIN-CATEGORY-004` | High | `GUI-ADMIN-CATEGORY-004` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/026-admin-category-empty.png) |
| `BUG-GUI-ADMIN-CATEGORY-006` | High | `GUI-ADMIN-CATEGORY-006` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/027-admin-category-delete.png) |
| `BUG-GUI-ADMIN-CATEGORY-008` | High | `GUI-ADMIN-CATEGORY-008` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/028-admin-category-delete-in-use.png) |
| `BUG-GUI-ADMIN-CATEGORY-009` | Low | `GUI-ADMIN-CATEGORY-009` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/029-admin-category-empty-state.png) |
| `BUG-GUI-ADMIN-CATEGORY-010` | Medium | `GUI-ADMIN-CATEGORY-010` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/030-admin-category-loading.png) |
| `BUG-GUI-ADMIN-CATEGORY-013` | Medium | `GUI-ADMIN-CATEGORY-013` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/033-admin-category-double-submit.png) |
| `BUG-GUI-MOBILE-LOGIN-002` | Medium | `GUI-MOBILE-LOGIN-002` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/034-mobile-login-baseline.png) |
| `BUG-GUI-MOBILE-LOGIN-004` | Medium | `GUI-MOBILE-LOGIN-004` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/034-mobile-login-baseline.png) |
| `BUG-GUI-MOBILE-LOGIN-010` | Medium | `GUI-MOBILE-LOGIN-010` | `PENDING_EXTERNAL_ACTION` | [PNG](evidence/executed-chrome/034-mobile-login-baseline.png) |

## BUG-GUI-WEB-LOGIN-001 — Kiểm tra tiêu đề chính trên trang Đăng nhập.

- Severity: **Medium**.
- Expected: Tiêu đề chính hiển thị văn bản 'Đăng Nhập' ở giữa trang.
- Actual: Heading is 'Đăng Ký'.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/001-web-login-baseline.png).
- Reproduction:
  1. Start EShop and open `/login`.
  2. Perform `GUI-WEB-LOGIN-001` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/199

## BUG-GUI-WEB-LOGIN-002 — Kiểm tra nhãn label và type của trường Email.

- Severity: **Medium**.
- Expected: Nhãn hiển thị 'Email', input có type='email'.
- Actual: First label 'Username', input type 'text'.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/001-web-login-baseline.png).
- Reproduction:
  1. Start EShop and open `/login`.
  2. Perform `GUI-WEB-LOGIN-002` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/203

## BUG-GUI-WEB-LOGIN-003 — Kiểm tra ẩn/hiển thị ký tự trường Mật khẩu.

- Severity: **Critical**.
- Expected: Ký tự mật khẩu khi nhập vào bị ẩn dạng dấu chấm (type='password').
- Actual: Password input type is 'text'.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/001-web-login-baseline.png).
- Reproduction:
  1. Start EShop and open `/login`.
  2. Perform `GUI-WEB-LOGIN-003` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/37

## BUG-GUI-WEB-LOGIN-007 — Kiểm tra link Quên mật khẩu.

- Severity: **Low**.
- Expected: Bấm vào link 'Quên mật khẩu?' chuyển hướng mượt mà SPA không reload trang.
- Actual: Reached /forgot-password; SPA marker lost due to full document navigation.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/004-web-login-forgot-navigation.png).
- Reproduction:
  1. Start EShop and open `/login`.
  2. Perform `GUI-WEB-LOGIN-007` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/230

## BUG-GUI-WEB-LOGIN-009 — Kiểm tra nhãn và giao diện nút Đăng nhập.

- Severity: **Medium**.
- Expected: Nút đăng nhập có nhãn tiếng Việt 'Đăng nhập', tabIndex mặc định.
- Actual: Submit button text is 'Sign In'.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/001-web-login-baseline.png).
- Reproduction:
  1. Start EShop and open `/login`.
  2. Perform `GUI-WEB-LOGIN-009` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/198

## BUG-GUI-WEB-LOGIN-010 — Kiểm tra phản hồi sau đúng ba lần đăng nhập sai liên tiếp.

- Severity: **High**.
- Expected: Sau lần sai thứ ba, backend khóa 30 giây và UI hiển thị trạng thái khóa phù hợp mà không lộ chi tiết tài khoản.
- Actual: Three wrong attempts returned HTTP 401/401/403; UI still says 'Đăng nhập thất bại. Vui lòng kiểm tra lại.'.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/006-web-login-lockout-feedback.png).
- Reproduction:
  1. Start EShop and open `/login`.
  2. Perform `GUI-WEB-LOGIN-010` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/238

## BUG-GUI-WEB-LOGIN-011 — Kiểm tra thứ tự Tab (Keyboard Navigation) và Visible Focus.

- Severity: **Medium**.
- Expected: Ấn phím Tab di chuyển tuần tự qua các input và button có viền focus rõ ràng.
- Actual: First eight Tab targets: BUTTON:Sign In[1] > A:EShop[auto] > A:Giỏ hàng[auto] > A:Đăng nhập[auto] > A:Đăng ký[auto] > INPUT:text[auto] > INPUT:text[auto] > A:Quên mật khẩu?[auto]. Positive-tabindex submit precedes inputs=true.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/007-web-login-keyboard-focus.png).
- Reproduction:
  1. Start EShop and open `/login`.
  2. Perform `GUI-WEB-LOGIN-011` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/201

## BUG-GUI-WEB-REGISTER-006 — Kiểm tra đăng ký với Email đã tồn tại trong database.

- Severity: **High**.
- Expected: Hiển thị thông báo lỗi từ backend 'User already exists' hoặc 'Email đã được sử dụng'.
- Actual: Second registration for the same email returned HTTP 200 and navigated as success.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/013-web-register-duplicate.png).
- Reproduction:
  1. Start EShop and open `/register`.
  2. Perform `GUI-WEB-REGISTER-006` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: https://github.com/trngnneee/eshop-sut/issues/117

## BUG-GUI-ADMIN-LOGIN-002 — Kiểm tra thẻ label liên kết với ô Email và Password.

- Severity: **Medium**.
- Expected: Mỗi ô input đều có thẻ <label> liên kết tương ứng.
- Actual: Admin login form contains 0 label elements for two inputs.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/018-admin-login-baseline.png).
- Reproduction:
  1. Start EShop and open `/ (Unauth)`.
  2. Perform `GUI-ADMIN-LOGIN-002` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-LOGIN-003 — Kiểm tra thông báo khi nhập sai mật khẩu Admin.

- Severity: **Medium**.
- Expected: Hiển thị thông báo lỗi dạng inline banner bên trong form admin.
- Actual: Native browser dialog captured with 'Đăng nhập thất bại'; inline feedback count=0.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/019-admin-login-invalid-dialog.png).
- Reproduction:
  1. Start EShop and open `/ (Unauth)`.
  2. Perform `GUI-ADMIN-LOGIN-003` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-LOGIN-004 — Kiểm tra thông báo khi tài khoản user thường đăng nhập vào Admin.

- Severity: **Medium**.
- Expected: Hiển thị thông báo lỗi phân quyền rõ ràng trên giao diện.
- Actual: Non-admin login produced native dialog 'Bạn không phải là admin!'; inline feedback count=0.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/020-admin-login-nonadmin-dialog.png).
- Reproduction:
  1. Start EShop and open `/ (Unauth)`.
  2. Perform `GUI-ADMIN-LOGIN-004` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-CATEGORY-004 — Kiểm tra thêm mới danh mục với tên rỗng.

- Severity: **High**.
- Expected: Form có thuộc tính required ngăn chặn submit tên danh mục rỗng.
- Actual: required attribute='null'; empty POST observed=true; payload={"name":""}.
- Mode: `MOCKED_WRITE_PREVENTION`.
- Evidence: [screenshot](evidence/executed-chrome/026-admin-category-empty.png).
- Reproduction:
  1. Start EShop and open `/ (Tab categories)`.
  2. Perform `GUI-ADMIN-CATEGORY-004` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-CATEGORY-006 — Kiểm tra popup xác nhận trước khi Xóa danh mục.

- Severity: **High**.
- Expected: Bấm nút 'Xóa' hiển thị modal xác nhận 'Bạn có chắc chắn muốn xóa danh mục này?'.
- Actual: Delete confirmation dialog observed=false.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/027-admin-category-delete.png).
- Reproduction:
  1. Start EShop and open `/ (Tab categories)`.
  2. Perform `GUI-ADMIN-CATEGORY-006` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-CATEGORY-008 — Kiểm tra báo lỗi khi xóa danh mục đang có sản phẩm.

- Severity: **High**.
- Expected: Không xóa category đang được product tham chiếu; UI hiển thị lỗi và category vẫn còn.
- Actual: Category referenced by synthetic product remained=false; error dialog=NONE. Backend allowed deletion=true.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/028-admin-category-delete-in-use.png).
- Reproduction:
  1. Start EShop and open `/ (Tab categories)`.
  2. Perform `GUI-ADMIN-CATEGORY-008` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-CATEGORY-009 — Kiểm tra giao diện khi danh sách danh mục rỗng.

- Severity: **Low**.
- Expected: Hiển thị thông báo hoặc minh họa 'Chưa có danh mục nào'.
- Actual: Mocked empty category response rendered rows=0; empty-state message count=0.
- Mode: `MOCKED_EMPTY_API_STATE`.
- Evidence: [screenshot](evidence/executed-chrome/029-admin-category-empty-state.png).
- Reproduction:
  1. Start EShop and open `/ (Tab categories)`.
  2. Perform `GUI-ADMIN-CATEGORY-009` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-CATEGORY-010 — Kiểm tra chỉ báo Loading khi đang tải dữ liệu danh mục.

- Severity: **Medium**.
- Expected: Hiển thị spinner hoặc skeleton loading khi fetch API.
- Actual: During a 2.5-second category delay, loading indicator count=0.
- Mode: `MOCKED_SLOW_API`.
- Evidence: [screenshot](evidence/executed-chrome/030-admin-category-loading.png).
- Reproduction:
  1. Start EShop and open `/ (Tab categories)`.
  2. Perform `GUI-ADMIN-CATEGORY-010` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-ADMIN-CATEGORY-013 — Kiểm tra ngăn chặn Double Submit khi nhấp liên tục nút Thêm mới.

- Severity: **Medium**.
- Expected: Nút Thêm mới tự động disable trong thời gian chờ gửi request.
- Actual: Rapid double click generated 2 POST request(s); button disabled after completion=false.
- Mode: `MOCKED_SLOW_WRITE`.
- Evidence: [screenshot](evidence/executed-chrome/033-admin-category-double-submit.png).
- Reproduction:
  1. Start EShop and open `/ (Tab categories)`.
  2. Perform `GUI-ADMIN-CATEGORY-013` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-MOBILE-LOGIN-002 — Kiểm tra nhãn label ô nhập Email trên Mobile.

- Severity: **Medium**.
- Expected: Nhãn hiển thị 'Email' phía trên ô nhập liệu.
- Actual: Visible Username label=true; standalone Email label=false.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/034-mobile-login-baseline.png).
- Reproduction:
  1. Start EShop and open `Screen Login`.
  2. Perform `GUI-MOBILE-LOGIN-002` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-MOBILE-LOGIN-004 — Kiểm tra nhãn nút Đăng nhập trên Mobile.

- Severity: **Medium**.
- Expected: Nút có nhãn tiếng Việt 'Đăng nhập'.
- Actual: Rendered submit label is 'Sign In'.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/034-mobile-login-baseline.png).
- Reproduction:
  1. Start EShop and open `Screen Login`.
  2. Perform `GUI-MOBILE-LOGIN-004` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

## BUG-GUI-MOBILE-LOGIN-010 — Kiểm tra Touch Target Size của nút Sign In trên màn hình cảm ứng Mobile.

- Severity: **Medium**.
- Expected: Kích thước vùng bấm đạt tối thiểu 44x44 dp theo tiêu chuẩn Mobile Accessibility.
- Actual: Sign In touch target bounding box={"x":24,"y":320,"width":342,"height":39} CSS px.
- Mode: `LIVE_LOCAL_SUT`.
- Evidence: [screenshot](evidence/executed-chrome/034-mobile-login-baseline.png).
- Reproduction:
  1. Start EShop and open `Screen Login`.
  2. Perform `GUI-MOBILE-LOGIN-010` as described by the checklist.
  3. Observe the recorded UI/network/dialog state.
- GitHub: PENDING_EXTERNAL_ACTION

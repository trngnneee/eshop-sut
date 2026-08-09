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

---

# Phiên làm việc mở rộng — Nâng FR-02 (và FR-07, FR-13) lên đúng quy mô HW04

**AI tool**: Claude Code (model `claude-sonnet-5`) — **Ngày**: `2026-08-08`

Phiên trước (Bước 1–5) chỉ mới tự động hóa **1 test case**. Đề bài HW04 (`docs/2026.HW04.Automation
Testing_En.pdf`) yêu cầu ≥12 case/tính năng, data-driven bằng file ngoài, ≥3 assertion pattern,
chạy đủ 3 browser cho **cả 3 tính năng** đã chọn ở HW02 (FR-02/FR-07/FR-13), review AI, và log bug
thật. Quy trình dưới đây ghi lại đúng các bước đã yêu cầu AI thực hiện, theo thứ tự thật.

## Bước 6: Phân tích yêu cầu đề bài & lập kế hoạch
- **Prompt của người dùng**: "dựa theo file HW4/docs/2026.HW04.Automation Testing_En.pdf để phân
  tích xem requirement này yêu cầu những gì và viết plan để thực hiện requirement đó"
- **AI thực hiện**: Đọc toàn bộ PDF, dò lại repo để xác nhận 3 tính năng đã chọn ở HW02
  (FR-02/FR-07/FR-13, từ branch `HW2-Khoa`), phát hiện kho 80+89+46 test case đã thiết kế sẵn và
  43 bug đã ghi nhận (kể cả một số đã có GitHub Issue), soạn plan chi tiết theo 5 phase.
- **Phản hồi & điều chỉnh của người dùng**: 2 lần yêu cầu tăng quy mô — "cần viết thêm nhiều test
  case hơn và để tìm được nhiều bug hơn", rồi "việc thêm test case và phát hiện thêm bug là cần
  thiết vì với số lượng test case như hiện tại thì số điểm của tui vẫn còn khá thấp". Plan được
  nâng mục tiêu từ 12–15 case/tính năng lên **Login ~50–60, Cart ~60–70, Dashboard ~35–40**, ưu
  tiên phủ hết các case đã biết gây lỗi.

## Bước 7: Áp dụng quy trình 7 bước AI-first cho FR-02 (Analyze → Design → Review → Model data → Map automation → Generate → Verify/repair)
- **Analyze**: Đọc trực tiếp `backend/server.js` để hiểu đúng cơ chế khóa tài khoản thật
  (`login_attempts += 2` mỗi lần sai, khóa khi `>=3`, khóa 180000ms) — phát hiện ngay từ bước phân
  tích rằng đây chính là nguyên nhân của `BUG-FR02-A-01`/`BUG-FR02-A-02` đã ghi nhận ở HW02.
- **Design/Review**: Duyệt qua 80 file `tests/test-cases/login/*.md` (copy tham chiếu tại
  `docs/hw02-reference/`), chọn 63 case chia thành 4 "shape": form-submission (31), UI-standards
  (8), lockout state machine (13, dùng bảng `login_attempts`/`locked_until` làm oracle), API
  contract + JWT (11, dùng `request` fixture của Playwright).
- **Model data**: Tạo 4 file JSON mảng trong `test-data/` (không hardcode mảng trong spec), có
  loader `loadJsonArray()` validate runtime (đủ field, không trùng `caseId`, tối thiểu số lượng).
- **Map automation**: Viết 2 helper `tests/utils/{db,api}.ts` — `db.ts` đọc/ghi trực tiếp
  `backend/database.sqlite` (tái sử dụng driver `sqlite3` đã cài sẵn của backend) để giả lập "đã
  hết thời gian khóa" thay vì phải chờ thật 3 phút; `api.ts` bọc các endpoint `/api/register`,
  `/api/login`, `/api/forgot-password`, `/api/reset-password`, `/api/admin/users`.
- **Generate**: Sinh `tests/login.spec.ts` (3 `describe` block ứng với 3 shape UI) và
  `tests/login-api.spec.ts` (shape API/JWT, tái sử dụng `backend/node_modules/jsonwebtoken` để
  tạo token giả mạo cho case JWT).
- **Verify/repair**: Chạy `npx playwright test --list` xác nhận đủ 63 case; sửa 2 lỗi
  `require()` sai số cấp thư mục tương đối (path resolution) bị phát hiện ngay lần chạy đầu; chạy
  full suite trên cả 3 browser.

## Bước 8: Kết quả thực thi thật & Phân tích lỗi (Analyse — G9.3)
- Kết quả: **46 passed / 17 failed** — **giống hệt nhau trên cả Chromium, Firefox, WebKit**
  (bằng chứng lỗi không phải do automation "flaky" mà do logic phía server, không phụ thuộc
  browser).
- Toàn bộ 17 case fail đã được đối chiếu thủ công với `backend/server.js` và 19 bug đã biết:
  12 case xác nhận đúng các bug cũ (`BUG-FR02-A-01/02/04-08/09/11/12/14/15/17`), **4 case phát
  hiện lỗi hoàn toàn mới** chưa từng được ghi nhận ở HW02 (2 lỗi API-level, 1 lỗi bảo mật lộ
  password dạng plaintext ở mức **High**, 1 lỗi so khớp email phân biệt hoa/thường) — chi tiết ở
  `docs/ai-review-login.md` và `docs/bug-report-login.md`.
- Không sửa assertion để "ép pass" — theo đúng nguyên tắc của `playwright-skill.md`: giữ nguyên kỳ
  vọng đúng đặc tả, để lỗi thật hiện ra làm bằng chứng bug.

## FR-13 Playwright 7-step conversion log

**User prompt:** Use `.agents/skills/playwright-skill/playwright-skill.md` to automate FR-13 EShop Dashboard according to the skill's seven-step process.
**Student ID:** `23127207`
**Scope:** FR-13, the existing Pool C feature in the HW4 three-feature assignment.

### Step 1 — Analyze

- **Inputs:** the HW02 FR-13 cases and bug reports under `docs/hw02-reference/`, `frontend-admin/src/App.jsx`, `backend/server.js`, and the database seed.
- **Action:** extracted actors (admin, regular user, guest), preconditions, metric oracles, API contracts, and the order state model `pending -> confirmed -> shipping -> delivered`, with `canceled` treated as terminal.
- **Outcome:** identified the dashboard UI plus admin user/order APIs. Existing revenue-doubling, role-guard, self-delete, ID-validation, canceled-resurrection, and load-error defects remain expected-failure oracles.

### Step 2 — Design

- **Inputs:** the existing 46 FR-13 HW02 test-case documents and known bugs.
- **Action:** selected non-duplicate positive, negative, boundary, state-transition, data-integrity, access-control, and resilience cases, prioritizing cases tied to known bugs.
- **Outcome:** 32 UI/metric cases and 36 API cases, 68 logical cases total; each has a stable `caseId`, category, description, and observable expected result.

### Step 3 — Review

- **Action:** checked actor, state-transition, boundary amount/count, authentication/authorization, data-exposure, error-handling, and isolation coverage against the source.
- **Outcome:** preserved requirement-conformant assertions even when the product is defective. The self-delete case uses a disposable admin account promoted through the test-only DB helper, so it never deletes the shared seed admin.

### Step 4 — Model data

- **Action:** kept the cases in external JSON: UI cases use `orders`, `expectedOrderCount`, `expectedRevenue`, and explicit `check`/transition fields; API cases use `action` and `from`/`to` for transitions.
- **Outcome:** `test-data/dashboard-data-cases.json` has 32 records and `test-data/dashboard-api-cases.json` has 36 records. Runtime validation now checks file shape, minimum count, duplicate/missing IDs, required fields, and the allowed action/check vocabulary.

### Step 5 — Map automation

- **Action:** mapped user-facing Playwright locators (`getByRole`, `getByPlaceholder`, `getByText`) and HTTP status/response assertions; used API/SQLite only for deterministic setup/cleanup and the admin UI for dashboard behavior.
- **Outcome:** removed fixed sleeps, replaced the styling-class card locator with a text-anchored locator, and retained isolated contexts, sequential workers for shared SQLite, and failure screenshot/trace/video artifacts.

### Step 6 — Generate

- **Affected files:** `tests/dashboard.spec.ts`, `tests/dashboard-api.spec.ts`, `tests/utils/data.ts`, `playwright.config.ts`, `scripts/run-matrix.js`, `scripts/inject-student-id.js`, and `docs/fr13-playwright-ledger.md`.
- **Outcome:** the feature consumes external data, includes case IDs in titles, uses actual student ID `23127207`, supports a report-root override, and records a traceability ledger.

### Step 7 — Verify and repair

- **Pre-check outcome:** `npx tsc --noEmit` passed; `FEATURE=dashboard npx playwright test --list --project=chromium` discovered 68 invocations on one browser, 204 across Chromium/Firefox/WebKit.
- **Execution result:** backend `http://localhost:3000`, storefront `http://localhost:5173`, and admin app `http://localhost:5174` responded locally. `node scripts/run-matrix.js --feature=dashboard` attempted all three cells sequentially, but each Playwright invocation stopped before the first test at Node `child_process.fork` with `Error: spawn EPERM` under Node `v24.10.0`.
- **Evidence:** `reports/fr13-validation/run-manifest.json` records Chromium, Firefox, and WebKit as `exitCode: 1`; no FR-13 HTML report was produced because the test worker could not start. This is recorded as an environment/runtime blocker, not as a product pass/fail result. No older report is being reused as evidence for this run.

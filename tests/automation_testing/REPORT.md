# HW04 — Báo cáo Automation Testing (Task 1)

**Sinh viên:** Đặng Trường Nguyên — MSSV 23127438
**SUT:** EShop (https://github.com/trngnneee/eshop-sut, branch `HW04-Nguyen`)
**Công cụ:** Playwright 1.62.1 (TypeScript), Playwright HTML Reporter
**Môi trường:** macOS (Darwin 24.5.0), Node v26.4.0 — Chromium / Firefox / WebKit
**Ngày chạy:** 2026-08-10 (ISO timestamp nhúng trong từng HTML report)

---

## 1. Tổng quan kết quả

| | FR-02 Đăng nhập & Khóa TK (Pool A) | FR-09 Mã giảm giá (Pool B) | FR-14 Danh mục CRUD (Pool C) | **Tổng** |
|---|---|---|---|---|
| Số test case | 15 | 13 | 12 | **40** |
| Browser runs | 3 | 3 | 3 | **9** |
| Tổng lượt test | 45 | 39 | 36 | **120** |
| Passed | 27 | 24 | 30 | **81** |
| Failed | 18 (= 6 TC × 3 browsers) | 15 (= 5 TC × 3) | 6 (= 2 TC × 3) | **39** |
| Bug phát hiện | 5 | 3 | 1 | **9** |

**Điểm quan trọng:** 100% test fail là *fail đúng kỳ vọng* — assertion viết theo đặc tả (SRS), còn SUT triển khai sai đặc tả. Kết quả **nhất quán tuyệt đối trên cả 3 browser** (cùng 13 TC fail trên Chromium, Firefox, WebKit), chứng tỏ fail do lỗi SUT chứ không phải flaky test. Không có test nào không automate được.

## 2. HTML Reports (đều hiển thị "Run by: 23127438" + ISO timestamp)

| Report | Đường dẫn | Phạm vi |
|---|---|---|
| Tổng hợp | `reports/all/index.html` | 3 features × 3 browsers |
| FR-02 | `reports/fr02-login/index.html` | 15 TC × 3 browsers |
| FR-09 | `reports/fr09-coupon/index.html` | 13 TC × 3 browsers |
| FR-14 | `reports/fr14-category/index.html` | 12 TC × 3 browsers |

Xem bằng: `npx playwright show-report reports/<tên>`

## 3. Thiết kế test

- **Data-driven:** toàn bộ test case nằm trong `data/*.json` (không có array/object hardcode trong spec). Spec chỉ là vòng lặp đọc từng dòng dữ liệu và dispatch theo `outcome`/`action`. Token động `{{UNIQUE}}`, `{{LONG255}}` được thay ở runtime.
- **Page Object Model:** `pages/LoginPage.ts`, `pages/CheckoutPage.ts`, `pages/AdminCategoriesPage.ts`.
- **Cô lập trạng thái** (3 browser dùng chung 1 backend SQLite): kịch bản lockout và coupon-usage đăng ký user mới qua API cho từng test; test danh mục snapshot trước mỗi test và dọn sạch trong `afterEach`; `workers: 1`.
- **7 assertion patterns** (yêu cầu tối thiểu 3): URL (`toHaveURL`), visibility/state (`toBeVisible`/`toBeDisabled`/`toBeHidden`), text (`toHaveText`/`toContainText`), attribute/value (`toHaveAttribute`/`toHaveValue`), count (`toHaveCount`), API response status (`resp.status()` qua `waitForResponse` — phân biệt 401 sai mật khẩu với 403 bị khóa trong khi UI chỉ hiện thông báo chung), soft assertion (`expect.soft`).

## 4. Danh sách test case

### FR-02 — Đăng nhập & Khóa tài khoản (15 TC, data: `data/fr02-login.json`)

| TC | Loại | Nội dung | Kết quả (3 browsers) |
|---|---|---|---|
| FR02-TC01 | positive | Đăng nhập thành công user hợp lệ, lưu JWT, redirect `/` | ✅ Pass |
| FR02-TC02 | positive | Đăng nhập tài khoản admin trên web user | ✅ Pass |
| FR02-TC03 | negative | Sai mật khẩu → 401 + thông báo chung | ✅ Pass |
| FR02-TC04 | negative | Email chưa đăng ký → 401 + thông báo chung | ✅ Pass |
| FR02-TC05 | negative | Email trống → HTML5 chặn submit | ✅ Pass |
| FR02-TC06 | negative | Mật khẩu trống → HTML5 chặn submit | ✅ Pass |
| FR02-TC07 | negative | Email sai định dạng phải bị chặn (type=email) | ❌ Fail → **BUG-02** |
| FR02-TC08 | edge | Email có khoảng trắng bao quanh → 401 | ✅ Pass |
| FR02-UI01 | ui | Tiêu đề trang phải là "Đăng nhập" | ❌ Fail → **BUG-01** |
| FR02-UI02 | ui | Ô email phải có `type="email"` | ❌ Fail → **BUG-02** |
| FR02-UI03 | ui | Ô mật khẩu phải che ký tự (`type="password"`) | ❌ Fail → **BUG-03** |
| FR02-UI04 | ui | Có liên kết "Quên mật khẩu?" | ✅ Pass |
| FR02-LK01 | edge | 2 lần sai + đăng nhập đúng → phải thành công | ❌ Fail → **BUG-04** |
| FR02-LK02 | negative | ≥3 lần sai → khóa, API trả 403, thông báo không lộ chi tiết | ✅ Pass |
| FR02-LK03 | edge | Sau khóa 31s (spec: khóa 30s) đăng nhập đúng → phải thành công | ❌ Fail → **BUG-05** |

### FR-09 — Mã giảm giá (13 TC, data: `data/fr09-coupon.json`)

| TC | Loại | Nội dung | Kết quả |
|---|---|---|---|
| FR09-TC01 | positive | SAVE10 10% đơn 500k → giảm 50k, còn 450k | ❌ Fail → **BUG-06** |
| FR09-TC02 | positive | BIGBUY 50k đơn 600k → còn 550k | ✅ Pass |
| FR09-TC03 | positive | VIP100 100k đơn 1.000k → còn 900k | ✅ Pass |
| FR09-TC04 | edge | Biên C3: VIP100 đơn đúng ngưỡng 300k (>=) | ❌ Fail → **BUG-07** |
| FR09-TC05 | edge | Biên C3: BIGBUY đơn đúng ngưỡng 500k (>=) | ❌ Fail → **BUG-07** |
| FR09-TC06 | negative | C1: mã không tồn tại → lỗi | ✅ Pass |
| FR09-TC07 | negative | C2: mã EXPIRED hết hạn → lỗi | ✅ Pass |
| FR09-TC08 | negative | C3: đơn dưới ngưỡng → lỗi | ✅ Pass |
| FR09-TC09 | edge | Mã chữ thường "save10" → chuẩn hóa, áp đúng 10% | ❌ Fail → **BUG-06** |
| FR09-TC10 | negative | C4: guest chưa đăng nhập không được áp mã | ❌ Fail → **BUG-08** |
| FR09-TC11 | negative | C5: vượt giới hạn lượt dùng → lỗi | ✅ Pass |
| FR09-TC12 | negative | Ô mã trống → nút Áp dụng vô hiệu | ✅ Pass |
| FR09-TC13 | positive | "Tổng thanh toán" cập nhật theo thành tiền | ✅ Pass |

### FR-14 — Quản lý Danh mục CRUD (12 TC, data: `data/fr14-category.json`)

| TC | Loại | Nội dung | Kết quả |
|---|---|---|---|
| FR14-TC01 | positive | Bảng hiển thị đủ cột + danh mục mặc định | ✅ Pass |
| FR14-TC02 | positive | Thêm danh mục hợp lệ → xuất hiện trong bảng | ✅ Pass |
| FR14-TC03 | negative | Tên rỗng phải bị từ chối | ❌ Fail → **BUG-09** |
| FR14-TC04 | negative | Tên toàn khoảng trắng phải bị từ chối | ❌ Fail → **BUG-09** |
| FR14-TC05 | edge | Tên unicode + emoji hiển thị đúng | ✅ Pass |
| FR14-TC06 | edge | Tên dài 255 ký tự | ✅ Pass |
| FR14-TC07 | edge | Tên trùng danh mục có sẵn (spec không cấm) | ✅ Pass |
| FR14-TC08 | edge | Tên chứa thẻ HTML → hiển thị văn bản thuần (chống XSS) | ✅ Pass |
| FR14-TC09 | positive | Xóa danh mục → biến mất khỏi bảng | ✅ Pass |
| FR14-TC10 | positive | Danh mục còn nguyên sau reload (persist DB) | ✅ Pass |
| FR14-TC11 | positive | Danh mục mới xuất hiện trong dropdown form sản phẩm | ✅ Pass |
| FR14-TC12 | positive | Ô nhập được xóa trống sau khi thêm | ✅ Pass |

## 5. Tổng hợp bug (chi tiết từng bug trên GitHub Issues)

| Bug | FR | Mô tả | Severity/Priority | TC phát hiện |
|---|---|---|---|---|
| BUG-01 | FR-02 | Trang đăng nhập hiển thị tiêu đề "Đăng Ký" | Minor / P2 | FR02-UI01 |
| BUG-02 | FR-02 | Ô email dùng `type="text"` — không validate định dạng email | Major / P1 | FR02-UI02, TC07 |
| BUG-03 | FR-02 | Ô mật khẩu không che ký tự (`type="text"`) | Major / P1 | FR02-UI03 |
| BUG-04 | FR-02 | Bộ đếm đăng nhập sai tăng +2/lần (spec: +1) → khóa chỉ sau 2 lần sai | Major / P1 | FR02-LK01 |
| BUG-05 | FR-02 | Thời gian khóa 180s (spec: 30s) | Minor / P2 | FR02-LK03 |
| BUG-06 | FR-09 | Công thức giảm % sai: `total×(1−value)` thay vì `total×value/100` | Critical / P0 | FR09-TC01, TC09 |
| BUG-07 | FR-09 | Ngưỡng đơn tối thiểu dùng `>` thay vì `>=` — đơn đúng ngưỡng bị từ chối | Major / P1 | FR09-TC04, TC05 |
| BUG-08 | FR-09 | Không kiểm tra đăng nhập (C4) — guest áp mã được, bỏ qua cả giới hạn lượt dùng | Major / P1 | FR09-TC10 |
| BUG-09 | FR-14 | Cho phép thêm danh mục tên rỗng / toàn khoảng trắng | Major / P1 | FR14-TC03, TC04 |

Screenshot từng bug: `bugs/screenshots/`. Trace + screenshot đầy đủ theo từng browser nằm trong HTML reports.

## 6. Review & gap analysis script do AI sinh (human review)

Các lỗi/thiếu sót của AI trong quá trình sinh script và cách khắc phục:

1. **AI mặc định dùng `getByLabel()` cho form login** — sai, vì label của SUT không gắn `htmlFor`/`id` với input nên locator không resolve được. *Nguyên nhân:* AI sinh code theo pattern chuẩn accessibility mà không nhìn DOM thật. *Fix:* soi source JSX thật rồi neo locator theo cấu trúc `form > div` chứa label (`pages/LoginPage.ts`).
2. **Bản nháp đầu hardcode test data trong spec** — vi phạm yêu cầu data-driven của đề. *Fix:* tách 100% test case ra `data/*.json`, spec chỉ còn vòng lặp.
3. **AI không lường trạng thái dùng chung giữa các browser run** — lockout counter, coupon usage, category nằm trong SQLite dùng chung; chạy 3 browser tuần tự sẽ dây bẩn nhau (browser 1 khóa tài khoản làm browser 2 fail oan). *Nguyên nhân:* đặc thù SUT (DB persistent) không thể hiện trong prompt ban đầu. *Fix:* seed user riêng qua API cho từng kịch bản lockout/usage; snapshot + dọn category trong `afterEach`; `workers: 1`.
4. **Assertion UI đơn thuần không phân biệt được "sai mật khẩu" và "bị khóa"** — frontend luôn hiện cùng một thông báo chung. *Fix:* thêm assertion tầng API (`waitForResponse` → check 401/403) để kịch bản lockout kiểm chứng được đúng hành vi backend.
5. **Kịch bản 3 lần sai của AI giả định mỗi lần sai đều trả 401** — thực tế do bug +2 của SUT, lần sai thứ 3 đã trả 403, làm assertion giữa chừng fail lạc đề. *Fix:* dùng `expect.soft([401,403]).toContain(...)` trong vòng lặp để kịch bản đi tới assertion chính.
6. **Race condition khi đếm dòng bảng danh mục** — assert `toHaveCount` ngay sau click có thể pass giả (đếm trước khi bảng refresh). *Fix:* `addCategory()` chờ POST + GET refresh hoàn tất rồi mới assert.
7. **Định dạng số tiền phụ thuộc locale** — `toLocaleString()` cho kết quả khác nhau giữa browser/máy. *Fix:* cố định `locale: 'en-US'` trong config và format expected value bằng cùng locale.

## 7. Cách chạy lại

```bash
cd tests/automation_testing
npm install && npx playwright install
npx playwright test                 # 3 features × 3 browsers → reports/all
npm run test:fr02 | test:fr09 | test:fr14   # report riêng từng feature
```

MSSV 23127438 đã đặt làm default trong `playwright.config.ts` (override bằng env `STUDENT_ID`).

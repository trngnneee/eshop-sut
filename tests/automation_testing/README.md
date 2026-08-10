# EShop Automation Testing — HW04

**Sinh viên:** Đặng Trường Nguyên — MSSV 23127438 — 23KTPM3
**Repo:** https://github.com/trngnneee/eshop-sut (branch `HW04-Nguyen`)

## Bảng tự chấm (Self-Assessment)

| No. | Criteria | Grade | Self-Assessed Grade |
|-----|----------|-------|---------------------|
| 1 | Task 1 - Feature A (FR-02 Đăng nhập & Khóa tài khoản) | 25 | 25 |
| 1 | Task 1 - Feature B (FR-09 Mã giảm giá) | 25 | 25 |
| 1 | Task 1 - Feature C (FR-14 Quản lý danh mục CRUD) | 25 | 25 |
| 2 | Task 2 — Demo video | 15 | 15 |
| 3 | Agent Skills | 10 | 10 |
| | **Total** | **100** | **100** |

## Test Summary Report

| Chỉ số | Giá trị |
|--------|---------|
| Số features | **3** (FR-02 · FR-09 · FR-14, mỗi pool A/B/C một feature) |
| Số test case automated | **40** (15 + 13 + 12) — 100% data-driven từ `data/*.json` |
| Số lượt test executed | **120** (40 TC × 3 browsers) |
| Passed | **81** |
| Failed | **39** (= 13 TC × 3 browsers — toàn bộ là fail đúng kỳ vọng, lộ bug SUT vi phạm spec; 0 flaky) |
| Số browser runs | **9** per-feature (3 features × Chromium/Firefox/WebKit) + 1 run tổng hợp |
| Số bug phát hiện | **9** — GitHub Issues [#390–#398](https://github.com/trngnneee/eshop-sut/issues?q=label%3A%22found-by%3A+test-case%22) kèm screenshot |
| HTML reports | `reports/all`, `reports/fr02-login`, `reports/fr09-coupon`, `reports/fr14-category` — đều hiển thị "Run by: 23127438" + ISO timestamp |
| Demo video (Task 2 + Agent Skill) | https://drive.google.com/drive/folders/1mqqIYAefulrImQr8dNTJc4VmbrVeanh8?usp=sharing |
| Agent Skill | `.claude/skills/playwright-data-driven-suite/SKILL.md` |
| Báo cáo chi tiết | `REPORT.md` · AI Audit/Critique: `ai_declaration/` · Git log: `git_log.txt` |

---

Playwright test suite (data-driven, multi-browser) cho 3 features của EShop SUT:

| Pool | Feature | Spec file | Data file | Số TC |
|------|---------|-----------|-----------|-------|
| A | FR-02 Đăng nhập & Khóa tài khoản | `tests/fr02-login.spec.ts` | `data/fr02-login.json` | 15 |
| B | FR-09 Mã giảm giá | `tests/fr09-coupon.spec.ts` | `data/fr09-coupon.json` | 13 |
| C | FR-14 Quản lý danh mục (CRUD) | `tests/fr14-category.spec.ts` | `data/fr14-category.json` | 12 |

## Chạy test

```bash
cd eshop-sut/tests/automation_testing
npm install
npx playwright install

# Chạy toàn bộ trên 3 browsers (Chromium + Firefox + WebKit), báo cáo ở reports/all
STUDENT_ID=<MSSV> npx playwright test

# Chạy từng feature, mỗi feature 1 HTML report riêng (vẫn đủ 3 browsers)
STUDENT_ID=<MSSV> npm run test:fr02
STUDENT_ID=<MSSV> npm run test:fr09
STUDENT_ID=<MSSV> npm run test:fr14

# Mở report
npm run report
```

Không cần khởi động server thủ công — `playwright.config.ts` khai báo `webServer` tự bật backend (:3000), web (:5173), admin (:5174) và tái sử dụng nếu đã chạy sẵn.

**Bắt buộc**: đặt biến môi trường `STUDENT_ID` — giá trị này được nhúng vào tiêu đề + metadata của HTML report (`Run by: {StudentID}` + ISO timestamp) theo yêu cầu anti-cheat của đề.

## Thiết kế

- **Data-driven**: 100% test case nằm trong `data/*.json` (không hardcode trong spec). Spec chỉ là vòng lặp đọc từng row và dispatch theo `outcome`/`action`. Token động (`{{UNIQUE}}`, `{{LONG255}}`) được thay ở runtime để tránh đụng dữ liệu giữa các browser run.
- **Page Object Model**: `pages/LoginPage.ts`, `pages/CheckoutPage.ts`, `pages/AdminCategoriesPage.ts`.
- **Cô lập trạng thái** (backend SQLite dùng chung cho mọi run):
  - Kịch bản lockout đăng ký user mới qua API cho từng test — không làm khóa tài khoản chung `test@eshop.com`.
  - Kịch bản coupon usage (C5) dùng user mới đăng ký riêng + seed lượt dùng qua API.
  - Test danh mục chụp snapshot trước mỗi test, `afterEach` xóa mọi danh mục phát sinh.
  - `workers: 1` + `fullyParallel: false` vì cả 3 browser cùng đánh vào một backend stateful.

## Assertion patterns sử dụng (≥3 theo yêu cầu đề)

1. **URL assertion** — `expect(page).toHaveURL(...)` (fr02: redirect sau login).
2. **Visibility/State** — `toBeVisible()`, `toBeHidden()`, `toBeDisabled()` (fr09: nút Áp dụng vô hiệu khi ô mã trống).
3. **Text content** — `toHaveText()`, `toContainText()` (fr02 heading, fr09 số tiền giảm/thành tiền).
4. **Attribute/Value** — `toHaveAttribute('type', ...)`, `toHaveValue()` (fr02: type=email/password; fr14: input cleared).
5. **Count** — `toHaveCount(n)` (fr14: số dòng bảng danh mục, số option trong select).
6. **API response status** — `expect(resp.status()).toBe(401/403/200)` qua `page.waitForResponse` (fr02: phân biệt sai mật khẩu 401 với bị khóa 403 — UI chỉ hiện thông báo chung).
7. **Soft assertion** — `expect.soft(...)` (fr02 lockout loop, fr14 view các danh mục mặc định).

## Bug cố ý của SUT mà suite này phát hiện (test fail = bug, không phải lỗi script)

| Test | Spec | SUT thực tế |
|------|------|-------------|
| FR02-UI01 | Trang đăng nhập tiêu đề "Đăng nhập" | Hiển thị "Đăng Ký" |
| FR02-UI02 / TC07 | Ô email `type="email"` (HTML5 validate) | `type="text"`, email sai định dạng vẫn gửi lên server |
| FR02-UI03 | Ô mật khẩu che ký tự | `type="text"` — mật khẩu hiển thị trần |
| FR02-LK01 | Mỗi lần sai tăng bộ đếm **+1** | Backend tăng **+2** → khóa sau 2 lần sai |
| FR02-LK03 | Khóa tạm **30 giây** | Backend khóa **180 giây** |
| FR09-TC01/09 | `discount = total × value / 100` | Backend tính `total × (1 − value)` → số tiền giảm âm/sai hoàn toàn |
| FR09-TC04/05 | Ngưỡng đơn hàng điều kiện **>=** | Backend dùng **>** → đơn đúng ngưỡng bị từ chối |
| FR09-TC10 | C4: phải đăng nhập mới được áp mã | Backend không kiểm tra JWT, guest áp mã được |
| FR14-TC03/04 | Tên danh mục bắt buộc | Backend + frontend đều nhận tên rỗng/khoảng trắng |

Chi tiết phân tích (kèm nguyên nhân AI bỏ sót ban đầu) nằm trong report chính của bài nộp.

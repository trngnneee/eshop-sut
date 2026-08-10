---
name: automation-testing
description: >
  Hướng dẫn agent thực hiện toàn bộ workflow kiểm thử tự động (Task 1 – HW04):
  sinh script với AI theo từng bước, tổ chức dữ liệu data-driven, chạy đa trình
  duyệt với Playwright, review & fix script, xuất HTML report có "Run by: <StudentID>",
  và cập nhật toàn bộ tài liệu nộp bài trong thư mục submission/.
  Kích hoạt khi người dùng yêu cầu: "viết/sinh automation script", "kiểm thử tự động",
  "chạy playwright", "data-driven testing", "tạo test script cho feature", hoặc
  bất kỳ yêu cầu nào liên quan đến automation testing cho bài tập HW04.
---

# Automation Testing Skill — HW04

## Mục tiêu

Thực hiện đầy đủ **Task 1 – AI-Generated Automation Scripts** theo yêu cầu HW04:

1. Sinh script bằng AI theo từng bước (không dùng 1 prompt duy nhất).
2. Tổ chức test data dưới dạng file `.json` hoặc `.csv` riêng biệt (data-driven).
3. Dùng ít nhất **3 assertion pattern** khác nhau.
4. Chạy trên **3 browsers** (Chromium / Firefox / WebKit).
5. Xuất HTML report có nhãn `"Run by: 23127486"`.
6. Review & fix script, ghi lại những gì AI sai/bỏ sót.
7. **Cập nhật toàn bộ tài liệu nộp bài** trong `submission/`.

---

## Thông tin sinh viên (cố định)

```
Student Name : Phan Quốc Thịnh
Student ID   : 23127486
Class        : 23KTPM3
Submission   : c:\Users\Public\Projects\Testing_HCMUS\HW4\eshop-sut\submission\
```

---

## PHASE 0 — Chuẩn bị

### 0.1 Xác định feature cần tự động hóa

Nhận từ người dùng (hoặc đọc từ `submission/MainReport.md`).

Nếu chưa chỉ định chức năng hoặc chỉ định chưa đủ 3 chức năng (mỗi pool 1 cái) thì yêu cầu người dùng chỉ định 3 chức năng thuộc 3 pool A, B, C.

### 0.2 Kiểm tra cấu trúc thư mục tests/

Kiểm tra xem thư mục `tests/` đã tồn tại chưa. Nếu chưa, tạo theo cấu trúc:

```
tests/
├── data/
│   ├── fr01_registration.json
│   ├── fr09_coupons.json
│   └── fr16_csv_import.json
├── fr01_registration.spec.ts
├── fr09_coupons.spec.ts
└── fr16_csv_import.spec.ts
playwright.config.ts
```

### 0.3 Kiểm tra Playwright đã cài chưa

```powershell
npx playwright --version
```

Nếu chưa có `playwright.config.ts`, tạo config với cấu hình chuẩn (xem Section 1.1).

---

## PHASE 1 — Cấu hình Playwright

### 1.1 Tạo/kiểm tra `playwright.config.ts`

File này phải:
- Chạy trên **3 projects**: `chromium`, `firefox`, `webkit`.
- Dùng **HTML reporter** với title chứa `Run by: 23127486`.
- Đặt `outputFolder` cho mỗi browser riêng biệt.

```typescript
// playwright.config.ts (template)
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30_000,
  retries: 1,
  reporter: [
    ['html', {
      outputFolder: 'playwright-report',
      open: 'never',
      // Thêm metadata vào report
    }],
    ['list'],
  ],
  use: {
    baseURL: 'http://localhost:3000', // TODO: cập nhật URL SUT
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox',  use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit',   use: { ...devices['Desktop WebKit'] } },
  ],
});
```

> **Quan trọng:** Để report hiển thị `Run by: 23127486`, thêm annotation vào
> `test.info().annotations` trong mỗi test file, hoặc dùng `globalSetup` để
> ghi metadata. Chi tiết tại `references/playwright_report_metadata.md`.

---

## PHASE 2 — Sinh Script bằng AI (theo từng bước)

> Áp dụng **AI-First strategy**: hướng dẫn AI từng bước, không dùng 1 prompt chung chung.

### Bước 2.1 — Prompt AI về cấu trúc feature

Gửi prompt đầu tiên với nội dung:

```
Tôi cần viết Playwright automation test cho feature [FEATURE_NAME] của ứng dụng
EShop (web e-commerce). Hãy liệt kê các test scenario quan trọng nhất cho feature
này, bao gồm: positive cases, negative cases, và edge cases. Tổng ít nhất 12 test cases.
Chưa viết code, chỉ cần liệt kê tên và mô tả ngắn gọn mỗi TC.
```

### Bước 2.2 — Prompt AI về test data

```
Dựa vào danh sách test cases trên, hãy tạo file test data dạng JSON để dùng
data-driven testing với Playwright. File sẽ được đặt tại tests/data/[feature].json.
Mỗi entry phải có đầy đủ các trường cần thiết cho từng test case.
```

Lưu file JSON thực vào `tests/data/[feature].json`.

### Bước 2.3 — Prompt AI sinh Playwright script

```
Bây giờ hãy viết Playwright test script TypeScript cho feature [FEATURE_NAME].
Yêu cầu:
1. Import test data từ file JSON (data-driven, không hardcode inline).
2. Dùng ít nhất 3 loại assertion khác nhau:
   - expect(locator).toBeVisible()
   - expect(locator).toHaveText() hoặc toContainText()
   - expect(page).toHaveURL() hoặc toHaveTitle()
3. Mỗi test case phải có annotation: test.info().annotations.push({ type: 'Run by', description: '23127486' })
4. Dùng Page Object Model nếu feature phức tạp.
5. Thêm meaningful test descriptions.
```

### Bước 2.4 — Prompt AI thêm error handling & edge cases

```
Review script vừa tạo và:
1. Thêm proper wait strategies (tránh hardcoded sleep).
2. Đảm bảo selectors ổn định (ưu tiên: data-testid > aria-label > role > text).
3. Thêm test.beforeEach() cho setup chung.
4. Thêm test.afterEach() cho cleanup.
```

---

## PHASE 3 — Chạy Test trên 3 Browsers

### 3.1 Chạy toàn bộ suite

```powershell
# Chạy tất cả browsers
npx playwright test

# Chạy từng browser riêng (nếu cần debug)
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### 3.2 Xuất HTML Report

```powershell
# Report tự động được tạo tại playwright-report/
# Xem report:
npx playwright show-report
```

### 3.3 Kiểm tra report có "Run by: 23127486"

Mở `playwright-report/index.html` và xác nhận nhãn `Run by: 23127486` xuất hiện
trong phần annotations hoặc metadata của report.

---

## PHASE 4 — Ghi nhận Bug (nếu có)

Nếu test fail vì lỗi thực sự trong SUT (không phải lỗi script):

1. **Chụp screenshot** lỗi (Playwright tự động lưu vào `test-results/`).
2. **Tạo GitHub Issue** với screenshot đính kèm.
3. **Ghi vào `submission/Bug_Report.md`** theo template có sẵn.

---

## PHASE 5 — Cập nhật tài liệu nộp bài (QUAN TRỌNG)

Sau khi hoàn thành test, **bắt buộc** cập nhật các file trong `submission/`:

### 5.1 Cập nhật `submission/MainReport.md`

Điền vào từng section theo feature đang làm:

**Section 2.X.1 – AI Generation Process:**
- Mô tả từng bước prompt đã gửi AI (copy từ Phase 2).
- Ghi rõ tên AI tool và thời điểm sử dụng.

**Section 2.X.2 – Test Cases Automated:**
- Điền tên 12 test cases vào bảng (TC01–TC12).
- Ghi type (Positive/Negative/Edge) và tên data file.
- Cập nhật Status (PASS/FAIL) sau khi chạy.

**Section 2.X.3 – Data-Driven Setup:**
- Điền tên file data (`tests/data/[feature].json`).
- Liệt kê 3 assertion patterns đã dùng.

**Section 2.X.4 – Multi-Browser Run Results:**
- Điền số liệu Total/Passed/Failed cho từng browser.
- Dán link HTML report (GitHub Pages hoặc đường dẫn repo).

**Section 2.X.5 – Human Review & Fixes:**
- Điền bảng issues đã tìm thấy và fix.
- Lý giải tại sao AI bỏ sót.

### 5.2 Cập nhật `submission/AI_Audit.md`

Với mỗi lần tương tác AI (mỗi prompt trong Phase 2):

Thêm 1 row vào bảng Section 3:

```
| Tool: [Tên AI], Time: [HH:MM DD/MM/YYYY]
  Prompt: "[Paste verbatim prompt]"
| [Paste verbatim AI output hoặc tóm tắt + screenshot label]
| VALID / INVALID / INCOMPLETE
| [Lý giải có trích dẫn ISTQB section]
| [Artifact đã sửa, highlight thay đổi]
```

Cập nhật Section 4 – Summary of AI Accuracy sau khi hoàn thành tất cả features.

### 5.3 Cập nhật `submission/AI_Critique.md`

Sau khi hoàn thành tất cả 3 features, viết đoạn critique 200–300 từ:
- Chỗ AI làm sai/bias/thiếu gì?
- Tại sao AI không phát hiện được?
- Bài học về cộng tác với AI.

### 5.4 Cập nhật `submission/Bug_Report.md`

Với mỗi bug phát hiện:
- Điền đầy đủ Bug ID, Title, Feature, Severity, Steps, Expected, Actual.
- Dán link GitHub Issue.
- Nhúng screenshot URL.

### 5.5 Cập nhật `submission/README.md`

Cập nhật bảng Test Summary Report:

```markdown
| Metric | Value |
|:-------|:------|
| Number of features automated | 3 |
| Feature A | FR-01 – Account Registration |
| Feature B | FR-09 – Discount Coupons |
| Feature C | FR-16 – Product Import from CSV |
| Total test cases automated | [số thực tế] |
| Total test cases executed   | [số thực tế] |
| Test cases passed           | [số thực tế] |
| Test cases failed           | [số thực tế] |
| Number of browser runs      | [số thực tế] |
| Number of bugs found        | [số thực tế] |
| Demo video link             | [YouTube URL] |
| GitHub repository           | [GitHub URL]  |
```

---

## PHASE 6 — Kiểm tra hoàn thành

Trước khi kết thúc, chạy checklist cuối:

### Checklist nộp bài

| # | Hạng mục | Yêu cầu | Xong? |
|:-:|:---------|:--------|:-----:|
| 1 | Script Feature A | ≥ 12 TCs, data-driven, 3 browser runs | [ ] |
| 2 | Script Feature B | ≥ 12 TCs, data-driven, 3 browser runs | [ ] |
| 3 | Script Feature C | ≥ 12 TCs, data-driven, 3 browser runs | [ ] |
| 4 | HTML Reports | Tất cả 9 reports có "Run by: 23127486" | [ ] |
| 5 | MainReport.md | Tất cả sections đã điền đầy đủ | [ ] |
| 6 | AI_Audit.md | Mỗi AI interaction có 1 row trong bảng | [ ] |
| 7 | AI_Critique.md | Đã viết 200–300 từ | [ ] |
| 8 | Bug_Report.md | Bugs (nếu có) đã ghi và link GitHub Issue | [ ] |
| 9 | README.md | Test summary đã cập nhật số liệu thực | [ ] |
| 10 | git_commit_log.txt | ≥ 8 commits trên ≥ 4 ngày (test scripts) | [ ] |
| 11 | Demo video | ≥ 5 phút, tiếng Việt, có authorship evidence | [ ] |
| 12 | GitHub repo | Public, scripts + data + HTML reports | [ ] |

---

## Tham khảo

- `references/playwright_report_metadata.md` — Cách inject "Run by: StudentID" vào HTML report.
- `references/data_driven_examples.md` — Mẫu file JSON/CSV và cách import trong Playwright.
- `references/assertion_patterns.md` — Danh sách assertion patterns và khi nào dùng.
- [Playwright Docs](https://playwright.dev/docs/intro)
- [ISTQB Foundation Level Syllabus](https://www.istqb.org)

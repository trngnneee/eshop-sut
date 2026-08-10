# Playwright Report Metadata — "Run by: StudentID"

## Vấn đề

Playwright HTML Reporter mặc định không có trường "Run by". Cần inject thông tin
`Run by: 23127486` vào report theo một trong các cách dưới đây.

---

## Cách 1: Test Annotation (khuyến nghị — đơn giản nhất)

Thêm vào mỗi `test()` block:

```typescript
import { test, expect } from '@playwright/test';

test('TC01 - Register with valid data', async ({ page }) => {
  test.info().annotations.push({
    type: 'Run by',
    description: '23127486 - Phan Quoc Thinh',
  });

  // ... rest of the test
});
```

Annotation này sẽ xuất hiện trong HTML report dưới mỗi test case.

---

## Cách 2: `test.use()` với Metadata (global cho cả file)

```typescript
import { test, expect } from '@playwright/test';

test.beforeEach(async ({}, testInfo) => {
  testInfo.annotations.push({
    type: 'Run by',
    description: '23127486',
  });
  testInfo.annotations.push({
    type: 'Student',
    description: 'Phan Quoc Thinh – 23KTPM3',
  });
});
```

---

## Cách 3: Global Setup — inject vào tất cả tests

Tạo file `tests/global-setup.ts`:

```typescript
import { FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  // Ghi metadata vào file để reporter đọc
  process.env.RUN_BY = '23127486';
  process.env.STUDENT_NAME = 'Phan Quoc Thinh';
  process.env.STUDENT_CLASS = '23KTPM3';
}

export default globalSetup;
```

Thêm vào `playwright.config.ts`:

```typescript
export default defineConfig({
  globalSetup: './tests/global-setup.ts',
  // ...
});
```

Rồi trong mỗi test file:

```typescript
test.beforeEach(async ({}, testInfo) => {
  testInfo.annotations.push({
    type: 'Run by',
    description: process.env.RUN_BY ?? '23127486',
  });
});
```

---

## Cách 4: Custom Reporter Title

Trong `playwright.config.ts`, dùng reporter với title:

```typescript
reporter: [
  ['html', {
    outputFolder: 'playwright-report',
    open: 'never',
    // Note: Playwright HTML reporter không có `title` option trực tiếp,
    // nhưng annotations sẽ hiện trong report.
  }],
],
```

---

## Kiểm tra kết quả

Sau khi chạy `npx playwright test`:

1. Mở `playwright-report/index.html`.
2. Click vào bất kỳ test case nào.
3. Xem section "Annotations" — phải thấy `Run by: 23127486`.

---

## Chạy trên nhiều browsers & tạo report riêng

```powershell
# Chạy và tạo report chung (mặc định)
npx playwright test

# Chạy từng browser, report riêng
npx playwright test --project=chromium --reporter=html
Move-Item playwright-report playwright-report-chromium

npx playwright test --project=firefox --reporter=html  
Move-Item playwright-report playwright-report-firefox

npx playwright test --project=webkit --reporter=html
Move-Item playwright-report playwright-report-webkit
```

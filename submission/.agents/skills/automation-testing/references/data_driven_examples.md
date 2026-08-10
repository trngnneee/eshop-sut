# Data-Driven Testing Examples — Playwright + JSON/CSV

## Nguyên tắc

- **KHÔNG** hardcode test data inline trong script.
- **BẮT BUỘC** lưu data vào file riêng: `tests/data/<feature>.json` hoặc `.csv`.
- Script đọc data từ file và dùng `test.each()` hoặc vòng lặp.

---

## Ví dụ 1: JSON + `test.each()` (khuyến nghị)

### File `tests/data/fr01_registration.json`

```json
[
  {
    "id": "TC01",
    "type": "positive",
    "description": "Register with valid data",
    "username": "testuser_001",
    "email": "testuser001@example.com",
    "password": "StrongPass@123",
    "confirmPassword": "StrongPass@123",
    "expectedResult": "success",
    "expectedMessage": "Đăng ký thành công"
  },
  {
    "id": "TC02",
    "type": "negative",
    "description": "Register with existing email",
    "username": "existing_user",
    "email": "existing@example.com",
    "password": "StrongPass@123",
    "confirmPassword": "StrongPass@123",
    "expectedResult": "failure",
    "expectedMessage": "Email đã được sử dụng"
  },
  {
    "id": "TC03",
    "type": "negative",
    "description": "Register with mismatched passwords",
    "username": "newuser003",
    "email": "newuser003@example.com",
    "password": "Password@123",
    "confirmPassword": "DifferentPass@456",
    "expectedResult": "failure",
    "expectedMessage": "Mật khẩu không khớp"
  },
  {
    "id": "TC04",
    "type": "edge",
    "description": "Register with minimum valid username length",
    "username": "ab",
    "email": "minuser@example.com",
    "password": "ValidPass@1",
    "confirmPassword": "ValidPass@1",
    "expectedResult": "success",
    "expectedMessage": "Đăng ký thành công"
  }
]
```

### File `tests/fr01_registration.spec.ts`

```typescript
import { test, expect } from '@playwright/test';
import testData from './data/fr01_registration.json';

test.describe('FR-01: Account Registration', () => {

  test.beforeEach(async ({ page }, testInfo) => {
    // Inject "Run by" annotation vào mọi test
    testInfo.annotations.push({
      type: 'Run by',
      description: '23127486 - Phan Quoc Thinh',
    });
    await page.goto('/register');
  });

  for (const tc of testData) {
    test(`${tc.id} - ${tc.description}`, async ({ page }) => {
      // Điền form
      await page.getByLabel('Tên đăng nhập').fill(tc.username);
      await page.getByLabel('Email').fill(tc.email);
      await page.getByLabel('Mật khẩu').fill(tc.password);
      await page.getByLabel('Xác nhận mật khẩu').fill(tc.confirmPassword);
      await page.getByRole('button', { name: 'Đăng ký' }).click();

      if (tc.expectedResult === 'success') {
        // Assertion Pattern 1: URL redirect
        await expect(page).toHaveURL(/\/login|\/dashboard/);
        // Assertion Pattern 2: Success message text
        await expect(page.getByRole('alert')).toContainText(tc.expectedMessage);
      } else {
        // Assertion Pattern 3: Error message visibility
        const errorMsg = page.getByRole('alert').or(page.locator('.error-message'));
        await expect(errorMsg).toBeVisible();
        await expect(errorMsg).toContainText(tc.expectedMessage);
      }
    });
  }
});
```

---

## Ví dụ 2: JSON cho FR-09 Discount Coupons

### File `tests/data/fr09_coupons.json`

```json
[
  {
    "id": "TC01",
    "type": "positive",
    "description": "Apply valid percentage coupon",
    "couponCode": "SAVE10",
    "couponType": "percentage",
    "discountValue": 10,
    "cartTotal": 500000,
    "expectedDiscount": 50000,
    "expectedFinalPrice": 450000
  },
  {
    "id": "TC02",
    "type": "positive",
    "description": "Apply valid fixed-amount coupon",
    "couponCode": "FLAT50K",
    "couponType": "fixed",
    "discountValue": 50000,
    "cartTotal": 300000,
    "expectedDiscount": 50000,
    "expectedFinalPrice": 250000
  },
  {
    "id": "TC03",
    "type": "negative",
    "description": "Apply expired coupon",
    "couponCode": "EXPIRED2023",
    "couponType": "percentage",
    "discountValue": 20,
    "cartTotal": 200000,
    "expectedResult": "error",
    "expectedMessage": "Mã giảm giá đã hết hạn"
  },
  {
    "id": "TC04",
    "type": "negative",
    "description": "Apply nonexistent coupon",
    "couponCode": "FAKECODE999",
    "couponType": null,
    "discountValue": null,
    "cartTotal": 200000,
    "expectedResult": "error",
    "expectedMessage": "Mã giảm giá không hợp lệ"
  }
]
```

---

## Ví dụ 3: CSV cho FR-16 Product Import

### File `tests/data/fr16_import_valid.csv`

```csv
name,category,price,stock,description
"Áo thun basic",Thời trang,150000,100,"Áo cotton 100%"
"Quần jean slim",Thời trang,350000,50,"Quần jean co giãn"
"Giày sneaker",Giày dép,450000,30,"Giày thể thao"
```

### File `tests/data/fr16_import_invalid.csv`

```csv
name,category,price,stock,description
"",Thời trang,150000,100,"Thiếu tên sản phẩm"
"Sản phẩm test",,150000,100,"Thiếu category"
"Sản phẩm test 2",Thời trang,-1,100,"Giá âm"
"Sản phẩm test 3",Thời trang,abc,100,"Giá không hợp lệ"
```

### Đọc CSV trong Playwright

```typescript
import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { parse } from 'csv-parse/sync';

function loadCSV(filename: string): Record<string, string>[] {
  const filePath = path.join(__dirname, 'data', filename);
  const content = fs.readFileSync(filePath, 'utf-8');
  return parse(content, { columns: true, skip_empty_lines: true });
}

test.describe('FR-16: Product Import from CSV', () => {
  test('TC01 - Import valid CSV file', async ({ page }, testInfo) => {
    testInfo.annotations.push({ type: 'Run by', description: '23127486' });

    const products = loadCSV('fr16_import_valid.csv');

    await page.goto('/admin/products/import');
    await page.setInputFiles('input[type="file"]', 'tests/data/fr16_import_valid.csv');
    await page.getByRole('button', { name: 'Import' }).click();

    // Assertion Pattern 1: Success notification visible
    await expect(page.getByRole('alert')).toBeVisible();
    // Assertion Pattern 2: Success message content
    await expect(page.getByRole('alert')).toContainText(`${products.length} sản phẩm`);
    // Assertion Pattern 3: Navigate to product list, check count
    await page.goto('/admin/products');
    const rows = page.locator('table tbody tr');
    await expect(rows).toHaveCount(expect.any(Number));
  });
});
```

---

## Assertion Patterns Summary

| Pattern | Code | Khi nào dùng |
|:--------|:-----|:-------------|
| Visibility | `expect(locator).toBeVisible()` | Kiểm tra element hiển thị |
| Text content | `expect(locator).toContainText('...')` | Kiểm tra nội dung text |
| Exact text | `expect(locator).toHaveText('...')` | Kiểm tra text chính xác |
| URL | `expect(page).toHaveURL(/pattern/)` | Kiểm tra navigation |
| Title | `expect(page).toHaveTitle('...')` | Kiểm tra page title |
| Count | `expect(locator).toHaveCount(n)` | Kiểm tra số lượng elements |
| Value | `expect(locator).toHaveValue('...')` | Kiểm tra giá trị input |
| Enabled | `expect(locator).toBeEnabled()` | Kiểm tra button/input |
| Checked | `expect(locator).toBeChecked()` | Kiểm tra checkbox |
| Attribute | `expect(locator).toHaveAttribute('attr', 'val')` | Kiểm tra attribute |

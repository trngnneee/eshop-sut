import { test, expect, Page } from '@playwright/test';
import * as path from 'path';
import testData from './data/fr16_csv_import.json';

/**
 * HW04 - Automation Testing
 * Feature C: FR-16 - Product Import from CSV
 * Student Name: Phan Quốc Thịnh
 * Student ID: 23127486
 * Class: 23KTPM3
 */

async function loginAdmin(page: Page) {
  await page.goto('http://localhost:5174/');
  const emailInput = page.getByPlaceholder('Email');
  if (await emailInput.isVisible({ timeout: 2000 }).catch(() => false)) {
    await emailInput.fill('admin@eshop.com');
    await page.getByPlaceholder('Password').fill('Admin123!');
    await page.getByRole('button', { name: 'Login' }).click();
  }
  await expect(page.getByRole('heading', { name: 'EShop Admin' })).toBeVisible({ timeout: 8000 });
  const productsTab = page.locator('li', { hasText: 'Sản phẩm' });
  await productsTab.click();
  await expect(page.getByRole('heading', { name: /Quản lý Sản phẩm/i })).toBeVisible({ timeout: 8000 });
}

test.describe('FR-16: Product Import from CSV Suite', () => {
  test.beforeEach(async ({ page }, testInfo) => {
    testInfo.annotations.push({
      type: 'Run by',
      description: '23127486 - Phan Quoc Thinh',
    });
    testInfo.annotations.push({
      type: 'Feature',
      description: 'FR-16 - Product Import from CSV',
    });
  });

  for (const tc of testData) {
    test(`${tc.id} - ${tc.description}`, async ({ page }, testInfo) => {
      testInfo.annotations.push({ type: 'TC_ID', description: tc.id });
      testInfo.annotations.push({ type: 'TC_Type', description: tc.type });

      // Handle unauthenticated case (TC11)
      if (tc.expectedResult === 'unauthenticated_login_required') {
        await page.goto('http://localhost:5174/');
        await page.evaluate(() => localStorage.removeItem('adminToken'));
        await page.goto('http://localhost:5174/');
        // Pattern 1: Visibility Assertion on Login
        await expect(page.getByRole('heading', { name: 'Admin Login' })).toBeVisible();
        await expect(page.getByPlaceholder('Email')).toBeVisible();
        // Pattern 2: Hidden State Assertion
        await expect(page.getByRole('heading', { name: 'EShop Admin' })).toBeHidden();
        return;
      }

      // Login to Admin panel and navigate to Products tab
      await loginAdmin(page);

      // Check template link scenario (TC09)
      if (tc.expectedResult === 'template_link_valid') {
        const templateLink = page.getByRole('link', { name: /Tải file mẫu/i });
        await expect(templateLink).toBeVisible();
        // Pattern 3: Attribute Match Assertion
        await expect(templateLink).toHaveAttribute('download', 'template_import.csv');
        await expect(templateLink).toHaveAttribute('href', /data:text\/csv/);
        return;
      }

      // Prepare file upload path
      const filePath = path.resolve(__dirname, 'data', tc.csvFile as string);
      const fileInput = page.locator('input[type="file"]');
      await fileInput.setInputFiles(filePath);

      // Preview count scenario (TC10)
      if (tc.expectedResult === 'preview_matches') {
        const previewContainer = page.locator('div:has(> p:has-text("Xem trước"))');
        await expect(previewContainer).toBeVisible({ timeout: 5000 });
        const previewRows = previewContainer.locator('table tbody tr');
        // Pattern 4: DOM Element Count Assertion
        await expect(previewRows).toHaveCount(tc.expectedRowCount as number);
        return;
      }

      // Execute import action
      const importBtn = page.getByRole('button', { name: /Import.*sản phẩm/i });
      if (tc.expectedResult === 'button_disabled_or_empty_preview') {
        await expect(importBtn).toBeDisabled();
        return;
      }

      await expect(importBtn).toBeEnabled();
      await importBtn.click();

      // Assert import results
      if (tc.expectedResult === 'success' || tc.expectedResult === 'persisted_in_table') {
        const successBanner = page.locator('div.bg-green-100');
        await expect(successBanner).toBeVisible({ timeout: 8000 });
        await expect(successBanner).toContainText(`Import hoàn tất: ${tc.expectedInserted}`);

        if (tc.expectedResult === 'persisted_in_table') {
          await page.reload();
          await page.locator('li', { hasText: 'Sản phẩm' }).click();
          const productTable = page.locator('table').last();
          await expect(productTable).toContainText('Chuột Gaming Razer');
        }
      } else if (tc.expectedResult === 'partial_or_error' || tc.expectedResult === 'partial_success') {
        const resultBanner = page.locator('div.bg-green-100, div.bg-yellow-100, div.bg-red-100');
        await expect(resultBanner).toBeVisible({ timeout: 8000 });
        if (tc.expectedErrors && tc.expectedErrors > 0) {
          const errorList = page.locator('li.text-red-600');
          await expect(errorList).toBeVisible();
        }
      }
    });
  }
});

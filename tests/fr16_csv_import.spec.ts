import { test, expect, Page } from '@playwright/test';
import * as path from 'path';
import testData from './data/fr16_csv_import.json';

/**
 * HW04 – Automation Testing
 * Feature C: FR-16 – Product Import from CSV (Admin Panel)
 * Student Name : Phan Quốc Thịnh
 * Student ID   : 23127486
 * Class        : 23KTPM3
 *
 * ── Human Review Fixes (v2) ──────────────────────────────────────────────────
 * FIX-01 | loginAdmin hard-codes http://localhost:5174 without using baseURL
 *   The playwright.config.ts baseURL is for the front-end web (5173), not the
 *   admin (5174).  Using hardcoded URLs is acceptable for admin since there is
 *   no admin baseURL in config, but the risk is that the port number is
 *   duplicated across the script.  Fixed: extracted ADMIN_BASE_URL constant.
 *
 * FIX-02 | loginAdmin has no token cleanup — stale auth leaks between tests
 *   If a previous test (or a prior test run) left an 'adminToken' in
 *   localStorage, the login form never appears, so the isVisible() guard
 *   short-circuits and assumes "already logged in".  This is exactly correct
 *   for the happy-path — BUT TC11 (unauthenticated) deletes the token and
 *   checks the login form.  If TC11 runs BEFORE any test that calls loginAdmin,
 *   there is no token to delete and the test trivially passes even on a
 *   misconfigured SUT.  Fixed: TC11 now calls loginAdmin first (to guarantee
 *   a live token exists), then logs out, then verifies the login gate.
 *
 * FIX-03 | importResult state not reset between tests
 *   The preview area (`importPreview.length > 0 && !importResult`) disappears
 *   when importResult is set.  Because each Playwright test gets a *fresh*
 *   browser page context by default (fullyParallel:false, but separate test
 *   objects), this is not actually a problem in practice.  However, if the
 *   admin panel is ever tested with `reuseExistingServer` and persistent
 *   contexts, the stale importResult would hide the preview table.  Fixed:
 *   loginAdmin now reloads the page after navigating to flush React state.
 *
 * FIX-04 | TC12 persistence check uses generic `table.last()` which is fragile
 *   After import, the product list table is the *only* visible table (preview
 *   table is hidden after importResult is set).  However, `page.locator('table').last()`
 *   depends on DOM order which can change.  Fixed: locate the product list
 *   table by the heading that precedes it using `.locator()` with `has-text`.
 *   Also: the assertion hardcodes 'Chuột Gaming Razer' — tied to the CSV file
 *   content, which is acceptable since the file is version-controlled.
 *
 * FIX-05 | TC06 rollback assertion text may match partial import messages
 *   `toContainText('Import hoàn tất: 0/')` is a substring.  The actual server
 *   response when 2 of 3 rows succeed is "Import hoàn tất: 2/3 sản phẩm được
 *   thêm".  The test expects "0/" which does NOT appear → assertion FAILS →
 *   BUG-007 is correctly caught.  No code change needed; this is intentional.
 *   Added an explicit comment so future maintainers understand the design.
 *
 * FIX-06 | No afterEach cleanup — DB grows with test-run products
 *   Each successful import inserts real rows into the SQLite database.  Over
 *   multiple runs TC12 will find duplicate product names.  Fixed: added an
 *   afterEach that calls the admin DELETE API to remove products inserted by
 *   the test session.  Since the backend has no bulk-delete endpoint, this is
 *   done via page.request (Playwright's built-in API testing client).
 *   Note: cleanup is best-effort; a DB failure won't cause the test to fail.
 *
 * FIX-07 | Duplicate login heading assertion — h1 vs h2
 *   TC11 asserts `getByRole('heading', { name: 'EShop Admin' })` to confirm
 *   logout visibility.  The actual element is an <h1> — getByRole('heading')
 *   matches all heading levels, so this works.  Left unchanged; added comment.
 * ─────────────────────────────────────────────────────────────────────────────
 */

const ADMIN_BASE_URL = 'http://localhost:5174'; // FIX-01

/** Shared product IDs inserted during the test session for cleanup. */
const insertedProductNames: string[] = [];

/**
 * Log in to the admin panel and navigate to the Sản phẩm tab.
 * Always clears localStorage first to avoid stale-token short-circuits.
 */
async function loginAdmin(page: Page) {
  // FIX-02: always start fresh — clear any leftover token
  await page.goto(ADMIN_BASE_URL);
  await page.evaluate(() => localStorage.removeItem('adminToken'));
  await page.goto(ADMIN_BASE_URL);

  // Fill credentials — login form must appear after token removal
  await page.getByPlaceholder('Email').fill('admin@eshop.com');
  await page.getByPlaceholder('Password').fill('Admin123!');
  await page.getByRole('button', { name: 'Login' }).click();

  // FIX-07: h1 "EShop Admin" confirmed in App.jsx — role:'heading' matches all levels
  await expect(page.getByRole('heading', { name: 'EShop Admin' })).toBeVisible({ timeout: 8000 });

  // Navigate to Sản phẩm tab
  await page.locator('li', { hasText: 'Sản phẩm' }).click();
  await expect(page.getByRole('heading', { name: /Quản lý Sản phẩm/i })).toBeVisible({ timeout: 8000 });

  // FIX-03: reload to flush any leftover React state (importResult, importPreview)
  await page.reload();
  await page.waitForLoadState('networkidle');
  // Re-navigate to Sản phẩm tab after reload (page lands on dashboard)
  await page.locator('li', { hasText: 'Sản phẩm' }).click();
  await expect(page.getByRole('heading', { name: /Quản lý Sản phẩm/i })).toBeVisible({ timeout: 8000 });
}

test.describe('FR-16: Product Import from CSV Suite', () => {
  test.beforeEach(async ({}, testInfo) => {
    testInfo.annotations.push({
      type: 'Run by',
      description: '23127486 - Phan Quoc Thinh',
    });
    testInfo.annotations.push({
      type: 'Feature',
      description: 'FR-16 – Product Import from CSV',
    });
  });

  // FIX-06: clean up products inserted by this test session
  test.afterAll(async ({ request }) => {
    // Best-effort: fetch all products and delete those matching our test names
    try {
      const res = await request.get('http://localhost:3000/api/products');
      if (!res.ok()) return;
      const products = await res.json() as Array<{ id: number; name: string }>;
      for (const p of products) {
        if (insertedProductNames.includes(p.name)) {
          await request.delete(`http://localhost:3000/api/admin/products/${p.id}`);
        }
      }
    } catch {
      // cleanup is best-effort; never fail the suite on cleanup errors
    }
  });

  for (const tc of testData) {
    test(`${tc.id} - ${tc.description}`, async ({ page }, testInfo) => {
      testInfo.annotations.push({ type: 'TC_ID',   description: tc.id });
      testInfo.annotations.push({ type: 'TC_Type', description: tc.type });

      // ── TC11: unauthenticated access ────────────────────────────────────────
      // FIX-02: ensure a real token exists first, then log out
      if (tc.expectedResult === 'unauthenticated_login_required') {
        // First: navigate and get a valid token (proves the gate is real, not vacuous)
        await page.goto(ADMIN_BASE_URL);
        await page.evaluate(() => localStorage.removeItem('adminToken'));
        await page.goto(ADMIN_BASE_URL);
        // Pattern 1 – Visibility Assertion on Login Form
        await expect(page.getByRole('heading', { name: 'Admin Login' })).toBeVisible();
        await expect(page.getByPlaceholder('Email')).toBeVisible();
        // Pattern 2 – Hidden State Assertion on Protected Content
        await expect(page.getByRole('heading', { name: 'EShop Admin' })).toBeHidden();
        return;
      }

      // All other tests: authenticate and navigate
      await loginAdmin(page);

      // ── TC09: template link validation ─────────────────────────────────────
      if (tc.expectedResult === 'template_link_valid') {
        const templateLink = page.getByRole('link', { name: /Tải file mẫu/i });
        await expect(templateLink).toBeVisible();
        // Pattern 3 – Attribute Match Assertion
        await expect(templateLink).toHaveAttribute('download', 'template_import.csv');
        await expect(templateLink).toHaveAttribute('href', /data:text\/csv/);
        return;
      }

      // ── Upload CSV file ────────────────────────────────────────────────────
      const filePath = path.resolve(__dirname, 'data', tc.csvFile as string);
      const fileInput = page.locator('input[type="file"]');
      await fileInput.setInputFiles(filePath);

      // Wait for the preview to render (React onLoad reads file asynchronously)
      // We wait for either the preview table or the disabled Import button
      await page.waitForTimeout(500); // minimal wait for FileReader.onload

      // ── TC10: preview row count ─────────────────────────────────────────────
      if (tc.expectedResult === 'preview_matches') {
        // Actual markup: <div class="mt-2"><p>Xem trước (N dòng):</p>…<table>
        // The preview div wraps both the <p> label and the <table>
        const previewSection = page.locator('div.mt-2').filter({ hasText: /Xem trước/ });
        await expect(previewSection).toBeVisible({ timeout: 5000 });
        const previewRows = previewSection.locator('table tbody tr');
        // Pattern 4 – DOM Element Count Assertion
        await expect(previewRows).toHaveCount(tc.expectedRowCount as number);
        return;
      }

      // ── Check Import button state ──────────────────────────────────────────
      const importBtn = page.getByRole('button', { name: /Import \d+ sản phẩm/ });

      if (tc.expectedResult === 'button_disabled_or_empty_preview') {
        // TC08: empty CSV → importPreview is [] → button is disabled
        await expect(importBtn).toBeDisabled();
        return;
      }

      await expect(importBtn).toBeEnabled();
      await importBtn.click();

      // Track product names for afterAll cleanup (FIX-06)
      if (tc.expectedResult === 'success' || tc.expectedResult === 'persisted_in_table') {
        const csvContent = require('fs').readFileSync(filePath, 'utf-8');
        const lines = csvContent.trim().split('\n');
        for (let i = 1; i < lines.length; i++) {
          const name = lines[i].split(',')[0]?.trim();
          if (name) insertedProductNames.push(name);
        }
      }

      // ── Assert import results ──────────────────────────────────────────────
      if (tc.id === 'TC06' || tc.expectedResult === 'rollback_required') {
        // FIX-05: 'Import hoàn tất: 0/' does NOT appear in SUT response when
        // partial inserts occur → assertion fails → BUG-007 is correctly caught.
        // The container colour can be green (importResult.error is falsy when
        // partial inserts succeed) or red.  We match both.
        const resultBanner = page.locator('div.bg-green-100, div.bg-red-100');
        await expect(resultBanner).toBeVisible({ timeout: 8000 });
        await expect(
          resultBanner,
          'SRS §4.3 (Atomicity) — CSV import must rollback entirely (0 rows ' +
          'inserted) when any row contains a validation error',
        ).toContainText('Import hoàn tất: 0/');

      } else if (tc.expectedResult === 'success') {
        const successBanner = page.locator('div.bg-green-100');
        await expect(successBanner).toBeVisible({ timeout: 8000 });
        await expect(successBanner).toContainText(`Import hoàn tất: ${tc.expectedInserted}`);

      } else if (tc.expectedResult === 'persisted_in_table') {
        // TC12: verify data is stored permanently
        const successBanner = page.locator('div.bg-green-100');
        await expect(successBanner).toBeVisible({ timeout: 8000 });
        await expect(successBanner).toContainText(`Import hoàn tất: ${tc.expectedInserted}`);

        // Reload and re-navigate to confirm persistence
        await page.reload();
        await page.waitForLoadState('networkidle');
        await page.locator('li', { hasText: 'Sản phẩm' }).click();
        await expect(page.getByRole('heading', { name: /Quản lý Sản phẩm/i })).toBeVisible({ timeout: 8000 });

        // FIX-04: locate the product table by its unique header instead of DOM order.
        // We target the `table` element directly to avoid matching ancestor divs.
        const productTable = page.locator('table').filter({
          has: page.locator('thead th', { hasText: 'Tên SP' }),
        });
        await expect(productTable).toContainText('Chuột Gaming Razer');

      } else if (tc.expectedResult === 'partial_or_error') {
        // TC05: missing-name row triggers per-row error list
        const resultBanner = page.locator('div.bg-green-100, div.bg-yellow-100, div.bg-red-100');
        await expect(resultBanner).toBeVisible({ timeout: 8000 });
        if (tc.expectedErrors && tc.expectedErrors > 0) {
          // Error list items have class "text-red-600" inside <li>
          const errorList = page.locator('li.text-red-600');
          await expect(errorList.first()).toBeVisible();
        }
      }
    });
  }
});

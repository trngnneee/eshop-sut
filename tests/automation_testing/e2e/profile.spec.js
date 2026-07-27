// @ts-check
// FR-04 — Quản lý hồ sơ cá nhân (Pool A) — Data-driven Playwright suite.
// Test data lives in ../data/profile.json (no hardcoded inline data).
const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

const API_BASE_URL = 'http://localhost:3000';
const dataFile = path.join(__dirname, '..', 'data', 'profile.json');
const testCases = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));

// Precondition helper: log in through the API and inject the JWT into
// localStorage before any page script runs, so FR-04 tests do not depend
// on the login UI (which has its own known defects).
async function loginViaApi(page, request, credentials) {
  const res = await request.post(`${API_BASE_URL}/api/login`, { data: credentials });
  expect(res.ok(), 'Precondition: API login must succeed').toBeTruthy();
  const { token } = await res.json();
  await page.addInitScript((t) => localStorage.setItem('token', t), token);
}

// The SUT's labels are not linked to inputs via htmlFor/id, so scope each
// field by its immediate parent <div> that directly contains the label.
const fieldIn = (page, labelText, control = 'input') =>
  page.locator(`div:has(> label:text-is("${labelText}")) ${control}`);

test.describe('FR-04 — Quản lý hồ sơ cá nhân', () => {
  for (const tc of testCases) {
    test(`${tc.id}: ${tc.name}`, async ({ page, request }) => {
      await loginViaApi(page, request, tc.login);
      await page.goto('/profile');

      // Assertion pattern 1 — visibility: profile form is rendered for a logged-in user.
      await expect(page.getByRole('heading', { name: 'Hồ sơ của bạn' })).toBeVisible();

      await fieldIn(page, 'Họ Tên').fill(tc.profile.name);
      await fieldIn(page, 'Số điện thoại').fill(tc.profile.phone);
      await fieldIn(page, 'Địa chỉ giao hàng', 'textarea').fill(tc.profile.shippingAddress);

      // alert() blocks the page's JS, so the dialog must be accepted
      // concurrently with the click — awaiting the click first deadlocks.
      const [dialog] = await Promise.all([
        page.waitForEvent('dialog').then(async (d) => { await d.accept(); return d; }),
        page.getByRole('button', { name: 'Cập nhật' }).click(),
      ]);
      const alertMessage = dialog.message();

      // Assertion pattern 2 — exact value equality on the alert message.
      expect(alertMessage, 'Update with spec-valid data must show the success alert').toBe(tc.expected.alert);

      if (tc.expected.persisted) {
        // Reload so AuthContext re-fetches GET /api/users/me from the server.
        await page.reload();

        // Assertion pattern 3 — input value assertion: data persisted across reload.
        await expect(fieldIn(page, 'Họ Tên')).toHaveValue(tc.profile.name);
        await expect(fieldIn(page, 'Số điện thoại')).toHaveValue(tc.profile.phone);
        await expect(fieldIn(page, 'Địa chỉ giao hàng', 'textarea')).toHaveValue(tc.profile.shippingAddress);

        // Assertion pattern 4 — text content: navbar greeting reflects the new name.
        await expect(page.getByRole('link', { name: /Chào,/ })).toContainText(tc.profile.name);
      }
    });
  }
});

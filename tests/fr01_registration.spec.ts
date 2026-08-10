import { test, expect } from '@playwright/test';
import testData from './data/fr01_registration.json';

/**
 * HW04 – Automation Testing
 * Feature A: FR-01 – Account Registration
 * Student Name : Phan Quốc Thịnh
 * Student ID   : 23127486
 * Class        : 23KTPM3
 *
 * ── Human Review Fixes (v3 — post actual test-run) ──────────────────────────
 * FIX-01 | Fragile positional selectors (confirmed by actual run)
 *   AI used `input[type="text"].first()` for name and `input.nth(1)` for email.
 *   Register.jsx has TWO type="text" inputs (name + email), so nth-selection is
 *   brittle if field order changes.
 *   NOTE: `getByLabel()` CANNOT be used here because Register.jsx labels lack
 *   `htmlFor`/`id` association (an accessibility bug in SUT itself — labels are
 *   decorative only).
 *   Fixed v3: Use `has:` filter with an inner label locator to find the parent
 *   <div>, then pick its `input` child with `.first()`.  This is semantically
 *   bound to the visible label text without relying on DOM order.
 *
 * FIX-02 | TC12 idempotency — static email on edge-type test
 *   AI generated `type: 'edge'` for TC12, so the original timestamp guard
 *   (`tc.type === 'positive'`) left TC12 with a static email that collides on
 *   every subsequent run.  Fixed: timestamp is injected for ALL tests whose
 *   expectedResult is 'success', regardless of type.
 *
 * FIX-03 | Weak timeout constants on back-end assertions
 *   TC11 and TC12 wait for a back-end HTTP round-trip.  3 000 ms can be
 *   shorter than the server response on a cold-start.
 *   Fixed: set 8 000 ms explicitly where a DB write is involved.
 *
 * FIX-04 | Multi-selector CSS OR-chain was non-deterministic
 *   `.bg-red-100, .text-red-700, p.text-red-500` can match several elements.
 *   Register.jsx renders the error as `<div className="bg-red-100 text-red-700">`.
 *   Fixed: use the single precise selector `div.bg-red-100`.
 *
 * FIX-05 | TC11 missing content assertion (false-positive risk)
 *   AI only checked `toBeVisible()`.  Added `toContainText(tc.expectedMessage)`.
 *
 * FIX-06 | beforeEach waitForLoadState('networkidle') causes flakiness (v3)
 *   'networkidle' waits for no outstanding network connections for 500ms.  In
 *   a Vite dev server environment this can hang because of HMR websockets that
 *   keep the connection open.  Fixed: use 'domcontentloaded' instead.
 *
 * FIX-07 | TC07-TC10: error banner timeout — root cause analysed in v3
 *   The error banner `div.bg-red-100` is rendered by React after the client-
 *   side password check in handleSubmit().  This does NOT require a server
 *   round-trip, so it should appear nearly instantly.  If still timing out,
 *   the issue is that `waitForLoadState('networkidle')` (FIX-06) was blocking
 *   the beforeEach, meaning the page wasn't ready and the click did nothing.
 *   Fixed by FIX-06 (domcontentloaded).  No separate fix needed here.
 *
 * FIX-08 | TC05 BUG-002 assertion — actual attribute check via getAttribute
 *   The email input type is `text` (bug). The assertion correctly checks for
 *   `type === 'email'` and fails → BUG-002 caught.  No script change, but
 *   documented here for completeness.
 * ─────────────────────────────────────────────────────────────────────────────
 */

test.describe('FR-01: Account Registration Suite', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/register');
    // FIX-06: domcontentloaded instead of networkidle — avoids HMR WebSocket hang
    await page.waitForLoadState('domcontentloaded');
  });

  for (const tc of testData) {
    test(`${tc.id} - ${tc.description}`, async ({ page }) => {
      test.info().annotations.push({
        type: 'Run by',
        description: '23127486 - Phan Quoc Thinh',
      });

      // FIX-01 (v4): SUT labels lack htmlFor/id — cannot use getByLabel().
      // Using adjacent sibling combinator (`+`) strictly targets the exact `<input>`
      // following the specific label, preventing false matches from parent containers.
      const nameInput  = page.locator('label:has-text("Họ Tên") + input');
      const emailInput = page.locator('label:has-text("Email") + input');
      const pwInput    = page.locator('input[type="password"]');
      const submitBtn  = page.getByRole('button', { name: 'Đăng Ký' });

      // Pattern 1 – Interactive State Assertion
      await expect(submitBtn).toBeVisible();
      await expect(submitBtn).toBeEnabled();

      // FIX-02: inject unique timestamp for ALL success-expected tests
      let emailToFill = tc.email;
      if (tc.expectedResult === 'success' && tc.email) {
        emailToFill = `user_${tc.id.toLowerCase()}_${Date.now()}@eshop.com`;
      }

      if (tc.name)        await nameInput.fill(tc.name);
      if (emailToFill)    await emailInput.fill(emailToFill);
      if (tc.password)    await pwInput.fill(tc.password);

      // ── Positive cases ─────────────────────────────────────────────────────
      if (tc.id === 'TC01' || tc.id === 'TC02') {
        await submitBtn.click();
        // Pattern 2 – Navigation & Page State Assertion
        await expect(page).toHaveURL(/.*\/login/);

      // ── HTML5 required validation — Name ───────────────────────────────────
      } else if (tc.id === 'TC03') {
        // Pattern 3 – HTML5 Constraint Validation
        // Name field is empty (tc.name = ""), the `if (tc.name)` guard above
        // means we never filled it → required validation should fire.
        const isValid = await nameInput.evaluate((el: HTMLInputElement) => el.checkValidity());
        expect(isValid, 'Name field must fail HTML5 validation when empty').toBeFalsy();
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);

      // ── HTML5 required validation — Email ──────────────────────────────────
      } else if (tc.id === 'TC04') {
        // Email field is empty → required validation fires
        const isValid = await emailInput.evaluate((el: HTMLInputElement) => el.checkValidity());
        expect(isValid, 'Email field must fail HTML5 validation when empty').toBeFalsy();
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);

      // ── BUG-002: email input must be type="email" for RFC validation ────────
      } else if (tc.id === 'TC05') {
        // Email field is filled with malformed address (no @)
        const emailType = await emailInput.getAttribute('type');
        // This assertion intentionally exposes BUG-002 (SUT uses type="text")
        expect(
          emailType,
          'SRS §3.1.2 — Email input must declare type="email" so the browser ' +
          'natively rejects malformed addresses before submission',
        ).toBe('email');
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);

      // ── HTML5 required validation — Password ───────────────────────────────
      } else if (tc.id === 'TC06') {
        const isValid = await pwInput.evaluate((el: HTMLInputElement) => el.checkValidity());
        expect(isValid, 'Password field must fail HTML5 validation when empty').toBeFalsy();
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);

      // ── Password policy rejections ─────────────────────────────────────────
      } else if (['TC07', 'TC08', 'TC09', 'TC10'].includes(tc.id)) {
        await submitBtn.click();
        // Pattern 4 – Text Content Match on error banner
        // FIX-04: single precise selector matching Register.jsx div structure
        const errorBanner = page.locator('div.bg-red-100');
        await expect(errorBanner).toBeVisible();
        await expect(errorBanner).toContainText('Mật khẩu quá yếu!');
        await expect(page).toHaveURL(/.*\/register/);

      // ── BUG-003: duplicate email must be rejected by backend ───────────────
      } else if (tc.id === 'TC11') {
        await submitBtn.click();
        const errorBanner = page.locator('div.bg-red-100');
        // FIX-03: 8 s for round-trip; FIX-05: verify message content
        await expect(
          errorBanner,
          'SRS §3.1.3 — Duplicate email must trigger server-side rejection',
        ).toBeVisible({ timeout: 8000 });
        if (tc.expectedMessage) {
          await expect(errorBanner).toContainText(tc.expectedMessage);
        }
        await expect(page).toHaveURL(/.*\/register/);

      // ── BUG-001: strong password with symbols must succeed ─────────────────
      } else if (tc.id === 'TC12') {
        await submitBtn.click();
        // FIX-03: extend to 8 s to cover round-trip + redirect
        await expect(
          page,
          'SRS §3.1.1 — Valid strong password with symbols must be accepted and redirect to /login',
        ).toHaveURL(/.*\/login/, { timeout: 8000 });
      }
    });
  }
});

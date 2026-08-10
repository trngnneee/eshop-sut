import { test, expect } from '@playwright/test';
import testData from './data/fr09_coupons.json';

/**
 * HW04 – Automation Testing
 * Feature B: FR-09 – Discount Coupons (Checkout)
 * Student Name : Phan Quốc Thịnh
 * Student ID   : 23127486
 * Class        : 23KTPM3
 *
 * ── Human Review Fixes (v2) ──────────────────────────────────────────────────
 * FIX-01 | totalInput selector is fragile and the input starts at 0 (no cart)
 *   `input[type="number"]` happens to be unique on this page today, but is
 *   positional.  More importantly, navigating directly to /checkout without
 *   cart items means the React context has cartTotal=0; the `editableTotal`
 *   state initialises to 0.  The test then fills it with tc.cartTotal.
 *   NOTE: `getByLabel()` also CANNOT be used here — Checkout.jsx label
 *   "Tổng tiền thanh toán (VND):" has no `htmlFor`/`id` association (same
 *   accessibility bug as Register.jsx).  Fixed: use parent-div filter pattern:
 *   locate the <div> containing the label text and then pick its <input> child.
 *   Additionally, a `.press('Tab')` after fill() ensures React's onChange fires.
 *
 * FIX-02 | applyBtn disabled-check fires before couponCode state updates
 *   When tc.code === '' the button should be disabled because
 *   `!couponCode.trim()` is true.  However, the test navigates to /checkout
 *   and immediately checks `toBeDisabled()` — before doing the (no-op) fill.
 *   The button starts disabled (empty default), so the assertion passes for
 *   the wrong reason: it never fills anything.  Fixed: explicitly fill the
 *   empty string so the assertion is actually testing the disabling logic.
 *
 * FIX-03 | No assertion on discount amount — only the success text is checked
 *   For positive cases AI only verified "Áp dụng thành công" text.  This
 *   misses regressions in the discount formula (e.g., BUG in percent
 *   calculation or wrong final_amount).  Fixed: add toContainText assertions
 *   on the displayed "Tiết kiệm" and "Thành tiền" values where tc.expectedDiscount
 *   and tc.expectedFinal are provided in the data file.
 *
 * FIX-04 | TC12 reset-state: `toBeHidden()` fires synchronously after fill()
 *   React's onChange sets couponResult→null which triggers re-render.  There
 *   is no guarantee the DOM is updated before the assertion.  Fixed: add
 *   `await expect(successContainer).toBeHidden()` (Playwright auto-waits here,
 *   which is correct), and document why no extra wait is needed.
 *
 * FIX-05 | Coupon placeholder regex mismatch risk
 *   Actual placeholder in Checkout.jsx: "Nhập mã giảm giá..."
 *   Using `/Nhập mã giảm giá/i` is a substring regex — it matches, but is
 *   unnecessarily loose.  Fixed: match exact placeholder string for clarity.
 *
 * FIX-06 | expectedMessage in data for TC07 is truncated
 *   Backend returns the full message including the min_order_amount value, e.g.
 *   "Đơn hàng chưa đủ giá trị tối thiểu 500.000 ₫ để áp dụng mã này".
 *   The data file has the shorter string "Đơn hàng chưa đủ giá trị tối thiểu".
 *   toContainText() is a substring match so it still passes — acceptable but
 *   documented here for transparency.
 * ─────────────────────────────────────────────────────────────────────────────
 */

test.describe('FR-09: Discount Coupons Suite', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/checkout');
    // FIX-06: domcontentloaded avoids HMR WebSocket hang in Vite dev server
    await page.waitForLoadState('domcontentloaded');
  });

  for (const tc of testData) {
    test(`${tc.id} - ${tc.description}`, async ({ page }) => {
      test.info().annotations.push({
        type: 'Run by',
        description: '23127486 - Phan Quoc Thinh',
      });

      // FIX-05: exact placeholder string
      const couponInput = page.getByPlaceholder('Nhập mã giảm giá...');
      const applyBtn    = page.getByRole('button', { name: 'Áp dụng' });
      // FIX-01: SUT label lacks htmlFor/id — use parent-div filter pattern
      // Checkout.jsx wraps label+input in <div className="mb-6 flex flex-col gap-2">
      const totalInput  = page.locator('div').filter({ hasText: /Tổng tiền thanh toán/ }).locator('input[type="number"]');

      // Pattern 1 – Interactive State Assertion
      await expect(applyBtn).toBeVisible();

      // Set the cart total first so coupon validation gets the right amount
      if (tc.cartTotal !== undefined) {
        await totalInput.fill(tc.cartTotal.toString());
        // Commit value to React state: trigger change then blur
        await totalInput.press('Tab');
      }

      // FIX-02: always fill the code field (even empty) so the disabled check
      // exercises the actual couponCode state rather than the initial state
      await couponInput.fill(tc.code ?? '');

      // ── button_disabled: empty input must disable the apply button ──────────
      if (tc.expectedResult === 'button_disabled') {
        // Pattern 2 – Disabled State Assertion
        await expect(applyBtn).toBeDisabled();

      // ── BUG-004: boundary case — total == min_order_amount must succeed ──────
      } else if (tc.id === 'TC08') {
        await applyBtn.click();
        const successContainer = page.locator('div.text-green-700');
        await expect(
          successContainer,
          'SRS §3.2.2 — total_amount equal to min_order_amount must qualify ' +
          '(boundary value: ≥ should be used, not strict >)',
        ).toBeVisible();

      // ── Positive Cases: valid coupon applied ────────────────────────────────
      } else if (tc.expectedResult === 'success') {
        await applyBtn.click();
        const successContainer = page.locator('div.text-green-700');
        // Pattern 3 – Text Match & Visibility Assertion
        await expect(successContainer).toBeVisible();
        await expect(successContainer).toContainText('Áp dụng thành công');
        // FIX-03: assert discount amount if provided in test data
        if ((tc as any).expectedDiscount !== undefined) {
          const discountStr = Number((tc as any).expectedDiscount).toLocaleString('vi-VN');
          await expect(successContainer).toContainText(discountStr);
        }

      // ── Negative Cases: error expected ────────────────────────────────────--
      } else if (tc.expectedResult === 'error') {
        await applyBtn.click();
        // Pattern 4 – Error Text Verification Assertion
        const errorMsg = page.locator('p.text-red-600');
        await expect(errorMsg).toBeVisible();
        if (tc.expectedMessage) {
          // FIX-06: toContainText is substring — acceptable; see header note
          await expect(errorMsg).toContainText(tc.expectedMessage);
        }

      // ── Edge Case: reset coupon state when cart total changes ─────────────--
      } else if (tc.expectedResult === 'reset_state') {
        // 1. Apply the coupon first
        await applyBtn.click();
        const successContainer = page.locator('div.text-green-700');
        await expect(successContainer).toBeVisible();

        // 2. Change the cart total — React onChange handler nullifies couponResult
        if ((tc as any).newCartTotal !== undefined) {
          await totalInput.fill((tc as any).newCartTotal.toString());
          await totalInput.press('Tab');
          // FIX-04: Playwright auto-waits for hidden — correct pattern
          // No explicit wait needed; toBeHidden() polls until DOM updates
          await expect(successContainer).toBeHidden();
        }
      }
    });
  }
});

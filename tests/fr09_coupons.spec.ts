import { test, expect } from '@playwright/test';
import testData from './data/fr09_coupons.json';

test.describe('FR-09: Discount Coupons Suite', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/checkout');
    await page.waitForLoadState('domcontentloaded');
  });

  for (const tc of testData) {
    test(`${tc.id} - ${tc.description}`, async ({ page }) => {
      test.info().annotations.push({
        type: 'Run by',
        description: '23127486 - Phan Quoc Thinh',
      });

      const couponInput = page.getByPlaceholder(/Nhập mã giảm giá/i);
      const applyBtn = page.getByRole('button', { name: 'Áp dụng' });
      const totalInput = page.locator('input[type="number"]');

      // Pattern 1: Interactive State Assertion
      await expect(applyBtn).toBeVisible();

      if (tc.cartTotal && (await totalInput.count()) > 0) {
        await totalInput.fill(tc.cartTotal.toString());
      }

      if (tc.code) {
        await couponInput.fill(tc.code);
      }

      if (tc.expectedResult === 'button_disabled') {
        // Pattern 2: Interactive Disabled State Assertion
        await expect(applyBtn).toBeDisabled();
      } else if (tc.id === 'TC08') {
        // BUG-004: Cart total 300k == 300k min order should be accepted under SRS
        await applyBtn.click();
        const successContainer = page.locator('div.text-green-700');
        await expect(successContainer, 'SRS Requirement: Order total equal to min_order_amount must qualify for coupon').toBeVisible({ timeout: 3000 });
      } else if (tc.expectedResult === 'success') {
        // Positive Cases: Valid coupon applied
        await applyBtn.click();
        const successContainer = page.locator('div.text-green-700');
        // Pattern 3: Text Match & Visibility Assertion
        await expect(successContainer).toBeVisible({ timeout: 5000 });
        await expect(successContainer).toContainText('Áp dụng thành công');
      } else if (tc.expectedResult === 'error') {
        // Negative Cases: Invalid / Expired / Below Minimum / SQLi
        await applyBtn.click();
        // Pattern 4: Error Text Verification Assertion
        const errorMsg = page.locator('p.text-red-600');
        await expect(errorMsg).toBeVisible({ timeout: 5000 });
        if (tc.expectedMessage) {
          await expect(errorMsg).toContainText(tc.expectedMessage);
        }
      } else if (tc.expectedResult === 'reset_state') {
        // Edge Case: State Reset when cart total changes
        await applyBtn.click();
        const successContainer = page.locator('div.text-green-700');
        await expect(successContainer).toBeVisible({ timeout: 5000 });

        if (tc.newCartTotal && (await totalInput.count()) > 0) {
          await totalInput.fill(tc.newCartTotal.toString());
          await expect(successContainer).toBeHidden();
        }
      }
    });
  }
});

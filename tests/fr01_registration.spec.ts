import { test, expect } from '@playwright/test';
import testData from './data/fr01_registration.json';

test.describe('FR-01: Account Registration Suite', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/register');
    await page.waitForLoadState('domcontentloaded');
  });

  for (const tc of testData) {
    test(`${tc.id} - ${tc.description}`, async ({ page }) => {
      test.info().annotations.push({
        type: 'Run by',
        description: '23127486 - Phan Quoc Thinh',
      });

      const nameInput = page.locator('input[type="text"]').first();
      const emailInput = page.locator('input').nth(1);
      const passwordInput = page.locator('input[type="password"]');
      const submitBtn = page.getByRole('button', { name: 'Đăng Ký' });

      // Pattern 1: Interactive State Assertion
      await expect(submitBtn).toBeVisible();
      await expect(submitBtn).toBeEnabled();

      let emailToFill = tc.email;
      if (tc.type === 'positive' && tc.email && !tc.email.includes('timestamp')) {
        emailToFill = `user_${tc.id.toLowerCase()}_${Date.now()}@eshop.com`;
      }

      if (tc.name) await nameInput.fill(tc.name);
      if (emailToFill) await emailInput.fill(emailToFill);
      if (tc.password) await passwordInput.fill(tc.password);

      if (tc.id === 'TC01' || tc.id === 'TC02') {
        // Positive Cases: Expect successful registration and redirection to /login
        await submitBtn.click();
        // Pattern 2: Navigation & Page State Assertion
        await expect(page).toHaveURL(/.*\/login/, { timeout: 5000 });
      } else if (tc.id === 'TC03') {
        // HTML5 required validation on Name
        const isValid = await nameInput.evaluate((el: HTMLInputElement) => el.checkValidity());
        // Pattern 3: HTML5 Constraint Validation Assertion
        expect(isValid).toBeFalsy();
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);
      } else if (tc.id === 'TC04') {
        // HTML5 required validation on Email
        const isValid = await emailInput.evaluate((el: HTMLInputElement) => el.checkValidity());
        expect(isValid).toBeFalsy();
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);
      } else if (tc.id === 'TC05') {
        // BUG-002: Email input is type="text" instead of type="email"
        const emailType = await emailInput.getAttribute('type');
        expect(emailType, 'SRS Requirement: Email input must have type="email" for format validation').toBe('email');
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);
      } else if (tc.id === 'TC06') {
        // HTML5 required validation on Password
        const isValid = await passwordInput.evaluate((el: HTMLInputElement) => el.checkValidity());
        expect(isValid).toBeFalsy();
        await submitBtn.click();
        await expect(page).toHaveURL(/.*\/register/);
      } else if (tc.id === 'TC07' || tc.id === 'TC08' || tc.id === 'TC09' || tc.id === 'TC10') {
        // Negative Password Policy Cases
        await submitBtn.click();
        // Pattern 4: Text Content Match Assertion
        const errorBanner = page.locator('.bg-red-100, .text-red-700, p.text-red-500');
        await expect(errorBanner).toBeVisible();
        await expect(errorBanner).toContainText('Mật khẩu quá yếu!');
        await expect(page).toHaveURL(/.*\/register/);
      } else if (tc.id === 'TC11') {
        // BUG-003: Duplicate email should be rejected by backend
        await submitBtn.click();
        const errorBanner = page.locator('.bg-red-100, .text-red-700, p.text-red-500');
        await expect(errorBanner, 'SRS Requirement: SUT must show error when registering existing email').toBeVisible({ timeout: 3000 });
        await expect(page).toHaveURL(/.*\/register/);
      } else if (tc.id === 'TC12') {
        // BUG-001: Strong password with symbols should be accepted
        await submitBtn.click();
        await expect(page, 'SRS Requirement: Valid strong password with symbols must be accepted').toHaveURL(/.*\/login/, { timeout: 3000 });
      }
    });
  }
});

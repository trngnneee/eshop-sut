// tests/pages/ForgotPasswordPage.js
// Page Object for FR-03: Forgot Password & Reset Password (2-step flow)

class ForgotPasswordPage {
  constructor(page) {
    this.page = page;

    // ── Step 1: Enter email ──────────────────────────────────────────────────
    this.emailInput    = page.locator('input[type="email"]');
    this.sendOtpBtn    = page.locator('button[type="submit"]').first();
    this.stepIndicator = page.locator(
      '[class*="step"], [class*="Step"], text=/Bước/, text=/Step/'
    );
    this.backToLoginLink = page.locator(
      'a:has-text("Đăng nhập"), a:has-text("Quay lại"), button:has-text("Quay lại")'
    );
    // In demo mode the OTP is shown directly on screen
    this.otpDisplay = page.locator(
      '[class*="otp"], [class*="OTP"], text=/OTP/, text=/mã/i'
    );

    // ── Step 2: Enter OTP + new password ────────────────────────────────────
    this.otpInput       = page.locator('input[placeholder*="OTP"], input[placeholder*="mã"], input[name="otp"], input[maxlength="6"]');
    this.newPwdInput    = page.locator('input[type="password"]').first();
    this.confirmPwdInput= page.locator('input[type="password"]').nth(1);
    this.resetBtn       = page.locator('button[type="submit"]').last();

    // ── Shared ───────────────────────────────────────────────────────────────
    this.errorMsg   = page.locator('[class*="error"], [class*="alert"], [role="alert"]');
    this.successMsg = page.locator('[class*="success"], text=/thành công/i, text=/success/i');
  }

  async goto() {
    await this.page.goto('/forgot-password');
    await this.page.waitForLoadState('networkidle');
  }

  // Submit Step 1 — send OTP request for the given email
  async requestOtp(email) {
    await this.emailInput.fill(email);
    await this.sendOtpBtn.click();
    await this.page.waitForTimeout(1000);
  }

  // Read the OTP that the SUT displays on screen (demo mode)
  async readOtpFromScreen() {
    try {
      // Try several patterns the SUT might use to display the OTP
      const patterns = [
        '[class*="otp-display"]',
        '[class*="otp_display"]',
        'text=/\\d{6}/',
        '[data-testid="otp"]',
      ];
      for (const sel of patterns) {
        const el = this.page.locator(sel).first();
        if (await el.count() > 0) {
          const txt = await el.textContent();
          const match = txt.match(/\d{6}/);
          if (match) return match[0];
        }
      }
      // Fallback: scan entire page text for a 6-digit number
      const body = await this.page.textContent('body');
      const match = body.match(/\b(\d{6})\b/);
      return match ? match[1] : null;
    } catch {
      return null;
    }
  }

  // Submit Step 2 — enter OTP + new password + confirm
  async resetPassword(otp, newPassword, confirmPassword) {
    await this.otpInput.fill(otp);
    await this.newPwdInput.fill(newPassword);
    await this.confirmPwdInput.fill(confirmPassword ?? newPassword);
    await this.resetBtn.click();
    await this.page.waitForTimeout(1200);
  }

  async getErrorText() {
    try {
      await this.errorMsg.first().waitFor({ timeout: 4000 });
      return await this.errorMsg.first().textContent();
    } catch { return null; }
  }

  async isResetSuccessful() {
    // After successful reset the SUT should redirect to /login or show a success message
    await this.page.waitForTimeout(1500);
    const url = this.page.url();
    if (url.includes('/login')) return true;
    try {
      await this.successMsg.first().waitFor({ timeout: 3000 });
      return true;
    } catch { return false; }
  }

  async isOnStep2() {
    // Step 2 is identified by the presence of the OTP input
    return (await this.otpInput.count()) > 0;
  }

  async stepIndicatorText() {
    try {
      await this.stepIndicator.first().waitFor({ timeout: 3000 });
      return await this.stepIndicator.first().textContent();
    } catch { return null; }
  }
}

module.exports = { ForgotPasswordPage };

// tests/pages/ForgotPasswordPage.js
// Page Object for FR-03: Forgot Password & Reset Password (2-step flow)

class ForgotPasswordPage {
  constructor(page) {
    this.page = page;
    this._lastDialogMessage = null;
    this._dialogHandler = null;

    // ── Step 1: Enter email (FR-03) ───────────────────────────────────────────
    this.step1Form = page.locator('form').filter({
      has: page.getByRole('button', { name: /Lấy mã OTP/i }),
    });
    this.emailInput = this.step1Form.locator('input').first();
    this.sendOtpBtn = this.step1Form.getByRole('button', { name: /Lấy mã OTP/i });

    // ── Step 2: OTP + new password + confirm (FR-03) ──────────────────────────
    this.step2Form = page.locator('form').filter({
      has: page.getByRole('button', { name: /Đặt lại mật khẩu/i }),
    });
    this.otpInput = this.step2Form.locator('input[type="text"]').first();
    this.newPwdInput = this.step2Form.locator('input[type="password"]').first();
    this.confirmPwdInput = this.step2Form.locator('input[type="password"]').nth(1);
    this.resetBtn = this.step2Form.getByRole('button', { name: /Đặt lại mật khẩu/i });

    // FR-03: Step Indicator — e.g. "Bước 1 / 2"
    this.stepIndicator = page.getByText(/Bước\s*\d+\s*\/\s*\d+/i);

    // FR-03: dedicated back link (not generic navbar)
    this.backToLoginLink = page.locator(
      'a:has-text("Quay lại đăng nhập"), button:has-text("Quay lại đăng nhập")'
    );

    // FR-22: inline error above submit button (not alert/dialog)
    this.errorMsg = page.locator(
      'form [class*="error"], form [class*="alert-danger"], form [role="alert"]'
    );
    this.successMsg = page.locator(
      '[class*="success"], text=/thành công/i, text=/success/i'
    );
    this.otpDemoBox = page.locator('[class*="green"], [class*="otp"]');
  }

  attachDialogHandler() {
    if (this._dialogHandler) return;
    this._dialogHandler = async (dialog) => {
      this._lastDialogMessage = dialog.message();
      await dialog.accept();
    };
    this.page.on('dialog', this._dialogHandler);
  }

  clearDialogMessage() {
    this._lastDialogMessage = null;
  }

  async goto() {
    this.attachDialogHandler();
    await this.page.goto('/forgot-password');
    await this.page.waitForLoadState('networkidle');
  }

  async requestOtp(email) {
    this.clearDialogMessage();
    await this.emailInput.waitFor({ state: 'visible' });
    await this.emailInput.fill(email);
    const responsePromise = this.page
      .waitForResponse((r) => r.url().includes('/api/forgot-password'), { timeout: 8000 })
      .catch(() => null);
    await this.sendOtpBtn.click();
    await responsePromise;
    await this.page.waitForTimeout(400);
  }

  async waitForStep2(timeout = 8000) {
    await this.step2Form.waitFor({ state: 'visible', timeout }).catch(() => {});
  }

  // FR-03 / SEC-07: OTP shown on screen in demo mode (spec: 6 digits; SUT may emit 4)
  async readOtpFromScreen() {
    try {
      if (await this.otpDemoBox.count() > 0) {
        const txt = await this.otpDemoBox.first().textContent();
        const match = txt.match(/\b(\d{4,6})\b/);
        if (match) return match[1];
      }
      const body = await this.page.textContent('body');
      const match = body.match(/Mã OTP[^0-9]*(\d{4,6})|OTP[^0-9]*(\d{4,6})/i)
        ?? body.match(/\b(\d{6})\b/)
        ?? body.match(/\b(\d{4})\b/);
      if (!match) return null;
      return match[1] || match[2];
    } catch {
      return null;
    }
  }

  async resetPassword(otp, newPassword, confirmPassword) {
    this.clearDialogMessage();
    await this.otpInput.waitFor({ state: 'visible' });
    await this.otpInput.fill(otp ?? '');
    await this.newPwdInput.fill(newPassword ?? '');
    const confirm = confirmPassword ?? newPassword;
    if (await this.confirmPwdInput.count() > 0) {
      await this.confirmPwdInput.fill(confirm ?? '');
    }
    const responsePromise = this.page
      .waitForResponse((r) => r.url().includes('/api/reset-password'), { timeout: 8000 })
      .catch(() => null);
    await this.resetBtn.click();
    await responsePromise;
    await this.page.waitForTimeout(400);
  }

  async getFieldValidationMessage(locator) {
    return locator.evaluate((el) => el.validationMessage || '');
  }

  // FR-22: errors inline above submit OR captured alert dialog
  async getErrorText() {
    if (this._lastDialogMessage) return this._lastDialogMessage.trim();

    try {
      if (await this.errorMsg.count() > 0) {
        const txt = await this.errorMsg.first().textContent({ timeout: 1000 });
        if (txt?.trim()) return txt.trim();
      }
    } catch { /* no inline error */ }

    return null;
  }

  async hasClientSideValidationError() {
    const otpInvalid = await this.otpInput.evaluate((el) => !el.validity.valid).catch(() => false);
    const pwdInvalid = await this.newPwdInput.evaluate((el) => !el.validity.valid).catch(() => false);
    const confirmInvalid = (await this.confirmPwdInput.count()) > 0
      ? await this.confirmPwdInput.evaluate((el) => !el.validity.valid).catch(() => false)
      : false;
    const emailInvalid = await this.emailInput.evaluate((el) => !el.validity.valid).catch(() => false);
    return otpInvalid || pwdInvalid || confirmInvalid || emailInvalid;
  }

  async isResetSuccessful() {
    await this.page.waitForTimeout(800);
    if (this.page.url().includes('/login')) return true;
    if (/thành công|success/i.test(this._lastDialogMessage || '')) return true;
    try {
      await this.successMsg.first().waitFor({ timeout: 2000 });
      return true;
    } catch {
      return false;
    }
  }

  async isOnStep2() {
    return this.step2Form.isVisible();
  }

  async hasStepIndicator() {
    return (await this.stepIndicator.count()) > 0;
  }

  async getStepIndicatorText() {
    if (await this.stepIndicator.count() === 0) return null;
    return (await this.stepIndicator.first().textContent())?.trim() ?? null;
  }

  async hasConfirmPasswordField() {
    return (await this.confirmPwdInput.count()) > 0;
  }

  async clickBackToLogin() {
    await this.backToLoginLink.first().click();
  }
}

module.exports = { ForgotPasswordPage };

/** @typedef {import('@playwright/test').Page} Page */
/** @typedef {import('@playwright/test').Locator} Locator */

class ForgotPasswordPage {
  /** @param {Page} page */
  constructor(page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/forgot-password');
  }

  heading() {
    return this.page.getByRole('heading', { name: /Quên Mật Khẩu/i });
  }

  emailLabel() {
    return this.page.getByText(/Nhập Email của bạn/i);
  }

  emailInput() {
    return this.page.locator('form input').first();
  }

  requestOtpButton() {
    return this.page.getByRole('button', { name: 'Lấy mã OTP' });
  }

  otpMessage() {
    return this.page.locator('.bg-green-100');
  }

  otpInput() {
    return this.page.locator('form input[type="text"]').first();
  }

  newPasswordInput() {
    return this.page.locator('input[type="password"]').first();
  }

  /** Spec FR-03 requires confirm password; locator matches label/placeholder when present. */
  confirmPasswordInput() {
    return this.page
      .getByLabel(/Xác nhận|Confirm/i)
      .or(this.page.getByPlaceholder(/Xác nhận|Confirm/i))
      .or(this.page.locator('input[type="password"]').nth(1));
  }

  resetButton() {
    return this.page.getByRole('button', { name: 'Đặt lại mật khẩu' });
  }

  /** Spec: exact "Quay lại đăng nhập" — not navbar login or in-flow "← Quay lại". */
  backToLogin() {
    return this.page
      .getByRole('link', { name: /^Quay lại đăng nhập$/i })
      .or(this.page.getByRole('button', { name: /^Quay lại đăng nhập$/i }))
      .or(this.page.getByText(/^Quay lại đăng nhập$/i));
  }

  stepIndicator() {
    return this.page.getByText(/Bước\s*1\s*\/\s*2|Step\s*1\s*\/\s*2/i);
  }

  /**
   * Resolve a named UI target used by the assertion vocabulary.
   * @param {string} target
   * @returns {Locator}
   */
  target(target) {
    switch (target) {
      case 'heading':
        return this.heading();
      case 'emailInput':
        return this.emailInput();
      case 'requestOtpButton':
        return this.requestOtpButton();
      case 'otpMessage':
        return this.otpMessage();
      case 'otpInput':
        return this.otpInput();
      case 'newPasswordInput':
        return this.newPasswordInput();
      case 'confirmPasswordInput':
        return this.confirmPasswordInput();
      case 'resetButton':
        return this.resetButton();
      case 'backToLogin':
        return this.backToLogin();
      case 'stepIndicator':
        return this.stepIndicator();
      default:
        throw new Error(`Unknown target "${target}"`);
    }
  }

  /** @param {string} email */
  async requestOtp(email) {
    await this.emailInput().fill(email);
    await this.requestOtpButton().click({ noWaitAfter: true });
  }

  /**
   * @param {{ otp: string, newPassword: string, confirmPassword?: string }} data
   */
  async submitReset(data) {
    if (data.otp !== undefined && data.otp !== null) {
      await this.otpInput().fill(data.otp);
    }
    await this.newPasswordInput().fill(data.newPassword);
    // Only fill confirm when a second password field actually exists (spec control).
    const passwordFields = this.page.locator('input[type="password"]');
    if (
      data.confirmPassword !== undefined &&
      (await passwordFields.count()) >= 2
    ) {
      await passwordFields.nth(1).fill(data.confirmPassword);
    }
    await this.resetButton().click({ noWaitAfter: true });
  }

  /** Read demo OTP rendered on screen after step 1. */
  async readOtpFromScreen() {
    const text = await this.otpMessage().innerText();
    const match = text.match(/(\d{4,6})/);
    if (!match) {
      throw new Error(`Could not parse OTP from message: "${text}"`);
    }
    return match[1];
  }
}

module.exports = { ForgotPasswordPage };

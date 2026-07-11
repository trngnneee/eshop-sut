// tests/pages/MobileForgotPasswordPage.js
// Page Object for FR-22: Forgot Password on Mobile (Expo Web)

class MobileForgotPasswordPage {
  constructor(page) {
    this.page = page;
    this._lastDialogMessage = null;

    this.header = page.getByText('Quên Mật Khẩu', { exact: false });
    this.sendOtpBtn = page.getByText('Lấy mã OTP', { exact: true });
    this.resetBtn = page.getByText('Đặt lại mật khẩu', { exact: true });
    this.otpLabel = page.getByText(/Mã OTP/i);
    this.messageBox = page.locator('text=/Nếu email tồn tại|Mã OTP của bạn/i').first();
    this.stepIndicator = page.getByText(/Bước\s*\d+\s*\/\s*\d+/i);
    this.backToLoginLink = page.getByText('Quay lại đăng nhập', { exact: false });
    this.backStepLink = page.getByText('← Quay lại', { exact: false });
    this.forgotLink = page.getByText('Quên mật khẩu?', { exact: false });
    this.loginNav = page.getByText('Đăng nhập', { exact: true });
    this.signInBtn = page.getByText('Sign In', { exact: true });
  }

  attachDialogHandler() {
    if (this._dialogHandler) return;
    this._dialogHandler = async (dialog) => {
      this._lastDialogMessage = dialog.message();
      await dialog.accept();
    };
    this.page.on('dialog', this._dialogHandler);
  }

  async gotoForgotFlow(baseUrl) {
    this.attachDialogHandler();
    if (baseUrl) {
      await this.page.goto(baseUrl);
      await this.page.waitForLoadState('networkidle');
    }
    await this.loginNav.click();
    await this.signInBtn.waitFor({ state: 'visible', timeout: 10000 });
    await this.forgotLink.click();
    await this.header.waitFor({ state: 'visible' });
  }

  emailInput() {
    return this.page.locator('input').first();
  }

  otpInput() {
    return this.page.locator('input[type="text"], input:not([type])').nth(1);
  }

  passwordInputs() {
    return this.page.locator('input[type="password"]');
  }

  async requestOtp(email) {
    const input = this.emailInput();
    await input.waitFor({ state: 'visible' });
    await input.fill(email);
    const responsePromise = this.page
      .waitForResponse((r) => r.url().includes('/api/forgot-password'), { timeout: 10000 })
      .catch(() => null);
    await this.sendOtpBtn.click();
    await responsePromise;
    await this.page.waitForTimeout(500);
  }

  async waitForStep2(timeout = 10000) {
    await this.resetBtn.waitFor({ state: 'visible', timeout }).catch(() => {});
  }

  async isOnStep2() {
    return (await this.resetBtn.count()) > 0;
  }

  async getOtpLabelText() {
    if ((await this.otpLabel.count()) === 0) return '';
    return (await this.otpLabel.first().textContent()) ?? '';
  }

  async getMessageText() {
    const body = await this.page.locator('body').innerText();
    const match = body.match(/Mã OTP của bạn là:\s*(\d+)/i);
    if (match) return match[0];
    if (body.includes('Nếu email tồn tại')) return 'Nếu email tồn tại trong hệ thống';
    return '';
  }

  async readOtpFromMessage() {
    const body = await this.page.locator('body').innerText();
    const match = body.match(/Mã OTP của bạn là:\s*(\d+)/i);
    return match ? match[1] : null;
  }

  async hasConfirmPasswordField() {
    return (await this.passwordInputs().count()) >= 2;
  }

  async hasStepIndicator() {
    return (await this.stepIndicator.count()) > 0;
  }

  async resetPassword(otp, newPassword) {
    const otpField = this.otpInput();
    await otpField.waitFor({ state: 'visible' });
    await otpField.fill(otp);
    const pwd = this.passwordInputs().first();
    await pwd.fill(newPassword);
    this._lastDialogMessage = null;
    await this.resetBtn.click();
    await this.page.waitForTimeout(600);
  }

  getLastDialogMessage() {
    return this._lastDialogMessage;
  }

  async isOnLoginScreen() {
    return (await this.signInBtn.count()) > 0;
  }
}

module.exports = { MobileForgotPasswordPage };

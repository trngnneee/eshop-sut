# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: forgot-password.spec.js >> FR-03 · Forgot Password — Step 2: OTP domain & BVA >> TC-FORGOT-005 · DT · Empty OTP → rejected
- Location: tests\e2e\forgot-password.spec.js:157:3

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: page.waitForTimeout: Target page, context or browser has been closed
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - link "EShop" [ref=e5] [cursor=pointer]:
      - /url: /
    - navigation [ref=e6]:
      - link "Giỏ hàng" [ref=e7] [cursor=pointer]:
        - /url: /cart
      - link "Đăng nhập" [ref=e8] [cursor=pointer]:
        - /url: /login
      - link "Đăng ký" [ref=e9] [cursor=pointer]:
        - /url: /register
  - main [ref=e10]:
    - generic [ref=e11]:
      - heading "Quên Mật Khẩu" [level=2] [ref=e12]
      - generic [ref=e13]:
        - generic [ref=e14]: "Mã OTP của bạn là: 5378"
        - generic [ref=e15]:
          - generic [ref=e16]: Mã OTP (4 số)
          - textbox [active] [ref=e17]
        - generic [ref=e18]:
          - generic [ref=e19]: Mật khẩu mới
          - textbox [ref=e20]: NewPass1!
        - button "Đặt lại mật khẩu" [ref=e21] [cursor=pointer]
        - button "← Quay lại" [ref=e22] [cursor=pointer]
  - contentinfo [ref=e23]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  44  |   attachDialogHandler() {
  45  |     if (this._dialogHandler) return;
  46  |     this._dialogHandler = async (dialog) => {
  47  |       this._lastDialogMessage = dialog.message();
  48  |       await dialog.accept();
  49  |     };
  50  |     this.page.on('dialog', this._dialogHandler);
  51  |   }
  52  | 
  53  |   clearDialogMessage() {
  54  |     this._lastDialogMessage = null;
  55  |   }
  56  | 
  57  |   async goto() {
  58  |     this.attachDialogHandler();
  59  |     await this.page.goto('/forgot-password');
  60  |     await this.page.waitForLoadState('networkidle');
  61  |   }
  62  | 
  63  |   async requestOtp(email) {
  64  |     this.clearDialogMessage();
  65  |     await this.emailInput.waitFor({ state: 'visible' });
  66  |     await this.emailInput.fill(email);
  67  |     const responsePromise = this.page
  68  |       .waitForResponse((r) => r.url().includes('/api/forgot-password'), { timeout: 8000 })
  69  |       .catch(() => null);
  70  |     await this.sendOtpBtn.click();
  71  |     await responsePromise;
  72  |     await this.page.waitForTimeout(400);
  73  |   }
  74  | 
  75  |   async waitForStep2(timeout = 8000) {
  76  |     await this.step2Form.waitFor({ state: 'visible', timeout }).catch(() => {});
  77  |   }
  78  | 
  79  |   // FR-03 / SEC-07: OTP shown on screen in demo mode (spec: 6 digits; SUT may emit 4)
  80  |   async readOtpFromScreen() {
  81  |     try {
  82  |       if (await this.otpDemoBox.count() > 0) {
  83  |         const txt = await this.otpDemoBox.first().textContent();
  84  |         const match = txt.match(/\b(\d{4,6})\b/);
  85  |         if (match) return match[1];
  86  |       }
  87  |       const body = await this.page.textContent('body');
  88  |       const match = body.match(/Mã OTP[^0-9]*(\d{4,6})|OTP[^0-9]*(\d{4,6})/i)
  89  |         ?? body.match(/\b(\d{6})\b/)
  90  |         ?? body.match(/\b(\d{4})\b/);
  91  |       if (!match) return null;
  92  |       return match[1] || match[2];
  93  |     } catch {
  94  |       return null;
  95  |     }
  96  |   }
  97  | 
  98  |   async resetPassword(otp, newPassword, confirmPassword) {
  99  |     this.clearDialogMessage();
  100 |     await this.otpInput.waitFor({ state: 'visible' });
  101 |     await this.otpInput.fill(otp ?? '');
  102 |     await this.newPwdInput.fill(newPassword ?? '');
  103 |     const confirm = confirmPassword ?? newPassword;
  104 |     if (await this.confirmPwdInput.count() > 0) {
  105 |       await this.confirmPwdInput.fill(confirm ?? '');
  106 |     }
  107 |     const responsePromise = this.page
  108 |       .waitForResponse((r) => r.url().includes('/api/reset-password'), { timeout: 8000 })
  109 |       .catch(() => null);
  110 |     await this.resetBtn.click();
  111 |     await responsePromise;
  112 |     await this.page.waitForTimeout(400);
  113 |   }
  114 | 
  115 |   async getFieldValidationMessage(locator) {
  116 |     return locator.evaluate((el) => el.validationMessage || '');
  117 |   }
  118 | 
  119 |   // FR-22: errors inline above submit OR captured alert dialog
  120 |   async getErrorText() {
  121 |     if (this._lastDialogMessage) return this._lastDialogMessage.trim();
  122 | 
  123 |     try {
  124 |       if (await this.errorMsg.count() > 0) {
  125 |         const txt = await this.errorMsg.first().textContent({ timeout: 1000 });
  126 |         if (txt?.trim()) return txt.trim();
  127 |       }
  128 |     } catch { /* no inline error */ }
  129 | 
  130 |     return null;
  131 |   }
  132 | 
  133 |   async hasClientSideValidationError() {
  134 |     const otpInvalid = await this.otpInput.evaluate((el) => !el.validity.valid).catch(() => false);
  135 |     const pwdInvalid = await this.newPwdInput.evaluate((el) => !el.validity.valid).catch(() => false);
  136 |     const confirmInvalid = (await this.confirmPwdInput.count()) > 0
  137 |       ? await this.confirmPwdInput.evaluate((el) => !el.validity.valid).catch(() => false)
  138 |       : false;
  139 |     const emailInvalid = await this.emailInput.evaluate((el) => !el.validity.valid).catch(() => false);
  140 |     return otpInvalid || pwdInvalid || confirmInvalid || emailInvalid;
  141 |   }
  142 | 
  143 |   async isResetSuccessful() {
> 144 |     await this.page.waitForTimeout(800);
      |                     ^ Error: page.waitForTimeout: Target page, context or browser has been closed
  145 |     if (this.page.url().includes('/login')) return true;
  146 |     if (/thành công|success/i.test(this._lastDialogMessage || '')) return true;
  147 |     try {
  148 |       await this.successMsg.first().waitFor({ timeout: 2000 });
  149 |       return true;
  150 |     } catch {
  151 |       return false;
  152 |     }
  153 |   }
  154 | 
  155 |   async isOnStep2() {
  156 |     return this.step2Form.isVisible();
  157 |   }
  158 | 
  159 |   async hasStepIndicator() {
  160 |     return (await this.stepIndicator.count()) > 0;
  161 |   }
  162 | 
  163 |   async getStepIndicatorText() {
  164 |     if (await this.stepIndicator.count() === 0) return null;
  165 |     return (await this.stepIndicator.first().textContent())?.trim() ?? null;
  166 |   }
  167 | 
  168 |   async hasConfirmPasswordField() {
  169 |     return (await this.confirmPwdInput.count()) > 0;
  170 |   }
  171 | 
  172 |   async clickBackToLogin() {
  173 |     await this.backToLoginLink.first().click();
  174 |   }
  175 | }
  176 | 
  177 | module.exports = { ForgotPasswordPage };
  178 | 
```
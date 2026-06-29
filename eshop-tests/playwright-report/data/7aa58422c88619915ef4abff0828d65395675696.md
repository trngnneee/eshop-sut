# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: forgot-password.spec.js >> FR-03 · Forgot Password — Step 2: Password BVA >> TC-FORGOT-031 · BVA · New password length 8 (min) → reset succeeds
- Location: tests\e2e\forgot-password.spec.js:291:3

# Error details

```
Error: Valid OTP + password must redirect to /login

expect(received).toBe(expected) // Object.is equality

Expected: true
Received: false
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
        - generic [ref=e14]: "Mã OTP của bạn là: 7246"
        - generic [ref=e15]:
          - generic [ref=e16]: Mã OTP (4 số)
          - textbox [ref=e17]: "7246"
        - generic [ref=e18]:
          - generic [ref=e19]: Mật khẩu mới
          - textbox [ref=e20]: Abc@1234
        - button "Đặt lại mật khẩu" [active] [ref=e21] [cursor=pointer]
        - button "← Quay lại" [ref=e22] [cursor=pointer]
  - contentinfo [ref=e23]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  1   | // tests/e2e/forgot-password.spec.js
  2   | // FR-03: Forgot Password & Reset Password (2-step flow)
  3   | // Techniques: Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
  4   | // TC IDs: TC-FORGOT-001 … TC-FORGOT-044
  5   | 
  6   | const { test, expect } = require('@playwright/test');
  7   | const { ForgotPasswordPage } = require('../pages/ForgotPasswordPage');
  8   | const { loginViaUI } = require('../helpers/auth');
  9   | const { requestOtpViaAPI, resetPasswordViaAPI, restoreUserPassword } = require('../helpers/forgot');
  10  | const { ACCOUNTS, FORGOT } = require('../fixtures/test-data');
  11  | 
  12  | // ── Shared helpers ────────────────────────────────────────────────────────────
  13  | async function openForgotPage(page) {
  14  |   const fp = new ForgotPasswordPage(page);
  15  |   await fp.goto();
  16  |   return fp;
  17  | }
  18  | 
  19  | async function goToStep2(page, email = FORGOT.registeredEmail) {
  20  |   const fp = await openForgotPage(page);
  21  |   await fp.requestOtp(email);
  22  |   await fp.waitForStep2();
  23  |   const otp = await fp.readOtpFromScreen();
  24  |   return { fp, otp };
  25  | }
  26  | 
  27  | async function expectRejected(fp, page, message) {
  28  |   const error = await fp.getErrorText();
  29  |   const blocked = await fp.hasClientSideValidationError();
  30  |   expect(
  31  |     error || blocked,
  32  |     message ?? 'Invalid input must show error feedback or block submit (FR-22)'
  33  |   ).toBeTruthy();
  34  |   expect(page.url(), 'Must remain on forgot-password flow').toContain('/forgot');
  35  |   expect(await fp.isResetSuccessful(), 'Password must not be reset').toBe(false);
  36  | }
  37  | 
  38  | async function expectNoLengthError(fp) {
  39  |   const error = await fp.getErrorText();
  40  |   expect(error ?? '', 'Must not report email length validation error').not.toMatch(/độ dài|length|100|5 ký tự/i);
  41  | }
  42  | 
  43  | async function expectResetSuccess(fp, page) {
> 44  |   expect(await fp.isResetSuccessful(), 'Valid OTP + password must redirect to /login').toBe(true);
      |                                                                                        ^ Error: Valid OTP + password must redirect to /login
  45  |   await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
  46  | }
  47  | 
  48  | // ─────────────────────────────────────────────────────────────────────────────
  49  | test.describe('FR-03 · Forgot Password — Happy path & UI', () => {
  50  | 
  51  |   test('TC-FORGOT-001 · DT · Full valid reset → login with new password succeeds', async ({ page }) => {
  52  |     const { fp, otp } = await goToStep2(page);
  53  |     expect(await fp.hasConfirmPasswordField(), 'Step 2 must include confirm-password field (FR-03)').toBe(true);
  54  |     if (!otp) test.skip(true, 'OTP not visible on screen — cannot complete Step 2');
  55  |     await fp.resetPassword(otp, FORGOT.newPwdValid, FORGOT.newPwdValid);
  56  |     expect(await fp.isResetSuccessful(), 'Reset must succeed and redirect to /login').toBe(true);
  57  |     await loginViaUI(page, FORGOT.registeredEmail, FORGOT.newPwdValid);
  58  |     expect(page.url(), 'Login with new password must succeed').not.toContain('/login');
  59  |     await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
  60  |   });
  61  | 
  62  |   test('TC-FORGOT-019 · GUI · Step Indicator shows correct step (Bước 1/2 → Bước 2/2)', async ({ page }) => {
  63  |     const fp = await openForgotPage(page);
  64  |     expect(await fp.hasStepIndicator(), 'Step 1 must show Step Indicator (FR-03)').toBe(true);
  65  |     const step1Text = await fp.getStepIndicatorText();
  66  |     expect(step1Text, 'Step 1 indicator must reference step 1').toMatch(/1\s*\/\s*2/i);
  67  |     await fp.requestOtp(FORGOT.registeredEmail);
  68  |     await fp.waitForStep2();
  69  |     expect(await fp.hasStepIndicator(), 'Step 2 must show Step Indicator (FR-03)').toBe(true);
  70  |     const step2Text = await fp.getStepIndicatorText();
  71  |     expect(step2Text, 'Step 2 indicator must reference step 2').toMatch(/2\s*\/\s*2/i);
  72  |   });
  73  | 
  74  |   test('TC-FORGOT-020 · GUI · "Quay lại đăng nhập" navigates to /login', async ({ page }) => {
  75  |     const fp = await openForgotPage(page);
  76  |     expect(await fp.backToLoginLink.count(), '"Quay lại đăng nhập" must be present (FR-03)').toBeGreaterThan(0);
  77  |     await fp.clickBackToLogin();
  78  |     await page.waitForURL('**/login', { timeout: 5000 });
  79  |     expect(page.url()).toContain('/login');
  80  | 
  81  |     const fp2 = await openForgotPage(page);
  82  |     await fp2.requestOtp(FORGOT.registeredEmail);
  83  |     await fp2.waitForStep2();
  84  |     expect(await fp2.backToLoginLink.count(), 'Back link must also be available on Step 2').toBeGreaterThan(0);
  85  |     await fp2.clickBackToLogin();
  86  |     await page.waitForURL('**/login', { timeout: 5000 });
  87  |     expect(page.url()).toContain('/login');
  88  |   });
  89  | });
  90  | 
  91  | // ─────────────────────────────────────────────────────────────────────────────
  92  | test.describe('FR-03 · Forgot Password — Step 1: Email domain & BVA', () => {
  93  | 
  94  |   test('TC-FORGOT-002 · DT · Empty email → rejected, stays on Step 1', async ({ page }) => {
  95  |     const fp = await openForgotPage(page);
  96  |     await fp.requestOtp('');
  97  |     await expectRejected(fp, page, 'Empty email must be rejected (SD-E01)');
  98  |     expect(await fp.isOnStep2(), 'Empty email must not advance to Step 2').toBe(false);
  99  |   });
  100 | 
  101 |   test('TC-FORGOT-003 · DT · Malformed email → format error, stays on Step 1', async ({ page }) => {
  102 |     const fp = await openForgotPage(page);
  103 |     await fp.requestOtp(FORGOT.malformedEmail);
  104 |     await expectRejected(fp, page, 'Malformed email must be rejected (SD-E02)');
  105 |     expect(await fp.isOnStep2(), 'Malformed email must not advance to Step 2').toBe(false);
  106 |   });
  107 | 
  108 |   test('TC-FORGOT-004 · DT · Unregistered email → error, no Step 2', async ({ page }) => {
  109 |     const fp = await openForgotPage(page);
  110 |     await fp.requestOtp(FORGOT.unregisteredEmail);
  111 |     await expectRejected(fp, page, 'Unregistered email must show error (SD-E03)');
  112 |     expect(await fp.isOnStep2(), 'Unregistered email must not advance to Step 2').toBe(false);
  113 |   });
  114 | 
  115 |   test('TC-FORGOT-021 · BVA · Email length 4 (min−) → length error', async ({ page }) => {
  116 |     const fp = await openForgotPage(page);
  117 |     await fp.requestOtp(FORGOT.emailMin4);
  118 |     await expectRejected(fp, page, 'Email of 4 chars (min−) must be rejected');
  119 |     expect(await fp.isOnStep2()).toBe(false);
  120 |   });
  121 | 
  122 |   test('TC-FORGOT-022 · BVA · Email length 5 (min on-point) → no length error', async ({ page }) => {
  123 |     const fp = await openForgotPage(page);
  124 |     await fp.requestOtp(FORGOT.emailMin5);
  125 |     await expectNoLengthError(fp);
  126 |   });
  127 | 
  128 |   test('TC-FORGOT-023 · BVA · Email length 6 (min+) → no length error', async ({ page }) => {
  129 |     const fp = await openForgotPage(page);
  130 |     await fp.requestOtp(FORGOT.emailMin6);
  131 |     await expectNoLengthError(fp);
  132 |   });
  133 | 
  134 |   test('TC-FORGOT-024 · BVA · Email length 99 (max−) → no length error', async ({ page }) => {
  135 |     const fp = await openForgotPage(page);
  136 |     await fp.requestOtp(FORGOT.emailMax99);
  137 |     await expectNoLengthError(fp);
  138 |   });
  139 | 
  140 |   test('TC-FORGOT-025 · BVA · Email length 100 (max on-point) → no length error', async ({ page }) => {
  141 |     const fp = await openForgotPage(page);
  142 |     await fp.requestOtp(FORGOT.emailMax100);
  143 |     await expectNoLengthError(fp);
  144 |   });
```
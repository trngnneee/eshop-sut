// tests/e2e/forgot-password.spec.js
// FR-03: Forgot Password & Reset Password (2-step flow)
// Techniques: Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
// TC IDs: TC-FORGOT-001 … TC-FORGOT-044

const { test, expect } = require('@playwright/test');
const { ForgotPasswordPage } = require('../pages/ForgotPasswordPage');
const { loginViaUI } = require('../helpers/auth');
const { requestOtpViaAPI, resetPasswordViaAPI, restoreUserPassword } = require('../helpers/forgot');
const { ACCOUNTS, FORGOT } = require('../fixtures/test-data');

// ── Shared helpers ────────────────────────────────────────────────────────────
async function openForgotPage(page) {
  const fp = new ForgotPasswordPage(page);
  await fp.goto();
  return fp;
}

async function goToStep2(page, email = FORGOT.registeredEmail) {
  const fp = await openForgotPage(page);
  await fp.requestOtp(email);
  await fp.waitForStep2();
  const otp = await fp.readOtpFromScreen();
  return { fp, otp };
}

async function expectRejected(fp, page, message) {
  const error = await fp.getErrorText();
  const blocked = await fp.hasClientSideValidationError();
  expect(
    error || blocked,
    message ?? 'Invalid input must show error feedback or block submit (FR-22)'
  ).toBeTruthy();
  expect(page.url(), 'Must remain on forgot-password flow').toContain('/forgot');
  expect(await fp.isResetSuccessful(), 'Password must not be reset').toBe(false);
}

async function expectNoLengthError(fp) {
  const error = await fp.getErrorText();
  expect(error ?? '', 'Must not report email length validation error').not.toMatch(/độ dài|length|100|5 ký tự/i);
}

async function expectResetSuccess(fp, page) {
  expect(await fp.isResetSuccessful(), 'Valid OTP + password must redirect to /login').toBe(true);
  await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
}

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Happy path & UI', () => {

  test('TC-FORGOT-001 · DT · Full valid reset → login with new password succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    expect(await fp.hasConfirmPasswordField(), 'Step 2 must include confirm-password field (FR-03)').toBe(true);
    if (!otp) test.skip(true, 'OTP not visible on screen — cannot complete Step 2');
    await fp.resetPassword(otp, FORGOT.newPwdValid, FORGOT.newPwdValid);
    expect(await fp.isResetSuccessful(), 'Reset must succeed and redirect to /login').toBe(true);
    await loginViaUI(page, FORGOT.registeredEmail, FORGOT.newPwdValid);
    expect(page.url(), 'Login with new password must succeed').not.toContain('/login');
    await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
  });

  test('TC-FORGOT-019 · GUI · Step Indicator shows correct step (Bước 1/2 → Bước 2/2)', async ({ page }) => {
    const fp = await openForgotPage(page);
    expect(await fp.hasStepIndicator(), 'Step 1 must show Step Indicator (FR-03)').toBe(true);
    const step1Text = await fp.getStepIndicatorText();
    expect(step1Text, 'Step 1 indicator must reference step 1').toMatch(/1\s*\/\s*2/i);
    await fp.requestOtp(FORGOT.registeredEmail);
    await fp.waitForStep2();
    expect(await fp.hasStepIndicator(), 'Step 2 must show Step Indicator (FR-03)').toBe(true);
    const step2Text = await fp.getStepIndicatorText();
    expect(step2Text, 'Step 2 indicator must reference step 2').toMatch(/2\s*\/\s*2/i);
  });

  test('TC-FORGOT-020 · GUI · "Quay lại đăng nhập" navigates to /login', async ({ page }) => {
    const fp = await openForgotPage(page);
    expect(await fp.backToLoginLink.count(), '"Quay lại đăng nhập" must be present (FR-03)').toBeGreaterThan(0);
    await fp.clickBackToLogin();
    await page.waitForURL('**/login', { timeout: 5000 });
    expect(page.url()).toContain('/login');

    const fp2 = await openForgotPage(page);
    await fp2.requestOtp(FORGOT.registeredEmail);
    await fp2.waitForStep2();
    expect(await fp2.backToLoginLink.count(), 'Back link must also be available on Step 2').toBeGreaterThan(0);
    await fp2.clickBackToLogin();
    await page.waitForURL('**/login', { timeout: 5000 });
    expect(page.url()).toContain('/login');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Step 1: Email domain & BVA', () => {

  test('TC-FORGOT-002 · DT · Empty email → rejected, stays on Step 1', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp('');
    await expectRejected(fp, page, 'Empty email must be rejected (SD-E01)');
    expect(await fp.isOnStep2(), 'Empty email must not advance to Step 2').toBe(false);
  });

  test('TC-FORGOT-003 · DT · Malformed email → format error, stays on Step 1', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.malformedEmail);
    await expectRejected(fp, page, 'Malformed email must be rejected (SD-E02)');
    expect(await fp.isOnStep2(), 'Malformed email must not advance to Step 2').toBe(false);
  });

  test('TC-FORGOT-004 · DT · Unregistered email → error, no Step 2', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.unregisteredEmail);
    await expectRejected(fp, page, 'Unregistered email must show error (SD-E03)');
    expect(await fp.isOnStep2(), 'Unregistered email must not advance to Step 2').toBe(false);
  });

  test('TC-FORGOT-021 · BVA · Email length 4 (min−) → length error', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.emailMin4);
    await expectRejected(fp, page, 'Email of 4 chars (min−) must be rejected');
    expect(await fp.isOnStep2()).toBe(false);
  });

  test('TC-FORGOT-022 · BVA · Email length 5 (min on-point) → no length error', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.emailMin5);
    await expectNoLengthError(fp);
  });

  test('TC-FORGOT-023 · BVA · Email length 6 (min+) → no length error', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.emailMin6);
    await expectNoLengthError(fp);
  });

  test('TC-FORGOT-024 · BVA · Email length 99 (max−) → no length error', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.emailMax99);
    await expectNoLengthError(fp);
  });

  test('TC-FORGOT-025 · BVA · Email length 100 (max on-point) → no length error', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.emailMax100);
    await expectNoLengthError(fp);
  });

  test('TC-FORGOT-026 · BVA · Email length 101 (max+) → length error', async ({ page }) => {
    const fp = await openForgotPage(page);
    await fp.requestOtp(FORGOT.emailMax101);
    await expectRejected(fp, page, 'Email of 101 chars (max+) must be rejected');
    expect(await fp.isOnStep2()).toBe(false);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Step 2: OTP domain & BVA', () => {

  test('TC-FORGOT-005 · DT · Empty OTP → rejected', async ({ page }) => {
    const { fp } = await goToStep2(page);
    await fp.resetPassword('', FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectRejected(fp, page, 'Empty OTP must be rejected (SD-O01)');
  });

  test('TC-FORGOT-006 · DT · Non-numeric OTP → rejected', async ({ page }) => {
    const { fp } = await goToStep2(page);
    await fp.resetPassword(FORGOT.otpNonNumeric, FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectRejected(fp, page, 'Non-numeric OTP must be rejected (SD-O02)');
  });

  test('TC-FORGOT-007 · DT · OTP 5 digits → rejected', async ({ page }) => {
    const { fp } = await goToStep2(page);
    await fp.resetPassword(FORGOT.otpWrongLength5, FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectRejected(fp, page, '5-digit OTP must be rejected (SD-O03)');
  });

  test('TC-FORGOT-008 · DT · OTP 7 digits → rejected', async ({ page }) => {
    const { fp } = await goToStep2(page);
    await fp.resetPassword(FORGOT.otpWrongLength7, FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectRejected(fp, page, '7-digit OTP must be rejected (SD-O04)');
  });

  test('TC-FORGOT-009 · DT · Wrong OTP value → rejected', async ({ page }) => {
    const { fp } = await goToStep2(page);
    await fp.resetPassword(FORGOT.otpAllZeros, FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectRejected(fp, page, 'Wrong OTP must be rejected (SD-O05)');
  });

  test('TC-FORGOT-010 · DT · OTP for email A used with email B → rejected via API', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    expect(body.resetToken, 'Must obtain OTP for test@eshop.com').toBeTruthy();
    const response = await resetPasswordViaAPI(
      page,
      FORGOT.adminEmail,
      body.resetToken,
      FORGOT.newPwdValid
    );
    expect(response.ok(), 'OTP must not reset password for a different email (SD-O07)').toBe(false);
  });

  test('TC-FORGOT-027 · BVA · OTP 5 digits (length min−) → rejected', async ({ page }) => {
    const { fp } = await goToStep2(page);
    await fp.resetPassword(FORGOT.otpWrongLength5, FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectRejected(fp, page, '5-digit OTP (min−) must be rejected');
  });

  test('TC-FORGOT-028 · BVA · Valid 6-digit OTP → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-029 · BVA · OTP 7 digits (length max+) → rejected', async ({ page }) => {
    const { fp } = await goToStep2(page);
    await fp.resetPassword(FORGOT.otpWrongLength7, FORGOT.newPwdValid, FORGOT.newPwdValid);
    await expectRejected(fp, page, '7-digit OTP (max+) must be rejected');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Step 2: Password domain', () => {

  test('TC-FORGOT-011 · DT · Empty new password → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, '', FORGOT.newPwdValid);
    await expectRejected(fp, page, 'Empty new password must be rejected (SD-P01)');
  });

  test('TC-FORGOT-012 · DT · Password too short (7 chars) → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdTooShort, FORGOT.newPwdTooShort);
    await expectRejected(fp, page, 'Password under 8 chars must be rejected (SD-P02, FR-01)');
  });

  test('TC-FORGOT-013 · DT · Password missing uppercase → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdNoUpper, FORGOT.newPwdNoUpper);
    await expectRejected(fp, page, 'Password without uppercase must be rejected (SD-P03, FR-01)');
  });

  test('TC-FORGOT-014 · DT · Password missing lowercase → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdNoLower, FORGOT.newPwdNoLower);
    await expectRejected(fp, page, 'Password without lowercase must be rejected (SD-P04, FR-01)');
  });

  test('TC-FORGOT-015 · DT · Password missing digit → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdNoDigit, FORGOT.newPwdNoDigit);
    await expectRejected(fp, page, 'Password without digit must be rejected (SD-P05, FR-01)');
  });

  test('TC-FORGOT-016 · DT · Password missing special char → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdNoSpecial, FORGOT.newPwdNoSpecial);
    await expectRejected(fp, page, 'Password without special char must be rejected (SD-P06, FR-01)');
  });

  test('TC-FORGOT-017 · DT · Empty confirm password → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    expect(await fp.hasConfirmPasswordField(), 'Confirm-password field required (FR-03)').toBe(true);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdValid, '');
    await expectRejected(fp, page, 'Empty confirm password must be rejected (SD-C01)');
  });

  test('TC-FORGOT-018 · DT · Confirm password mismatch → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    expect(await fp.hasConfirmPasswordField(), 'Confirm-password field required (FR-03)').toBe(true);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdValid, FORGOT.newPwdAlt);
    await expectRejected(fp, page, 'Mismatched passwords must be rejected (SD-C02, FR-03)');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Step 2: Password BVA', () => {

  test('TC-FORGOT-030 · BVA · New password length 7 (min−) → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin7, FORGOT.newPwdMin7);
    await expectRejected(fp, page, 'Password of 7 chars (min−) must be rejected (FR-01)');
  });

  test('TC-FORGOT-031 · BVA · New password length 8 (min) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin8);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-032 · BVA · New password length 9 (min+) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin9, FORGOT.newPwdMin9);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-033 · BVA · New password length 49 (max−) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.pwdMax49, FORGOT.pwdMax49);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-034 · BVA · New password length 50 (max) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.pwdMax50, FORGOT.pwdMax50);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-035 · BVA · New password length 51 (max+) → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.pwdMax51, FORGOT.pwdMax51);
    await expectRejected(fp, page, 'Password of 51 chars (max+) must be rejected');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Step 2: Confirm-password BVA', () => {

  test('TC-FORGOT-036 · BVA · Confirm password length 7 (min−) → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin7);
    await expectRejected(fp, page, 'Confirm at min− with new at min must be rejected');
  });

  test('TC-FORGOT-037 · BVA · Confirm password length 8 (min) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin8);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-038 · BVA · Confirm password length 9 (min+) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin9, FORGOT.newPwdMin9);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-039 · BVA · Confirm password length 49 (max−) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.pwdMax49, FORGOT.pwdMax49);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-040 · BVA · Confirm password length 50 (max) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.pwdMax50, FORGOT.pwdMax50);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-041 · BVA · Confirm password length 51 (max+) → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.pwdMax50, FORGOT.pwdMax51);
    await expectRejected(fp, page, 'Confirm password of 51 chars (max+) must be rejected');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Cross-boundary BVA', () => {

  test('TC-FORGOT-042 · BVA · Both passwords at min (8) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin8);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-043 · BVA · Both passwords at max (50) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.pwdMax50, FORGOT.pwdMax50);
    await expectResetSuccess(fp, page);
  });

  test('TC-FORGOT-044 · BVA · New at min (8), confirm at min− (7) → rejected', async ({ page }) => {
    const { fp, otp } = await goToStep2(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin7);
    await expectRejected(fp, page, 'Cross-boundary mismatch at min must be rejected');
  });
});

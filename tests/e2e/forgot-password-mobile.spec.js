// tests/e2e/forgot-password-mobile.spec.js
// FR-22: Forgot Password on Mobile (Expo Web + API)
// TC IDs aligned with tests/test-cases/forgot-mobile/

const { test, expect } = require('@playwright/test');
const { MobileForgotPasswordPage } = require('../pages/MobileForgotPasswordPage');
const { requestOtpViaAPI, resetPasswordViaAPI, restoreUserPassword } = require('../helpers/forgot');
const { FORGOT, ACCOUNTS } = require('../fixtures/test-data');

const MOBILE_URL = process.env.MOBILE_URL || 'http://localhost:8081';

async function openMobileForgot(page) {
  const mfp = new MobileForgotPasswordPage(page);
  await mfp.gotoForgotFlow(MOBILE_URL);
  return mfp;
}

async function goToMobileStep2(page, email = FORGOT.registeredEmail) {
  const mfp = await openMobileForgot(page);
  await mfp.requestOtp(email);
  await mfp.waitForStep2();
  return mfp;
}

// ── Supplementary (GAP remediation) ───────────────────────────────────────────
test.describe('FR-22 · Mobile Forgot — Supplementary', () => {
  test.setTimeout(60_000);

  test('TC-MFORGOT-SUP-001 · API OTP 6 digits + Mobile label', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    expect(body.resetToken, 'resetToken must be 6 digits (FR-22)').toMatch(/^\d{6}$/);

    const mfp = await goToMobileStep2(page);
    const label = await mfp.getOtpLabelText();
    expect(label, 'OTP label must describe 6 digits').toMatch(/6\s*số/i);
    expect(label, 'Must not say 4 digits').not.toMatch(/4\s*số/i);
  });

  test('TC-MFORGOT-SUP-002 · Demo OTP displayed on screen after Step 1', async ({ page }) => {
    const mfp = await goToMobileStep2(page);
    const msg = await mfp.getMessageText();
    expect(msg, 'Demo must show OTP on screen (FR-22)').toMatch(/Mã OTP của bạn là:\s*\d{6}/i);
  });

  test('TC-MFORGOT-SUP-003 · Backend rejects weak password on reset', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    const response = await resetPasswordViaAPI(
      page,
      FORGOT.registeredEmail,
      body.resetToken,
      'weakpass'
    );
    expect(response.ok(), 'API must reject weak password (FR-01)').toBe(false);
  });

  test('TC-MFORGOT-SUP-004 · OTP cannot be reused after successful reset', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    const otp = body.resetToken;
    const first = await resetPasswordViaAPI(page, FORGOT.registeredEmail, otp, 'MobileT1!');
    expect(first.ok()).toBe(true);
    const second = await resetPasswordViaAPI(page, FORGOT.registeredEmail, otp, 'MobileT2!');
    expect(second.ok(), 'Second reset with same OTP must fail').toBe(false);
    await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
  });

  test('TC-MFORGOT-SUP-005 · Step 2 must include confirm-password field', async ({ page }) => {
    const mfp = await goToMobileStep2(page);
    expect(await mfp.hasConfirmPasswordField(), 'Confirm-password field required (FR-22)').toBe(true);
  });

  test('TC-MFORGOT-SUP-006 · Validation error inline above submit (not Alert only)', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    const mfp = await goToMobileStep2(page);
    await mfp.resetPassword(body.resetToken, 'weakpass');
    const dialog = mfp.getLastDialogMessage();
    const inlineError = await page.getByText(/mật khẩu|yếu|lỗi/i).count();
    expect(
      inlineError > 0 && !dialog,
      'FR-22: error must be inline above submit, not Alert dialog only'
    ).toBe(true);
  });

  test('TC-MFORGOT-SUP-007 · Reject password with special char outside FR-01 whitelist', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    const mfp = await goToMobileStep2(page);
    await mfp.resetPassword(body.resetToken, 'Test1234+');
    const dialog = mfp.getLastDialogMessage() ?? '';
    const accepted = dialog.toLowerCase().includes('thành công');
    expect(accepted, 'Client must reject Test1234+ per FR-01 whitelist').toBe(false);
  });
});

// ── Domain Testing (EP highlights) ────────────────────────────────────────────
test.describe('FR-22 · Mobile Forgot — Domain Testing', () => {
  test.setTimeout(60_000);

  test('TC-MFORGOT-001 · DT · Full valid reset flow', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    const mfp = await goToMobileStep2(page);
    expect(await mfp.hasConfirmPasswordField()).toBe(true);
    await mfp.resetPassword(body.resetToken, FORGOT.newPwdValid);
    const dialog = mfp.getLastDialogMessage() ?? '';
    expect(dialog).toMatch(/thành công/i);
    await expect(page.getByText('Sign In')).toBeVisible({ timeout: 5000 });
    await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
  });

  test('TC-MFORGOT-004 · DT · Unregistered email rejected', async ({ page }) => {
    const mfp = await openMobileForgot(page);
    await mfp.requestOtp(FORGOT.unregisteredEmail);
    const dialog = mfp.getLastDialogMessage() ?? '';
    expect(dialog.length > 0 || !(await mfp.isOnStep2()), 'Unregistered email must be rejected').toBe(true);
  });

  test('TC-MFORGOT-010 · DT · OTP for email A cannot reset email B', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    const response = await resetPasswordViaAPI(
      page,
      FORGOT.adminEmail,
      body.resetToken,
      FORGOT.newPwdValid
    );
    expect(response.ok()).toBe(false);
  });

  test('TC-MFORGOT-019 · GUI · Step Indicator on Step 1 and 2', async ({ page }) => {
    const mfp = await openMobileForgot(page);
    expect(await mfp.hasStepIndicator(), 'Step 1 must show indicator (FR-22)').toBe(true);
    await mfp.requestOtp(FORGOT.registeredEmail);
    await mfp.waitForStep2();
    expect(await mfp.hasStepIndicator(), 'Step 2 must show indicator (FR-22)').toBe(true);
  });

  test('TC-MFORGOT-020 · GUI · "Quay lại đăng nhập" returns to login', async ({ page }) => {
    const mfp = await openMobileForgot(page);
    expect(await mfp.backToLoginLink.count(), '"Quay lại đăng nhập" required on Step 1').toBeGreaterThan(0);
    await mfp.backToLoginLink.first().click();
    expect(await mfp.isOnLoginScreen()).toBe(true);

    const mfp2 = await goToMobileStep2(page);
    expect(await mfp2.backToLoginLink.count(), 'Back to login required on Step 2').toBeGreaterThan(0);
    await mfp2.backToLoginLink.first().click();
    expect(await mfp2.isOnLoginScreen()).toBe(true);
  });
});

// ── BVA highlights ────────────────────────────────────────────────────────────
test.describe('FR-22 · Mobile Forgot — BVA', () => {
  test.setTimeout(60_000);

  test('TC-MFORGOT-028 · BVA · Valid 6-digit OTP on-point', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    expect(body.resetToken).toMatch(/^\d{6}$/);
    const mfp = await goToMobileStep2(page);
    await mfp.resetPassword(body.resetToken, FORGOT.newPwdValid);
    const dialog = mfp.getLastDialogMessage() ?? '';
    expect(dialog).toMatch(/thành công/i);
    await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
  });

  test('TC-MFORGOT-031 · BVA · Password min length 8 accepted', async ({ page }) => {
    const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
    const mfp = await goToMobileStep2(page);
    await mfp.resetPassword(body.resetToken, FORGOT.newPwdMin8);
    const dialog = mfp.getLastDialogMessage() ?? '';
    expect(dialog).toMatch(/thành công/i);
    await restoreUserPassword(page, FORGOT.registeredEmail, ACCOUNTS.user.password);
  });
});

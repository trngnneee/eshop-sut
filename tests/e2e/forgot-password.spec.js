// tests/e2e/forgot-password.spec.js
// FR-03: Forgot Password & Reset Password (2-step flow)
// Techniques: Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
// TC IDs: TC-FORGOT-001 … TC-FORGOT-018

const { test, expect } = require('@playwright/test');
const { ForgotPasswordPage } = require('../pages/ForgotPasswordPage');
const { FORGOT, ACCOUNTS, uniqueEmail } = require('../fixtures/test-data');

// ─────────────────────────────────────────────────────────────────────────────
// STEP 1 tests — "Enter email to receive OTP"
// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Step 1: Request OTP', () => {

  // ── Domain Testing: Valid domain — registered email ───────────────────────
  test('TC-FORGOT-001 · DT · Registered email → OTP sent, step indicator moves to Step 2', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    await fp.requestOtp(FORGOT.registeredEmail);
    // Should advance to Step 2 (OTP input visible) or show OTP on screen
    const onStep2 = await fp.isOnStep2();
    expect(onStep2, 'After valid email, UI must advance to Step 2 (OTP entry)').toBe(true);
  });

  // ── Domain Testing: Valid domain — step indicator present ────────────────
  test('TC-FORGOT-002 · GUI · Step indicator visible on the forgot-password page (FR-03)', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    const body = await page.textContent('body');
    // Spec: "Giao diện phải hiển thị chỉ báo bước (Step Indicator)"
    const hasIndicator = /bước|step\s*1|step indicator/i.test(body);
    expect(hasIndicator, 'Step Indicator (Bước 1 / 2) must be visible on forgot-password page').toBe(true);
  });

  // ── Domain Testing: Valid domain — "Quay lại đăng nhập" link present ─────
  test('TC-FORGOT-003 · GUI · "Quay lại đăng nhập" / back link is present (FR-03)', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    const backLink = page.locator('a:has-text("đăng nhập"), a:has-text("Quay lại"), button:has-text("Quay lại")');
    const count = await backLink.count();
    expect(count, '"Quay lại đăng nhập" link must be present on the forgot-password page').toBeGreaterThan(0);
  });

  // ── Domain Testing: "Quay lại" link navigates back to /login ─────────────
  test('TC-FORGOT-004 · DT · Clicking "Quay lại đăng nhập" → navigates to /login', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    await fp.backToLoginLink.first().click();
    await page.waitForTimeout(800);
    expect(page.url(), '"Quay lại đăng nhập" must navigate to /login').toContain('/login');
  });

  // ── Domain Testing: Invalid domain — unregistered email ──────────────────
  test('TC-FORGOT-005 · DT · Unregistered email → error message shown', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    await fp.requestOtp(FORGOT.unregisteredEmail);
    const error = await fp.getErrorText();
    expect(error, 'Unregistered email must produce an error message').not.toBeNull();
  });

  // ── Domain Testing: Invalid domain — empty email ─────────────────────────
  test('TC-FORGOT-006 · DT · Empty email → browser/form validation fires, stays on page', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    await fp.requestOtp('');
    await page.waitForTimeout(500);
    expect(page.url()).toContain('/forgot');
  });

  // ── Domain Testing: Invalid domain — malformed email ─────────────────────
  test('TC-FORGOT-007 · DT · Malformed email (no @) → HTML5 validation blocks submit', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    // Email input must be type="email" per FR-22
    const type = await fp.emailInput.getAttribute('type');
    expect(type, 'Forgot-password email input must be type="email" (FR-22)').toBe('email');
    await fp.requestOtp('notanemail');
    await page.waitForTimeout(500);
    expect(page.url()).toContain('/forgot');
  });

  // ── Domain Testing: OTP displayed on screen in demo mode ─────────────────
  test('TC-FORGOT-008 · DT · Demo mode: OTP is shown on screen after email submitted', async ({ page }) => {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    await fp.requestOtp(FORGOT.registeredEmail);
    // Spec: "trong môi trường demo: hiển thị trực tiếp trên màn hình"
    const otp = await fp.readOtpFromScreen();
    expect(otp, 'In demo mode the 6-digit OTP must be visible on screen').not.toBeNull();
    expect(otp?.length, 'OTP must be exactly 6 digits').toBe(6);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// STEP 2 tests — "Enter OTP + new password"
// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-03 · Forgot Password — Step 2: Reset Password', () => {

  // Shared setup: navigate to forgot-password and request OTP for the test user
  async function requestOtpAndReadIt(page) {
    const fp = new ForgotPasswordPage(page);
    await fp.goto();
    await fp.requestOtp(FORGOT.registeredEmail);
    await page.waitForTimeout(800);
    const otp = await fp.readOtpFromScreen();
    return { fp, otp };
  }

  // ── Domain Testing: Valid OTP + valid new password → reset succeeds ───────
  test('TC-FORGOT-009 · DT · Valid OTP + valid new password → reset succeeds, redirects to /login', async ({ page }) => {
    const { fp, otp } = await requestOtpAndReadIt(page);
    if (!otp) test.skip(true, 'OTP not visible on screen — cannot complete Step 2');
    await fp.resetPassword(otp, FORGOT.newPwdValid, FORGOT.newPwdValid);
    const ok = await fp.isResetSuccessful();
    expect(ok, 'Valid OTP + valid password must reset successfully and redirect to /login').toBe(true);
  });

  // ── Domain Testing: Invalid OTP (wrong value) → error ────────────────────
  test('TC-FORGOT-010 · DT · Wrong OTP value → error message shown', async ({ page }) => {
    const { fp } = await requestOtpAndReadIt(page);
    await fp.resetPassword('000000', FORGOT.newPwdValid, FORGOT.newPwdValid);
    const error = await fp.getErrorText();
    expect(error, 'Wrong OTP must produce an error message').not.toBeNull();
  });

  // ── Domain Testing: Passwords do not match → error ───────────────────────
  test('TC-FORGOT-011 · DT · OTP correct but passwords do not match → error', async ({ page }) => {
    const { fp, otp } = await requestOtpAndReadIt(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, 'NewPass@99', 'Different@88');
    const error = await fp.getErrorText();
    expect(error, 'Mismatched passwords must produce an error').not.toBeNull();
  });

  // ── Domain Testing: New password missing uppercase → error ───────────────
  test('TC-FORGOT-012 · DT · New password has no uppercase → error', async ({ page }) => {
    const { fp, otp } = await requestOtpAndReadIt(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    const weakPwd = 'newpass@99';   // no uppercase
    await fp.resetPassword(otp, weakPwd, weakPwd);
    const error = await fp.getErrorText();
    expect(error, 'Password without uppercase must be rejected in reset flow').not.toBeNull();
  });

  // ── BVA: New password length 7 (min−1) → invalid ─────────────────────────
  test('TC-FORGOT-013 · BVA · New password length 7 (min−1) → error shown', async ({ page }) => {
    const { fp, otp } = await requestOtpAndReadIt(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin7, FORGOT.newPwdMin7);
    const error = await fp.getErrorText();
    expect(error, 'Password of 7 chars (min−1) must be rejected in reset flow').not.toBeNull();
  });

  // ── BVA: New password length 8 (min on-point) → valid ────────────────────
  test('TC-FORGOT-014 · BVA · New password length 8 (min on-point) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await requestOtpAndReadIt(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin8);
    const ok = await fp.isResetSuccessful();
    expect(ok, 'Password of 8 chars (min) must be accepted in reset flow').toBe(true);
  });

  // ── BVA: New password length 9 (min+1) → valid ───────────────────────────
  test('TC-FORGOT-015 · BVA · New password length 9 (min+1) → reset succeeds', async ({ page }) => {
    const { fp, otp } = await requestOtpAndReadIt(page);
    if (!otp) test.skip(true, 'OTP not visible on screen');
    await fp.resetPassword(otp, FORGOT.newPwdMin9, FORGOT.newPwdMin9);
    const ok = await fp.isResetSuccessful();
    expect(ok, 'Password of 9 chars (min+1) must be accepted in reset flow').toBe(true);
  });

  // ── BVA: OTP length 5 (min−1 for 6-digit OTP) → error ───────────────────
  test('TC-FORGOT-016 · BVA · OTP with 5 digits (length min−1) → error', async ({ page }) => {
    const { fp } = await requestOtpAndReadIt(page);
    await fp.resetPassword(FORGOT.otpWrongLength5, FORGOT.newPwdValid, FORGOT.newPwdValid);
    const error = await fp.getErrorText();
    expect(error, '5-digit OTP (min−1) must be rejected').not.toBeNull();
  });

  // ── BVA: OTP length 7 (max+1 for 6-digit OTP) → error ───────────────────
  test('TC-FORGOT-017 · BVA · OTP with 7 digits (length max+1) → error', async ({ page }) => {
    const { fp } = await requestOtpAndReadIt(page);
    await fp.resetPassword(FORGOT.otpWrongLength7, FORGOT.newPwdValid, FORGOT.newPwdValid);
    const error = await fp.getErrorText();
    expect(error, '7-digit OTP (max+1) must be rejected').not.toBeNull();
  });

  // ── Domain Testing: OTP non-numeric → error ──────────────────────────────
  test('TC-FORGOT-018 · DT · Non-numeric OTP → error shown', async ({ page }) => {
    const { fp } = await requestOtpAndReadIt(page);
    await fp.resetPassword(FORGOT.otpNonNumeric, FORGOT.newPwdValid, FORGOT.newPwdValid);
    const error = await fp.getErrorText();
    expect(error, 'Non-numeric OTP must be rejected').not.toBeNull();
  });
});

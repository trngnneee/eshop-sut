// @ts-check
const { test, expect } = require('@playwright/test');
const { loadFeatureCases } = require('../helpers/load-test-data');
const { registerUser, loginUser } = require('../helpers/auth-api');
const { ForgotPasswordPage } = require('../pages/ForgotPasswordPage');

const { cases } = loadFeatureCases('fr03-forgot-password.json', {
  minCases: 12,
  feature: 'FR-03',
});

/**
 * Assertion patterns used in this feature (HW04 Task 1 — ≥3 distinct):
 * 1. Visibility / hidden: toBeVisible, toBeHidden
 * 2. Text content: toContainText
 * 3. Attribute: toHaveAttribute
 * 4. URL / navigation: toHaveURL
 * 5. Plain value / dialog / API status: expect(...).toBe / toMatch
 */

/**
 * @param {import('@playwright/test').Page} page
 * @param {ForgotPasswordPage} fp
 * @param {any} tc
 * @param {{ email: string, initialPassword: string, newPassword: string }} account
 */
async function resolveEmail(tc, account) {
  const mode = tc.inputs?.emailMode;
  switch (mode) {
    case 'registered':
      return account.email;
    case 'unregistered':
      return `missing.${Date.now()}@hw4-fr03.local`;
    case 'empty':
      return '';
    case 'custom':
      return tc.inputs.customEmail ?? '';
    case undefined:
      return '';
    default:
      throw new Error(`${tc.id}: unknown emailMode "${mode}"`);
  }
}

/**
 * @param {ForgotPasswordPage} fp
 * @param {any} tc
 */
async function resolveOtp(fp, tc) {
  const mode = tc.inputs?.otpMode;
  switch (mode) {
    case 'fromScreen':
      return fp.readOtpFromScreen();
    case 'empty':
      return '';
    case 'custom':
      return tc.inputs.customOtp ?? '';
    case undefined:
      return undefined;
    default:
      throw new Error(`${tc.id}: unknown otpMode "${mode}"`);
  }
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {ForgotPasswordPage} fp
 * @param {any} tc
 * @param {{ email: string, initialPassword: string, newPassword: string }} account
 * @param {{ dialogMessages: string[] }} runtime
 */
async function applyAssertions(page, fp, tc, account, runtime) {
  for (const assertion of tc.expected.assertions) {
    switch (assertion.type) {
      case 'visible':
        await expect(fp.target(assertion.target)).toBeVisible();
        break;
      case 'hidden':
        await expect(fp.target(assertion.target)).toBeHidden();
        break;
      case 'containText':
        await expect(fp.target(assertion.target)).toContainText(assertion.value);
        break;
      case 'attribute':
        await expect(fp.target(assertion.target)).toHaveAttribute(
          assertion.name,
          assertion.value,
        );
        break;
      case 'dialog': {
        const last = runtime.dialogMessages.at(-1);
        expect(last, `${tc.id}: expected dialog "${assertion.value}"`).toBe(
          assertion.value,
        );
        break;
      }
      case 'dialogMatches': {
        const last = runtime.dialogMessages.at(-1) ?? '';
        expect(
          last,
          `${tc.id}: expected dialog matching /${assertion.pattern}/, got "${last}"`,
        ).toMatch(new RegExp(assertion.pattern, 'i'));
        break;
      }
      case 'url':
        await expect(page).toHaveURL(new RegExp(assertion.pattern));
        break;
      case 'apiLogin': {
        const password =
          assertion.passwordSource === 'new'
            ? account.newPassword
            : account.initialPassword;
        const loginResult = await loginUser({
          email: account.email,
          password,
        });
        expect(loginResult.status).toBe(assertion.status);
        break;
      }
      case 'otpLength': {
        const otp = await fp.readOtpFromScreen();
        expect(otp.length).toBe(assertion.value);
        break;
      }
      default:
        throw new Error(`${tc.id}: unsupported assertion type "${assertion.type}"`);
    }
  }
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {ForgotPasswordPage} fp
 * @param {any} tc
 * @param {{ email: string, initialPassword: string, newPassword: string }} account
 * @param {{ dialogMessages: string[] }} runtime
 */
async function runJourney(page, fp, tc, account, runtime) {
  await fp.goto();

  if (tc.journey === 'uiContract') {
    return;
  }

  if (tc.journey === 'backToLogin') {
    const link = fp.backToLogin();
    await expect(link).toBeVisible({ timeout: 5_000 });
    await link.click();
    return;
  }

  const email = await resolveEmail(tc, account);

  /**
   * Accept dialogs without deadlocking on sync alert() during click.
   * @param {() => Promise<void>} action
   */
  async function runWithDialogCapture(action) {
    const dialogPromise = page.waitForEvent('dialog', { timeout: 10_000 });
    await Promise.all([
      dialogPromise.then(async (dialog) => {
        runtime.dialogMessages.push(dialog.message());
        await dialog.accept();
      }),
      action(),
    ]);
  }

  if (tc.journey === 'requestOnly') {
    const expectsDialog = tc.expected.assertions.some(
      (a) => a.type === 'dialog' || a.type === 'dialogMatches',
    );
    if (expectsDialog) {
      await runWithDialogCapture(() => fp.requestOtp(email));
    } else {
      await fp.requestOtp(email);
    }
    return;
  }

  // requestThenInspect | fullReset
  await fp.requestOtp(email);
  await expect(fp.otpMessage()).toBeVisible({ timeout: 10_000 });

  if (tc.journey === 'requestThenInspect') {
    return;
  }

  const otp = await resolveOtp(fp, tc);
  const newPassword = tc.inputs?.newPassword ?? account.newPassword;
  account.newPassword = newPassword;

  const expectsDialog = tc.expected.assertions.some(
    (a) => a.type === 'dialog' || a.type === 'dialogMatches',
  );

  const submit = () =>
    fp.submitReset({
      otp: otp ?? '',
      newPassword,
      confirmPassword: tc.inputs?.confirmPassword ?? newPassword,
    });

  if (expectsDialog) {
    await runWithDialogCapture(submit);
  } else {
    await submit();
  }
}

for (const tc of cases) {
  test.describe(`FR-03 Forgot password — ${tc.id}`, () => {
    /** @type {{ email: string, initialPassword: string, newPassword: string }} */
    let account;
    /** @type {{ dialogMessages: string[] }} */
    let runtime;

    test.beforeEach(async () => {
      const stamp = `${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
      account = {
        email: `${tc.id.toLowerCase()}.${stamp}@hw4-fr03.local`,
        initialPassword: 'SeedPass1!',
        newPassword: tc.inputs?.newPassword || 'NewPass1 ',
      };
      runtime = { dialogMessages: [] };

      if (tc.setup.createUser) {
        await registerUser({
          name: `HW4 ${tc.id}`,
          email: account.email,
          password: account.initialPassword,
        });
      }
    });

    test(`${tc.id}: ${tc.purpose}`, async ({ page }) => {
      const fp = new ForgotPasswordPage(page);
      await runJourney(page, fp, tc, account, runtime);
      await applyAssertions(page, fp, tc, account, runtime);
    });
  });
}

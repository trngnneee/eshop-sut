const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const webBaseUrl = process.env.ESHOP_WEB_URL || 'http://127.0.0.1:5173';
const evidenceDir = path.resolve(
  __dirname,
  '..',
  'evidence',
  'technical-preflight',
);

fs.mkdirSync(evidenceDir, { recursive: true });

const runId = new Date().toISOString().replace(/[-:.TZ]/g, '');
const testEmail = `ux.preflight.${runId}@example.com`;
const testPassword = 'EShop123!';
const result = {
  actor: 'TECHNICAL_PREFLIGHT',
  participantEvidence: false,
  label: 'PROVISIONAL',
  startedAt: new Date().toISOString(),
  webBaseUrl,
  testEmail,
  browser: 'chromium',
  assertions: [],
  dialogs: [],
  overall: 'FAILED',
};

function record(name, passed, details) {
  result.assertions.push({ name, passed, details });
  if (!passed) {
    throw new Error(`${name}: ${details}`);
  }
}

async function capture(page, filename) {
  await page.screenshot({
    path: path.join(evidenceDir, filename),
    fullPage: true,
  });
}

(async () => {
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();

    await page.goto(`${webBaseUrl}/register`, { waitUntil: 'networkidle' });
    await page.locator('#register-name').fill('Technical Preflight');
    await page.locator('#register-email').fill(testEmail);
    await page.locator('#register-password').fill(testPassword);
    await page.locator('#register-confirm-password').fill(testPassword);
    await page.getByRole('button', { name: 'Đăng Ký' }).click();
    await page.waitForURL('**/login');
    record('registration_redirects_to_login', true, page.url());
    await capture(page, '01-after-registration.png');

    const loginInputs = page.locator('form input');
    await loginInputs.nth(0).fill(testEmail);
    await loginInputs.nth(1).fill(testPassword);
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.waitForURL((url) => new URL(url).pathname === '/');
    const tokenAfterLogin = await page.evaluate(() => localStorage.getItem('token'));
    record('login_sets_authentication_token', Boolean(tokenAfterLogin), 'Token present after login');
    await capture(page, '02-after-login.png');

    await page.locator('a[href="/profile"]').click();
    await page.waitForURL('**/profile');
    await page.getByRole('heading', { name: 'Hồ sơ của bạn' }).waitFor();
    record('profile_is_reachable', true, page.url());

    const profileInputs = page.locator('form input');
    await profileInputs.nth(1).fill('Technical Preflight Updated');
    await profileInputs.nth(2).fill('0912345678');
    await page.locator('form textarea').fill(
      '123 Đường Kiểm Thử, Phường Bến Nghé, Quận 1, TP.HCM',
    );

    const validPhoneDialogPromise = new Promise((resolve) => {
      page.once('dialog', async (dialog) => {
        const message = dialog.message();
        await dialog.accept();
        resolve(message);
      });
    });
    await page.getByRole('button', { name: 'Cập nhật' }).click();
    const validPhoneMessage = await validPhoneDialogPromise;
    result.dialogs.push({ step: 'valid_phone', message: validPhoneMessage });
    const validPhoneRejected = validPhoneMessage.includes('không hợp lệ');
    result.assertions.push({
      name: 'specification_valid_phone_accepted',
      passed: !validPhoneRejected,
      details: validPhoneMessage,
      expectedBySpecification: true,
      provisionalBugIfFalse: 'PF-02',
    });
    await capture(page, '03-after-valid-phone-attempt.png');

    if (validPhoneRejected) {
      await profileInputs.nth(2).fill('912345678');
      const fallbackDialogPromise = new Promise((resolve) => {
        page.once('dialog', async (dialog) => {
          const message = dialog.message();
          await dialog.accept();
          resolve(message);
        });
      });
      await page.getByRole('button', { name: 'Cập nhật' }).click();
      const fallbackMessage = await fallbackDialogPromise;
      result.dialogs.push({ step: 'fallback_phone', message: fallbackMessage });
      record(
        'fallback_phone_reaches_profile_save',
        fallbackMessage.includes('thành công'),
        fallbackMessage,
      );
    }

    await page.reload({ waitUntil: 'networkidle' });
    await page.getByRole('heading', { name: 'Hồ sơ của bạn' }).waitFor();
    const persistedName = await page.locator('form input').nth(1).inputValue();
    const persistedAddress = await page.locator('form textarea').inputValue();
    record(
      'profile_update_persists_after_reload',
      persistedName === 'Technical Preflight Updated' &&
        persistedAddress.includes('123 Đường Kiểm Thử'),
      `name=${persistedName}; address=${persistedAddress}`,
    );
    await capture(page, '04-profile-after-reload.png');

    await page.getByRole('button', { name: 'Thoát' }).click();
    const tokenAfterLogout = await page.evaluate(() => localStorage.getItem('token'));
    const loggedOutMessageVisible = await page
      .getByText('Vui lòng đăng nhập')
      .isVisible();
    record(
      'logout_removes_token',
      tokenAfterLogout === null,
      `token=${tokenAfterLogout}`,
    );
    record(
      'profile_route_exposes_logged_out_state',
      loggedOutMessageVisible,
      `url=${page.url()}`,
    );
    await capture(page, '05-after-logout.png');

    result.overall = result.assertions.every((item) => item.passed)
      ? 'PASS'
      : 'PASS_WITH_PROVISIONAL_DEFECT';
  } catch (error) {
    result.error = error.stack || String(error);
  } finally {
    result.finishedAt = new Date().toISOString();
    fs.writeFileSync(
      path.join(evidenceDir, 'result.json'),
      `${JSON.stringify(result, null, 2)}\n`,
      'utf8',
    );
    if (browser) {
      await browser.close();
    }
  }

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  process.exitCode = result.overall === 'FAILED' ? 1 : 0;
})();

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const webBaseUrl = process.env.ESHOP_WEB_URL || 'http://127.0.0.1:5173';
const apiBaseUrl = process.env.ESHOP_API_URL || 'http://127.0.0.1:3000';
const isolatedDatabaseAsserted = process.env.ESHOP_ISOLATED_DB === '1';
const evidenceDir = path.resolve(
  __dirname,
  '..',
  'evidence',
  'github-issue-reproduction',
);

fs.mkdirSync(evidenceDir, { recursive: true });

const runId = new Date().toISOString().replace(/[-:.TZ]/g, '');
const testEmail = `github.issue.evidence.${runId}@example.com`;
const testPassword = 'EShop123!';
const passwordPolicyEmail = `github.issue.password-policy.${runId}@example.com`;
const missingSpecialPassword = 'NoSpecial1';
const result = {
  actor: 'FRESH_GITHUB_ISSUE_REPRODUCTION',
  participantEvidence: false,
  safeSyntheticData: true,
  label: 'INDEPENDENT_REPRODUCTION',
  startedAt: new Date().toISOString(),
  webBaseUrl,
  apiBaseUrl,
  isolatedDatabaseAsserted,
  testEmail,
  browser: 'chromium',
  assertions: [],
  dialogs: [],
  evidenceFiles: [],
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
  result.evidenceFiles.push(filename);
}

(async () => {
  let browser;
  try {
    if (!isolatedDatabaseAsserted) {
      throw new Error(
        'Refusing to create synthetic accounts without ESHOP_ISOLATED_DB=1. Run only against a disposable database.',
      );
    }
    browser = await chromium.launch({ headless: true });
    const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
    const page = await context.newPage();

    const weakRegistrationResponse = await context.request.post(
      `${apiBaseUrl}/api/register`,
      {
        data: {
          name: 'Synthetic Password Policy Test',
          email: passwordPolicyEmail,
          password: missingSpecialPassword,
          confirm_password: missingSpecialPassword,
        },
      },
    );
    const weakRegistrationStatus = weakRegistrationResponse.status();
    const weakRegistrationBody = await weakRegistrationResponse
      .json()
      .catch(() => ({ nonJsonResponse: true }));
    const weakLoginResponse = await context.request.post(`${apiBaseUrl}/api/login`, {
      data: {
        email: passwordPolicyEmail,
        password: missingSpecialPassword,
      },
    });
    const weakAccountCanLogin = weakLoginResponse.ok();
    const weakRegistrationRejected = weakRegistrationStatus >= 400;
    result.assertions.push({
      name: 'registration_api_rejects_missing_special_character',
      passed: weakRegistrationRejected && !weakAccountCanLogin,
      details: `expected register=4xx; actual register=${weakRegistrationStatus}; login=${weakLoginResponse.status()}`,
      requirement: 'FR-01',
      partition: 'INVALID_MISSING_ALLOWED_SPECIAL_CHARACTER',
      expectedAllowedSpecialSet: '@ $ ! % * ? &',
      actualResponse: weakRegistrationBody,
      accountCanLogin: weakAccountCanLogin,
      participantEvidence: false,
      canonicalDuplicate: 'https://github.com/trngnneee/eshop-sut/issues/118',
      provisionalBugIfFalse: 'BUG-REG-PASSWORD-POLICY-01',
    });
    await page.goto(`${webBaseUrl}/register`, { waitUntil: 'networkidle' });
    await page.evaluate(
      ({ registerStatus, loginStatus }) => {
        const banner = document.createElement('div');
        banner.id = 'password-policy-api-evidence';
        banner.textContent =
          `Independent API test with synthetic data: FR-01 requires one special character from @ $ ! % * ? &. ` +
          `The tested password omitted that class. Expected registration 4xx; observed ${registerStatus}. ` +
          `Login with the newly created synthetic account returned ${loginStatus}.`;
        banner.setAttribute(
          'style',
          'position:fixed;top:12px;right:12px;z-index:2147483647;max-width:620px;padding:16px;border:3px solid #b91c1c;border-radius:8px;background:#fef2f2;color:#7f1d1d;font:700 16px/1.4 Segoe UI,Arial,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.25)',
        );
        document.body.appendChild(banner);
      },
      {
        registerStatus: weakRegistrationStatus,
        loginStatus: weakLoginResponse.status(),
      },
    );
    await capture(page, 'BUG-REG-PASSWORD-POLICY-01-safe-reproduction.png');

    await page.goto(`${webBaseUrl}/login`, { waitUntil: 'networkidle' });
    const evidenceLoginInputs = page.locator('form input');
    await evidenceLoginInputs.nth(1).fill('NotARealCredential!42');
    const observedPasswordInputType = await evidenceLoginInputs.nth(1).getAttribute('type');
    result.assertions.push({
      name: 'login_password_masked_by_default',
      passed: observedPasswordInputType === 'password',
      details: `observed input type=${observedPasswordInputType}`,
      expectedBySecurityBaseline: true,
      provisionalBugIfFalse: 'BUG-AUTH-PLAINTEXT-01',
    });
    await capture(page, 'BUG-AUTH-PLAINTEXT-01-safe-reproduction.png');
    await evidenceLoginInputs.nth(1).fill('');

    await page.goto(`${webBaseUrl}/register`, { waitUntil: 'networkidle' });
    await page.locator('#register-name').fill('Technical Preflight');
    await page.locator('#register-email').fill(testEmail);
    await page.locator('#register-password').fill(testPassword);
    await page.locator('#register-confirm-password').fill(testPassword);
    await page.getByRole('button', { name: 'Đăng Ký' }).click();
    await page.waitForURL('**/login');
    record('registration_redirects_to_login', true, page.url());

    const loginInputs = page.locator('form input');
    await loginInputs.nth(0).fill(testEmail);
    await loginInputs.nth(1).fill(testPassword);
    await page.getByRole('button', { name: 'Sign In' }).click();
    await page.waitForURL((url) => new URL(url).pathname === '/');
    const tokenAfterLogin = await page.evaluate(() => localStorage.getItem('token'));
    record('login_sets_authentication_token', Boolean(tokenAfterLogin), 'Token present after login');

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
      provisionalBugIfFalse: 'BUG-PF-02',
    });
    await page.evaluate((message) => {
      const banner = document.createElement('div');
      banner.id = 'test-harness-alert-evidence';
      banner.textContent = `Test harness captured native alert using synthetic data: ${message}`;
      banner.setAttribute('style', 'position:fixed;top:12px;right:12px;z-index:2147483647;max-width:520px;padding:16px;border:3px solid #b91c1c;border-radius:8px;background:#fef2f2;color:#7f1d1d;font:700 16px/1.4 Segoe UI,Arial,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.25)');
      document.body.appendChild(banner);
    }, validPhoneMessage);
    await capture(page, 'BUG-PF-02-safe-reproduction.png');

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

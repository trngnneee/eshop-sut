// @ts-check
const { test, expect } = require('@playwright/test');
const { loadFeatureCases } = require('../helpers/load-test-data');
const {
  registerUser,
  loginUser,
  checkoutApi,
  getMyOrders,
} = require('../helpers/auth-api');
const {
  CheckoutPage,
  CartPage,
  HomePage,
} = require('../pages/CheckoutPage');

const { cases } = loadFeatureCases('fr08-checkout.json', {
  minCases: 12,
  feature: 'FR-08',
});

/**
 * Assertion patterns (HW04 Task 1 — ≥3 distinct):
 * 1. Visibility / hidden
 * 2. Text content
 * 3. URL / navigation
 * 4. Collection size (toHaveCount / count)
 * 5. Attribute / readonly + plain API values
 */

/**
 * @param {import('@playwright/test').Page} page
 * @param {string} token
 */
async function injectAuthToken(page, token) {
  await page.goto('/');
  await page.evaluate((t) => {
    localStorage.setItem('token', t);
  }, token);
  await page.reload();
  await expect(page.getByRole('button', { name: /Thoát|Đăng xuất/i })).toBeVisible({
    timeout: 15_000,
  });
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {any} tc
 * @param {{ email: string, password: string, token: string | null, cartTotal: number }} session
 * @param {{ dialogMessages: string[], apiStatus?: number }} runtime
 */
async function runJourney(page, tc, session, runtime) {
  const checkout = new CheckoutPage(page);
  const cart = new CartPage(page);
  const home = new HomePage(page);

  if (tc.journey === 'apiCheckoutUnauthorized') {
    const result = await checkoutApi('', {
      total_amount: tc.inputs?.total_amount ?? 1,
      shipping_address: 'HW4 FR-08',
      items: [],
    });
    runtime.apiStatus = result.status;
    return;
  }

  if (tc.setup.login && session.token) {
    await injectAuthToken(page, session.token);
  } else {
    await page.goto('/');
    await page.evaluate(() => localStorage.removeItem('token'));
    await page.reload();
  }

  if (tc.setup.seedCartCount > 0) {
    const added = await home.addFirstNProducts(tc.setup.seedCartCount);
    expect(added).toBeGreaterThanOrEqual(tc.setup.seedCartCount);
    await cart.waitForItemRows(tc.setup.seedCartCount);
  }

  if (tc.journey === 'guestCartCheckout') {
    await cart.gotoSpa();
    await expect(cart.checkoutButton()).toBeVisible();
    const dialogPromise = page.waitForEvent('dialog', { timeout: 10_000 });
    await Promise.all([
      dialogPromise.then(async (dialog) => {
        runtime.dialogMessages.push(dialog.message());
        await dialog.accept();
      }),
      cart.clickCheckout(),
    ]);
    return;
  }

  if (tc.journey === 'guestDirectCheckout') {
    await checkout.gotoHard();
    return;
  }

  if (tc.journey === 'emptyCartCheckout') {
    await cart.gotoSpa();
    // Spec: empty cart must not complete payment. Try hard navigation to checkout.
    await checkout.gotoHard();
    if (await checkout.confirmButton().count()) {
      await checkout.confirmPayment();
      await page
        .getByRole('heading', { name: /Thanh toán thành công/i })
        .waitFor({ state: 'visible', timeout: 3_000 })
        .catch(() => {});
    }
    return;
  }

  if (tc.journey === 'inspectCheckout') {
    await checkout.gotoSpaFromCart(cart);
    await expect(checkout.heading()).toBeVisible({ timeout: 10_000 });
    await expect(checkout.productLines().first()).toBeVisible({ timeout: 10_000 });
    session.cartTotal = await checkout.readDisplayedTotal();
    expect(session.cartTotal).toBeGreaterThan(0);
    return;
  }

  if (tc.journey === 'tamperTotalCheckout') {
    await checkout.gotoSpaFromCart(cart);
    await expect(checkout.heading()).toBeVisible({ timeout: 10_000 });
    await expect(checkout.productLines().first()).toBeVisible({ timeout: 10_000 });
    session.cartTotal = await checkout.readDisplayedTotal();
    expect(session.cartTotal).toBeGreaterThan(0);
    await checkout.setTotal(tc.inputs?.tamperedTotal ?? 1);
    await checkout.confirmPayment();
    await expect(checkout.successHeading()).toBeVisible({ timeout: 15_000 });
    return;
  }

  if (tc.journey === 'fullCheckout') {
    await checkout.gotoSpaFromCart(cart);
    await expect(checkout.heading()).toBeVisible({ timeout: 10_000 });
    await expect(checkout.productLines().first()).toBeVisible({ timeout: 10_000 });
    session.cartTotal = await checkout.readDisplayedTotal();
    expect(session.cartTotal).toBeGreaterThan(0);
    await checkout.confirmPayment();
    await expect(checkout.successHeading()).toBeVisible({ timeout: 15_000 });
    return;
  }

  throw new Error(`${tc.id}: unsupported journey ${tc.journey}`);
}

/**
 * @param {import('@playwright/test').Page} page
 * @param {any} tc
 * @param {{ email: string, password: string, token: string | null, cartTotal: number }} session
 * @param {{ dialogMessages: string[], apiStatus?: number }} runtime
 */
async function applyAssertions(page, tc, session, runtime) {
  const checkout = new CheckoutPage(page);
  const cart = new CartPage(page);

  for (const assertion of tc.expected.assertions) {
    switch (assertion.type) {
      case 'visible':
        await expect(checkout.target(assertion.target)).toBeVisible();
        break;
      case 'hidden':
        await expect(checkout.target(assertion.target)).toBeHidden();
        break;
      case 'containText':
        await expect(checkout.target(assertion.target)).toContainText(
          assertion.value,
        );
        break;
      case 'attribute':
        await expect(checkout.target(assertion.target)).toHaveAttribute(
          assertion.name,
          assertion.value,
        );
        break;
      case 'dialogMatches': {
        const last = runtime.dialogMessages.at(-1) ?? '';
        expect(last).toMatch(new RegExp(assertion.pattern, 'i'));
        break;
      }
      case 'url':
        await expect(page).toHaveURL(new RegExp(assertion.pattern));
        break;
      case 'count': {
        const locator = checkout.target(assertion.target);
        const n = await locator.count();
        expect(n).toBeGreaterThanOrEqual(assertion.min);
        break;
      }
      case 'totalReadonly': {
        const input = checkout.totalInput();
        // Spec: total not user-editable — editable number input is a defect.
        if ((await input.count()) === 0) {
          expect(true).toBe(true);
          break;
        }
        const readonly = await input.getAttribute('readonly');
        const disabled = await input.isDisabled();
        expect(
          readonly !== null || disabled,
          'FR-08: payment total must not be directly editable',
        ).toBeTruthy();
        break;
      }
      case 'cartEmpty': {
        // SPA navigate so we observe post-checkout cart state (not a remount).
        await page.getByRole('link', { name: /Giỏ hàng/i }).click();
        await page.waitForURL(/\/cart/);
        await expect(cart.emptyMessage()).toBeVisible({ timeout: 10_000 });
        break;
      }
      case 'orderTotalEquals': {
        if (!session.token) throw new Error(`${tc.id}: missing token for order check`);
        const orders = await getMyOrders(session.token);
        expect(orders.status).toBe(200);
        expect(Array.isArray(orders.body) && orders.body.length > 0).toBeTruthy();
        const latest = orders.body[0];
        expect(Number(latest.total_amount)).toBe(Number(session.cartTotal));
        break;
      }
      case 'apiStatus':
        expect(runtime.apiStatus).toBe(assertion.status);
        break;
      default:
        throw new Error(`${tc.id}: unsupported assertion ${assertion.type}`);
    }
  }
}

for (const tc of cases) {
  test.describe(`FR-08 Checkout — ${tc.id}`, () => {
    /** @type {{ email: string, password: string, token: string | null, cartTotal: number }} */
    let session;
    /** @type {{ dialogMessages: string[], apiStatus?: number }} */
    let runtime;

    test.beforeEach(async () => {
      const stamp = `${Date.now()}-${Math.floor(Math.random() * 1e6)}`;
      session = {
        email: `${tc.id.toLowerCase()}.${stamp}@hw4-fr08.local`,
        password: 'SeedPass1!',
        token: null,
        cartTotal: 0,
      };
      runtime = { dialogMessages: [] };

      if (tc.setup.login || tc.journey === 'tamperTotalCheckout') {
        await registerUser({
          name: `HW4 ${tc.id}`,
          email: session.email,
          password: session.password,
        });
        const login = await loginUser({
          email: session.email,
          password: session.password,
        });
        expect(login.status).toBe(200);
        session.token = login.body.token;
      }
    });

    test(`${tc.id}: ${tc.purpose}`, async ({ page }) => {
      await runJourney(page, tc, session, runtime);
      await applyAssertions(page, tc, session, runtime);
    });
  });
}

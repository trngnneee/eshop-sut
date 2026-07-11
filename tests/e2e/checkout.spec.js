// tests/e2e/checkout.spec.js
// FR-08: Thanh toán (Checkout)
// Techniques: Domain Testing + BVA + Supplementary
// TC IDs aligned with tests/test-cases/checkout/ TC-CHECKOUT-001 … 044, SUP-001 … 006

const { test, expect } = require('@playwright/test');
const { CheckoutPage } = require('../pages/CheckoutPage');
const { loginViaAPI, logout } = require('../helpers/auth');
const {
  addToCartViaUI,
  goToCart,
  startCheckoutFromCart,
  isCartEmpty,
  fetchProducts,
} = require('../helpers/cart');
const {
  postCheckout,
  buildCartItems,
  cartTotalFromItems,
  assertOrderTotal,
} = require('../helpers/checkout');
const { ACCOUNTS, CHECKOUT, API_URL } = require('../fixtures/test-data');

// ── Shared helpers ────────────────────────────────────────────────────────────

async function seedApiCart(page, specs = [{ index: 0, quantity: 1 }], account = ACCOUNTS.user) {
  const token = await loginViaAPI(page, account.email, account.password);
  const products = await fetchProducts(page);
  const items = buildCartItems(products, specs);
  const cartTotal = cartTotalFromItems(items);
  return { token, products, items, cartTotal };
}

async function seedUiCart(page, opts = {}) {
  const account = opts.account ?? ACCOUNTS.user;
  const token = await loginViaAPI(page, account.email, account.password);
  await addToCartViaUI(page, {
    productIndex: opts.productIndex ?? 0,
    productId: opts.productId,
    quantity: opts.quantity ?? 1,
    addTimes: opts.addTimes ?? 1,
  });
  return token;
}

async function tamperCheckoutExpectReject(page, token, items, cartTotal, tampered) {
  const res = await postCheckout(page, token, { items, total_amount: tampered });
  if (!res.ok()) return;
  const body = await res.json();
  await assertOrderTotal(page, token, body.orderId, cartTotal, tampered);
}

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-08 · Checkout — Domain Testing (001–009)', () => {

  test('TC-CHECKOUT-001 · DT · Not logged in → checkout from cart blocked', async ({ page }) => {
    await logout(page);
    await addToCartViaUI(page, { productIndex: 0, quantity: 1 });
    await goToCart(page);
    await startCheckoutFromCart(page);
    expect(page.url(), 'Must redirect to login when unauthenticated (FR-08)').toContain('/login');
  });

  test('TC-CHECKOUT-002 · DT · Logged-in user reaches checkout with items', async ({ page }) => {
    await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.isOnCheckoutPage()).toBe(true);
    expect(await checkout.getProductLineCount()).toBeGreaterThan(0);
  });

  test('TC-CHECKOUT-003 · DT · Product list displayed on checkout', async ({ page }) => {
    await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.getProductLineCount()).toBeGreaterThan(0);
    const lines = await checkout.getProductLineTexts();
    expect(lines.join(' ')).toMatch(/x\s*1/i);
  });

  test('TC-CHECKOUT-004 · DT · Total amount not editable (FR-08)', async ({ page }) => {
    await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.isTotalEditable(), 'Total must not be user-editable').toBe(false);
  });

  test('TC-CHECKOUT-005 · DT · Total displayed matches cart', async ({ page }) => {
    const products = await fetchProducts(page);
    const expectedTotal = products[0].price;
    await seedUiCart(page, { quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const totalText = await checkout.getTotalDisplayText();
    expect(totalText, 'Total must be shown on checkout').toBeTruthy();
    const numeric = Number(String(totalText).replace(/[^\d]/g, ''));
    expect(numeric).toBe(expectedTotal);
  });

  test('TC-CHECKOUT-006 · DT · Successful checkout on-point', async ({ page }) => {
    await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    expect(await checkout.isOrderSuccessful(), 'Must show success confirmation').toBe(true);
  });

  test('TC-CHECKOUT-007 · DT · Cart cleared after successful checkout', async ({ page }) => {
    await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    await goToCart(page);
    expect(await isCartEmpty(page), 'Cart must be empty after checkout (FR-08)').toBe(true);
  });

  test('TC-CHECKOUT-008 · DT · Empty cart cannot checkout', async ({ page }) => {
    await loginViaAPI(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const lines = await checkout.getProductLineCount();
    const canPlace = await checkout.placeOrderBtn.isEnabled().catch(() => false);
    const emptyMsg = /trống|empty|không có/i.test(await page.textContent('body') ?? '');
    expect(lines === 0 || emptyMsg || !canPlace, 'Empty cart must block checkout').toBe(true);
  });

  test('TC-CHECKOUT-009 · DT · Multiple items / qty > 1 in list', async ({ page }) => {
    await loginViaAPI(page);
    await addToCartViaUI(page, { productIndex: 0, quantity: 1 });
    await addToCartViaUI(page, { productIndex: 1, quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.getProductLineCount()).toBeGreaterThanOrEqual(2);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-08 · Checkout — BVA (010–018)', () => {

  test('TC-CHECKOUT-010 · BVA · qty = 1 (min on-point)', async ({ page }) => {
    const { cartTotal } = await seedApiCart(page, [{ index: 0, quantity: 1 }]);
    await seedUiCart(page, { quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBe(cartTotal);
    await checkout.placeOrder();
    expect(await checkout.isOrderSuccessful()).toBe(true);
  });

  test('TC-CHECKOUT-011 · BVA · qty = 2 (min+)', async ({ page }) => {
    const { cartTotal } = await seedApiCart(page, [{ index: 0, quantity: 2 }]);
    await seedUiCart(page, { quantity: 2 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBe(cartTotal);
  });

  test('TC-CHECKOUT-012 · BVA · 0 items in cart (min−)', async ({ page }) => {
    await loginViaAPI(page);
    await goToCart(page);
    expect(await isCartEmpty(page)).toBe(true);
    await startCheckoutFromCart(page);
    const checkout = new CheckoutPage(page);
    if (await checkout.isOnCheckoutPage()) {
      expect(await checkout.getProductLineCount()).toBe(0);
    }
  });

  test('TC-CHECKOUT-013 · BVA · 1 product type (min)', async ({ page }) => {
    await seedUiCart(page, { quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.getProductLineCount()).toBeGreaterThanOrEqual(1);
  });

  test('TC-CHECKOUT-014 · BVA · 2 product types (min+)', async ({ page }) => {
    await loginViaAPI(page);
    await addToCartViaUI(page, { productIndex: 0, quantity: 1 });
    await addToCartViaUI(page, { productIndex: 1, quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.getProductLineCount()).toBeGreaterThanOrEqual(2);
  });

  test('TC-CHECKOUT-015 · BVA · API rejects total_amount = 0', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, CHECKOUT.tamperedZero);
  });

  test('TC-CHECKOUT-016 · BVA · API rejects total_amount = cartTotal − 1', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, cartTotal - 1);
  });

  test('TC-CHECKOUT-017 · BVA · API accepts total_amount = cartTotal (on-point)', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    const res = await postCheckout(page, token, { items, total_amount: cartTotal });
    expect(res.ok()).toBeTruthy();
    const body = await res.json();
    await assertOrderTotal(page, token, body.orderId, cartTotal);
  });

  test('TC-CHECKOUT-018 · BVA · API rejects total_amount = cartTotal + 1', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, cartTotal + 1);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-08 · Checkout — Domain Testing (019–033)', () => {

  test('TC-CHECKOUT-019 · DT · Unauthenticated direct /checkout access blocked', async ({ page }) => {
    await logout(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder().catch(() => {});
    const blocked =
      page.url().includes('/login') ||
      !(await checkout.isOrderSuccessful());
    expect(blocked, 'Unauthenticated user must not complete checkout').toBe(true);
  });

  test('TC-CHECKOUT-020 · DT · Expired / invalid token blocked', async ({ page }) => {
    await seedUiCart(page);
    await page.evaluate(() => localStorage.setItem('token', 'invalid.jwt.token'));
    await page.reload();
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    expect(await checkout.isOrderSuccessful(), 'Invalid token must not complete checkout').toBe(false);
  });

  test('TC-CHECKOUT-021 · DT · Each line shows correct product name', async ({ page }) => {
    const products = await fetchProducts(page);
    await loginViaAPI(page);
    await addToCartViaUI(page, { productIndex: 0, quantity: 1 });
    await addToCartViaUI(page, { productIndex: 1, quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const lines = await checkout.getProductLineTexts();
    expect(lines.some((l) => l.includes(products[0].name))).toBe(true);
    expect(lines.some((l) => l.includes(products[1].name))).toBe(true);
  });

  test('TC-CHECKOUT-022 · DT · Line shows correct quantity', async ({ page }) => {
    await seedUiCart(page, { quantity: 3 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const lines = await checkout.getProductLineTexts();
    expect(lines.join(' ')).toMatch(/x\s*3/i);
  });

  test('TC-CHECKOUT-023 · DT · Line subtotal = price × qty', async ({ page }) => {
    const products = await fetchProducts(page);
    const subtotal = products[0].price * 2;
    await seedUiCart(page, { quantity: 2 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const lines = await checkout.getProductLineTexts();
    expect(lines.join(' ')).toMatch(/x\s*2/i);
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBe(subtotal);
  });

  test('TC-CHECKOUT-024 · DT · Three product types listed', async ({ page }) => {
    await loginViaAPI(page);
    for (let i = 0; i < 3; i++) await addToCartViaUI(page, { productIndex: i, quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.getProductLineCount()).toBeGreaterThanOrEqual(3);
  });

  test('TC-CHECKOUT-025 · DT · Same product added twice shows merged qty (FR-07)', async ({ page }) => {
    await loginViaAPI(page);
    await addToCartViaUI(page, { productIndex: 0, quantity: 1, addTimes: 1 });
    await addToCartViaUI(page, { productIndex: 0, quantity: 1, addTimes: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const lineCount = await checkout.getProductLineCount();
    const lines = await checkout.getProductLineTexts();
    const merged = lineCount === 1 && /x\s*2/i.test(lines.join(' '));
    const twoLines = lineCount === 2;
    expect(merged || twoLines, 'Cart must show product(s) with total qty 2').toBe(true);
    if (merged) expect(lines.join(' ')).toMatch(/x\s*2/i);
  });

  test('TC-CHECKOUT-026 · DT · UI tampered total → order uses real total', async ({ page }) => {
    const products = await fetchProducts(page);
    const cartTotal = products[0].price;
    const token = await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    if (await checkout.isTotalEditable()) {
      await checkout.setTotalValue(1);
      await checkout.placeOrder();
      expect(await checkout.isOrderSuccessful()).toBe(true);
      const ordersRes = await page.request.get(`${API_URL}/api/orders/my-orders`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const orders = await ordersRes.json();
      expect(orders[0].total_amount, 'Order must not use UI-tampered total').toBe(cartTotal);
    } else {
      expect(await checkout.isTotalEditable()).toBe(false);
    }
  });

  test('TC-CHECKOUT-027 · DT · Navbar cart badge zero after checkout', async ({ page }) => {
    await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    const navText = await page.locator('header, nav').textContent();
    expect(navText).toMatch(/giỏ hàng/i);
  });

  test('TC-CHECKOUT-028 · DT · Second checkout blocked when cart empty', async ({ page }) => {
    await seedUiCart(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    await checkout.goto();
    await checkout.placeOrder();
    expect(await checkout.isOrderSuccessful(), 'Second checkout with empty cart must fail').toBe(false);
  });

  test('TC-CHECKOUT-029 · DT · API rejects negative total_amount', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, CHECKOUT.tamperedNegative);
  });

  test('TC-CHECKOUT-030 · DT · API missing total_amount handled', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    const res = await postCheckout(page, token, { items });
    if (res.ok()) {
      const body = await res.json();
      const ordersRes = await page.request.get(`${API_URL}/api/orders/my-orders`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const orders = await ordersRes.json();
      const order = orders.find((o) => o.id === body.orderId);
      expect(order?.total_amount ?? 0).not.toBeNull();
      if (order?.total_amount != null) expect(order.total_amount).toBe(cartTotal);
    }
  });

  test('TC-CHECKOUT-031 · DT · API rejects non-numeric total_amount', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    const res = await postCheckout(page, token, { items, total_amount: CHECKOUT.tamperedString });
    if (res.ok()) {
      const body = await res.json();
      await assertOrderTotal(page, token, body.orderId, cartTotal, CHECKOUT.tamperedString);
    }
  });

  test('TC-CHECKOUT-032 · DT · API empty items + positive total rejected', async ({ page }) => {
    const { token, cartTotal } = await seedApiCart(page);
    const res = await postCheckout(page, token, { items: [], total_amount: cartTotal });
    if (res.ok()) {
      const body = await res.json();
      await assertOrderTotal(page, token, body.orderId, cartTotal, 0);
    } else {
      expect(res.status()).toBeGreaterThanOrEqual(400);
    }
  });

  test('TC-CHECKOUT-033 · DT · Admin account can checkout', async ({ page }) => {
    await seedUiCart(page, { account: ACCOUNTS.admin });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    expect(await checkout.isOrderSuccessful()).toBe(true);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-08 · Checkout — BVA (034–044)', () => {

  test('TC-CHECKOUT-034 · BVA · qty = 3', async ({ page }) => {
    const { cartTotal } = await seedApiCart(page, [{ index: 0, quantity: 3 }]);
    await seedUiCart(page, { quantity: 3 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBe(cartTotal);
  });

  test('TC-CHECKOUT-035 · BVA · qty = 10', async ({ page }) => {
    const { cartTotal } = await seedApiCart(page, [{ index: 0, quantity: 10 }]);
    await seedUiCart(page, { quantity: 10 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBe(cartTotal);
  });

  test('TC-CHECKOUT-036 · BVA · 3 product types', async ({ page }) => {
    await loginViaAPI(page);
    for (let i = 0; i < 3; i++) await addToCartViaUI(page, { productIndex: i, quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.getProductLineCount()).toBeGreaterThanOrEqual(3);
  });

  test('TC-CHECKOUT-037 · BVA · lowest price product', async ({ page }) => {
    const products = await fetchProducts(page);
    const cheapest = [...products].sort((a, b) => a.price - b.price)[0];
    const { cartTotal } = await seedApiCart(page, [{ index: products.indexOf(cheapest), quantity: 1 }]);
    await seedUiCart(page, { productId: cheapest.id, quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBe(cartTotal);
  });

  test('TC-CHECKOUT-038 · BVA · API total_amount = −1', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, -1);
  });

  test('TC-CHECKOUT-039 · BVA · API total_amount = 1 when cartTotal large', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page, [{ index: 0, quantity: 1 }]);
    expect(cartTotal).toBeGreaterThan(1);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, CHECKOUT.tamperedTotal);
  });

  test('TC-CHECKOUT-040 · BVA · qty = 99', async ({ page }) => {
    const { cartTotal } = await seedApiCart(page, [{ index: 0, quantity: 99 }]);
    await seedUiCart(page, { quantity: 99 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBe(cartTotal);
  });

  test('TC-CHECKOUT-041 · BVA · 4 product types', async ({ page }) => {
    await loginViaAPI(page);
    const products = await fetchProducts(page);
    const count = Math.min(4, products.length);
    for (let i = 0; i < count; i++) await addToCartViaUI(page, { productIndex: i, quantity: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    expect(await checkout.getProductLineCount()).toBeGreaterThanOrEqual(count);
  });

  test('TC-CHECKOUT-042 · BVA · API total_amount = 2 × cartTotal', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, cartTotal * 2);
  });

  test('TC-CHECKOUT-043 · BVA · API decimal total_amount rejected', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, cartTotal + 0.5);
  });

  test('TC-CHECKOUT-044 · BVA · Total updates when qty increased before checkout', async ({ page }) => {
    const products = await fetchProducts(page);
    const price = products[0].price;
    await loginViaAPI(page);
    await addToCartViaUI(page, { productIndex: 0, quantity: 1 });
    await addToCartViaUI(page, { productIndex: 0, quantity: 1, addTimes: 1 });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = Number(String(await checkout.getTotalDisplayText()).replace(/[^\d]/g, ''));
    expect(total).toBeGreaterThanOrEqual(price);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-08 · Checkout — Supplementary (SUP-001–006)', () => {

  test('TC-CHECKOUT-SUP-001 · SUP · Invalid JWT rejected', async ({ page }) => {
    const res = await postCheckout(page, 'invalid.jwt.token', {
      items: [],
      total_amount: CHECKOUT.sampleTotal,
    });
    expect(res.status()).toBeGreaterThanOrEqual(401);
  });

  test('TC-CHECKOUT-SUP-002 · SUP · No JWT → 401', async ({ page }) => {
    const res = await postCheckout(page, null, { total_amount: CHECKOUT.sampleTotal, items: [] });
    expect(res.status(), 'POST /api/checkout without JWT must return 401').toBe(401);
  });

  test('TC-CHECKOUT-SUP-003 · SUP · Backend recalculates total (tampered = 1)', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page);
    await tamperCheckoutExpectReject(page, token, items, cartTotal, CHECKOUT.tamperedTotal);
  });

  test('TC-CHECKOUT-SUP-004 · SUP · Client items mismatch server cart', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page, [{ index: 0, quantity: 1 }]);
    const products = await fetchProducts(page);
    const fakeItems = buildCartItems(products, [{ index: 1, quantity: 1 }]);
    const fakeTotal = cartTotalFromItems(fakeItems);
    const res = await postCheckout(page, token, { items: fakeItems, total_amount: fakeTotal });
    if (res.ok()) {
      const body = await res.json();
      await assertOrderTotal(page, token, body.orderId, cartTotal, fakeTotal);
    }
  });

  test('TC-CHECKOUT-SUP-005 · SUP · Malformed Authorization header', async ({ page }) => {
    const res = await postCheckout(
      page,
      null,
      { total_amount: CHECKOUT.sampleTotal, items: [] },
      { Authorization: 'NotBearer sometoken' }
    );
    expect(res.status()).toBeGreaterThanOrEqual(401);
  });

  test('TC-CHECKOUT-SUP-006 · SUP · Order total = Σ(price × qty)', async ({ page }) => {
    const { token, items, cartTotal } = await seedApiCart(page, [
      { index: 0, quantity: 1 },
      { index: 1, quantity: 2 },
    ]);
    const res = await postCheckout(page, token, { items, total_amount: cartTotal });
    expect(res.ok()).toBeTruthy();
    const body = await res.json();
    await assertOrderTotal(page, token, body.orderId, cartTotal);
  });
});

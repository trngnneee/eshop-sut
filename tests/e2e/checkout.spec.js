// tests/e2e/checkout.spec.js
// FR-08: Checkout
// Techniques: Domain Testing (Equivalence Partitioning) + BVA
// TC IDs: TC-CHECKOUT-001 … TC-CHECKOUT-012

const { test, expect } = require('@playwright/test');
const { CheckoutPage } = require('../pages/CheckoutPage');
const { loginViaAPI, loginViaUI } = require('../helpers/auth');
const { addToCartViaAPI, getFirstProductId } = require('../helpers/cart');
const { ACCOUNTS, API_URL, CHECKOUT } = require('../fixtures/test-data');

// ── Shared setup helpers ───────────────────────────────────────────────────
async function loginAndAddOneItem(page) {
  const token = await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
  const pid   = await getFirstProductId(page);
  await addToCartViaAPI(page, token, pid, 1);
  return token;
}

async function loginAndAddHighValueItems(page) {
  const token = await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
  const pid   = await getFirstProductId(page);
  await addToCartViaAPI(page, token, pid, 10);   // enough quantity for coupon threshold tests
  return token;
}

test.describe('FR-08 · Checkout', () => {

  // ── Domain Testing: C4 — Unauthenticated access blocked ──────────────────
  test('TC-CHECKOUT-001 · DT · Not logged in → /checkout redirects to /login', async ({ page }) => {
    // Clear any residual session
    await page.goto('/');
    await page.evaluate(() => { localStorage.clear(); sessionStorage.clear(); });
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const accessible = await checkout.isAccessible();
    expect(accessible, 'Unauthenticated user must not reach /checkout — must be redirected').toBe(false);
  });

  // ── Domain Testing: Valid domain — logged-in user can access checkout ─────
  test('TC-CHECKOUT-002 · DT · Logged-in user with items → checkout page loads', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const accessible = await checkout.isAccessible();
    expect(accessible, 'Logged-in user with cart items must be able to reach /checkout').toBe(true);
  });

  // ── Domain Testing: Checkout displays cart items ──────────────────────────
  test('TC-CHECKOUT-003 · DT · Checkout page shows ordered items list (FR-08)', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const count = await checkout.getItemCount();
    expect(count, 'Checkout page must display the list of items being ordered').toBeGreaterThan(0);
  });

  // ── Domain Testing: Total is auto-calculated, not user-editable ──────────
  test('TC-CHECKOUT-004 · DT · Total amount field is read-only / not an editable input (FR-08)', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const editable = await checkout.isTotalEditable();
    expect(editable, 'Total amount must NOT be editable by the user (FR-08 spec)').toBe(false);
  });

  // ── Security: Backend recalculates total — client-sent amount rejected ────
  test('TC-CHECKOUT-005 · SEC · Tampered total_amount=1 sent to API → backend uses real total', async ({ page }) => {
    const token = await loginAndAddOneItem(page);
    const response = await page.request.post(`${API_URL}/api/orders`, {
      headers: { Authorization: `Bearer ${token}` },
      data: { total_amount: CHECKOUT.tamperedTotal },   // tampered: 1₫
    });
    if (response.ok()) {
      const body = await response.json();
      const saved = body.data?.total_amount ?? body.total_amount ?? body.order?.total_amount;
      if (saved !== undefined) {
        expect(saved, 'Backend must NOT accept client-supplied total_amount (FR-08 security)').not.toBe(1);
      }
    }
    // HTTP 400/422 is also a correct result — backend rejected the tampered value
  });

  // ── Domain Testing: Valid order placement → success confirmation ──────────
  test('TC-CHECKOUT-006 · DT · Logged-in user places order → success message shown', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    const ok = await checkout.isOrderSuccessful();
    expect(ok, 'Successfully placed order must show a confirmation message or redirect').toBe(true);
  });

  // ── Domain Testing: Cart is cleared after successful order ────────────────
  test('TC-CHECKOUT-007 · DT · After successful order → cart is emptied (FR-08)', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    // Navigate to cart and verify it is empty
    await page.goto('/cart');
    await page.waitForLoadState('networkidle');
    const body = await page.textContent('body');
    // Cart should be empty — show empty state text or 0 items
    const cartItems = page.locator('tbody tr, [class*="cart-item"], [class*="CartItem"]');
    const itemCount = await cartItems.count();
    const hasEmptyMsg = /trống|empty|chưa có/i.test(body);
    expect(
      itemCount === 0 || hasEmptyMsg,
      'Cart must be cleared after a successful order (FR-08)'
    ).toBe(true);
  });

  // ── Domain Testing: Checkout from empty cart ──────────────────────────────
  test('TC-CHECKOUT-008 · DT · Checkout with empty cart → blocked or warned', async ({ page }) => {
    // Login but do NOT add any items
    await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const body = await page.textContent('body');
    // Either redirected away, or an empty-state warning is shown
    const isBlocked = !page.url().includes('/checkout') ||
                      /trống|empty|không có sản phẩm/i.test(body);
    // A place-order button should be absent or disabled when cart is empty
    const placeBtn = page.locator('button:has-text("Đặt hàng"), button:has-text("Thanh toán")');
    const btnCount = await placeBtn.count();
    const btnDisabled = btnCount > 0 ? await placeBtn.first().isDisabled() : true;
    expect(
      isBlocked || btnDisabled,
      'Checkout with empty cart must not allow order placement'
    ).toBe(true);
  });

  // ── BVA: Minimum viable order (1 item, qty=1) ────────────────────────────
  test('TC-CHECKOUT-009 · BVA · Order with exactly 1 item, qty=1 (minimum) → succeeds', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const count = await checkout.getItemCount();
    expect(count, 'Checkout with 1 item (minimum) must display the item').toBeGreaterThan(0);
    await checkout.placeOrder();
    const ok = await checkout.isOrderSuccessful();
    expect(ok, 'Order with 1 item at qty=1 must be accepted').toBe(true);
  });

  // ── Domain Testing: Correct total displayed before placing order ──────────
  test('TC-CHECKOUT-010 · DT · Total amount is displayed on checkout page', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    const total = await checkout.getTotalText();
    expect(total, 'Total amount must be displayed on the checkout page').not.toBeNull();
    // Total must contain ₫ symbol per FR-21 currency standard
    expect(total).toMatch(/₫|VND|đ/i);
  });

  // ── Security: Checkout API requires JWT token ─────────────────────────────
  test('TC-CHECKOUT-011 · SEC · POST /api/orders without token → 401 Unauthorized', async ({ page }) => {
    const response = await page.request.post(`${API_URL}/api/orders`, {
      data: { total_amount: 100_000 },
      // No Authorization header
    });
    expect(
      response.status(),
      'POST /api/orders without JWT must return 401 (SEC-02)'
    ).toBe(401);
  });

  // ── Domain Testing: Order history shows placed order ─────────────────────
  test('TC-CHECKOUT-012 · DT · After order → order appears in user order history (FR-11)', async ({ page }) => {
    await loginAndAddOneItem(page);
    const checkout = new CheckoutPage(page);
    await checkout.goto();
    await checkout.placeOrder();
    // Navigate to order history
    await page.goto('/orders');
    await page.waitForLoadState('networkidle');
    const body = await page.textContent('body');
    // Order history page must load and show at least one order
    const hasOrders = !/không có đơn|no orders|trống/i.test(body);
    expect(hasOrders, 'Order history must show the newly placed order').toBe(true);
  });
});

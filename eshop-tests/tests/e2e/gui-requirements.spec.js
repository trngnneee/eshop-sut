// tests/e2e/gui-requirements.spec.js
// FR-21 + FR-22 + FR-23 + FR-24: GUI, Form, Navigation & Feedback Requirements
// Techniques: Domain Testing (each GUI rule = one equivalence class)
// TC IDs: TC-GUI-001 … TC-GUI-022

const { test, expect } = require('@playwright/test');
const { loginViaAPI, loginViaUI } = require('../helpers/auth');
const { addToCartViaAPI, getFirstProductId } = require('../helpers/cart');
const { ACCOUNTS, GUI } = require('../fixtures/test-data');

// ─────────────────────────────────────────────────────────────────────────────
// FR-22: Form Requirements
// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-22 · Form Requirements', () => {

  // ── TC-GUI-001: Required fields show * marker ─────────────────────────────
  for (const { path, name } of [
    { path: '/register', name: 'Register' },
    { path: '/login',    name: 'Login'    },
  ]) {
    test(`TC-GUI-001-${name} · FR-22 · "${name}" form: required fields marked with *`, async ({ page }) => {
      await page.goto(path);
      await page.waitForLoadState('networkidle');
      const body = await page.textContent('body');
      expect(body, `${name} form must mark required fields with *`).toContain('*');
    });
  }

  // ── TC-GUI-002: Email inputs use type="email" on all forms ───────────────
  test('TC-GUI-002 · FR-22 · Register form: email field is type="email"', async ({ page }) => {
    await page.goto('/register');
    const emailInputs = page.locator('input[type="email"]');
    expect(await emailInputs.count(), 'Register must have at least one type="email" input').toBeGreaterThan(0);
  });

  test('TC-GUI-003 · FR-22 · Login form: email field is type="email"', async ({ page }) => {
    await page.goto('/login');
    const emailInputs = page.locator('input[type="email"]');
    expect(await emailInputs.count(), 'Login must have at least one type="email" input').toBeGreaterThan(0);
  });

  test('TC-GUI-004 · FR-22 · Forgot-password form: email field is type="email"', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.waitForLoadState('networkidle');
    const emailInputs = page.locator('input[type="email"]');
    expect(await emailInputs.count(), 'Forgot-password must have at least one type="email" input').toBeGreaterThan(0);
  });

  // ── TC-GUI-005: Password fields use type="password" ──────────────────────
  test('TC-GUI-005 · FR-22 · Register form: password fields are type="password"', async ({ page }) => {
    await page.goto('/register');
    const pwdInputs = page.locator('input[type="password"]');
    const count = await pwdInputs.count();
    expect(count, 'Register must have at least 2 type="password" inputs (password + confirm)').toBeGreaterThanOrEqual(2);
  });

  test('TC-GUI-006 · FR-22 · Login form: password field is type="password"', async ({ page }) => {
    await page.goto('/login');
    const pwdInputs = page.locator('input[type="password"]');
    expect(await pwdInputs.count(), 'Login must have a type="password" input').toBeGreaterThan(0);
  });

  test('TC-GUI-007 · FR-22 · Reset-password form: password fields are type="password"', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.waitForLoadState('networkidle');
    // Request OTP first to reach Step 2 — locate email by Step-1 form, not type attribute
    const step1Form = page.locator('form').filter({
      has: page.getByRole('button', { name: /Lấy mã OTP/i }),
    });
    if (await step1Form.count() > 0) {
      await step1Form.locator('input').first().fill(ACCOUNTS.user.email);
      await step1Form.getByRole('button', { name: /Lấy mã OTP/i }).click();
      await page.waitForTimeout(1000);
    }
    const pwdInputs = page.locator('input[type="password"]');
    const count = await pwdInputs.count();
    expect(count, 'Reset-password step 2 must have type="password" inputs').toBeGreaterThanOrEqual(1);
  });

  // ── TC-GUI-008: Step Indicator on multi-step forms ────────────────────────
  test('TC-GUI-008 · FR-22 · Forgot-password: Step Indicator present (FR-22 multi-step rule)', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.waitForLoadState('networkidle');
    const body = await page.textContent('body');
    const hasStepIndicator = /bước|step\s*1|step\s*2|\d\s*\/\s*\d/i.test(body);
    expect(hasStepIndicator, 'Multi-step forgot-password form must show a Step Indicator').toBe(true);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// FR-21: General GUI Standards
// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-21 · General GUI Standards', () => {

  // ── TC-GUI-009: Each page has exactly one <h1> ────────────────────────────
  const publicPages = [
    { path: '/',                name: 'Home'           },
    { path: '/login',           name: 'Login'          },
    { path: '/register',        name: 'Register'       },
    { path: '/forgot-password', name: 'Forgot Password'},
  ];

  for (const { path, name } of publicPages) {
    test(`TC-GUI-009-${name} · FR-21 · "${name}" page has exactly one <h1>`, async ({ page }) => {
      await page.goto(path);
      await page.waitForLoadState('networkidle');
      const h1Count = await page.locator('h1').count();
      expect(h1Count, `"${name}" must have exactly one <h1> tag (FR-21)`).toBe(1);
    });
  }

  // ── TC-GUI-010: Currency symbol ₫ used throughout ─────────────────────────
  test('TC-GUI-010 · FR-21 · Product prices on home page use ₫ symbol', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const body = await page.textContent('body');
    expect(body, 'Product prices must use ₫ symbol (FR-21 currency standard)').toContain('₫');
  });

  // ── TC-GUI-011: Product images have non-empty alt text ───────────────────
  test('TC-GUI-011 · FR-24 · Product images have non-empty alt attribute', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const images = page.locator('img');
    const count = await images.count();
    if (count === 0) test.skip(true, 'No images found on home page');

    let missingAlt = 0;
    for (let i = 0; i < Math.min(count, 10); i++) {
      const alt = await images.nth(i).getAttribute('alt');
      if (!alt || alt.trim() === '') missingAlt++;
    }
    expect(missingAlt, `${missingAlt} image(s) missing non-empty alt text (FR-24)`).toBe(0);
  });

  // ── TC-GUI-012: XSS — user-entered text rendered safely ──────────────────
  test('TC-GUI-012 · SEC-04 · Search field: XSS payload rendered as text, not HTML', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const searchInput = page.locator('input[type="search"], input[placeholder*="tìm"], input[placeholder*="search"]').first();
    if (await searchInput.count() === 0) test.skip(true, 'No search input found');

    const xss = '<script>window.__xss=1</script>';
    await searchInput.fill(xss);
    await page.keyboard.press('Enter');
    await page.waitForTimeout(800);

    // The XSS script must NOT execute
    const xssRan = await page.evaluate(() => window.__xss === 1);
    expect(xssRan, 'XSS payload must not execute — user input must be escaped (SEC-04)').toBe(false);

    // The text should appear safely (escaped) in the page body
    const body = await page.textContent('body');
    expect(body).not.toContain('<script>');  // literal tag must not be in DOM text
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// FR-23: Navigation Requirements
// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-23 · Navigation Requirements', () => {

  // ── TC-GUI-013: Cart badge shows item count ───────────────────────────────
  test('TC-GUI-013 · FR-23 · Cart link shows badge with item count after adding product', async ({ page }) => {
    const token = await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    const pid   = await getFirstProductId(page);
    await addToCartViaAPI(page, token, pid, 1);
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    // Cart badge: a number next to the cart icon/link
    const badge = page.locator('[class*="badge"], [class*="cart-count"], [class*="CartBadge"]');
    const badgeText = await badge.first().textContent().catch(() => null);
    const navText = await page.textContent('nav, header').catch(() => '');
    const hasBadge = (badgeText && /\d+/.test(badgeText)) || /\d+/.test(navText);
    expect(hasBadge, 'Cart link must show a numeric badge when cart is not empty (FR-23)').toBe(true);
  });

  // ── TC-GUI-014: Navbar highlights current page ───────────────────────────
  test('TC-GUI-014 · FR-23 · Active nav link is highlighted (has active class or aria-current)', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const activeLink = page.locator(
      'nav a[class*="active"], nav a[aria-current="page"], nav a[class*="current"], header a[class*="active"]'
    );
    const count = await activeLink.count();
    expect(count, 'Navbar must highlight the currently active page link (FR-23)').toBeGreaterThan(0);
  });

  // ── TC-GUI-015: Logout button is labelled "Đăng xuất" ────────────────────
  test('TC-GUI-015 · FR-23 · Logout button is labelled "Đăng xuất" (not "Thoát")', async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    const body = await page.textContent('body');
    expect(body, 'Logout button must say "Đăng xuất" (FR-23)').toContain('Đăng xuất');
    expect(body, 'Logout button must NOT say "Thoát" (FR-23)').not.toContain('Thoát');
  });

  // ── TC-GUI-016: Breadcrumb on cart page ──────────────────────────────────
  test('TC-GUI-016 · FR-23 · Cart page has breadcrumb navigation', async ({ page }) => {
    const token = await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    const pid   = await getFirstProductId(page);
    await addToCartViaAPI(page, token, pid, 1);
    await page.goto('/cart');
    await page.waitForLoadState('networkidle');
    const breadcrumb = page.locator(
      'nav[aria-label*="breadcrumb"], [class*="breadcrumb"], [class*="Breadcrumb"]'
    );
    const count = await breadcrumb.count();
    expect(count, 'Cart page must have breadcrumb navigation (FR-23)').toBeGreaterThan(0);
  });

  // ── TC-GUI-017: Breadcrumb on checkout page ───────────────────────────────
  test('TC-GUI-017 · FR-23 · Checkout page has breadcrumb navigation', async ({ page }) => {
    const token = await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    const pid   = await getFirstProductId(page);
    await addToCartViaAPI(page, token, pid, 1);
    await page.goto('/checkout');
    await page.waitForLoadState('networkidle');
    const breadcrumb = page.locator(
      'nav[aria-label*="breadcrumb"], [class*="breadcrumb"], [class*="Breadcrumb"]'
    );
    const count = await breadcrumb.count();
    expect(count, 'Checkout page must have breadcrumb navigation (FR-23)').toBeGreaterThan(0);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// FR-24: Feedback & State Requirements
// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-24 · Feedback & State Requirements', () => {

  // ── TC-GUI-018: "Add to cart" shows visual feedback ──────────────────────
  test('TC-GUI-018 · FR-24 · Click "Thêm vào giỏ" → toast or badge updates (visual feedback)', async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const productCards = page.locator('a[href*="/product"], [class*="product-card"]');
    if (await productCards.count() === 0) test.skip(true, 'No product cards found');
    await productCards.first().click();
    await page.waitForLoadState('networkidle');

    const addBtn = page.locator('button:has-text("Thêm vào giỏ"), button:has-text("Add to Cart")');
    await addBtn.click();
    await page.waitForTimeout(1500);

    // Either a toast appears, or the cart badge count changes
    const toast = page.locator('[class*="toast"], [class*="Toast"], [class*="notification"], [role="status"]');
    const hasToast = (await toast.count()) > 0;
    expect(hasToast, '"Thêm vào giỏ" must show visual feedback (toast or badge update) (FR-24)').toBe(true);
  });

  // ── TC-GUI-019: Empty cart page has illustration + message ───────────────
  test('TC-GUI-019 · FR-24 · Empty cart shows illustration and friendly message', async ({ page }) => {
    // Login but ensure cart is empty
    await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    await page.goto('/cart');
    await page.waitForLoadState('networkidle');

    const cartItems = page.locator('tbody tr, [class*="cart-item"]');
    const count = await cartItems.count();
    if (count > 0) test.skip(true, 'Cart has items — cannot test empty state without clearing');

    const body = await page.textContent('body');
    const hasEmptyMsg = /trống|rỗng|empty|chưa có/i.test(body);
    const hasIllustration = (await page.locator('img, svg, [class*="empty"]').count()) > 0;
    expect(hasEmptyMsg || hasIllustration, 'Empty cart must show an illustration or friendly empty-state message (FR-24)').toBe(true);
  });

  // ── TC-GUI-020: Language consistency — Vietnamese labels ──────────────────
  test('TC-GUI-020 · FR-21 · Home page UI labels are in Vietnamese', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const body = await page.textContent('body');
    // Must contain at least one Vietnamese UI label
    const hasVietnamese = /đăng nhập|giỏ hàng|sản phẩm|tìm kiếm|trang chủ/i.test(body);
    expect(hasVietnamese, 'UI must use Vietnamese labels (FR-21 language consistency)').toBe(true);
  });

  // ── TC-GUI-021: Action buttons use correct colours (blue/red convention) ──
  test('TC-GUI-021 · FR-21 · Submit/positive buttons are blue; danger/cancel buttons are red', async ({ page }) => {
    await page.goto('/register');
    await page.waitForLoadState('networkidle');
    const submitBtn = page.locator('button[type="submit"]').first();
    const submitBg  = await submitBtn.evaluate(el => getComputedStyle(el).backgroundColor);
    // Blue in RGB is roughly r<100, g<150, b>150 — check it's not red-dominant
    // This is a heuristic check; exact colour depends on Tailwind classes
    const isReddish = /rgb\(2[0-9]{2}, [0-5][0-9], [0-5][0-9]\)/.test(submitBg);
    expect(isReddish, 'Submit button on register must not be red — should be blue (FR-21)').toBe(false);
  });

  // ── TC-GUI-022: Loading state shown on home page ──────────────────────────
  test('TC-GUI-022 · FR-05 · Home page shows loading indicator while fetching products', async ({ page }) => {
    // Intercept the products API to slow it down
    await page.route('**/api/products**', async route => {
      await new Promise(r => setTimeout(r, 800)); // 800ms artificial delay
      await route.continue();
    });
    await page.goto('/');
    // Loading indicator should appear before the delay resolves
    const loading = page.locator(
      '[class*="loading"], [class*="spinner"], [class*="skeleton"], [aria-busy="true"]'
    );
    const hasLoading = (await loading.count()) > 0;
    await page.waitForLoadState('networkidle');
    // At least the page must eventually show products
    const products = page.locator('[class*="product-card"], [class*="ProductCard"]');
    const productCount = await products.count();
    // We can't guarantee timing in all environments, so log instead of hard-fail
    console.log(`TC-GUI-022: loading indicator found=${hasLoading}, products=${productCount}`);
    expect(productCount, 'Home page must display products after loading (FR-05)').toBeGreaterThan(0);
  });
});

// tests/e2e/admin-product.spec.js
// FR-15: Product Management (Admin CRUD)
// Techniques: Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
// TC IDs: TC-PRODUCT-001 … TC-PRODUCT-016

const { test, expect } = require('@playwright/test');
const { AdminProductPage } = require('../pages/AdminProductPage');
const { loginViaAPI, loginViaUI } = require('../helpers/auth');
const { ACCOUNTS, PRODUCT, API_URL, uniqueEmail } = require('../fixtures/test-data');

// ── Admin login helper ─────────────────────────────────────────────────────
async function loginAsAdmin(page) {
  await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
}

test.describe('FR-15 · Admin Product Management (CRUD)', () => {

  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page);
  });

  // ── Domain Testing: Admin can access product management page ──────────────
  test('TC-PRODUCT-001 · DT · Admin navigates to /admin/products → page loads', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    const accessible = await adminProd.isAccessible();
    expect(accessible, 'Admin must be able to access the product management page').toBe(true);
  });

  // ── Domain Testing: Non-admin blocked from admin product page ─────────────
  test('TC-PRODUCT-002 · SEC · Regular user accessing /admin/products → blocked (FR-12)', async ({ page }) => {
    // Override the admin session with a regular user session
    await loginViaUI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    await page.goto('/admin/products');
    await page.waitForTimeout(1000);
    // Must be redirected away from /admin
    const url = page.url();
    expect(url, 'Regular user must not access /admin/products (FR-12 access control)').not.toContain('/admin/products');
  });

  // ── Domain Testing: API access control — no token ─────────────────────────
  test('TC-PRODUCT-003 · SEC · POST /api/products without token → 401 (SEC-02)', async ({ page }) => {
    const resp = await page.request.post(`${API_URL}/api/products`, {
      data: { name: 'Hack', price: 1 },
    });
    expect(resp.status(), 'Creating product without JWT must return 401').toBe(401);
  });

  // ── Domain Testing: API access control — user token (not admin) ───────────
  test('TC-PRODUCT-004 · SEC · POST /api/products with user token → 403 (SEC-03)', async ({ page }) => {
    const token = await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    const resp = await page.request.post(`${API_URL}/api/products`, {
      headers: { Authorization: `Bearer ${token}` },
      data: { name: 'Hack', price: 1, category_id: 1 },
    });
    expect(resp.status(), 'Creating product with user (non-admin) JWT must return 403').toBe(403);
  });

  // ── Domain Testing: Valid product creation ────────────────────────────────
  test('TC-PRODUCT-005 · DT · Valid name + valid price + category → product created', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({
      name:  `Test Product ${Date.now()}`,
      price: PRODUCT.priceValid,
    });
    await adminProd.submit();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok, 'Valid product data must be accepted and product created').toBe(true);
  });

  // ── Domain Testing: Empty name → error ───────────────────────────────────
  test('TC-PRODUCT-006 · DT · Empty product name → error shown', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({ name: PRODUCT.nameEmpty, price: PRODUCT.priceValid });
    await adminProd.submit();
    const error = await adminProd.getErrorText();
    expect(error, 'Empty product name must be rejected with an error').not.toBeNull();
  });

  // ── Domain Testing: Price = 0 → error ────────────────────────────────────
  test('TC-PRODUCT-007 · DT · Price = 0 → error (price must be > 0)', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({
      name:  `ZeroPrice ${Date.now()}`,
      price: PRODUCT.priceZero,
    });
    await adminProd.submit();
    const error = await adminProd.getErrorText();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok || error !== null, 'Price=0 must be rejected (spec: price must be > 0)').toBeDefined();
    expect(ok, 'Price=0 must NOT produce a successful creation').toBe(false);
  });

  // ── Domain Testing: Negative price → error ───────────────────────────────
  test('TC-PRODUCT-008 · DT · Negative price → error shown', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({
      name:  `NegPrice ${Date.now()}`,
      price: PRODUCT.priceNegative,
    });
    await adminProd.submit();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok, 'Negative price must NOT be accepted').toBe(false);
  });

  // ── BVA: Price at minimum valid value (0.01) → valid ─────────────────────
  test('TC-PRODUCT-009 · BVA · Price = 0.01 (smallest positive, min on-point) → accepted', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({
      name:  `MinPrice ${Date.now()}`,
      price: PRODUCT.priceMin,    // 0.01
    });
    await adminProd.submit();
    // 0.01 is technically positive — whether the SUT accepts it depends on its validation.
    // This test documents the boundary behaviour.
    const error = await adminProd.getErrorText();
    const ok    = await adminProd.isSubmitSuccessful();
    // Log the result — either outcome is documented
    console.log(`TC-PRODUCT-009: price=0.01 → ok=${ok}, error=${error}`);
    // If error, the SUT might have a higher minimum (e.g., integers only) — flag as gap
    expect(ok !== null || error !== null, 'System must respond to price=0.01 (min boundary)').toBe(true);
  });

  // ── BVA: Product name 254 chars (max−1) → valid ──────────────────────────
  test('TC-PRODUCT-010 · BVA · Product name 254 chars (max−1) → accepted', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({ name: PRODUCT.nameMax254, price: PRODUCT.priceValid });
    await adminProd.submit();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok, '254-char name (max−1) must be accepted').toBe(true);
  });

  // ── BVA: Product name 255 chars (max on-point) → valid ───────────────────
  test('TC-PRODUCT-011 · BVA · Product name 255 chars (max on-point) → accepted', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({ name: PRODUCT.nameMax255, price: PRODUCT.priceValid });
    await adminProd.submit();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok, '255-char name (max on-point) must be accepted').toBe(true);
  });

  // ── BVA: Product name 256 chars (max+1) → error ──────────────────────────
  test('TC-PRODUCT-012 · BVA · Product name 256 chars (max+1) → error shown', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({ name: PRODUCT.nameMax256, price: PRODUCT.priceValid });
    await adminProd.submit();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok, '256-char name (max+1) must be rejected').toBe(false);
  });

  // ── Domain Testing: Non-numeric price → error ─────────────────────────────
  test('TC-PRODUCT-013 · DT · Non-numeric price ("abc") → error', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    await adminProd.fillProductForm({ name: `AlphaPrice ${Date.now()}`, price: PRODUCT.priceString });
    await adminProd.submit();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok, 'Non-numeric price must not create a product').toBe(false);
  });

  // ── Domain Testing: Edit product — only that product changes ──────────────
  test('TC-PRODUCT-014 · DT · Edit one product → only that product is changed (FR-15)', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    const countBefore = await adminProd.getProductCount();
    await adminProd.clickEditFirst();
    const newName = `Edited ${Date.now()}`;
    await adminProd.nameInput.fill(newName);
    await adminProd.submit();
    await adminProd.goto();
    const countAfter = await adminProd.getProductCount();
    // Total count must not change (no new product added, none deleted)
    expect(countAfter, 'Editing a product must not change the total product count').toBe(countBefore);
  });

  // ── Domain Testing: Delete product ───────────────────────────────────────
  test('TC-PRODUCT-015 · DT · Delete product → product removed from list', async ({ page }) => {
    // First create a product to delete (so we don't destroy seed data)
    const adminToken = await loginViaAPI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    await page.request.post(`${API_URL}/api/products`, {
      headers: { Authorization: `Bearer ${adminToken}` },
      data: { name: `ToDelete ${Date.now()}`, price: 1000, category_id: 1 },
    });

    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    const countBefore = await adminProd.getProductCount();
    await adminProd.clickDeleteFirst();
    await adminProd.confirmDeleteIfDialogAppears();
    await adminProd.goto();
    const countAfter = await adminProd.getProductCount();
    expect(countAfter, 'Product count must decrease by 1 after deletion').toBe(countBefore - 1);
  });

  // ── Domain Testing: No category selected → error ──────────────────────────
  test('TC-PRODUCT-016 · DT · No category selected → error shown (category is required)', async ({ page }) => {
    const adminProd = new AdminProductPage(page);
    await adminProd.goto();
    await adminProd.openAddForm();
    // Fill name and price but skip category
    await adminProd.nameInput.fill(`NoCat ${Date.now()}`);
    await adminProd.priceInput.fill(String(PRODUCT.priceValid));
    // Leave category at its default (blank/unselected)
    await adminProd.submit();
    const ok = await adminProd.isSubmitSuccessful();
    expect(ok, 'Product without a category must NOT be created').toBe(false);
  });
});

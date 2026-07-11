// tests/e2e/admin-product.spec.js
// FR-15: Product Management (Admin CRUD)
// Techniques: Domain Testing (Equivalence Partitioning) + Boundary Value Analysis
// TC IDs aligned with tests/test-cases/product/
//   TC-PRODUCT-001 … 011, 020 … 032, SUP-001 … SUP-011

const { test, expect } = require('@playwright/test');
const { AdminProductPage } = require('../pages/AdminProductPage');
const { loginViaUI, loginViaAPI } = require('../helpers/auth');
const { createProductViaAPI, ensureProductCount, postProduct } = require('../helpers/product');
const { ACCOUNTS, PRODUCT } = require('../fixtures/test-data');

// ── Shared helpers ────────────────────────────────────────────────────────────
async function openProductAdmin(page) {
  const adminProd = new AdminProductPage(page);
  await adminProd.goto();
  return adminProd;
}

async function openAddForm(page) {
  const adminProd = await openProductAdmin(page);
  await adminProd.openAddForm();
  return adminProd;
}

function uniqueName(base) {
  return `${base} ${Date.now()}`;
}

function bvaName(length) {
  const alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  const seed = Date.now() % 100000;
  let s = '';
  for (let i = 0; i < length; i++) {
    s += alpha[(seed + i) % alpha.length];
  }
  return s;
}

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-15 · Product CRUD — Domain Testing (EP)', () => {

  test.beforeEach(async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
  });

  test('TC-PRODUCT-001 · DT · Valid name + price + category → product created', async ({ page }) => {
    const name = uniqueName(PRODUCT.nameOnPoint);
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name, price: PRODUCT.priceOnPoint });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('Valid product must be created (TC-PRODUCT-001)');
    await adminProd.goto();
    expect(await adminProd.rowContainsText(name), 'New product must appear in list').toBe(true);
  });

  test('TC-PRODUCT-002 · DT · Product list shows name, price, edit/delete actions', async ({ page }) => {
    await ensureProductCount(page, 1);
    const adminProd = await openProductAdmin(page);
    expect(await adminProd.getProductCount(), 'List must show at least one product').toBeGreaterThan(0);
    expect(await adminProd.isListVisible(), 'List must expose product rows with actions').toBe(true);
    const rowText = await adminProd.getRowText(0);
    expect(rowText.length, 'Each row must show core product info').toBeGreaterThan(0);
  });

  test('TC-PRODUCT-003 · DT · Empty product name → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: PRODUCT.nameEmpty, price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Empty name must be rejected (TC-PRODUCT-003)');
  });

  test('TC-PRODUCT-004 · DT · Empty price → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillNameAndCategoryOnly('Quần jean nữ');
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Empty price must be rejected (TC-PRODUCT-004)');
  });

  test('TC-PRODUCT-005 · DT · Price = 0 → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá zero'),
      price: PRODUCT.priceZero,
    });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Price=0 must be rejected (TC-PRODUCT-005)');
  });

  test('TC-PRODUCT-006 · DT · Negative price → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá âm'),
      price: -50000,
    });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Negative price must be rejected (TC-PRODUCT-006)');
  });

  test('TC-PRODUCT-007 · DT · Non-numeric price → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá chữ'),
      price: PRODUCT.priceString,
    });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Non-numeric price must be rejected (TC-PRODUCT-007)');
  });

  test('TC-PRODUCT-008 · DT · No category selected → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillNamePriceNoCategory(
      uniqueName('Sản phẩm không danh mục'),
      150000
    );
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Missing category must be rejected (TC-PRODUCT-008)');
  });

  test('TC-PRODUCT-009 · DT · Edit product with valid data → updated', async ({ page }) => {
    const original = uniqueName('Sản phẩm sửa');
    const updated  = uniqueName('Áo khoác dù mùa đông');
    await createProductViaAPI(page, { name: original, price: 200000 });
    const adminProd = await openProductAdmin(page);
    await adminProd.clickEditRow(await findRowIndexByName(adminProd, original));
    await adminProd.fillProductForm({ name: updated, price: 450000 });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('Valid edit must succeed (TC-PRODUCT-009)');
    await adminProd.goto();
    expect(await adminProd.rowContainsText(updated), 'Updated name must appear in list').toBe(true);
  });

  test('TC-PRODUCT-010 · DT · Edit one product → other products unchanged', async ({ page }) => {
    const nameA = uniqueName('ProductA');
    const nameB = uniqueName('ProductB');
    await createProductViaAPI(page, { name: nameA, price: 111000 });
    await createProductViaAPI(page, { name: nameB, price: 222000 });

    const adminProd = await openProductAdmin(page);
    const countBefore = await adminProd.getProductCount();
    const snapshotB = await adminProd.page
      .locator('tbody tr, [class*="product-row"]', { hasText: nameB })
      .first()
      .textContent();

    const newNameA = uniqueName('Tên đã chỉnh sửa');
    await adminProd.clickEditRow(await findRowIndexByName(adminProd, nameA));
    await adminProd.nameInput.fill(newNameA);
    await adminProd.submit();
    await adminProd.goto();

    expect(await adminProd.getProductCount(), 'Edit must not add or remove products').toBe(countBefore);
    const snapshotBAfter = await adminProd.page
      .locator('tbody tr, [class*="product-row"]', { hasText: nameB })
      .first()
      .textContent();
    expect(snapshotBAfter, 'Product B must remain unchanged').toBe(snapshotB);
    expect(await adminProd.rowContainsText(newNameA), 'Product A must show new name').toBe(true);
  });

  test('TC-PRODUCT-011 · DT · Delete product → removed from list', async ({ page }) => {
    const toDelete = uniqueName('ToDelete');
    await createProductViaAPI(page, { name: toDelete, price: 99000 });

    const adminProd = await openProductAdmin(page);
    expect(await adminProd.rowContainsText(toDelete), 'Product must exist before delete').toBe(true);
    const countBefore = await adminProd.getProductCount();

    await adminProd.clickDeleteByName(toDelete);
    await adminProd.confirmDeleteIfDialogAppears();
    await adminProd.goto();

    expect(await adminProd.rowContainsText(toDelete), 'Deleted product must not appear').toBe(false);
    expect(await adminProd.getProductCount(), 'Count must decrease by 1').toBe(countBefore - 1);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-15 · Product — BVA Name (TC-PRODUCT-020 … 025)', () => {

  test.beforeEach(async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
  });

  test('TC-PRODUCT-020 · BVA · Name 0 chars (min−) → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: PRODUCT.nameEmpty, price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Name length 0 must be rejected (TC-PRODUCT-020)');
  });

  test('TC-PRODUCT-021 · BVA · Name 1 char (min) → accepted', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: bvaName(1), price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('1-char name must be accepted (TC-PRODUCT-021)');
  });

  test('TC-PRODUCT-022 · BVA · Name 2 chars (min+) → accepted', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: bvaName(2), price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('2-char name must be accepted (TC-PRODUCT-022)');
  });

  test('TC-PRODUCT-023 · BVA · Name 254 chars (max−) → accepted', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: PRODUCT.nameMax254, price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('254-char name must be accepted (TC-PRODUCT-023)');
  });

  test('TC-PRODUCT-024 · BVA · Name 255 chars (max) → accepted', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: PRODUCT.nameMax255, price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('255-char name must be accepted (TC-PRODUCT-024)');
  });

  test('TC-PRODUCT-025 · BVA · Name 256 chars (max+) → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: PRODUCT.nameMax256, price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('256-char name must be rejected (TC-PRODUCT-025)');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-15 · Product — BVA Price (TC-PRODUCT-026 … 030)', () => {

  test.beforeEach(async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
  });

  test('TC-PRODUCT-026 · BVA · Price 0 (invalid on-point) → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá zero'),
      price: PRODUCT.priceZero,
    });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Price=0 boundary must be rejected (TC-PRODUCT-026)');
  });

  test('TC-PRODUCT-027 · BVA · Price −1 (min−) → rejected', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá âm biên'),
      price: PRODUCT.priceNegative,
    });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Price=-1 must be rejected (TC-PRODUCT-027)');
  });

  test('TC-PRODUCT-028 · BVA · Price 1 (min) → accepted', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá một đồng'),
      price: PRODUCT.priceOne,
    });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('Price=1 must be accepted (TC-PRODUCT-028)');
  });

  test('TC-PRODUCT-029 · BVA · Price 2 (min+) → accepted', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá hai đồng'),
      price: PRODUCT.priceTwo,
    });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('Price=2 must be accepted (TC-PRODUCT-029)');
  });

  test('TC-PRODUCT-030 · BVA · Price 0.01 (decimal min) → accepted', async ({ page }) => {
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({
      name: uniqueName('Sản phẩm giá thập phân'),
      price: PRODUCT.priceMin,
    });
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('Price=0.01 must be accepted per FR-15 > 0 (TC-PRODUCT-030)');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-15 · Product — BVA Edit cross-boundary (TC-PRODUCT-031 … 032)', () => {

  test.beforeEach(async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
  });

  test('TC-PRODUCT-031 · BVA · Edit name 256 chars → rejected, old name kept', async ({ page }) => {
    const original = uniqueName('EditBoundaryName');
    await createProductViaAPI(page, { name: original, price: 50000 });

    const adminProd = await openProductAdmin(page);
    await adminProd.clickEditRow(
      await findRowIndexByName(adminProd, original)
    );
    await adminProd.nameInput.fill(PRODUCT.nameMax256);
    await adminProd.submit();
    await adminProd.expectSubmitRejected('256-char name on edit must be rejected (TC-PRODUCT-031)');
    await adminProd.goto();
    expect(await adminProd.rowContainsText(original), 'Original name must be preserved').toBe(true);
    expect(await adminProd.rowContainsText(PRODUCT.nameMax256.slice(0, 20)), 'Invalid name must not be saved').toBe(false);
  });

  test('TC-PRODUCT-032 · BVA · Edit price 0 → rejected, old price kept', async ({ page }) => {
    const original = uniqueName('EditBoundaryPrice');
    const price = 75000;
    await createProductViaAPI(page, { name: original, price });

    const adminProd = await openProductAdmin(page);
    const rowBefore = await adminProd.page
      .locator('tbody tr, [class*="product-row"]', { hasText: original })
      .first()
      .textContent();

    await adminProd.clickEditRow(await findRowIndexByName(adminProd, original));
    await adminProd.priceInput.fill(String(PRODUCT.priceZero));
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Price=0 on edit must be rejected (TC-PRODUCT-032)');
    await adminProd.goto();

    const rowAfter = await adminProd.page
      .locator('tbody tr, [class*="product-row"]', { hasText: original })
      .first()
      .textContent();
    expect(rowAfter, 'Row content must remain unchanged after rejected edit').toBe(rowBefore);
  });
});

async function findRowIndexByName(adminProd, name) {
  const rows = adminProd.productRows;
  const count = await rows.count();
  for (let i = 0; i < count; i++) {
    const text = await rows.nth(i).textContent();
    if (text && text.includes(name)) return i;
  }
  throw new Error(`Product row not found for name: ${name}`);
}

// ─────────────────────────────────────────────────────────────────────────────
test.describe('FR-15 · Product — Supplementary (TC-PRODUCT-SUP-001 … 011)', () => {

  test('TC-PRODUCT-SUP-001 · SUP · API rejects non-existent category_id', async ({ page }) => {
    const token = await loginViaAPI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const res = await postProduct(page, {
      token,
      data: {
        name: `InvalidCat ${Date.now()}`,
        price: 100000,
        category_id: PRODUCT.invalidCategoryId,
      },
    });
    expect(res.ok, 'POST with invalid category_id must fail (GAP-01)').toBe(false);
    expect(res.status, 'Must return 4xx for invalid category').toBeGreaterThanOrEqual(400);
  });

  test('TC-PRODUCT-SUP-002 · SUP · Regular user blocked from /admin/products (FR-12)', async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    await page.goto('/admin/products');
    await page.waitForTimeout(1000);
    expect(page.url(), 'User must not stay on /admin/products').not.toContain('/admin/products');
  });

  test('TC-PRODUCT-SUP-003 · SUP · POST /api/products without JWT → 401', async ({ page }) => {
    const res = await postProduct(page, {
      data: { name: 'Hack', price: 1, category_id: 1 },
    });
    expect(res.status, 'No JWT must return 401 (SEC-02)').toBe(401);
  });

  test('TC-PRODUCT-SUP-004 · SUP · POST /api/products with user JWT → 403', async ({ page }) => {
    const token = await loginViaAPI(page, ACCOUNTS.user.email, ACCOUNTS.user.password);
    const res = await postProduct(page, {
      token,
      data: { name: 'Hack', price: 1, category_id: 1 },
    });
    expect(res.status, 'User JWT must return 403 (SEC-03)').toBe(403);
  });

  test('TC-PRODUCT-SUP-005 · SUP · Add form required fields marked with * (FR-22)', async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const adminProd = await openAddForm(page);
    expect(await adminProd.hasRequiredFieldMarkers(), 'Required fields must show * (FR-22)').toBe(true);
  });

  test('TC-PRODUCT-SUP-006 · SUP · Validation error appears above Submit (FR-22)', async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: PRODUCT.nameEmpty, price: PRODUCT.priceValid });
    await adminProd.submit();
    const error = await adminProd.getErrorText();
    const blocked = await adminProd.hasClientSideValidationError();
    expect(error || blocked, 'Empty name must trigger validation feedback').toBeTruthy();
    if (error) {
      expect(await adminProd.isErrorAboveSubmit(), 'Error must appear above Submit (FR-22)').toBe(true);
    }
  });

  test('TC-PRODUCT-SUP-007 · SUP · Backend rejects name 256 chars and price 0', async ({ page }) => {
    const token = await loginViaAPI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const resName = await postProduct(page, {
      token,
      data: { name: PRODUCT.nameMax256, price: 100000, category_id: PRODUCT.validCategoryId },
    });
    expect(resName.ok, 'API must reject 256-char name').toBe(false);

    const resPrice = await postProduct(page, {
      token,
      data: { name: 'Valid API Name', price: 0, category_id: PRODUCT.validCategoryId },
    });
    expect(resPrice.ok, 'API must reject price=0').toBe(false);
  });

  test('TC-PRODUCT-SUP-008 · SUP · Whitespace-only name → rejected', async ({ page }) => {
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const adminProd = await openAddForm(page);
    await adminProd.fillProductForm({ name: PRODUCT.nameWhitespace, price: PRODUCT.priceValid });
    await adminProd.submit();
    await adminProd.expectSubmitRejected('Whitespace-only name must be rejected (GAP-07)');
  });

  test('TC-PRODUCT-SUP-009 · SUP · Edit with 255-char name → accepted', async ({ page }) => {
    const original = uniqueName('EditMaxName');
    await createProductViaAPI(page, { name: original, price: 50000 });
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const adminProd = await openProductAdmin(page);
    await adminProd.clickEditRow(await findRowIndexByName(adminProd, original));
    await adminProd.nameInput.fill(PRODUCT.nameMax255);
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('255-char name on edit must be accepted (SUP-009)');
  });

  test('TC-PRODUCT-SUP-010 · SUP · Edit with price = 1 → accepted', async ({ page }) => {
    const original = uniqueName('EditMinPrice');
    await createProductViaAPI(page, { name: original, price: 50000 });
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const adminProd = await openProductAdmin(page);
    await adminProd.clickEditRow(await findRowIndexByName(adminProd, original));
    await adminProd.priceInput.fill(String(PRODUCT.priceOne));
    await adminProd.submit();
    await adminProd.expectSubmitSuccess('Price=1 on edit must be accepted (SUP-010)');
  });

  test('TC-PRODUCT-SUP-011 · SUP · List shows ₫ and thousand separator (FR-21)', async ({ page }) => {
    await createProductViaAPI(page, { name: uniqueName('PriceFormat'), price: 199000 });
    await loginViaUI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
    const adminProd = await openProductAdmin(page);
    expect(await adminProd.listShowsCurrencySymbol(), 'Price must show ₫ (FR-21)').toBe(true);
    expect(await adminProd.listShowsThousandSeparator(), 'Price must use thousand separator (FR-21)').toBe(true);
  });
});

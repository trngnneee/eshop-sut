// tests/helpers/cart.js
// Cart setup for FR-08 checkout (web uses client-side CartContext)

const { API_URL } = require('../fixtures/test-data');

async function fetchProducts(page) {
  const resp = await page.request.get(`${API_URL}/api/products`);
  if (!resp.ok()) return [];
  const body = await resp.json();
  return Array.isArray(body) ? body : body.data ?? body.products ?? [];
}

async function getFirstProductId(page) {
  const products = await fetchProducts(page);
  if (products.length > 0) return products[0].id ?? 1;
  return 1;
}

/**
 * SUT quirk: first click on "Thêm vào giỏ hàng" is ignored — requires 2 clicks.
 */
async function clickAddToCartButton(page) {
  const addBtn = page.locator('button:has-text("Thêm vào giỏ hàng"), button:has-text("Thêm vào giỏ")');
  await addBtn.waitFor({ state: 'visible', timeout: 10_000 });
  // SUT quirk: first click is ignored — requires 2 clicks.
  await addBtn.click();
  await page.waitForTimeout(250);
  await addBtn.click();
  await page.getByText('Đã thêm').waitFor({ state: 'visible', timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(300);
}

/**
 * Add product to client cart via UI.
 * @param {object} opts - { productId, productIndex, quantity, addTimes }
 */
async function addToCartViaUI(page, opts = {}) {
  const { productId, productIndex = 0, quantity = 1, addTimes = 1 } = opts;

  if (productId) {
    const productLink = page.locator(`a[href="/product/${productId}"]`);
    if ((await productLink.count()) > 0) {
      await productLink.first().click();
    } else {
      await page.goto(`/product/${productId}`);
    }
  } else {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const link = page.locator('a[href*="/product/"]').nth(productIndex);
    await link.waitFor({ state: 'visible', timeout: 10_000 });
    await link.click();
  }
  await page.waitForLoadState('networkidle');
  await page.locator('h1').first().waitFor({ state: 'visible', timeout: 10_000 });

  const qtyInput = page.locator('label:has-text("Số lượng") + input, input[type="number"]').first();
  await qtyInput.fill(String(quantity));

  for (let i = 0; i < addTimes; i++) {
    await clickAddToCartButton(page);
  }
}

/** @deprecated Web checkout uses CartContext — prefer addToCartViaUI */
async function addToCartViaAPI(page, token, productId = 1, quantity = 1) {
  return page.request.post(`${API_URL}/api/cart`, {
    headers: { Authorization: `Bearer ${token}` },
    data: { product_id: productId, quantity },
  });
}

async function goToCart(page) {
  const cartLink = page.locator('a[href="/cart"]');
  if ((await cartLink.count()) > 0) {
    await cartLink.first().click();
    await page.waitForURL('**/cart', { timeout: 10_000 });
  } else {
    await page.goto('/cart');
  }
  await page.waitForLoadState('networkidle');
}

async function startCheckoutFromCart(page) {
  const dialogPromise = page.waitForEvent('dialog', { timeout: 3000 }).catch(() => null);
  await page.locator('button:has-text("Tiến hành thanh toán")').click();
  const dialog = await dialogPromise;
  if (dialog) await dialog.accept();
  await page.waitForTimeout(500);
}

async function isCartEmpty(page) {
  const body = await page.textContent('body');
  return /trống|empty|chưa có/i.test(body ?? '');
}

/** Seed cart with one product line; leaves browser on /cart. */
async function seedOneProduct(page, opts = {}) {
  const { expect } = require('@playwright/test');
  const products = await fetchProducts(page);
  expect(products.length, 'Catalog must have products').toBeGreaterThan(0);
  const index = opts.productIndex ?? 0;
  const productId = products[index]?.id ?? products[0].id;

  await addToCartViaUI(page, {
    productId,
    productIndex: index,
    quantity: opts.quantity ?? 1,
    addTimes: opts.addTimes ?? 1,
  });

  await goToCart(page);
  const rows = page.locator('table tbody tr');
  if ((await rows.count()) === 0) {
    await addToCartViaUI(page, { productId, quantity: opts.quantity ?? 1, addTimes: 1 });
    await goToCart(page);
  }
  await expect(rows.first(), 'Cart must contain at least one line after seed').toBeVisible({
    timeout: 10_000,
  });
  return { productId, products };
}

/** Seed cart with two distinct product lines via SPA navigation. */
async function seedTwoProducts(page) {
  const { expect } = require('@playwright/test');
  const products = await fetchProducts(page);
  expect(products.length, 'Need ≥2 products for two-line cart').toBeGreaterThanOrEqual(2);

  await seedOneProduct(page, { productIndex: 0, productId: products[0].id, quantity: 1 });
  await page.locator('a[href="/"]').filter({ hasText: /Mua tiếp|Tiếp tục mua sắm/i }).first().click();
  await page.waitForURL('**/');
  await page.waitForLoadState('networkidle');
  const secondLink = page.locator(`a[href="/product/${products[1].id}"]`);
  await secondLink.first().waitFor({ state: 'visible', timeout: 10_000 });
  await secondLink.first().click();
  await page.locator('h1').first().waitFor({ state: 'visible' });
  await clickAddToCartButton(page);
  await goToCart(page);
  await expect(page.locator('table tbody tr')).toHaveCount(2, { timeout: 10_000 });
  return products;
}

/** Re-add same product from home without clearing cart (SPA). */
async function addSameProductAgain(page, productIndex = 0) {
  const products = await fetchProducts(page);
  const productId = products[productIndex]?.id ?? products[0]?.id;
  await page.locator('a[href="/"]').filter({ hasText: /Mua tiếp|Tiếp tục mua sắm/i }).first().click();
  await page.waitForURL('**/');
  if (productId) {
    const link = page.locator(`a[href="/product/${productId}"]`);
    if ((await link.count()) > 0) {
      await link.first().click();
    } else {
      await page.locator('a[href*="/product/"]').nth(productIndex).click();
    }
  } else {
    await page.locator('a[href*="/product/"]').nth(productIndex).click();
  }
  await page.locator('h1').first().waitFor({ state: 'visible' });
  await clickAddToCartButton(page);
}

module.exports = {
  addToCartViaAPI,
  addToCartViaUI,
  getFirstProductId,
  fetchProducts,
  goToCart,
  startCheckoutFromCart,
  isCartEmpty,
  clickAddToCartButton,
  seedOneProduct,
  seedTwoProducts,
  addSameProductAgain,
};

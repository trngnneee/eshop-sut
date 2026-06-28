// tests/helpers/cart.js
// Utility to add a product to the cart via API for checkout/coupon test setup

const { API_URL } = require('../fixtures/test-data');

/**
 * Add a product to the cart via API.
 * @param {import('@playwright/test').Page} page
 * @param {string} token  - JWT from loginViaAPI
 * @param {number} productId - product ID in the SUT (default: 1)
 * @param {number} quantity
 */
async function addToCartViaAPI(page, token, productId = 1, quantity = 1) {
  const response = await page.request.post(`${API_URL}/api/cart`, {
    headers: { Authorization: `Bearer ${token}` },
    data: { product_id: productId, quantity },
  });
  return response;
}

/**
 * Get the first available product ID from the API.
 */
async function getFirstProductId(page) {
  const resp = await page.request.get(`${API_URL}/api/products`);
  if (!resp.ok()) return 1;
  const body = await resp.json();
  const products = body.data ?? body.products ?? body;
  if (Array.isArray(products) && products.length > 0) {
    return products[0].id ?? products[0].product_id ?? 1;
  }
  return 1;
}

/**
 * Add product(s) to cart via UI (navigate to product page and click "Thêm vào giỏ").
 * Use when testing the cart UI itself.
 */
async function addToCartViaUI(page, productIndex = 0) {
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  // Click a product card to open detail page
  const productCards = page.locator('a[href*="/product"], [class*="product-card"], [class*="ProductCard"]');
  await productCards.nth(productIndex).click();
  await page.waitForLoadState('networkidle');
  // Click "Thêm vào giỏ hàng"
  const addBtn = page.locator('button:has-text("Thêm vào giỏ"), button:has-text("Add to Cart")');
  await addBtn.click();
  await page.waitForTimeout(800);
}

module.exports = { addToCartViaAPI, addToCartViaUI, getFirstProductId };

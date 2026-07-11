// tests/helpers/product.js
// API helpers for FR-15 product management tests

const { loginViaAPI } = require('./auth');
const { ACCOUNTS, API_URL } = require('../fixtures/test-data');

/**
 * POST /api/products with optional JWT and custom headers.
 */
async function postProduct(page, { token = null, data, headers = {} } = {}) {
  const h = { ...headers };
  if (token) h.Authorization = `Bearer ${token}`;
  const resp = await page.request.post(`${API_URL}/api/products`, { headers: h, data });
  const body = await resp.json().catch(() => ({}));
  return { status: resp.status(), body, ok: resp.ok() };
}

/**
 * Create a product via API (admin). Returns parsed response.
 */
async function createProductViaAPI(page, { name, price = 1000, category_id = 1, description = 'E2E test' } = {}) {
  const token = await loginViaAPI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
  return postProduct(page, {
    token,
    data: { name, price, category_id, description },
  });
}

/**
 * Ensure at least `count` products exist; creates missing ones via API.
 */
async function ensureProductCount(page, count = 1) {
  const token = await loginViaAPI(page, ACCOUNTS.admin.email, ACCOUNTS.admin.password);
  const listResp = await page.request.get(`${API_URL}/api/products`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const listBody = await listResp.json().catch(() => ({}));
  const products = listBody.data ?? listBody.products ?? listBody;
  const existing = Array.isArray(products) ? products.length : 0;
  const needed = Math.max(0, count - existing);
  for (let i = 0; i < needed; i++) {
    await createProductViaAPI(page, {
      name: `Seed Product ${Date.now()}_${i}`,
      price: 100000 + i,
    });
  }
}

module.exports = { postProduct, createProductViaAPI, ensureProductCount };

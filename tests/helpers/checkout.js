// tests/helpers/checkout.js
// API helpers for FR-08 checkout tests

const { expect } = require('@playwright/test');
const { API_URL } = require('../fixtures/test-data');

async function postCheckout(page, token, body, headers = {}) {
  const reqHeaders = { ...headers };
  if (token) reqHeaders.Authorization = `Bearer ${token}`;
  return page.request.post(`${API_URL}/api/checkout`, {
    headers: reqHeaders,
    data: body,
  });
}

async function getMyOrders(page, token) {
  return page.request.get(`${API_URL}/api/orders/my-orders`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

async function fetchProducts(page) {
  const resp = await page.request.get(`${API_URL}/api/products`);
  if (!resp.ok()) return [];
  const body = await resp.json();
  return Array.isArray(body) ? body : body.data ?? body.products ?? [];
}

function buildCartItems(products, specs) {
  return specs.map(({ index = 0, quantity = 1 }) => {
    const p = products[index];
    if (!p) throw new Error(`Product index ${index} not found`);
    return {
      id: p.id,
      name: p.name,
      price: p.price,
      quantity,
    };
  });
}

function cartTotalFromItems(items) {
  return items.reduce((sum, item) => sum + Number(item.price) * Number(item.quantity), 0);
}

/**
 * After checkout API call, assert order total matches spec (not client tamper).
 */
async function assertOrderTotal(page, token, orderId, expectedTotal, tamperedValue) {
  const ordersRes = await getMyOrders(page, token);
  expect(ordersRes.ok()).toBeTruthy();
  const orders = await ordersRes.json();
  const order = orders.find((o) => o.id === orderId) ?? orders[0];
  expect(order, 'Order must exist in my-orders').toBeTruthy();
  if (tamperedValue !== undefined && tamperedValue !== expectedTotal) {
    expect(
      order.total_amount,
      `Backend must not persist tampered total_amount=${tamperedValue}`
    ).not.toBe(tamperedValue);
  }
  expect(
    order.total_amount,
    `Order total must equal server-calculated cartTotal=${expectedTotal}`
  ).toBe(expectedTotal);
}

module.exports = {
  postCheckout,
  getMyOrders,
  fetchProducts,
  buildCartItems,
  cartTotalFromItems,
  assertOrderTotal,
};

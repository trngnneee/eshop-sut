const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:3000';

/**
 * @param {{ name: string, email: string, password: string }} user
 */
async function registerUser(user) {
  const res = await fetch(`${API_BASE_URL}/api/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(user),
  });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(`Register failed (${res.status}): ${JSON.stringify(body)}`);
  }
  return body;
}

/**
 * @param {{ email: string, password: string }} credentials
 */
async function loginUser(credentials) {
  const res = await fetch(`${API_BASE_URL}/api/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials),
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

/**
 * @param {string} token
 * @param {{ total_amount: number, shipping_address?: string, items?: unknown[] }} payload
 */
async function checkoutApi(token, payload) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(`${API_BASE_URL}/api/checkout`, {
    method: 'POST',
    headers,
    body: JSON.stringify(payload),
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

/**
 * @param {string} token
 */
async function getMyOrders(token) {
  const res = await fetch(`${API_BASE_URL}/api/orders/my-orders`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const body = await res.json().catch(() => []);
  return { status: res.status, body };
}

/**
 * @param {string} [search]
 */
async function listProducts(search = '') {
  const res = await fetch(
    `${API_BASE_URL}/api/products?search=${encodeURIComponent(search)}`,
  );
  const body = await res.json().catch(() => []);
  if (!res.ok || !Array.isArray(body)) {
    throw new Error(`listProducts failed (${res.status})`);
  }
  return body;
}

module.exports = {
  API_BASE_URL,
  registerUser,
  loginUser,
  checkoutApi,
  getMyOrders,
  listProducts,
};

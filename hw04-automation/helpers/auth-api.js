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
 * Admin credentials from env — never from test-data JSON.
 * @returns {{ email: string, password: string }}
 */
function getAdminCredentials() {
  return {
    email: process.env.ADMIN_EMAIL || 'admin@eshop.com',
    password: process.env.ADMIN_PASSWORD || 'Admin123!',
  };
}

/**
 * @returns {Promise<{ status: number, body: any, token: string | null }>}
 */
async function loginAdmin() {
  const creds = getAdminCredentials();
  const result = await loginUser(creds);
  return {
    status: result.status,
    body: result.body,
    token: result.body?.token || null,
  };
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
  getAdminCredentials,
  loginAdmin,
  checkoutApi,
  getMyOrders,
  listProducts,
};

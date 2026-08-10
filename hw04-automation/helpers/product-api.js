const { API_BASE_URL } = require('./auth-api');

/**
 * @param {string} [token]
 */
function authHeaders(token) {
  /** @type {Record<string, string>} */
  const headers = { 'Content-Type': 'application/json' };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

async function listCategories() {
  const res = await fetch(`${API_BASE_URL}/api/categories`);
  const body = await res.json().catch(() => []);
  if (!res.ok || !Array.isArray(body)) {
    throw new Error(`listCategories failed (${res.status})`);
  }
  return body;
}

async function listProducts() {
  const res = await fetch(`${API_BASE_URL}/api/products`);
  const body = await res.json().catch(() => []);
  if (!res.ok || !Array.isArray(body)) {
    throw new Error(`listProducts failed (${res.status})`);
  }
  return body;
}

/**
 * @param {string|number} id
 */
async function getProduct(id) {
  const res = await fetch(`${API_BASE_URL}/api/products/${id}`);
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

/**
 * @param {Record<string, unknown>} payload
 * @param {string} [token]
 */
async function createProduct(payload, token) {
  const res = await fetch(`${API_BASE_URL}/api/products`, {
    method: 'POST',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

/**
 * @param {string|number} id
 * @param {Record<string, unknown>} payload
 * @param {string} [token]
 */
async function updateProduct(id, payload, token) {
  const res = await fetch(`${API_BASE_URL}/api/products/${id}`, {
    method: 'PUT',
    headers: authHeaders(token),
    body: JSON.stringify(payload),
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

/**
 * @param {string|number} id
 * @param {string} [token]
 */
async function deleteProduct(id, token) {
  const res = await fetch(`${API_BASE_URL}/api/products/${id}`, {
    method: 'DELETE',
    headers: authHeaders(token),
  });
  const body = await res.json().catch(() => ({}));
  return { status: res.status, body };
}

/**
 * @param {any} inputs
 * @param {string} [suffix]
 */
function resolveProductName(inputs, suffix = `${Date.now()}`) {
  const mode = inputs?.nameMode || 'unique';
  if (mode === 'empty') return '';
  if (mode === 'fixedLength') {
    const ch = inputs.nameChar || 'X';
    const len = Number(inputs.nameLength);
    if (!Number.isFinite(len) || len < 0) {
      throw new Error(`Invalid nameLength: ${inputs.nameLength}`);
    }
    return ch.repeat(len);
  }
  const prefix = inputs.namePrefix || 'HW04-P';
  return `${prefix}-${suffix}`;
}

/**
 * @param {any} inputs
 * @param {string} [suffix]
 */
function resolveEditedName(inputs, suffix = `${Date.now()}`) {
  const prefix = inputs?.editNamePrefix || `${inputs?.namePrefix || 'HW04-P'}-EDIT`;
  return `${prefix}-${suffix}`;
}

/**
 * @param {any} inputs
 * @param {string} [suffix]
 */
function resolveSiblingName(inputs, suffix = `${Date.now()}`) {
  const prefix = inputs?.siblingNamePrefix || 'HW04-P-SIB';
  return `${prefix}-${suffix}`;
}

/**
 * @param {any} inputs
 * @param {{ id: number }[]} categories
 */
function resolveCategoryId(inputs, categories) {
  const mode = inputs?.categoryMode || 'existingFirst';
  if (mode === 'existingFirst') {
    if (!categories.length) throw new Error('No categories available');
    return Number(categories[0].id);
  }
  if (mode === 'invalidId' || mode === 'literal') {
    return Number(inputs.categoryId);
  }
  throw new Error(`Unknown categoryMode: ${mode}`);
}

/**
 * @param {any[]} products
 * @param {string} name
 */
function findByName(products, name) {
  return products.find((p) => p && p.name === name) || null;
}

/**
 * @param {any[]} products
 * @param {string|number} id
 */
function findById(products, id) {
  return products.find((p) => Number(p.id) === Number(id)) || null;
}

module.exports = {
  listCategories,
  listProducts,
  getProduct,
  createProduct,
  updateProduct,
  deleteProduct,
  resolveProductName,
  resolveEditedName,
  resolveSiblingName,
  resolveCategoryId,
  findByName,
  findById,
};

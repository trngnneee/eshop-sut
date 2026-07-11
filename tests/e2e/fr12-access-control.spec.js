// tests/e2e/fr12-access-control.spec.js
// FR-12: Access Control
// Source test design:
// - SoftwareTesting-HW/DTT/Test Case/FR-12-DTT-test-cases.md
// - SoftwareTesting-HW/DTT/Test Case/FR-12-Pairwise-test-cases.md

const { test, expect } = require('@playwright/test');
const crypto = require('crypto');
const { API_URL, ACCOUNTS } = require('../fixtures/test-data');

const JWT_SECRET = 'super_secret_key_that_should_not_be_here';

function base64Url(input) {
  return Buffer.from(input)
    .toString('base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
}

function signHs256(payload, secret) {
  const headerPart = base64Url(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
  const payloadPart = base64Url(JSON.stringify(payload));
  const unsigned = `${headerPart}.${payloadPart}`;
  const signature = crypto
    .createHmac('sha256', secret)
    .update(unsigned)
    .digest('base64')
    .replace(/=/g, '')
    .replace(/\+/g, '-')
    .replace(/\//g, '_');
  return `${unsigned}.${signature}`;
}

function decodeJwtPayload(token) {
  const parts = String(token || '').split('.');
  if (parts.length < 2) return {};
  const padded = parts[1].replace(/-/g, '+').replace(/_/g, '/');
  const padLen = (4 - (padded.length % 4)) % 4;
  const decoded = Buffer.from(`${padded}${'='.repeat(padLen)}`, 'base64').toString('utf8');
  return JSON.parse(decoded);
}

async function loginAndGetToken(request, account) {
  const res = await request.post(`${API_URL}/api/login`, {
    data: { email: account.email, password: account.password },
  });
  expect(res.ok(), `Login must succeed for ${account.email}`).toBeTruthy();
  const body = await res.json();
  expect(body.token, 'Login response must include token').toBeTruthy();
  return body.token;
}

async function callProtectedEndpoint(request, endpointGroup, authMode, tokenForBearer, payloadOverride) {
  const endpoint =
    endpointGroup === 'admin_api'
      ? { method: 'GET', url: `${API_URL}/api/admin/users` }
      : { method: 'POST', url: `${API_URL}/api/products` };

  const headers = {};
  if (authMode === 'bearer') headers.Authorization = `Bearer ${tokenForBearer}`;
  if (authMode === 'wrong_scheme') headers.Authorization = `Token ${tokenForBearer}`;

  const reqOpts = { headers };
  if (endpoint.method !== 'GET') {
    reqOpts.data =
      payloadOverride ??
      {
        name: `FR12 Auth Product ${Date.now()}`,
        price: 123456,
        description: 'FR-12 automation',
        category_id: 1,
      };
  }

  return request.fetch(endpoint.url, { method: endpoint.method, ...reqOpts });
}

function expectAccessResult(res, expected) {
  if (expected === 'allow') {
    expect([401, 403], 'Allowed case must not be rejected by auth').not.toContain(res.status());
    return;
  }
  if (expected === '401') {
    expect(res.status(), 'Expected 401 Unauthorized').toBe(401);
    return;
  }
  if (expected === '403') {
    expect(res.status(), 'Expected 403 Forbidden').toBe(403);
    return;
  }
  throw new Error(`Unknown expected outcome: ${expected}`);
}

test.describe('FR-12 · DTT automation (TC-FR12-DTT-01..08)', () => {
  test('TC-FR12-DTT-01 · Valid admin token -> allow', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const res = await callProtectedEndpoint(request, 'data_api', 'bearer', adminToken);
    expectAccessResult(res, 'allow');
  });

  test('TC-FR12-DTT-02 · Missing Authorization header -> 401', async ({ request }) => {
    const res = await callProtectedEndpoint(request, 'data_api', 'missing', null);
    expectAccessResult(res, '401');
  });

  test('TC-FR12-DTT-03 · Malformed token -> 401', async ({ request }) => {
    const res = await callProtectedEndpoint(request, 'data_api', 'bearer', 'abc.def');
    expectAccessResult(res, '401');
  });

  test('TC-FR12-DTT-04 · Expired token -> 401', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const payload = decodeJwtPayload(adminToken);
    const expiredToken = signHs256({ id: payload.id, role: 'admin', exp: Math.floor(Date.now() / 1000) - 60 }, JWT_SECRET);
    const res = await callProtectedEndpoint(request, 'admin_api', 'bearer', expiredToken);
    expectAccessResult(res, '401');
  });

  test('TC-FR12-DTT-05 · Missing role claim token -> 401', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const payload = decodeJwtPayload(adminToken);
    const noRoleToken = signHs256({ id: payload.id }, JWT_SECRET);
    const res = await callProtectedEndpoint(request, 'data_api', 'bearer', noRoleToken);
    expectAccessResult(res, '401');
  });

  test('TC-FR12-DTT-06 · Non-admin user token -> 403', async ({ request }) => {
    const userToken = await loginAndGetToken(request, ACCOUNTS.user);
    const res = await callProtectedEndpoint(request, 'data_api', 'bearer', userToken);
    expectAccessResult(res, '403');
  });

  test('TC-FR12-DTT-07 · Non-admin user on /api/admin/* -> 403', async ({ request }) => {
    const userToken = await loginAndGetToken(request, ACCOUNTS.user);
    const res = await callProtectedEndpoint(request, 'admin_api', 'bearer', userToken);
    expectAccessResult(res, '403');
  });

  test('TC-FR12-DTT-08 · Wrong auth scheme -> 401', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const res = await callProtectedEndpoint(request, 'data_api', 'wrong_scheme', adminToken);
    expectAccessResult(res, '401');
  });
});

test.describe('FR-12 · Pairwise automation (PW-01..08)', () => {
  test('PW-01 · admin_api + bearer + valid + role present + admin -> Allow', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const res = await callProtectedEndpoint(request, 'admin_api', 'bearer', adminToken);
    expectAccessResult(res, 'allow');
  });

  test('PW-02 · data_api + missing header -> 401', async ({ request }) => {
    const res = await callProtectedEndpoint(request, 'data_api', 'missing', null);
    expectAccessResult(res, '401');
  });

  test('PW-03 · admin_api + wrong scheme + malformed token -> 401', async ({ request }) => {
    const res = await callProtectedEndpoint(request, 'admin_api', 'wrong_scheme', 'broken.token.value');
    expectAccessResult(res, '401');
  });

  test('PW-04 · data_api + bearer + expired token -> 401', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const payload = decodeJwtPayload(adminToken);
    const expiredToken = signHs256({ id: payload.id, role: 'admin', exp: Math.floor(Date.now() / 1000) - 60 }, JWT_SECRET);
    const res = await callProtectedEndpoint(request, 'data_api', 'bearer', expiredToken);
    expectAccessResult(res, '401');
  });

  test('PW-05 · admin_api + bearer + valid + role missing -> 401', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const payload = decodeJwtPayload(adminToken);
    const noRoleToken = signHs256({ id: payload.id }, JWT_SECRET);
    const res = await callProtectedEndpoint(request, 'admin_api', 'bearer', noRoleToken);
    expectAccessResult(res, '401');
  });

  test('PW-06 · data_api + bearer + valid + non-admin -> 403', async ({ request }) => {
    const userToken = await loginAndGetToken(request, ACCOUNTS.user);
    const res = await callProtectedEndpoint(request, 'data_api', 'bearer', userToken);
    expectAccessResult(res, '403');
  });

  test('PW-07 · admin_api + bearer + valid + non-admin -> 403', async ({ request }) => {
    const userToken = await loginAndGetToken(request, ACCOUNTS.user);
    const res = await callProtectedEndpoint(request, 'admin_api', 'bearer', userToken);
    expectAccessResult(res, '403');
  });

  test('PW-08 · data_api + bearer + valid + admin -> Allow', async ({ request }) => {
    const adminToken = await loginAndGetToken(request, ACCOUNTS.admin);
    const res = await callProtectedEndpoint(request, 'data_api', 'bearer', adminToken);
    expectAccessResult(res, 'allow');
  });
});

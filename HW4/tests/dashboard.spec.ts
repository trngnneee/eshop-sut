import { test, expect, type Page, type APIRequestContext } from '@playwright/test';
import { API_BASE_URL, apiLogin, ADMIN_CREDENTIALS, SEED_USER_CREDENTIALS } from './utils/api';
import { clearAllOrders } from './utils/db';
import { loadJsonArray, type DataRowValidator } from './utils/data';

const STUDENT_ID = '23127207';

interface OrderSeed {
  amount: number | null;
  finalStatus: string;
}

interface DataCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  orders?: OrderSeed[];
  expectedOrderCount?: number;
  expectedRevenue?: number;
  thenTransitionLastOrderTo?: string;
  expectedRevenueAfterTransition?: number;
  check?: string;
}

const ALLOWED_CHECKS = new Set(['non-admin-blocked-at-login', 'offline-during-load']);

const validateDataCase: DataRowValidator<DataCase> = (row, index) => {
  if (typeof row.category !== 'string' || typeof row.description !== 'string') {
    throw new Error(`dashboard-data-cases.json row ${index + 1}: category and description are required`);
  }
  if (row.check !== undefined) {
    if (!ALLOWED_CHECKS.has(row.check)) {
      throw new Error(`dashboard-data-cases.json row ${index + 1}: unknown check "${row.check}"`);
    }
    return;
  }
  if (!Array.isArray(row.orders)) {
    throw new Error(`dashboard-data-cases.json row ${index + 1}: orders must be an array`);
  }
  for (const [orderIndex, order] of row.orders.entries()) {
    if (!order || typeof order.finalStatus !== 'string' || !Object.hasOwn(TRANSITION_PATH, order.finalStatus)) {
      throw new Error(
        `dashboard-data-cases.json row ${index + 1}, order ${orderIndex + 1}: unknown finalStatus`,
      );
    }
    if (order.amount !== null && typeof order.amount !== 'number') {
      throw new Error(`dashboard-data-cases.json row ${index + 1}, order ${orderIndex + 1}: amount must be a number or null`);
    }
  }
  if (typeof row.expectedOrderCount !== 'number' || typeof row.expectedRevenue !== 'number') {
    throw new Error(
      `dashboard-data-cases.json row ${index + 1}: expectedOrderCount and expectedRevenue are required for metric cases`,
    );
  }
  if (row.thenTransitionLastOrderTo !== undefined && !Object.hasOwn(TRANSITION_PATH, row.thenTransitionLastOrderTo)) {
    throw new Error(`dashboard-data-cases.json row ${index + 1}: unknown transition target`);
  }
  if (row.thenTransitionLastOrderTo !== undefined && row.orders.length === 0) {
    throw new Error(`dashboard-data-cases.json row ${index + 1}: a transition target needs at least one order`);
  }
  if (row.expectedRevenueAfterTransition !== undefined && typeof row.expectedRevenueAfterTransition !== 'number') {
    throw new Error(`dashboard-data-cases.json row ${index + 1}: expectedRevenueAfterTransition must be a number`);
  }
};

// pending is the natural state right after checkout; list the *additional* hops needed.
const TRANSITION_PATH: Record<string, string[]> = {
  pending: [],
  confirmed: ['confirmed'],
  canceled: ['canceled'],
  shipping: ['confirmed', 'shipping'],
  delivered: ['confirmed', 'shipping', 'delivered'],
};

const dataCases = loadJsonArray<DataCase>('dashboard-data-cases.json', 12, validateDataCase);

async function seedOrder(
  request: APIRequestContext,
  userToken: string,
  adminToken: string,
  amount: number | null,
  finalStatus: string,
): Promise<number> {
  const res = await request.post(`${API_BASE_URL}/api/checkout`, {
    headers: { Authorization: `Bearer ${userToken}` },
    data: { total_amount: amount, items: [] },
  });
  const body = (await res.json()) as { orderId?: unknown };
  if (typeof body.orderId !== 'number') throw new Error('Checkout setup did not return a numeric orderId');
  const orderId = body.orderId;
  for (const status of TRANSITION_PATH[finalStatus] ?? []) {
    await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
      headers: { Authorization: `Bearer ${adminToken}` },
      data: { status },
    });
  }
  return orderId;
}

async function loginAdminUI(page: Page, email: string, password: string) {
  await page.goto('/');
  await page.getByPlaceholder('Email').fill(email);
  await page.getByPlaceholder('Password').fill(password);
  await page.getByRole('button', { name: 'Login' }).click();
}

/** Reads the numeric value out of one of the two dashboard metric cards. */
async function readMetricNumber(page: Page, heading: string): Promise<number> {
  const card = page.getByText(heading, { exact: false }).locator('..');
  const text = (await card.locator('p').textContent()) ?? '';
  const cleaned = text
    .replace(/[^\d.,-]/g, '')
    .replace(/\.(?=\d{3}(\D|$))/g, '') // strip thousands separators
    .replace(',', '.'); // decimal comma -> dot
  return parseFloat(cleaned);
}

// Assertion patterns in this file: toBeVisible (dialog/login-form checks), toContain
// (dialog message text), and expect.poll(...).toBe (exact numeric equality on the two
// rendered metric cards — the primary oracle for the revenue-doubling bug).
test.describe('FR-13 Admin Dashboard metrics (data-driven)', () => {
  for (const c of dataCases) {
    test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      if (c.check === 'non-admin-blocked-at-login') {
        const dialogPromise = page.waitForEvent('dialog').then(async (dialog) => {
          const message = dialog.message();
          await dialog.accept();
          return message;
        });
        await loginAdminUI(page, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
        const dialogMessage = await dialogPromise;
        // Assertion pattern: alert dialog content
        expect(dialogMessage).toContain('admin');
        // Assertion pattern: still on the admin login form, not the dashboard
        await expect(page.getByRole('heading', { name: 'Admin Login' })).toBeVisible();
        return;
      }

      if (c.check === 'offline-during-load') {
        // App.jsx's fetchData() fires 5 sequential axios calls with a single catch block
        // that only handles 401/403 (forces logout); any other failure — including one
        // request in the middle of the chain being unreachable — breaks the whole chain
        // silently with no user-facing message. Abort just one call (admin/orders) so the
        // login itself still succeeds and only the data-load step is affected — a more
        // targeted repro than a full offline reload (which would also break the SPA shell).
        await page.route('**/api/admin/orders', (route) => route.abort());
        await loginAdminUI(page, ADMIN_CREDENTIALS.email, ADMIN_CREDENTIALS.password);
        await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
        // Spec-conformant expectation: the admin should be told something went wrong
        // instead of seeing an unexplained blank/stale dashboard.
        await expect(page.getByText(/lỗi|error|không thể tải|thử lại/i)).toBeVisible();
        return;
      }

      await clearAllOrders();
      const userLogin = (await (await apiLogin(request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password)).json()) as { token?: unknown };
      const adminLogin = (await (await apiLogin(request, ADMIN_CREDENTIALS.email, ADMIN_CREDENTIALS.password)).json()) as { token?: unknown };
      if (typeof userLogin.token !== 'string' || typeof adminLogin.token !== 'string') {
        throw new Error('Dashboard setup could not obtain both user and admin tokens');
      }
      const userToken = userLogin.token;
      const adminToken = adminLogin.token;

      const orderIds: number[] = [];
      for (const o of c.orders ?? []) {
        orderIds.push(await seedOrder(request, userToken, adminToken, o.amount, o.finalStatus));
      }

      await loginAdminUI(page, ADMIN_CREDENTIALS.email, ADMIN_CREDENTIALS.password);
      await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();

      // Assertion pattern: numeric equality on the order-count card
      await expect
        .poll(async () => readMetricNumber(page, 'Tổng số đơn hàng'))
        .toBe(c.expectedOrderCount);
      // Assertion pattern: numeric equality on the revenue card
      await expect
        .poll(async () => readMetricNumber(page, 'Tổng doanh thu'))
        .toBe(c.expectedRevenue);

      if (c.thenTransitionLastOrderTo) {
        const lastId = orderIds[orderIds.length - 1];
        await request.put(`${API_BASE_URL}/api/admin/orders/${lastId}/status`, {
          headers: { Authorization: `Bearer ${adminToken}` },
          data: { status: c.thenTransitionLastOrderTo },
        });
        await page.reload();
        await expect
          .poll(async () => readMetricNumber(page, 'Tổng doanh thu'))
          .toBe(c.expectedRevenueAfterTransition);
      }
    });
  }
});

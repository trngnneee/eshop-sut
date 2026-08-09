import { test, expect, type Page, type APIRequestContext } from '@playwright/test';
import { API_BASE_URL, apiLogin, ADMIN_CREDENTIALS, SEED_USER_CREDENTIALS } from './utils/api';
import { clearAllOrders } from './utils/db';
import { loadJsonArray } from './utils/data';

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

const dataCases = loadJsonArray<DataCase>('dashboard-data-cases.json', 5);

// pending is the natural state right after checkout; list the *additional* hops needed.
const TRANSITION_PATH: Record<string, string[]> = {
  pending: [],
  confirmed: ['confirmed'],
  canceled: ['canceled'],
  shipping: ['confirmed', 'shipping'],
  delivered: ['confirmed', 'shipping', 'delivered'],
};

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
  const body = await res.json();
  const orderId = body.orderId as number;
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
  const card = page.locator('div.bg-white').filter({ hasText: heading });
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
        let dialogMessage = '';
        page.on('dialog', async (d) => {
          dialogMessage = d.message();
          await d.accept();
        });
        await loginAdminUI(page, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
        await page.waitForTimeout(500);
        // Assertion pattern: alert dialog content
        expect(dialogMessage).toContain('admin');
        // Assertion pattern: still on the admin login form, not the dashboard
        await expect(page.getByText('Admin Login')).toBeVisible();
        return;
      }

      await clearAllOrders();
      const userToken = (await (await apiLogin(request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password)).json()).token;
      const adminToken = (await (await apiLogin(request, ADMIN_CREDENTIALS.email, ADMIN_CREDENTIALS.password)).json()).token;

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

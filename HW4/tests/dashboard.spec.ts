import { test, expect, type Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';
import { API_BASE_URL, apiLogin, ADMIN_CREDENTIALS, SEED_USER_CREDENTIALS } from './utils/api';
import { clearAllOrders } from './utils/db';

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

function loadJsonArray<T extends { caseId: string }>(fileName: string, minCount: number): T[] {
  const filePath = path.join(__dirname, '../test-data', fileName);
  if (!fs.existsSync(filePath)) throw new Error(`Test data file not found: ${filePath}`);
  const parsed = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  if (!Array.isArray(parsed)) throw new Error(`${fileName} must contain a JSON array`);
  if (parsed.length < minCount) throw new Error(`${fileName} needs at least ${minCount} cases, found ${parsed.length}`);
  const seen = new Set<string>();
  for (const row of parsed) {
    if (!row || typeof row.caseId !== 'string') throw new Error(`${fileName}: a case is missing caseId`);
    if (seen.has(row.caseId)) throw new Error(`${fileName}: duplicate caseId ${row.caseId}`);
    seen.add(row.caseId);
  }
  return parsed as T[];
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
  request: any,
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

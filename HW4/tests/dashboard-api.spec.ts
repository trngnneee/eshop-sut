import { test, expect, type APIRequestContext } from '@playwright/test';
import { API_BASE_URL, apiLogin, ensureFreshAccount, ADMIN_CREDENTIALS } from './utils/api';
import { clearAllOrders, deleteUserByEmail, promoteToAdmin } from './utils/db';
import { loadJsonArray } from './utils/data';

const STUDENT_ID = '23127207';

interface ApiCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  action: string;
  from?: string;
  to?: string;
}

/** Shape of one row in the /api/admin/users response — only the fields these cases inspect. */
interface AdminUserRow {
  id: number;
  email: string;
  password?: unknown;
}

const cases = loadJsonArray<ApiCase>('dashboard-api-cases.json', 1);

const TRANSITION_PATH: Record<string, string[]> = {
  pending: [],
  confirmed: ['confirmed'],
  canceled: ['canceled'],
  shipping: ['confirmed', 'shipping'],
  delivered: ['confirmed', 'shipping', 'delivered'],
};

async function regularUserToken(request: APIRequestContext, caseId: string): Promise<string> {
  const email = `dash-${caseId.toLowerCase()}@eshop.com`;
  await deleteUserByEmail(email).catch(() => undefined);
  await ensureFreshAccount(request, email, 'ValidPassword1!');
  const res = await apiLogin(request, email, 'ValidPassword1!');
  return (await res.json()).token;
}

async function adminToken(request: APIRequestContext): Promise<string> {
  const res = await apiLogin(request, ADMIN_CREDENTIALS.email, ADMIN_CREDENTIALS.password);
  return (await res.json()).token;
}

/** Creates one order and walks it to `fromStatus`, returning its id. */
async function seedOrderAt(request: APIRequestContext, userTok: string, adminTok: string, fromStatus: string): Promise<number> {
  const res = await request.post(`${API_BASE_URL}/api/checkout`, {
    headers: { Authorization: `Bearer ${userTok}` },
    data: { total_amount: 100000, items: [] },
  });
  const orderId = (await res.json()).orderId as number;
  for (const status of TRANSITION_PATH[fromStatus] ?? []) {
    await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
      headers: { Authorization: `Bearer ${adminTok}` },
      data: { status },
    });
  }
  return orderId;
}

test.describe('FR-13 Dashboard/admin API access control', () => {
  for (const c of cases) {
    test(`${c.caseId}: ${c.description}`, async ({ request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      switch (c.action) {
        case 'admin-users-no-token': {
          const res = await request.get(`${API_BASE_URL}/api/admin/users`);
          expect(res.status()).toBe(401);
          break;
        }
        case 'admin-users-regular-user-token': {
          const token = await regularUserToken(request, c.caseId);
          const res = await request.get(`${API_BASE_URL}/api/admin/users`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          expect(res.status()).toBe(403);
          break;
        }
        case 'admin-orders-regular-user-token': {
          const token = await regularUserToken(request, c.caseId);
          const res = await request.get(`${API_BASE_URL}/api/admin/orders`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          expect(res.status()).toBe(403);
          break;
        }
        case 'admin-orders-no-token': {
          const res = await request.get(`${API_BASE_URL}/api/admin/orders`);
          expect(res.status()).toBe(401);
          break;
        }
        case 'delete-user-no-token': {
          const res = await request.delete(`${API_BASE_URL}/api/admin/users/1`);
          expect(res.status()).toBe(401);
          break;
        }
        case 'delete-user-regular-user-token': {
          const victimEmail = `dash-victim-${c.caseId.toLowerCase()}@eshop.com`;
          await deleteUserByEmail(victimEmail).catch(() => undefined);
          await ensureFreshAccount(request, victimEmail, 'ValidPassword1!');
          const victimRes = await apiLogin(request, victimEmail, 'ValidPassword1!');
          const admin = await adminToken(request);
          const victimList = await (
            await request.get(`${API_BASE_URL}/api/admin/users`, { headers: { Authorization: `Bearer ${admin}` } })
          ).json();
          const victimId = victimList.find((u: AdminUserRow) => u.email === victimEmail)?.id;
          const attackerToken = await regularUserToken(request, `${c.caseId}-attacker`);
          const res = await request.delete(`${API_BASE_URL}/api/admin/users/${victimId}`, {
            headers: { Authorization: `Bearer ${attackerToken}` },
          });
          expect(res.status()).toBe(403);
          break;
        }
        case 'delete-nonexistent-user': {
          const admin = await adminToken(request);
          const res = await request.delete(`${API_BASE_URL}/api/admin/users/99999999`, {
            headers: { Authorization: `Bearer ${admin}` },
          });
          expect(res.status()).toBe(404);
          break;
        }
        case 'admin-self-delete-blocked': {
          // Uses a disposable account promoted to role='admin' via direct DB write
          // instead of the real seed admin@eshop.com — if this really is unguarded
          // (NEW-BUG-FR13-02), deleting the actual seed admin would permanently break
          // every other admin-authenticated case that runs afterward.
          const disposableAdminEmail = `dash-${c.caseId.toLowerCase()}-admin@eshop.com`;
          await deleteUserByEmail(disposableAdminEmail).catch(() => undefined);
          await ensureFreshAccount(request, disposableAdminEmail, 'ValidPassword1!');
          await promoteToAdmin(disposableAdminEmail);
          const selfRes = await apiLogin(request, disposableAdminEmail, 'ValidPassword1!');
          const selfToken = (await selfRes.json()).token;
          const users = await (
            await request.get(`${API_BASE_URL}/api/admin/users`, { headers: { Authorization: `Bearer ${selfToken}` } })
          ).json();
          const selfUser = users.find((u: AdminUserRow) => u.email === disposableAdminEmail);
          const res = await request.delete(`${API_BASE_URL}/api/admin/users/${selfUser.id}`, {
            headers: { Authorization: `Bearer ${selfToken}` },
          });
          expect(res.status()).toBe(400);
          break;
        }
        case 'invalid-transition': {
          await clearAllOrders();
          const userTok = await regularUserToken(request, c.caseId);
          const admin = await adminToken(request);
          const orderId = await seedOrderAt(request, userTok, admin, c.from!);
          const res = await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
            headers: { Authorization: `Bearer ${admin}` },
            data: { status: c.to },
          });
          expect(res.status()).toBe(400);
          break;
        }
        case 'valid-transition': {
          await clearAllOrders();
          const userTok = await regularUserToken(request, c.caseId);
          const admin = await adminToken(request);
          const orderId = await seedOrderAt(request, userTok, admin, c.from!);
          const res = await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
            headers: { Authorization: `Bearer ${admin}` },
            data: { status: c.to },
          });
          expect(res.status()).toBe(200);
          break;
        }
        case 'update-status-nonexistent-order': {
          const admin = await adminToken(request);
          const res = await request.put(`${API_BASE_URL}/api/admin/orders/99999999/status`, {
            headers: { Authorization: `Bearer ${admin}` },
            data: { status: 'confirmed' },
          });
          expect(res.status()).toBe(404);
          break;
        }
        case 'admin-users-malformed-token': {
          const res = await request.get(`${API_BASE_URL}/api/admin/users`, {
            headers: { Authorization: 'Bearer not-a-real-token' },
          });
          expect(res.status()).not.toBe(500);
          break;
        }
        case 'update-status-regular-user-token': {
          await clearAllOrders();
          const admin = await adminToken(request);
          const userTok = await regularUserToken(request, c.caseId);
          const orderId = await seedOrderAt(request, userTok, admin, 'pending');
          const attackerToken = await regularUserToken(request, `${c.caseId}-attacker`);
          const res = await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
            headers: { Authorization: `Bearer ${attackerToken}` },
            data: { status: 'confirmed' },
          });
          expect(res.status()).toBe(403);
          break;
        }
        case 'admin-users-no-password-leak': {
          const admin = await adminToken(request);
          const users = await (
            await request.get(`${API_BASE_URL}/api/admin/users`, { headers: { Authorization: `Bearer ${admin}` } })
          ).json();
          expect(users.every((u: AdminUserRow) => u.password === undefined)).toBe(true);
          break;
        }
        case 'update-status-missing-field': {
          await clearAllOrders();
          const userTok = await regularUserToken(request, c.caseId);
          const admin = await adminToken(request);
          const orderId = await seedOrderAt(request, userTok, admin, 'pending');
          const res = await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
            headers: { Authorization: `Bearer ${admin}` },
            data: {},
          });
          expect(res.status()).toBe(400);
          break;
        }
        case 'delete-non-numeric-id': {
          const admin = await adminToken(request);
          const res = await request.delete(`${API_BASE_URL}/api/admin/users/abc`, {
            headers: { Authorization: `Bearer ${admin}` },
          });
          expect(res.status()).toBe(400);
          break;
        }
        case 'delete-sql-injection-id': {
          const admin = await adminToken(request);
          const before = await (
            await request.get(`${API_BASE_URL}/api/admin/users`, { headers: { Authorization: `Bearer ${admin}` } })
          ).json();
          const res = await request.delete(`${API_BASE_URL}/api/admin/users/${encodeURIComponent('1 OR 1=1')}`, {
            headers: { Authorization: `Bearer ${admin}` },
          });
          const after = await (
            await request.get(`${API_BASE_URL}/api/admin/users`, { headers: { Authorization: `Bearer ${admin}` } })
          ).json();
          // Spec-conformant expectation: malformed id is rejected outright.
          expect(res.status()).toBe(400);
          // Regardless of the status code above, the user table must never be wiped.
          expect(after.length).toBe(before.length);
          break;
        }
        case 'admin-users-exposes-lockout-fields': {
          const admin = await adminToken(request);
          const users = await (
            await request.get(`${API_BASE_URL}/api/admin/users`, { headers: { Authorization: `Bearer ${admin}` } })
          ).json();
          expect(users.length).toBeGreaterThan(0);
          expect(users.every((u: any) => 'login_attempts' in u && 'locked_until' in u)).toBe(true);
          break;
        }
        case 'admin-orders-empty-token': {
          const res = await request.get(`${API_BASE_URL}/api/admin/orders`, {
            headers: { Authorization: 'Bearer ' },
          });
          expect(res.status()).not.toBe(500);
          break;
        }
        case 'status-update-reflected': {
          await clearAllOrders();
          const userTok = await regularUserToken(request, c.caseId);
          const admin = await adminToken(request);
          const orderId = await seedOrderAt(request, userTok, admin, 'pending');
          await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, {
            headers: { Authorization: `Bearer ${admin}` },
            data: { status: 'confirmed' },
          });
          const orders = await (
            await request.get(`${API_BASE_URL}/api/admin/orders`, { headers: { Authorization: `Bearer ${admin}` } })
          ).json();
          const updated = orders.find((o: any) => o.id === orderId);
          expect(updated?.status).toBe('confirmed');
          break;
        }
        case 'delete-negative-id': {
          const admin = await adminToken(request);
          const res = await request.delete(`${API_BASE_URL}/api/admin/users/-1`, {
            headers: { Authorization: `Bearer ${admin}` },
          });
          expect(res.status()).toBe(400);
          break;
        }
        default:
          throw new Error(`Unknown action "${c.action}" for ${c.caseId}`);
      }
    });
  }
});

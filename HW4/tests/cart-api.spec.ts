import { test, expect, type APIRequestContext } from '@playwright/test';
import { API_BASE_URL, ensureFreshAccount, apiLogin, loginAdminToken } from './utils/api';
import { loadJsonArray } from './utils/data';

const STUDENT_ID = '23127207';
const CATALOG_PRODUCT = { id: 1, name: 'iPhone 15 Pro Max', price: 30000000 };

interface ApiCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  action: string;
  body?: Record<string, unknown>;
  price?: number;
  quantity?: number;
  quantityRaw?: unknown;
}

/** Shape of one item in the /api/cart response — only the fields these cases inspect. */
interface CartItem {
  id: number;
  name?: string;
  price?: number;
  isAdmin?: unknown;
}

const cases = loadJsonArray<ApiCase>('cart-api-cases.json', 1);

async function freshToken(request: APIRequestContext, suffix: string): Promise<string> {
  const email = `cart-${suffix}@eshop.com`;
  await ensureFreshAccount(request, email, 'ValidPassword1!');
  const res = await apiLogin(request, email, 'ValidPassword1!');
  const body = await res.json();
  return body.token as string;
}

test.describe('FR-07 Cart API contract', () => {
  for (const c of cases) {
    test(`${c.caseId}: ${c.description}`, async ({ request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      const token = await freshToken(request, c.caseId.toLowerCase());
      const auth = { Authorization: `Bearer ${token}` };

      switch (c.action) {
        case 'get-cart-with-token': {
          const res = await request.get(`${API_BASE_URL}/api/cart`, { headers: auth });
          expect(res.status()).toBe(200);
          expect(Array.isArray(await res.json())).toBe(true);
          break;
        }
        case 'get-cart-no-token': {
          const res = await request.get(`${API_BASE_URL}/api/cart`);
          expect(res.status()).toBe(401);
          break;
        }
        case 'post-valid-item': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { ...CATALOG_PRODUCT, quantity: 1 },
          });
          expect(res.status()).toBe(200);
          const cart = await (await request.get(`${API_BASE_URL}/api/cart`, { headers: auth })).json();
          expect(cart.some((i: CartItem) => i.id === CATALOG_PRODUCT.id)).toBe(true);
          break;
        }
        case 'post-duplicate-id-merges': {
          await request.post(`${API_BASE_URL}/api/cart`, { headers: auth, data: { ...CATALOG_PRODUCT, quantity: 2 } });
          await request.post(`${API_BASE_URL}/api/cart`, { headers: auth, data: { ...CATALOG_PRODUCT, quantity: 3 } });
          const cart = await (await request.get(`${API_BASE_URL}/api/cart`, { headers: auth })).json();
          expect(cart.filter((i: CartItem) => i.id === CATALOG_PRODUCT.id)).toHaveLength(1);
          break;
        }
        case 'post-quantity-value': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { ...CATALOG_PRODUCT, quantity: c.quantity },
          });
          // Spec-conformant expectation: an invalid quantity must be rejected.
          expect(res.status()).toBe(400);
          break;
        }
        case 'post-missing-field': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, { headers: auth, data: c.body });
          expect(res.status()).toBe(400);
          break;
        }
        case 'post-no-token': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, { data: { ...CATALOG_PRODUCT, quantity: 1 } });
          expect(res.status()).toBe(401);
          break;
        }
        case 'get-cart-invalid-token': {
          const res = await request.get(`${API_BASE_URL}/api/cart`, {
            headers: { Authorization: 'Bearer this-is-not-a-real-token' },
          });
          expect(res.status()).not.toBe(500);
          expect([401, 403]).toContain(res.status());
          break;
        }
        case 'cart-isolated-between-users': {
          const tokenB = await freshToken(request, `${c.caseId.toLowerCase()}-b`);
          await request.post(`${API_BASE_URL}/api/cart`, { headers: auth, data: { ...CATALOG_PRODUCT, quantity: 1 } });
          const cartB = await (
            await request.get(`${API_BASE_URL}/api/cart`, { headers: { Authorization: `Bearer ${tokenB}` } })
          ).json();
          expect(cartB).toHaveLength(0);
          break;
        }
        case 'post-price-value': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { id: CATALOG_PRODUCT.id, name: CATALOG_PRODUCT.name, price: c.price, quantity: 1 },
          });
          expect(res.status()).toBe(400);
          break;
        }
        case 'post-nonexistent-product-id': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { id: 999999, name: 'Ghost Product', price: 1, quantity: 1 },
          });
          expect(res.status()).toBe(400);
          break;
        }
        case 'post-tampered-name': {
          await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { id: CATALOG_PRODUCT.id, name: 'TOTALLY DIFFERENT NAME', price: CATALOG_PRODUCT.price, quantity: 1 },
          });
          const cart = await (await request.get(`${API_BASE_URL}/api/cart`, { headers: auth })).json();
          const item = cart.find((i: CartItem) => i.id === CATALOG_PRODUCT.id);
          expect(item?.name).toBe(CATALOG_PRODUCT.name);
          break;
        }
        case 'post-tampered-price-lower': {
          await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { id: CATALOG_PRODUCT.id, name: CATALOG_PRODUCT.name, price: 1, quantity: 1 },
          });
          const cart = await (await request.get(`${API_BASE_URL}/api/cart`, { headers: auth })).json();
          const item = cart.find((i: CartItem) => i.id === CATALOG_PRODUCT.id);
          expect(item?.price).toBe(CATALOG_PRODUCT.price);
          break;
        }
        case 'post-quantity-raw': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { ...CATALOG_PRODUCT, quantity: c.quantityRaw },
          });
          expect(res.status()).not.toBe(500);
          break;
        }
        case 'post-empty-body': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, { headers: auth, data: {} });
          expect(res.status()).toBe(400);
          break;
        }
        case 'post-malformed-json': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, {
            headers: { ...auth, 'Content-Type': 'application/json' },
            data: '{ broken json',
          });
          expect(res.status()).not.toBe(500);
          break;
        }
        case 'post-mass-assignment': {
          await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { ...CATALOG_PRODUCT, quantity: 1, isAdmin: true, discount: 99 },
          });
          const cart = await (await request.get(`${API_BASE_URL}/api/cart`, { headers: auth })).json();
          const item = cart.find((i: CartItem) => i.id === CATALOG_PRODUCT.id);
          expect(item?.isAdmin).toBeUndefined();
          break;
        }
        case 'get-cart-malformed-token': {
          const res = await request.get(`${API_BASE_URL}/api/cart`, {
            headers: { Authorization: 'Bearer not.a.jwt' },
          });
          expect(res.status()).not.toBe(500);
          break;
        }
        case 'cross-user-item-access': {
          // No PUT/DELETE-by-id endpoint exists for individual cart items — removal is
          // entirely client-side (see docs/ai-review-cart.md). This documents that the
          // attack surface described by the original manual case does not exist yet.
          const res = await request.delete(`${API_BASE_URL}/api/cart/999`, { headers: auth });
          expect(res.status()).toBe(404);
          break;
        }
        case 'post-compound-invalid': {
          const res = await request.post(`${API_BASE_URL}/api/cart`, {
            headers: auth,
            data: { id: CATALOG_PRODUCT.id, name: CATALOG_PRODUCT.name, price: -100, quantity: -5 },
          });
          expect(res.status()).toBe(400);
          break;
        }
        case 'post-multiple-order-consistency': {
          const items = [
            { id: 1, name: 'iPhone 15 Pro Max', price: 30000000 },
            { id: 2, name: 'Samsung Galaxy S24 Ultra', price: 28000000 },
            { id: 4, name: 'Tai nghe AirPods Pro 2', price: 6000000 },
          ];
          for (const item of items) {
            await request.post(`${API_BASE_URL}/api/cart`, { headers: auth, data: { ...item, quantity: 1 } });
          }
          const cart: CartItem[] = await (await request.get(`${API_BASE_URL}/api/cart`, { headers: auth })).json();
          expect(cart).toHaveLength(items.length);
          expect(items.every((item) => cart.some((c2) => c2.id === item.id))).toBe(true);
          break;
        }
        case 'unauthenticated-order-view-blocked': {
          // Checkout as the "victim" to create a real order with private data in it
          // (shipping_address), then try to read it back via GET /api/orders/:id with
          // NO Authorization header at all — this route has no authenticateToken
          // middleware and no ownership check, so anyone who can guess/enumerate an
          // order id can currently read any customer's shipping address and order total.
          const checkoutRes = await request.post(`${API_BASE_URL}/api/checkout`, {
            headers: auth,
            data: { total_amount: 555000, shipping_address: `Secret Address ${c.caseId}` },
          });
          const { orderId } = await checkoutRes.json();
          const unauthRes = await request.get(`${API_BASE_URL}/api/orders/${orderId}`);
          // Spec-conformant expectation: viewing an order requires authentication and
          // ownership (or admin), not just knowing/guessing its numeric id.
          expect([401, 403]).toContain(unauthRes.status());
          break;
        }
        case 'cancel-shipping-order-blocked': {
          const checkoutRes = await request.post(`${API_BASE_URL}/api/checkout`, {
            headers: auth,
            data: { total_amount: 200000, shipping_address: 'N/A' },
          });
          const { orderId } = await checkoutRes.json();
          const adminTok = await loginAdminToken(request);
          const adminAuth = { Authorization: `Bearer ${adminTok}` };
          await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, { headers: adminAuth, data: { status: 'confirmed' } });
          await request.put(`${API_BASE_URL}/api/admin/orders/${orderId}/status`, { headers: adminAuth, data: { status: 'shipping' } });
          const cancelRes = await request.put(`${API_BASE_URL}/api/orders/${orderId}/cancel`, { headers: auth });
          // Spec-conformant expectation: once an order is out for shipping, the customer
          // should no longer be able to self-cancel it (only pending/confirmed orders
          // should be cancelable) — the SUT's own source comment on this handler agrees
          // ("Lẽ ra phải là: if (order.status !== 'pending' && order.status !== 'confirmed')").
          expect(cancelRes.status()).toBe(400);
          break;
        }
        default:
          throw new Error(`Unknown API action "${c.action}" for ${c.caseId}`);
      }
    });
  }
});

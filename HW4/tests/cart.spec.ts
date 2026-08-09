import { test, expect, type Page, type APIRequestContext } from '@playwright/test';
import { API_BASE_URL, apiLogin, SEED_USER_CREDENTIALS } from './utils/api';
import { loadJsonArray } from './utils/data';

const STUDENT_ID = '23127207';
const PRODUCT_A_ID = 1;
const PRODUCT_A_NAME = 'iPhone 15 Pro Max';
const PRODUCT_A_PRICE = 30000000;
const PRODUCT_B_ID = 2;
const PRODUCT_B_NAME = 'Samsung Galaxy S24 Ultra';
const PRODUCT_B_PRICE = 28000000;

// ---------------------------------------------------------------------------------
interface UiCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  check: string;
  quantity?: string | number;
}

interface EdgeCase {
  caseId: string;
  category: string;
  description: string;
  bugRef?: string;
  action: string;
  tamperedTotal?: number;
}

const uiCases = loadJsonArray<UiCase>('cart-ui-cases.json', 12);
const edgeCases = loadJsonArray<EdgeCase>('cart-edge-cases.json', 1);

// ---------------------------------------------------------------------------------
// Page helpers.
//
// IMPORTANT: `CartContext` keeps the cart purely in React memory (see
// docs/ai-review-cart.md). `page.goto()` always performs a real browser navigation,
// which remounts the whole SPA and silently wipes that in-memory cart. Every helper
// below that needs to preserve cart state across steps therefore navigates by
// *clicking* an in-app link/button (a client-side route change) instead of calling
// `page.goto()` a second time within the same test.
// ---------------------------------------------------------------------------------
async function loginViaToken(page: Page, request: APIRequestContext, email: string, password: string) {
  const res = await apiLogin(request, email, password);
  const body = await res.json();
  await page.goto('/');
  await page.evaluate((t) => localStorage.setItem('token', t as string), body.token);
  await page.reload();
}

function homeCard(page: Page, productId: number) {
  return page.locator('div.border').filter({ has: page.locator(`a[href="/product/${productId}"]`) });
}

async function gotoHome(page: Page) {
  const onApp = page.url().includes('localhost');
  if (!onApp) {
    await page.goto('/');
    return;
  }
  await page.getByRole('link', { name: 'EShop' }).click();
  await expect(page).toHaveURL('http://localhost:5173/');
}

async function gotoProductDetail(page: Page, productId: number) {
  await gotoHome(page);
  await homeCard(page, productId).getByRole('link', { name: 'Xem chi tiết' }).click();
  await expect(page).toHaveURL(new RegExp(`/product/${productId}$`));
}

async function gotoCart(page: Page) {
  await page.getByRole('link', { name: /Giỏ hàng/ }).first().click();
  await expect(page).toHaveURL(/\/cart$/);
}

/** Adds a product from the detail page, working around the known "first click is
 * swallowed" defect (see docs/ai-review-cart.md) so this becomes a reliable setup step
 * for every case that isn't specifically testing that defect (TC-CART-054 tests it
 * directly). Always navigates client-side so cart state accumulated by earlier calls
 * within the same test is preserved. */
async function addFromDetailReliable(page: Page, productId: number, quantity?: string | number) {
  await gotoProductDetail(page, productId);
  if (quantity !== undefined) {
    await page.locator('input[type="number"]').fill(String(quantity));
  }
  const addButton = page.getByRole('button', { name: /Thêm vào giỏ hàng|Đã thêm/ });
  await addButton.click(); // swallowed by the known bug
  await addButton.click(); // actually adds
}

/** Same as `addFromDetailReliable`, but jumps straight to `/product/:id` by URL instead
 * of clicking through the home page's product grid. Needed for products created via API
 * moments earlier in the same test: Home's product list is fetched once on mount and a
 * same-route client-side "navigation" back to `/` does not remount/refetch it, so a
 * brand-new product's card would not exist yet to click. Only safe to use as the first
 * navigation in a test (a real `goto()` still wipes any in-memory cart). */
async function addFromDetailByUrl(page: Page, productId: number) {
  await page.goto(`/product/${productId}`);
  const addButton = page.getByRole('button', { name: /Thêm vào giỏ hàng|Đã thêm/ });
  await addButton.click(); // swallowed by the known bug
  await addButton.click(); // actually adds
}

function cartRow(page: Page, productName: string) {
  return page.locator('tr').filter({ hasText: productName });
}

/** Creates a throwaway product via the (unauthenticated — no authenticateToken middleware
 * on this route) product-management API, for cases that need a specific name/price
 * without touching the shared seed catalog. */
async function createDisposableProduct(request: APIRequestContext, name: string, price = 100000): Promise<number> {
  const res = await request.post(`${API_BASE_URL}/api/products`, {
    data: { name, price, description: '', imageUrl: '', category_id: 1 },
  });
  return (await res.json()).id as number;
}

// ---------------------------------------------------------------------------------
// Shape A — Cart page UI/UX (32 cases)
//
// Assertion patterns demonstrated across this file's switch cases: toBeVisible (most
// checks), toHaveCount (row/product counting), toContainText (price/subtotal text),
// toBeDisabled (checkout guard), toHaveText (exact quantity cell value), and plain
// `expect(x).toBe(y)` on captured dialog state/badge text (not.toBe for change checks).
// ---------------------------------------------------------------------------------
test.describe('FR-07 Shopping Cart UI', () => {
  for (const c of uiCases) {
    test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);

      switch (c.check) {
        case 'empty-message': {
          await gotoCart(page);
          await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
          break;
        }
        case 'empty-icon': {
          await gotoCart(page);
          await expect(page.locator('svg, img').first()).toBeVisible();
          break;
        }
        case 'empty-continue-link': {
          await gotoCart(page);
          await expect(page.getByRole('link', { name: 'Tiếp tục mua sắm' })).toBeVisible();
          break;
        }
        case 'breadcrumb': {
          await gotoCart(page);
          await expect(page.getByRole('navigation').filter({ hasText: /Trang chủ|Home/ })).toBeVisible();
          break;
        }
        case 'table-columns': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          for (const col of ['Sản phẩm', 'Giá', 'Số lượng', 'Thành tiền', 'Thao tác']) {
            await expect(page.getByRole('columnheader', { name: col })).toBeVisible();
          }
          break;
        }
        case 'price-format': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await expect(cartRow(page, PRODUCT_A_NAME)).toContainText(/\d{1,3}(\.\d{3})*\s*₫/);
          break;
        }
        case 'subtotal-single': {
          await addFromDetailReliable(page, PRODUCT_A_ID, c.quantity);
          await gotoCart(page);
          const expected = (PRODUCT_A_PRICE * Number(c.quantity)).toLocaleString('vi-VN');
          await expect(cartRow(page, PRODUCT_A_NAME)).toContainText(expected);
          break;
        }
        case 'total-label': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await expect(page.getByText('Tổng cộng', { exact: false })).toBeVisible();
          break;
        }
        case 'add-from-home': {
          await gotoHome(page);
          await homeCard(page, PRODUCT_A_ID).getByRole('button', { name: 'Thêm vào giỏ' }).click();
          await gotoCart(page);
          await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
          break;
        }
        case 'add-from-detail': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
          break;
        }
        case 'merge-duplicate-id': {
          await addFromDetailReliable(page, PRODUCT_A_ID, 2);
          await addFromDetailReliable(page, PRODUCT_A_ID, 3);
          await gotoCart(page);
          await expect(page.locator('tr').filter({ hasText: PRODUCT_A_NAME })).toHaveCount(1);
          await expect(cartRow(page, PRODUCT_A_NAME).locator('td').nth(2)).toHaveText('5');
          break;
        }
        case 'separate-rows-different-id': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await addFromDetailReliable(page, PRODUCT_B_ID);
          await gotoCart(page);
          await expect(page.locator('tbody tr')).toHaveCount(2);
          break;
        }
        case 'add-with-quantity': {
          await addFromDetailReliable(page, PRODUCT_A_ID, c.quantity);
          await gotoCart(page);
          // Spec-conformant expectation: an invalid quantity must not result in an
          // item silently added to the cart.
          await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
          break;
        }
        case 'qty-adjust-buttons-missing': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await expect(cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: /^[+-]$/ })).toBeVisible();
          break;
        }
        case 'total-realtime-multi': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await addFromDetailReliable(page, PRODUCT_B_ID);
          await gotoCart(page);
          const expected = (PRODUCT_A_PRICE + PRODUCT_B_PRICE).toLocaleString('vi-VN');
          // Scoped to the total footer, not a page-wide text search — the same amount
          // can legitimately also appear in a unit-price/subtotal cell.
          await expect(page.locator('div.text-xl.font-bold')).toContainText(expected);
          break;
        }
        case 'total-after-remove': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await addFromDetailReliable(page, PRODUCT_B_ID);
          await gotoCart(page);
          await cartRow(page, PRODUCT_B_NAME).getByRole('button', { name: 'Xóa' }).click();
          const expected = PRODUCT_A_PRICE.toLocaleString('vi-VN');
          await expect(page.locator('div.text-xl.font-bold')).toContainText(expected);
          break;
        }
        case 'remove-confirm-dialog-missing': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          let dialogAppeared = false;
          page.on('dialog', async (d) => {
            dialogAppeared = true;
            await d.accept();
          });
          await cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' }).click();
          expect(dialogAppeared).toBe(true);
          break;
        }
        case 'remove-last-item-empty-state': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' }).click();
          await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
          break;
        }
        case 'badge-after-add': {
          await gotoHome(page);
          const badgeBefore = await page.getByRole('link', { name: /Giỏ hàng/ }).textContent();
          await homeCard(page, PRODUCT_A_ID).getByRole('button', { name: 'Thêm vào giỏ' }).click();
          const badgeAfter = await page.getByRole('link', { name: /Giỏ hàng/ }).textContent();
          expect(badgeAfter).not.toBe(badgeBefore);
          break;
        }
        case 'badge-after-remove': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' }).click();
          await expect(page.getByRole('link', { name: /Giỏ hàng/ }).locator('span')).toHaveCount(0);
          break;
        }
        case 'toast-on-add-missing': {
          await gotoHome(page);
          await homeCard(page, PRODUCT_A_ID).getByRole('button', { name: 'Thêm vào giỏ' }).click();
          await expect(page.getByRole('alert')).toBeVisible();
          break;
        }
        case 'remove-repeated-click': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          const removeBtn = cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' });
          await removeBtn.click();
          await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
          // A second click has nothing left to act on; the page must stay usable.
          await expect(page.locator('body')).toBeVisible();
          break;
        }
        case 'add-single-click-works': {
          await gotoProductDetail(page, PRODUCT_A_ID);
          await page.getByRole('button', { name: /Thêm vào giỏ hàng/ }).click();
          await expect(page.getByRole('button', { name: 'Đã thêm' })).toBeVisible();
          break;
        }
        case 'stock-info-missing': {
          await gotoProductDetail(page, PRODUCT_A_ID);
          await expect(page.getByText(/còn|tồn kho|in stock/i)).toBeVisible();
          break;
        }
        case 'checkout-blocked-when-empty': {
          // Cart.jsx renders no checkout button at all when empty, so this is the one
          // legitimate case that must reach /checkout directly instead of via the cart
          // page's button.
          await page.goto('/checkout');
          await expect(page.getByRole('button', { name: /Xác Nhận Thanh Toán/i })).toBeDisabled();
          break;
        }
        case 'reload-persistence': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
          await page.reload();
          await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
          break;
        }
        case 'checkout-clears-cart': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await page.getByRole('button', { name: 'Tiến hành thanh toán' }).click();
          await expect(page).toHaveURL(/\/checkout$/);
          await page.getByRole('button', { name: /Xác Nhận Thanh Toán/i }).click();
          await expect(page.getByText('Thanh toán thành công')).toBeVisible();
          await gotoHome(page);
          await gotoCart(page);
          await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
          break;
        }
        case 'diacritics-product-name': {
          const name = 'Bàn phím cơ Dạ Quang Đặc Biệt';
          const id = await createDisposableProduct(request, name);
          await addFromDetailByUrl(page, id);
          await gotoCart(page);
          await expect(cartRow(page, name)).toBeVisible();
          break;
        }
        case 'special-char-product-name': {
          const name = `Tai nghe "Pro" & Co.`;
          const id = await createDisposableProduct(request, name);
          await addFromDetailByUrl(page, id);
          await gotoCart(page);
          await expect(cartRow(page, name)).toBeVisible();
          break;
        }
        case 'long-product-name': {
          const name = 'Sản phẩm siêu dài dùng để kiểm tra layout '.repeat(6).trim();
          const id = await createDisposableProduct(request, name);
          await addFromDetailByUrl(page, id);
          await gotoCart(page);
          await expect(page.locator('tbody tr')).toHaveCount(1);
          await expect(page.locator('body')).toBeVisible();
          break;
        }
        case 'xss-product-name': {
          const name = `<script>window.__xssFired = true</script>`;
          const id = await createDisposableProduct(request, name);
          let dialogAppeared = false;
          page.on('dialog', async (d) => {
            dialogAppeared = true;
            await d.dismiss();
          });
          await addFromDetailByUrl(page, id);
          await gotoCart(page);
          const fired = await page.evaluate(() => (window as any).__xssFired === true);
          expect(fired).toBe(false);
          expect(dialogAppeared).toBe(false);
          break;
        }
        case 'many-items-cart': {
          const ids: number[] = [];
          for (let i = 0; i < 12; i++) {
            ids.push(await createDisposableProduct(request, `Bulk Item ${i}`, 10000 + i));
          }
          await page.reload(); // safe: cart is still empty here, this just refreshes Home's product list
          for (const id of ids) {
            await gotoProductDetail(page, id);
            const addButton = page.getByRole('button', { name: /Thêm vào giỏ hàng|Đã thêm/ });
            await addButton.click();
            await addButton.click();
          }
          await gotoCart(page);
          await expect(page.locator('tbody tr')).toHaveCount(12);
          break;
        }
        case 'very-large-total': {
          const id = await createDisposableProduct(request, 'Kim Cương Xanh', 999999999999);
          await addFromDetailByUrl(page, id);
          await gotoCart(page);
          await expect(page.locator('div.text-xl.font-bold')).not.toContainText(/e\+|NaN/i);
          await expect(page.locator('div.text-xl.font-bold')).toContainText('999.999.999.999');
          break;
        }
        case 'cross-tab-no-sync': {
          await addFromDetailReliable(page, PRODUCT_A_ID);
          const secondPage = await page.context().newPage();
          await secondPage.goto('/cart');
          // Spec-conformant expectation (per a synced-cart design): the item added in the
          // first tab should be visible in a second tab of the same logged-in session.
          await expect(secondPage.getByText(PRODUCT_A_NAME)).toBeVisible();
          await secondPage.close();
          break;
        }
        default:
          throw new Error(`Unknown UI check "${c.check}" for ${c.caseId}`);
      }
    });
  }
});

// ---------------------------------------------------------------------------------
// Shape B — cross-session / data-integrity edge cases (5 cases)
// ---------------------------------------------------------------------------------
test.describe('FR-07 Shopping Cart edge cases', () => {
  for (const c of edgeCases) {
    test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
      testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
      if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });

      switch (c.action) {
        case 'cart-cleared-on-user-switch': {
          await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
          await addFromDetailReliable(page, PRODUCT_A_ID);
          const adminRes = await apiLogin(request, 'admin@eshop.com', 'Admin123!');
          const adminBody = await adminRes.json();
          await page.evaluate((t) => localStorage.setItem('token', t as string), adminBody.token);
          await page.reload(); // switching identity is itself a full reload in this SUT
          await gotoCart(page);
          await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
          break;
        }
        case 'cart-lost-on-relogin': {
          await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
          await gotoCart(page);
          await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
          break;
        }
        case 'cart-with-deleted-product': {
          // Uses a disposable product created just for this test instead of mutating
          // the shared seed catalog (deleting a real seed product would permanently
          // break every other case/browser run that assumes it still exists).
          await loginViaToken(page, request, 'admin@eshop.com', 'Admin123!');
          const token = await page.evaluate(() => localStorage.getItem('token'));
          const created = await request.post(`${API_BASE_URL}/api/products`, {
            headers: { Authorization: `Bearer ${token}` },
            data: { name: 'Disposable Test Product', price: 123000, description: '', imageUrl: '', category_id: 1 },
          });
          const disposableId = (await created.json()).id as number;
          await addFromDetailByUrl(page, disposableId);
          await request.delete(`${API_BASE_URL}/api/products/${disposableId}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          await gotoCart(page);
          await expect(page.locator('body')).toBeVisible();
          break;
        }
        case 'cart-with-price-changed-product': {
          // Same reasoning as above: create a disposable product, add it to the cart,
          // change ITS price, then restore it — the shared catalog products (used by
          // PRODUCT_A_PRICE-based assertions elsewhere) are never touched.
          await loginViaToken(page, request, 'admin@eshop.com', 'Admin123!');
          const token = await page.evaluate(() => localStorage.getItem('token'));
          const originalPrice = 9999000;
          const created = await request.post(`${API_BASE_URL}/api/products`, {
            headers: { Authorization: `Bearer ${token}` },
            data: { name: 'Price Drift Product', price: originalPrice, description: '', imageUrl: '', category_id: 1 },
          });
          const disposableId = (await created.json()).id as number;
          await addFromDetailByUrl(page, disposableId);
          await request.put(`${API_BASE_URL}/api/products/${disposableId}`, {
            headers: { Authorization: `Bearer ${token}` },
            data: { name: 'Price Drift Product', price: 1, description: '', imageUrl: '', category_id: 1 },
          });
          await gotoCart(page);
          // Spec-conformant expectation: cart should reflect the live catalog price.
          await expect(page.getByText('1 ₫', { exact: false })).toBeVisible();
          await request.delete(`${API_BASE_URL}/api/products/${disposableId}`, {
            headers: { Authorization: `Bearer ${token}` },
          });
          break;
        }
        case 'checkout-editable-total-tampering': {
          await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
          await addFromDetailReliable(page, PRODUCT_A_ID);
          await gotoCart(page);
          await page.getByRole('button', { name: 'Tiến hành thanh toán' }).click();
          await page.locator('input[type="number"]').fill(String(c.tamperedTotal));
          await page.getByRole('button', { name: /Xác Nhận Thanh Toán/i }).click();
          // Spec-conformant expectation: server should reject/recompute an implausible total.
          await expect(page.getByText(/không hợp lệ|invalid|từ chối/i)).toBeVisible();
          break;
        }
        default:
          throw new Error(`Unknown edge action "${c.action}" for ${c.caseId}`);
      }
    });
  }
});

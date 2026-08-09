# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: cart.spec.ts >> FR-07 Shopping Cart edge cases >> TC-CART-088-CHECKOUT-TAMPER: Sửa trực tiếp ô Tổng tiền thanh toán trên trang Checkout thành giá trị bất kỳ rồi xác nhận vẫn được backend chấp nhận (Price Tampering qua Checkout)
- Location: tests\cart.spec.ts:336:9

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText(/không hợp lệ|invalid|từ chối/i)
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByText(/không hợp lệ|invalid|từ chối/i)

```

```yaml
- banner:
  - link "EShop":
    - /url: /
  - navigation:
    - link "Giỏ hàng 1":
      - /url: /cart
    - link "Chào, Test User":
      - /url: /profile
    - button "Thoát"
- main:
  - heading "Thanh toán thành công!" [level=2]
  - paragraph: Cảm ơn bạn đã mua sắm tại EShop.
  - button "Quay lại trang chủ"
- contentinfo: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  312 |         case 'checkout-clears-cart': {
  313 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  314 |           await gotoCart(page);
  315 |           await page.getByRole('button', { name: 'Tiến hành thanh toán' }).click();
  316 |           await expect(page).toHaveURL(/\/checkout$/);
  317 |           await page.getByRole('button', { name: /Xác Nhận Thanh Toán/i }).click();
  318 |           await expect(page.getByText('Thanh toán thành công')).toBeVisible();
  319 |           await gotoHome(page);
  320 |           await gotoCart(page);
  321 |           await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
  322 |           break;
  323 |         }
  324 |         default:
  325 |           throw new Error(`Unknown UI check "${c.check}" for ${c.caseId}`);
  326 |       }
  327 |     });
  328 |   }
  329 | });
  330 | 
  331 | // ---------------------------------------------------------------------------------
  332 | // Shape B — cross-session / data-integrity edge cases (5 cases)
  333 | // ---------------------------------------------------------------------------------
  334 | test.describe('FR-07 Shopping Cart edge cases', () => {
  335 |   for (const c of edgeCases) {
  336 |     test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
  337 |       testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
  338 |       if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });
  339 | 
  340 |       switch (c.action) {
  341 |         case 'cart-cleared-on-user-switch': {
  342 |           await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
  343 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  344 |           const adminRes = await apiLogin(request, 'admin@eshop.com', 'Admin123!');
  345 |           const adminBody = await adminRes.json();
  346 |           await page.evaluate((t) => localStorage.setItem('token', t as string), adminBody.token);
  347 |           await page.reload(); // switching identity is itself a full reload in this SUT
  348 |           await gotoCart(page);
  349 |           await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
  350 |           break;
  351 |         }
  352 |         case 'cart-lost-on-relogin': {
  353 |           await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
  354 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  355 |           await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
  356 |           await gotoCart(page);
  357 |           await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
  358 |           break;
  359 |         }
  360 |         case 'cart-with-deleted-product': {
  361 |           // Uses a disposable product created just for this test instead of mutating
  362 |           // the shared seed catalog (deleting a real seed product would permanently
  363 |           // break every other case/browser run that assumes it still exists).
  364 |           await loginViaToken(page, request, 'admin@eshop.com', 'Admin123!');
  365 |           const token = await page.evaluate(() => localStorage.getItem('token'));
  366 |           const created = await request.post(`${API_BASE_URL}/api/products`, {
  367 |             headers: { Authorization: `Bearer ${token}` },
  368 |             data: { name: 'Disposable Test Product', price: 123000, description: '', imageUrl: '', category_id: 1 },
  369 |           });
  370 |           const disposableId = (await created.json()).id as number;
  371 |           await addFromDetailByUrl(page, disposableId);
  372 |           await request.delete(`${API_BASE_URL}/api/products/${disposableId}`, {
  373 |             headers: { Authorization: `Bearer ${token}` },
  374 |           });
  375 |           await gotoCart(page);
  376 |           await expect(page.locator('body')).toBeVisible();
  377 |           break;
  378 |         }
  379 |         case 'cart-with-price-changed-product': {
  380 |           // Same reasoning as above: create a disposable product, add it to the cart,
  381 |           // change ITS price, then restore it — the shared catalog products (used by
  382 |           // PRODUCT_A_PRICE-based assertions elsewhere) are never touched.
  383 |           await loginViaToken(page, request, 'admin@eshop.com', 'Admin123!');
  384 |           const token = await page.evaluate(() => localStorage.getItem('token'));
  385 |           const originalPrice = 9999000;
  386 |           const created = await request.post(`${API_BASE_URL}/api/products`, {
  387 |             headers: { Authorization: `Bearer ${token}` },
  388 |             data: { name: 'Price Drift Product', price: originalPrice, description: '', imageUrl: '', category_id: 1 },
  389 |           });
  390 |           const disposableId = (await created.json()).id as number;
  391 |           await addFromDetailByUrl(page, disposableId);
  392 |           await request.put(`${API_BASE_URL}/api/products/${disposableId}`, {
  393 |             headers: { Authorization: `Bearer ${token}` },
  394 |             data: { name: 'Price Drift Product', price: 1, description: '', imageUrl: '', category_id: 1 },
  395 |           });
  396 |           await gotoCart(page);
  397 |           // Spec-conformant expectation: cart should reflect the live catalog price.
  398 |           await expect(page.getByText('1 ₫', { exact: false })).toBeVisible();
  399 |           await request.delete(`${API_BASE_URL}/api/products/${disposableId}`, {
  400 |             headers: { Authorization: `Bearer ${token}` },
  401 |           });
  402 |           break;
  403 |         }
  404 |         case 'checkout-editable-total-tampering': {
  405 |           await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
  406 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  407 |           await gotoCart(page);
  408 |           await page.getByRole('button', { name: 'Tiến hành thanh toán' }).click();
  409 |           await page.locator('input[type="number"]').fill(String(c.tamperedTotal));
  410 |           await page.getByRole('button', { name: /Xác Nhận Thanh Toán/i }).click();
  411 |           // Spec-conformant expectation: server should reject/recompute an implausible total.
> 412 |           await expect(page.getByText(/không hợp lệ|invalid|từ chối/i)).toBeVisible();
      |                                                                         ^ Error: expect(locator).toBeVisible() failed
  413 |           break;
  414 |         }
  415 |         default:
  416 |           throw new Error(`Unknown edge action "${c.action}" for ${c.caseId}`);
  417 |       }
  418 |     });
  419 |   }
  420 | });
  421 | 
```
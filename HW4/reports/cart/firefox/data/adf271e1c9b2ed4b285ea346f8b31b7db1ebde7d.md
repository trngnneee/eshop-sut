# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: cart.spec.ts >> FR-07 Shopping Cart UI >> TC-CART-017: Nhập quantity = 0 khi thêm vào giỏ
- Location: tests\cart.spec.ts:130:9

# Error details

```
Error: expect(locator).toBeVisible() failed

Locator: getByText('Giỏ hàng của bạn đang trống')
Expected: visible
Timeout: 5000ms
Error: element(s) not found

Call log:
  - Expect "toBeVisible" with timeout 5000ms
  - waiting for getByText('Giỏ hàng của bạn đang trống')

```

```yaml
- banner:
  - link "EShop":
    - /url: /
  - navigation:
    - link "Giỏ hàng":
      - /url: /cart
    - link "Chào, Test User":
      - /url: /profile
    - button "Thoát"
- main:
  - heading "Giỏ Hàng" [level=2]
  - table:
    - rowgroup:
      - row "Sản phẩm Giá Số lượng Thành tiền Thao tác":
        - columnheader "Sản phẩm"
        - columnheader "Giá"
        - columnheader "Số lượng"
        - columnheader "Thành tiền"
        - columnheader "Thao tác"
    - rowgroup:
      - row "iPhone 15 Pro Max 30.000.000 ₫ 0 0 ₫ Xóa":
        - cell "iPhone 15 Pro Max"
        - cell "30.000.000 ₫"
        - cell "0"
        - cell "0 ₫"
        - cell "Xóa":
          - button "Xóa"
  - text: "Tổng tạm tính: 0 ₫"
  - link "← Mua tiếp":
    - /url: /
  - button "Tiến hành thanh toán"
- contentinfo: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  117 |   return (await res.json()).id as number;
  118 | }
  119 | 
  120 | // ---------------------------------------------------------------------------------
  121 | // Shape A — Cart page UI/UX (32 cases)
  122 | //
  123 | // Assertion patterns demonstrated across this file's switch cases: toBeVisible (most
  124 | // checks), toHaveCount (row/product counting), toContainText (price/subtotal text),
  125 | // toBeDisabled (checkout guard), toHaveText (exact quantity cell value), and plain
  126 | // `expect(x).toBe(y)` on captured dialog state/badge text (not.toBe for change checks).
  127 | // ---------------------------------------------------------------------------------
  128 | test.describe('FR-07 Shopping Cart UI', () => {
  129 |   for (const c of uiCases) {
  130 |     test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
  131 |       testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
  132 |       if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });
  133 | 
  134 |       await loginViaToken(page, request, SEED_USER_CREDENTIALS.email, SEED_USER_CREDENTIALS.password);
  135 | 
  136 |       switch (c.check) {
  137 |         case 'empty-message': {
  138 |           await gotoCart(page);
  139 |           await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
  140 |           break;
  141 |         }
  142 |         case 'empty-icon': {
  143 |           await gotoCart(page);
  144 |           await expect(page.locator('svg, img').first()).toBeVisible();
  145 |           break;
  146 |         }
  147 |         case 'empty-continue-link': {
  148 |           await gotoCart(page);
  149 |           await expect(page.getByRole('link', { name: 'Tiếp tục mua sắm' })).toBeVisible();
  150 |           break;
  151 |         }
  152 |         case 'breadcrumb': {
  153 |           await gotoCart(page);
  154 |           await expect(page.getByRole('navigation').filter({ hasText: /Trang chủ|Home/ })).toBeVisible();
  155 |           break;
  156 |         }
  157 |         case 'table-columns': {
  158 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  159 |           await gotoCart(page);
  160 |           for (const col of ['Sản phẩm', 'Giá', 'Số lượng', 'Thành tiền', 'Thao tác']) {
  161 |             await expect(page.getByRole('columnheader', { name: col })).toBeVisible();
  162 |           }
  163 |           break;
  164 |         }
  165 |         case 'price-format': {
  166 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  167 |           await gotoCart(page);
  168 |           await expect(cartRow(page, PRODUCT_A_NAME)).toContainText(/\d{1,3}(\.\d{3})*\s*₫/);
  169 |           break;
  170 |         }
  171 |         case 'subtotal-single': {
  172 |           await addFromDetailReliable(page, PRODUCT_A_ID, c.quantity);
  173 |           await gotoCart(page);
  174 |           const expected = (PRODUCT_A_PRICE * Number(c.quantity)).toLocaleString('vi-VN');
  175 |           await expect(cartRow(page, PRODUCT_A_NAME)).toContainText(expected);
  176 |           break;
  177 |         }
  178 |         case 'total-label': {
  179 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  180 |           await gotoCart(page);
  181 |           await expect(page.getByText('Tổng cộng', { exact: false })).toBeVisible();
  182 |           break;
  183 |         }
  184 |         case 'add-from-home': {
  185 |           await gotoHome(page);
  186 |           await homeCard(page, PRODUCT_A_ID).getByRole('button', { name: 'Thêm vào giỏ' }).click();
  187 |           await gotoCart(page);
  188 |           await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
  189 |           break;
  190 |         }
  191 |         case 'add-from-detail': {
  192 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  193 |           await gotoCart(page);
  194 |           await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
  195 |           break;
  196 |         }
  197 |         case 'merge-duplicate-id': {
  198 |           await addFromDetailReliable(page, PRODUCT_A_ID, 2);
  199 |           await addFromDetailReliable(page, PRODUCT_A_ID, 3);
  200 |           await gotoCart(page);
  201 |           await expect(page.locator('tr').filter({ hasText: PRODUCT_A_NAME })).toHaveCount(1);
  202 |           await expect(cartRow(page, PRODUCT_A_NAME).locator('td').nth(2)).toHaveText('5');
  203 |           break;
  204 |         }
  205 |         case 'separate-rows-different-id': {
  206 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  207 |           await addFromDetailReliable(page, PRODUCT_B_ID);
  208 |           await gotoCart(page);
  209 |           await expect(page.locator('tbody tr')).toHaveCount(2);
  210 |           break;
  211 |         }
  212 |         case 'add-with-quantity': {
  213 |           await addFromDetailReliable(page, PRODUCT_A_ID, c.quantity);
  214 |           await gotoCart(page);
  215 |           // Spec-conformant expectation: an invalid quantity must not result in an
  216 |           // item silently added to the cart.
> 217 |           await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
      |                                                                       ^ Error: expect(locator).toBeVisible() failed
  218 |           break;
  219 |         }
  220 |         case 'qty-adjust-buttons-missing': {
  221 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  222 |           await gotoCart(page);
  223 |           await expect(cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: /^[+-]$/ })).toBeVisible();
  224 |           break;
  225 |         }
  226 |         case 'total-realtime-multi': {
  227 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  228 |           await addFromDetailReliable(page, PRODUCT_B_ID);
  229 |           await gotoCart(page);
  230 |           const expected = (PRODUCT_A_PRICE + PRODUCT_B_PRICE).toLocaleString('vi-VN');
  231 |           // Scoped to the total footer, not a page-wide text search — the same amount
  232 |           // can legitimately also appear in a unit-price/subtotal cell.
  233 |           await expect(page.locator('div.text-xl.font-bold')).toContainText(expected);
  234 |           break;
  235 |         }
  236 |         case 'total-after-remove': {
  237 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  238 |           await addFromDetailReliable(page, PRODUCT_B_ID);
  239 |           await gotoCart(page);
  240 |           await cartRow(page, PRODUCT_B_NAME).getByRole('button', { name: 'Xóa' }).click();
  241 |           const expected = PRODUCT_A_PRICE.toLocaleString('vi-VN');
  242 |           await expect(page.locator('div.text-xl.font-bold')).toContainText(expected);
  243 |           break;
  244 |         }
  245 |         case 'remove-confirm-dialog-missing': {
  246 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  247 |           await gotoCart(page);
  248 |           let dialogAppeared = false;
  249 |           page.on('dialog', async (d) => {
  250 |             dialogAppeared = true;
  251 |             await d.accept();
  252 |           });
  253 |           await cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' }).click();
  254 |           expect(dialogAppeared).toBe(true);
  255 |           break;
  256 |         }
  257 |         case 'remove-last-item-empty-state': {
  258 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  259 |           await gotoCart(page);
  260 |           await cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' }).click();
  261 |           await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
  262 |           break;
  263 |         }
  264 |         case 'badge-after-add': {
  265 |           await gotoHome(page);
  266 |           const badgeBefore = await page.getByRole('link', { name: /Giỏ hàng/ }).textContent();
  267 |           await homeCard(page, PRODUCT_A_ID).getByRole('button', { name: 'Thêm vào giỏ' }).click();
  268 |           const badgeAfter = await page.getByRole('link', { name: /Giỏ hàng/ }).textContent();
  269 |           expect(badgeAfter).not.toBe(badgeBefore);
  270 |           break;
  271 |         }
  272 |         case 'badge-after-remove': {
  273 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  274 |           await gotoCart(page);
  275 |           await cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' }).click();
  276 |           await expect(page.getByRole('link', { name: /Giỏ hàng/ }).locator('span')).toHaveCount(0);
  277 |           break;
  278 |         }
  279 |         case 'toast-on-add-missing': {
  280 |           await gotoHome(page);
  281 |           await homeCard(page, PRODUCT_A_ID).getByRole('button', { name: 'Thêm vào giỏ' }).click();
  282 |           await expect(page.getByRole('alert')).toBeVisible();
  283 |           break;
  284 |         }
  285 |         case 'remove-repeated-click': {
  286 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  287 |           await gotoCart(page);
  288 |           const removeBtn = cartRow(page, PRODUCT_A_NAME).getByRole('button', { name: 'Xóa' });
  289 |           await removeBtn.click();
  290 |           await expect(page.getByText('Giỏ hàng của bạn đang trống')).toBeVisible();
  291 |           // A second click has nothing left to act on; the page must stay usable.
  292 |           await expect(page.locator('body')).toBeVisible();
  293 |           break;
  294 |         }
  295 |         case 'add-single-click-works': {
  296 |           await gotoProductDetail(page, PRODUCT_A_ID);
  297 |           await page.getByRole('button', { name: /Thêm vào giỏ hàng/ }).click();
  298 |           await expect(page.getByRole('button', { name: 'Đã thêm' })).toBeVisible();
  299 |           break;
  300 |         }
  301 |         case 'stock-info-missing': {
  302 |           await gotoProductDetail(page, PRODUCT_A_ID);
  303 |           await expect(page.getByText(/còn|tồn kho|in stock/i)).toBeVisible();
  304 |           break;
  305 |         }
  306 |         case 'checkout-blocked-when-empty': {
  307 |           // Cart.jsx renders no checkout button at all when empty, so this is the one
  308 |           // legitimate case that must reach /checkout directly instead of via the cart
  309 |           // page's button.
  310 |           await page.goto('/checkout');
  311 |           await expect(page.getByRole('button', { name: /Xác Nhận Thanh Toán/i })).toBeDisabled();
  312 |           break;
  313 |         }
  314 |         case 'reload-persistence': {
  315 |           await addFromDetailReliable(page, PRODUCT_A_ID);
  316 |           await gotoCart(page);
  317 |           await expect(cartRow(page, PRODUCT_A_NAME)).toBeVisible();
```
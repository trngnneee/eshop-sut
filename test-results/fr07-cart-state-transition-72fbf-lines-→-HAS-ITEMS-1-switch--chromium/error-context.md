# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr07-cart-state-transition.spec.js >> FR-07 · Cart — State Transition Testing (ST-001 … ST-INV-03) >> TC-CART-ST-010 · T-08 · confirm delete with other lines → HAS_ITEMS (1-switch)
- Location: tests\e2e\fr07-cart-state-transition.spec.js:121:3

# Error details

```
Error: expect(received).toBe(expected) // Object.is equality

Expected: true
Received: false
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - link "EShop" [ref=e5] [cursor=pointer]:
      - /url: /
    - navigation [ref=e6]:
      - link "Giỏ hàng" [ref=e7] [cursor=pointer]:
        - /url: /cart
      - link "Đăng nhập" [ref=e8] [cursor=pointer]:
        - /url: /login
      - link "Đăng ký" [ref=e9] [cursor=pointer]:
        - /url: /register
  - main [ref=e10]:
    - generic [ref=e11]:
      - heading "Giỏ Hàng" [level=2] [ref=e12]
      - table [ref=e13]:
        - rowgroup [ref=e14]:
          - row "Sản phẩm Giá Số lượng Thành tiền Thao tác" [ref=e15]:
            - columnheader "Sản phẩm" [ref=e16]
            - columnheader "Giá" [ref=e17]
            - columnheader "Số lượng" [ref=e18]
            - columnheader "Thành tiền" [ref=e19]
            - columnheader "Thao tác" [ref=e20]
        - rowgroup [ref=e21]:
          - row "Samsung Galaxy S24 Ultra 28.000.000 ₫ 1 28.000.000 ₫ Xóa" [ref=e22]:
            - cell "Samsung Galaxy S24 Ultra" [ref=e23]
            - cell "28.000.000 ₫" [ref=e24]
            - cell "1" [ref=e25]
            - cell "28.000.000 ₫" [ref=e26]
            - cell "Xóa" [ref=e27]:
              - button "Xóa" [active] [ref=e28] [cursor=pointer]
      - generic [ref=e29]:
        - generic [ref=e30]:
          - text: "Tổng tạm tính:"
          - generic [ref=e31]: 28.000.000 ₫
        - generic [ref=e32]:
          - link "← Mua tiếp" [ref=e33] [cursor=pointer]:
            - /url: /
          - button "Tiến hành thanh toán" [ref=e34] [cursor=pointer]
  - contentinfo [ref=e35]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  32  |     );
  33  |     await expect(cart.getPlusButton().first()).toBeVisible();
  34  |     await expect(cart.getMinusButton().first()).toBeVisible();
  35  |     await expect(cart.getDeleteButton()).toBeVisible();
  36  |   });
  37  | 
  38  |   test('TC-CART-ST-003 · HAS_ITEMS · total label "Tổng cộng"', async ({ page }) => {
  39  |     await seedOneProduct(page, { quantity: 1 });
  40  |     const cart = new CartPage(page);
  41  |     const totalText = await cart.getGrandTotalText();
  42  |     expect(totalText, 'FR-07 requires label "Tổng cộng"').toMatch(/Tổng cộng/);
  43  |     const unitPrice = cart.parseVnd(await page.locator('table tbody tr td').nth(1).textContent());
  44  |     const qty = Number((await cart.getFirstRowQuantity()).trim());
  45  |     const lineTotal = cart.parseVnd(await cart.getFirstRowLineTotal());
  46  |     expect(lineTotal).toBe(unitPrice * qty);
  47  |   });
  48  | 
  49  |   test('TC-CART-ST-004 · T-02 · add_same_product merges quantity', async ({ page }) => {
  50  |     await seedOneProduct(page, { quantity: 1 });
  51  |     await addSameProductAgain(page, 0);
  52  |     const cart = new CartPage(page);
  53  |     await cart.goto();
  54  |     expect(await cart.getRowCount(), 'FR-07: one row after merge').toBe(1);
  55  |     expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(2);
  56  |   });
  57  | 
  58  |   test('TC-CART-ST-005 · T-03 · click_plus increases quantity', async ({ page }) => {
  59  |     await seedOneProduct(page, { quantity: 1 });
  60  |     const cart = new CartPage(page);
  61  |     const qtyBefore = Number((await cart.getFirstRowQuantity()).trim());
  62  |     const plus = cart.getPlusButton();
  63  |     await expect(plus.first(), 'FR-07: + control on cart').toBeVisible();
  64  |     await plus.first().click();
  65  |     await page.waitForTimeout(400);
  66  |     expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(qtyBefore + 1);
  67  |     expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
  68  |   });
  69  | 
  70  |   test('TC-CART-ST-006 · T-04 · click_minus decreases quantity (qty>1)', async ({ page }) => {
  71  |     await seedOneProduct(page, { quantity: 2 });
  72  |     const cart = new CartPage(page);
  73  |     const minus = cart.getMinusButton();
  74  |     await expect(minus.first(), 'FR-07: − control on cart').toBeVisible();
  75  |     const qtyBefore = Number((await cart.getFirstRowQuantity()).trim());
  76  |     await minus.first().click();
  77  |     await page.waitForTimeout(400);
  78  |     expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(qtyBefore - 1);
  79  |     expect(await cart.getRowCount()).toBe(1);
  80  |   });
  81  | 
  82  |   test('TC-CART-ST-007 · T-05 · minus at qty 1 → EMPTY', async ({ page }) => {
  83  |     await seedOneProduct(page, { quantity: 1 });
  84  |     const cart = new CartPage(page);
  85  |     const minus = cart.getMinusButton();
  86  |     await expect(minus.first(), 'FR-07: − control to reach EMPTY').toBeVisible();
  87  |     await minus.first().click();
  88  |     await page.waitForTimeout(400);
  89  |     expect(await cart.isEmpty()).toBe(true);
  90  |     await expect(cart.getEmptyMessage()).toBeVisible();
  91  |   });
  92  | 
  93  |   test('TC-CART-ST-008 · T-06 · delete opens confirmation dialog', async ({ page }) => {
  94  |     await seedOneProduct(page);
  95  |     const cart = new CartPage(page);
  96  |     let dialogSeen = false;
  97  |     page.once('dialog', () => {
  98  |       dialogSeen = true;
  99  |     });
  100 |     const rowsBefore = await cart.getRowCount();
  101 |     await cart.getDeleteButton().click();
  102 |     await page.waitForTimeout(500);
  103 |     expect(dialogSeen, 'T-06: HAS_ITEMS → DELETE_CONFIRM').toBe(true);
  104 |     expect(await cart.getRowCount()).toBe(rowsBefore);
  105 |   });
  106 | 
  107 |   test('TC-CART-ST-009 · T-07 · confirm delete last item → EMPTY (1-switch)', async ({ page }) => {
  108 |     await seedOneProduct(page);
  109 |     const cart = new CartPage(page);
  110 |     let dialogSeen = false;
  111 |     page.once('dialog', async (dialog) => {
  112 |       dialogSeen = true;
  113 |       await dialog.accept();
  114 |     });
  115 |     await cart.getDeleteButton().click();
  116 |     await page.waitForTimeout(600);
  117 |     expect(dialogSeen).toBe(true);
  118 |     expect(await cart.isEmpty()).toBe(true);
  119 |   });
  120 | 
  121 |   test('TC-CART-ST-010 · T-08 · confirm delete with other lines → HAS_ITEMS (1-switch)', async ({ page }) => {
  122 |     await seedTwoProducts(page);
  123 |     const cart = new CartPage(page);
  124 |     const nameB = (await page.locator('table tbody tr').nth(1).locator('td').first().textContent())?.trim();
  125 |     let dialogSeen = false;
  126 |     page.once('dialog', async (dialog) => {
  127 |       dialogSeen = true;
  128 |       await dialog.accept();
  129 |     });
  130 |     await page.locator('table tbody button:has-text("Xóa")').first().click();
  131 |     await page.waitForTimeout(600);
> 132 |     expect(dialogSeen).toBe(true);
      |                        ^ Error: expect(received).toBe(expected) // Object.is equality
  133 |     expect(await cart.getRowCount()).toBe(1);
  134 |     await expect(page.locator('table tbody tr td').first()).toHaveText(nameB ?? '');
  135 |   });
  136 | 
  137 |   test('TC-CART-ST-011 · T-09 · cancel delete → HAS_ITEMS unchanged (1-switch)', async ({ page }) => {
  138 |     await seedOneProduct(page);
  139 |     const cart = new CartPage(page);
  140 |     const qtyBefore = (await cart.getFirstRowQuantity()).trim();
  141 |     let dialogSeen = false;
  142 |     page.once('dialog', async (dialog) => {
  143 |       dialogSeen = true;
  144 |       await dialog.dismiss();
  145 |     });
  146 |     await cart.getDeleteButton().click();
  147 |     await page.waitForTimeout(600);
  148 |     expect(dialogSeen).toBe(true);
  149 |     expect(await cart.getRowCount()).toBe(1);
  150 |     expect((await cart.getFirstRowQuantity()).trim()).toBe(qtyBefore);
  151 |   });
  152 | 
  153 |   test('TC-CART-ST-012 · T-10 · continue shopping preserves cart', async ({ page }) => {
  154 |     await seedOneProduct(page);
  155 |     const cart = new CartPage(page);
  156 |     const productName = (await page.locator('table tbody tr td').first().textContent())?.trim();
  157 |     await cart.clickContinueShopping();
  158 |     expect(page.url()).toMatch(/\/($|\?)/);
  159 |     await cart.goto();
  160 |     expect(await cart.getRowCount()).toBe(1);
  161 |     await expect(page.locator('table tbody tr td').first()).toHaveText(productName ?? '');
  162 |   });
  163 | 
  164 |   test('TC-CART-ST-E2E-01 · 3-switch E2E · add, +, delete confirm, EMPTY', async ({ page }) => {
  165 |     await seedOneProduct(page, { quantity: 1 });
  166 |     const cart = new CartPage(page);
  167 |     expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
  168 |     const plus = cart.getPlusButton();
  169 |     await expect(plus.first()).toBeVisible();
  170 |     await plus.first().click();
  171 |     await page.waitForTimeout(400);
  172 |     let dialogSeen = false;
  173 |     page.once('dialog', async (dialog) => {
  174 |       dialogSeen = true;
  175 |       await dialog.accept();
  176 |     });
  177 |     await cart.getDeleteButton().click();
  178 |     await page.waitForTimeout(600);
  179 |     expect(dialogSeen).toBe(true);
  180 |     expect(await cart.isEmpty()).toBe(true);
  181 |   });
  182 | 
  183 |   test('TC-CART-ST-E2E-02 · 2-switch E2E · merge, continue shopping, persist', async ({ page }) => {
  184 |     await seedOneProduct(page, { quantity: 1 });
  185 |     await addSameProductAgain(page, 0);
  186 |     const cart = new CartPage(page);
  187 |     await cart.goto();
  188 |     expect(await cart.getRowCount()).toBe(1);
  189 |     expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(2);
  190 |     await cart.clickContinueShopping();
  191 |     await cart.goto();
  192 |     expect(await cart.getRowCount()).toBe(1);
  193 |     expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(2);
  194 |     expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
  195 |   });
  196 | 
  197 |   test('TC-CART-ST-INV-01 · T-INV-01 · cannot delete from EMPTY', async ({ page }) => {
  198 |     const cart = new CartPage(page);
  199 |     await cart.goto();
  200 |     expect(await cart.isEmpty()).toBe(true);
  201 |     await expect(cart.getDeleteButton()).toHaveCount(0);
  202 |   });
  203 | 
  204 |   test('TC-CART-ST-INV-02 · T-INV-02 · no +/- on EMPTY', async ({ page }) => {
  205 |     const cart = new CartPage(page);
  206 |     await cart.goto();
  207 |     await expect(cart.getPlusButton()).toHaveCount(0);
  208 |     await expect(cart.getMinusButton()).toHaveCount(0);
  209 |   });
  210 | 
  211 |   test('TC-CART-ST-INV-03 · T-INV-03 · delete requires dialog before removal', async ({ page }) => {
  212 |     await seedOneProduct(page);
  213 |     const cart = new CartPage(page);
  214 |     const { dialogAppeared, rowCountBefore, rowCountAfter } = await cart.clickDeleteAndCaptureDialog();
  215 |     expect(dialogAppeared, 'T-INV-03: must enter DELETE_CONFIRM').toBe(true);
  216 |     expect(rowCountAfter).toBe(rowCountBefore);
  217 |   });
  218 | });
  219 | 
```
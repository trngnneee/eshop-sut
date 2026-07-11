// FR-07: Giỏ hàng — State Transition automation
// Design: SoftwareTesting-HW/Assigment/State Transition/Test Case/FR-07-state-transition-test-cases.md

const { test, expect } = require('@playwright/test');
const { CartPage } = require('../pages/CartPage');
const {
  seedOneProduct,
  seedTwoProducts,
  addSameProductAgain,
} = require('../helpers/cart');

test.describe('FR-07 · Cart — State Transition Testing (ST-001 … ST-INV-03)', () => {
  test('TC-CART-ST-001 · EMPTY · illustration and message', async ({ page }) => {
    const cart = new CartPage(page);
    await cart.goto();
    expect(await cart.isEmpty()).toBe(true);
    await expect(cart.getEmptyMessage()).toBeVisible();
    const hasIllustration =
      (await page.locator('img').count()) > 0 || (await cart.emptyIllustrationLocator().count()) > 0;
    expect(hasIllustration, 'FR-07: empty cart must show illustration').toBe(true);
    expect(await cart.getRowCount()).toBe(0);
    await expect(cart.getPlusButton()).toHaveCount(0);
  });

  test('TC-CART-ST-002 · T-01 · EMPTY → HAS_ITEMS', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    expect(await cart.isEmpty()).toBe(false);
    const headers = await cart.getHeaderTexts();
    expect(headers).toEqual(
      expect.arrayContaining(['Sản phẩm', 'Số lượng', 'Thành tiền', 'Thao tác']),
    );
    await expect(cart.getPlusButton().first()).toBeVisible();
    await expect(cart.getMinusButton().first()).toBeVisible();
    await expect(cart.getDeleteButton()).toBeVisible();
  });

  test('TC-CART-ST-003 · HAS_ITEMS · total label "Tổng cộng"', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    const cart = new CartPage(page);
    const totalText = await cart.getGrandTotalText();
    expect(totalText, 'FR-07 requires label "Tổng cộng"').toMatch(/Tổng cộng/);
    const unitPrice = cart.parseVnd(await page.locator('table tbody tr td').nth(1).textContent());
    const qty = Number((await cart.getFirstRowQuantity()).trim());
    const lineTotal = cart.parseVnd(await cart.getFirstRowLineTotal());
    expect(lineTotal).toBe(unitPrice * qty);
  });

  test('TC-CART-ST-004 · T-02 · add_same_product merges quantity', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    await addSameProductAgain(page, 0);
    const cart = new CartPage(page);
    await cart.goto();
    expect(await cart.getRowCount(), 'FR-07: one row after merge').toBe(1);
    expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(2);
  });

  test('TC-CART-ST-005 · T-03 · click_plus increases quantity', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    const cart = new CartPage(page);
    const qtyBefore = Number((await cart.getFirstRowQuantity()).trim());
    const plus = cart.getPlusButton();
    await expect(plus.first(), 'FR-07: + control on cart').toBeVisible();
    await plus.first().click();
    await page.waitForTimeout(400);
    expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(qtyBefore + 1);
    expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
  });

  test('TC-CART-ST-006 · T-04 · click_minus decreases quantity (qty>1)', async ({ page }) => {
    await seedOneProduct(page, { quantity: 2 });
    const cart = new CartPage(page);
    const minus = cart.getMinusButton();
    await expect(minus.first(), 'FR-07: − control on cart').toBeVisible();
    const qtyBefore = Number((await cart.getFirstRowQuantity()).trim());
    await minus.first().click();
    await page.waitForTimeout(400);
    expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(qtyBefore - 1);
    expect(await cart.getRowCount()).toBe(1);
  });

  test('TC-CART-ST-007 · T-05 · minus at qty 1 → EMPTY', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    const cart = new CartPage(page);
    const minus = cart.getMinusButton();
    await expect(minus.first(), 'FR-07: − control to reach EMPTY').toBeVisible();
    await minus.first().click();
    await page.waitForTimeout(400);
    expect(await cart.isEmpty()).toBe(true);
    await expect(cart.getEmptyMessage()).toBeVisible();
  });

  test('TC-CART-ST-008 · T-06 · delete opens confirmation dialog', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    let dialogSeen = false;
    page.once('dialog', () => {
      dialogSeen = true;
    });
    const rowsBefore = await cart.getRowCount();
    await cart.getDeleteButton().click();
    await page.waitForTimeout(500);
    expect(dialogSeen, 'T-06: HAS_ITEMS → DELETE_CONFIRM').toBe(true);
    expect(await cart.getRowCount()).toBe(rowsBefore);
  });

  test('TC-CART-ST-009 · T-07 · confirm delete last item → EMPTY (1-switch)', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    let dialogSeen = false;
    page.once('dialog', async (dialog) => {
      dialogSeen = true;
      await dialog.accept();
    });
    await cart.getDeleteButton().click();
    await page.waitForTimeout(600);
    expect(dialogSeen).toBe(true);
    expect(await cart.isEmpty()).toBe(true);
  });

  test('TC-CART-ST-010 · T-08 · confirm delete with other lines → HAS_ITEMS (1-switch)', async ({ page }) => {
    await seedTwoProducts(page);
    const cart = new CartPage(page);
    const nameB = (await page.locator('table tbody tr').nth(1).locator('td').first().textContent())?.trim();
    let dialogSeen = false;
    page.once('dialog', async (dialog) => {
      dialogSeen = true;
      await dialog.accept();
    });
    await page.locator('table tbody button:has-text("Xóa")').first().click();
    await page.waitForTimeout(600);
    expect(dialogSeen).toBe(true);
    expect(await cart.getRowCount()).toBe(1);
    await expect(page.locator('table tbody tr td').first()).toHaveText(nameB ?? '');
  });

  test('TC-CART-ST-011 · T-09 · cancel delete → HAS_ITEMS unchanged (1-switch)', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    const qtyBefore = (await cart.getFirstRowQuantity()).trim();
    let dialogSeen = false;
    page.once('dialog', async (dialog) => {
      dialogSeen = true;
      await dialog.dismiss();
    });
    await cart.getDeleteButton().click();
    await page.waitForTimeout(600);
    expect(dialogSeen).toBe(true);
    expect(await cart.getRowCount()).toBe(1);
    expect((await cart.getFirstRowQuantity()).trim()).toBe(qtyBefore);
  });

  test('TC-CART-ST-012 · T-10 · continue shopping preserves cart', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    const productName = (await page.locator('table tbody tr td').first().textContent())?.trim();
    await cart.clickContinueShopping();
    expect(page.url()).toMatch(/\/($|\?)/);
    await cart.goto();
    expect(await cart.getRowCount()).toBe(1);
    await expect(page.locator('table tbody tr td').first()).toHaveText(productName ?? '');
  });

  test('TC-CART-ST-E2E-01 · 3-switch E2E · add, +, delete confirm, EMPTY', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    const cart = new CartPage(page);
    expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
    const plus = cart.getPlusButton();
    await expect(plus.first()).toBeVisible();
    await plus.first().click();
    await page.waitForTimeout(400);
    let dialogSeen = false;
    page.once('dialog', async (dialog) => {
      dialogSeen = true;
      await dialog.accept();
    });
    await cart.getDeleteButton().click();
    await page.waitForTimeout(600);
    expect(dialogSeen).toBe(true);
    expect(await cart.isEmpty()).toBe(true);
  });

  test('TC-CART-ST-E2E-02 · 2-switch E2E · merge, continue shopping, persist', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    await addSameProductAgain(page, 0);
    const cart = new CartPage(page);
    await cart.goto();
    expect(await cart.getRowCount()).toBe(1);
    expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(2);
    await cart.clickContinueShopping();
    await cart.goto();
    expect(await cart.getRowCount()).toBe(1);
    expect(Number((await cart.getFirstRowQuantity()).trim())).toBe(2);
    expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
  });

  test('TC-CART-ST-INV-01 · T-INV-01 · cannot delete from EMPTY', async ({ page }) => {
    const cart = new CartPage(page);
    await cart.goto();
    expect(await cart.isEmpty()).toBe(true);
    await expect(cart.getDeleteButton()).toHaveCount(0);
  });

  test('TC-CART-ST-INV-02 · T-INV-02 · no +/- on EMPTY', async ({ page }) => {
    const cart = new CartPage(page);
    await cart.goto();
    await expect(cart.getPlusButton()).toHaveCount(0);
    await expect(cart.getMinusButton()).toHaveCount(0);
  });

  test('TC-CART-ST-INV-03 · T-INV-03 · delete requires dialog before removal', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    const { dialogAppeared, rowCountBefore, rowCountAfter } = await cart.clickDeleteAndCaptureDialog();
    expect(dialogAppeared, 'T-INV-03: must enter DELETE_CONFIRM').toBe(true);
    expect(rowCountAfter).toBe(rowCountBefore);
  });
});

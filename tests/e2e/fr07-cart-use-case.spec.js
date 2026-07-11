// FR-07: Giỏ hàng — Use-Case automation
// Design: SoftwareTesting-HW/Assigment/Use Case/Test Case/FR-07-use-case-test-cases.md

const { test, expect } = require('@playwright/test');
const { CartPage } = require('../pages/CartPage');
const {
  addToCartViaUI,
  fetchProducts,
  goToCart,
  seedOneProduct,
  addSameProductAgain,
} = require('../helpers/cart');

test.describe('FR-07 · Cart — Use-Case Testing (UC-001 … UC-EF-03)', () => {
  test('TC-CART-UC-001 · MF · View cart, increase quantity, totals update', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    const cart = new CartPage(page);
    await cart.goto();

    const headers = await cart.getHeaderTexts();
    expect(headers).toEqual(
      expect.arrayContaining(['Sản phẩm', 'Số lượng', 'Thành tiền', 'Thao tác']),
    );
    expect(headers.some((h) => /Giá|Đơn giá/i.test(h)), 'Price column header (Đơn giá)').toBe(true);

    const totalText = await cart.getGrandTotalText();
    expect(totalText, 'Grand total label must be "Tổng cộng" (FR-07)').toMatch(/Tổng cộng/);

    const qtyBefore = Number((await cart.getFirstRowQuantity()).trim());
    const lineBefore = cart.parseVnd(await cart.getFirstRowLineTotal());
    const grandBefore = cart.parseVnd(totalText);

    const plus = cart.getPlusButton();
    await expect(plus.first(), 'FR-07 requires +/- quantity controls on cart page').toBeVisible();
    await plus.first().click();
    await page.waitForTimeout(400);

    const qtyAfter = Number((await cart.getFirstRowQuantity()).trim());
    const lineAfter = cart.parseVnd(await cart.getFirstRowLineTotal());
    const grandAfter = cart.parseVnd(await cart.getGrandTotalText());

    expect(qtyAfter).toBe(qtyBefore + 1);
    expect(lineAfter).toBe(Math.round(lineBefore * (qtyAfter / qtyBefore)));
    expect(grandAfter).toBeGreaterThanOrEqual(grandBefore);
  });

  test('TC-CART-UC-002 · AF-01 · Empty cart illustration and message', async ({ page }) => {
    const cart = new CartPage(page);
    await cart.goto();
    expect(await cart.isEmpty()).toBe(true);

    await expect(cart.getEmptyMessage()).toBeVisible();

    const imgCount = await page.locator('img').count();
    const svgCount = await cart.emptyIllustrationLocator().count();
    const hasIllustration = imgCount > 0 || svgCount > 0;
    expect(hasIllustration, 'FR-07: empty cart must show illustration').toBe(true);

    expect(await cart.getRowCount()).toBe(0);
    await expect(cart.getPlusButton()).toHaveCount(0);
  });

  test('TC-CART-UC-003 · AF-02 · Continue shopping preserves cart', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1 });
    const cart = new CartPage(page);
    await cart.goto();

    const productName = await page.locator('table tbody tr td').first().textContent();
    await cart.clickContinueShopping();
    expect(page.url()).toMatch(/\/($|\?)/);

    await cart.goto();
    expect(await cart.getRowCount()).toBe(1);
    await expect(page.locator('table tbody tr td').first()).toHaveText(productName?.trim() ?? '');
    const totalText = await cart.getGrandTotalText();
    expect(totalText).toMatch(/Tổng cộng/);
  });

  test('TC-CART-UC-004 · AF-03 · Delete product after confirmation', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    await cart.goto();

    let dialogSeen = false;
    page.once('dialog', async (dialog) => {
      dialogSeen = true;
      await dialog.accept();
    });

    const rowsBefore = await cart.getRowCount();
    await cart.getDeleteButton().click();
    await page.waitForTimeout(600);

    expect(dialogSeen, 'FR-07: delete must show confirmation dialog before removal').toBe(true);
    const rowsAfter = await cart.getRowCount();
    expect(rowsAfter).toBeLessThan(rowsBefore);
  });

  test('TC-CART-UC-005 · AF-04 · Cancel delete dialog', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    await cart.goto();

    const qtyBefore = (await cart.getFirstRowQuantity()).trim();
    let dialogSeen = false;
    page.once('dialog', async (dialog) => {
      dialogSeen = true;
      await dialog.dismiss();
    });

    await cart.getDeleteButton().click();
    await page.waitForTimeout(600);

    expect(dialogSeen, 'Delete confirmation dialog must appear').toBe(true);
    expect(await cart.getRowCount()).toBe(1);
    expect((await cart.getFirstRowQuantity()).trim()).toBe(qtyBefore);
  });

  test('TC-CART-UC-006 · AF-05 · Decrease quantity', async ({ page }) => {
    await seedOneProduct(page, { quantity: 2 });
    const cart = new CartPage(page);
    await cart.goto();

    const minus = cart.getMinusButton();
    await expect(minus.first(), 'FR-07 requires minus (−) control on cart').toBeVisible();

    const qtyBefore = Number((await cart.getFirstRowQuantity()).trim());
    expect(qtyBefore).toBeGreaterThanOrEqual(2);

    await minus.first().click();
    await page.waitForTimeout(400);

    const qtyAfter = Number((await cart.getFirstRowQuantity()).trim());
    expect(qtyAfter).toBe(qtyBefore - 1);
    expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
  });

  test('TC-CART-UC-007 · AF-06 · Add same product merges quantity', async ({ page }) => {
    await seedOneProduct(page, { quantity: 1, addTimes: 1 });
    await addSameProductAgain(page, 0);

    const cart = new CartPage(page);
    await cart.goto();

    const rowCount = await cart.getRowCount();
    expect(rowCount, 'FR-07: same product must merge — exactly one row').toBe(1);

    const qty = Number((await cart.getFirstRowQuantity()).trim());
    expect(qty).toBe(2);
    expect(await cart.getGrandTotalText()).toMatch(/Tổng cộng/);
  });

  test('TC-CART-UC-EF-01 · EF-01 · Empty cart has illustration and message', async ({ page }) => {
    const cart = new CartPage(page);
    await cart.goto();

    await expect(cart.getEmptyMessage()).toBeVisible();
    const hasImg = (await page.locator('img').count()) > 0;
    expect(hasImg, 'Empty cart missing illustration image (FR-07)').toBe(true);
  });

  test('TC-CART-UC-EF-02 · EF-02 · Total label is "Tổng cộng"', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    await cart.goto();

    const totalText = await cart.getGrandTotalText();
    expect(totalText).toMatch(/Tổng cộng/);
    expect(totalText).not.toMatch(/Tổng tạm tính/);
  });

  test('TC-CART-UC-EF-03 · EF-03 · Delete must not proceed without dialog', async ({ page }) => {
    await seedOneProduct(page);
    const cart = new CartPage(page);
    await cart.goto();

    const { dialogAppeared, rowCountBefore, rowCountAfter } = await cart.clickDeleteAndCaptureDialog();

    expect(dialogAppeared, 'Confirmation dialog required before delete (FR-07)').toBe(true);
    expect(rowCountAfter, 'Item must not be removed before confirm').toBe(rowCountBefore);
  });
});

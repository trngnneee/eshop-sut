// tests/pages/CartPage.js — FR-07 Shopping Cart (web)

class CartPage {
  constructor(page) {
    this.page = page;
  }

  async goto() {
    const cartLink = this.page.locator('a[href="/cart"]');
    if ((await cartLink.count()) > 0) {
      await cartLink.first().click();
      await this.page.waitForURL('**/cart', { timeout: 10_000 });
    } else {
      await this.page.goto('/cart');
    }
    await this.page.waitForLoadState('networkidle');
  }

  async isEmpty() {
    const body = await this.page.textContent('body');
    return /đang trống|trống/i.test(body ?? '');
  }

  getTable() {
    return this.page.locator('table');
  }

  async getHeaderTexts() {
    const headers = this.page.locator('table thead th');
    return headers.allTextContents();
  }

  async getRowCount() {
    return this.page.locator('table tbody tr').count();
  }

  async getFirstRowQuantity() {
    return this.page.locator('table tbody tr').first().locator('td').nth(2).textContent();
  }

  async getFirstRowLineTotal() {
    return this.page.locator('table tbody tr').first().locator('td').nth(3).textContent();
  }

  async getGrandTotalText() {
    const totalBlock = this.page.locator('div.text-xl.font-bold, .text-xl.font-bold').first();
    return totalBlock.textContent();
  }

  hasTotalLabel(text) {
    return this.page.getByText(text, { exact: false });
  }

  getPlusButton() {
    return this.page.locator('button:has-text("+"), button[aria-label*="tăng"], button[aria-label*="plus"]');
  }

  getMinusButton() {
    return this.page.locator('button:has-text("−"), button:has-text("-"), button[aria-label*="giảm"]');
  }

  getDeleteButton() {
    return this.page.locator('table tbody button:has-text("Xóa")').first();
  }

  getContinueShoppingLink() {
    return this.page.locator(
      'a:has-text("Tiếp tục mua sắm"), a:has-text("Mua tiếp"), link:has-text("Tiếp tục mua sắm")',
    );
  }

  async clickContinueShopping() {
    const link = this.page.locator('a[href="/"]').filter({ hasText: /Tiếp tục mua sắm|Mua tiếp/i });
    await link.first().click();
    await this.page.waitForLoadState('networkidle');
  }

  async clickDeleteAndCaptureDialog() {
    let dialogAppeared = false;
    const handler = () => {
      dialogAppeared = true;
    };
    this.page.once('dialog', handler);
    const rowCountBefore = await this.getRowCount();
    await this.getDeleteButton().click();
    await this.page.waitForTimeout(500);
    return { dialogAppeared, rowCountBefore, rowCountAfter: await this.getRowCount() };
  }

  emptyIllustrationLocator() {
    return this.page.locator('img[alt*="empty"], img[alt*="trống"], img[src*="empty"], svg');
  }

  getEmptyMessage() {
    return this.page.getByText(/đang trống|giỏ hàng.*trống/i);
  }

  parseVnd(text) {
    return Number(String(text).replace(/[^\d]/g, '')) || 0;
  }
}

module.exports = { CartPage };

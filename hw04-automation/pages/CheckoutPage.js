/** @typedef {import('@playwright/test').Page} Page */
/** @typedef {import('@playwright/test').Locator} Locator */

class CheckoutPage {
  /** @param {Page} page */
  constructor(page) {
    this.page = page;
  }

  /** Full document load — clears in-memory cart. Use only before seeding. */
  async gotoHard() {
    await this.page.goto('/checkout');
  }

  /** SPA navigation — preserves CartContext state. */
  async gotoSpaFromCart(cartPage) {
    await cartPage.gotoSpa();
    await cartPage.checkoutButton().click();
    await this.page.waitForURL(/\/checkout/);
  }

  heading() {
    return this.page.getByRole('heading', { name: /Xác Nhận Đơn Hàng/i });
  }

  productList() {
    return this.page.locator('ul.list-disc');
  }

  productLines() {
    return this.productList().locator('li');
  }

  totalLabel() {
    return this.page.getByText(/Tổng tiền thanh toán/i);
  }

  totalInput() {
    return this.page.locator('input[type="number"]').first();
  }

  payableTotal() {
    return this.page.getByText(/Tổng thanh toán:/i);
  }

  confirmButton() {
    return this.page.getByRole('button', { name: /Xác Nhận Thanh Toán/i });
  }

  successHeading() {
    return this.page.getByRole('heading', { name: /Thanh toán thành công/i });
  }

  /**
   * @param {string} target
   * @returns {Locator}
   */
  target(target) {
    switch (target) {
      case 'heading':
        return this.heading();
      case 'productList':
        return this.productList();
      case 'productLines':
        return this.productLines();
      case 'totalLabel':
        return this.totalLabel();
      case 'totalInput':
        return this.totalInput();
      case 'payableTotal':
        return this.payableTotal();
      case 'confirmButton':
        return this.confirmButton();
      case 'successHeading':
        return this.successHeading();
      default:
        throw new Error(`Unknown checkout target "${target}"`);
    }
  }

  async confirmPayment() {
    await this.confirmButton().click({ noWaitAfter: true });
  }

  /** @param {number} value */
  async setTotal(value) {
    await this.totalInput().fill(String(value));
  }

  async readDisplayedTotal() {
    if ((await this.totalInput().count()) > 0) {
      return Number(await this.totalInput().inputValue());
    }
    const text = await this.payableTotal().innerText();
    const digits = text.replace(/[^\d]/g, '');
    return Number(digits);
  }
}

class CartPage {
  /** @param {Page} page */
  constructor(page) {
    this.page = page;
  }

  /** Full document load — clears in-memory cart. */
  async gotoHard() {
    await this.page.goto('/cart');
  }

  /** SPA navigation via header link — keeps cart. */
  async gotoSpa() {
    await this.page.getByRole('link', { name: /Giỏ hàng/i }).click();
    await this.page.waitForURL(/\/cart/);
  }

  emptyMessage() {
    return this.page.getByText(/Giỏ hàng của bạn đang trống/i);
  }

  rows() {
    return this.page.locator('table tbody tr');
  }

  checkoutButton() {
    return this.page.getByRole('button', { name: /Tiến hành thanh toán/i });
  }

  async clickCheckout() {
    await this.checkoutButton().click({ noWaitAfter: true });
  }

  /** @param {number} min */
  async waitForItemRows(min = 1) {
    await this.gotoSpa();
    await this.rows().nth(min - 1).waitFor({ state: 'visible', timeout: 10_000 });
  }
}

class HomePage {
  /** @param {Page} page */
  constructor(page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/');
  }

  addToCartButtons() {
    return this.page.getByRole('button', { name: 'Thêm vào giỏ' });
  }

  /** @param {number} count */
  async addFirstNProducts(count) {
    await this.goto();
    const buttons = this.addToCartButtons();
    await buttons.first().waitFor({ state: 'visible', timeout: 15_000 });
    const available = await buttons.count();
    const n = Math.min(count, available);
    if (n < 1) {
      throw new Error('No Thêm vào giỏ buttons found on home');
    }
    for (let i = 0; i < n; i += 1) {
      // Re-query each time — home re-renders after each add.
      await this.addToCartButtons().nth(i).click();
      await this.page.waitForTimeout(150);
    }
    return n;
  }
}

class LoginPage {
  /** @param {Page} page */
  constructor(page) {
    this.page = page;
  }

  async goto() {
    await this.page.goto('/login');
  }

  /**
   * @param {{ email: string, password: string }} credentials
   */
  async login(credentials) {
    await this.goto();
    await this.page.locator('form input').nth(0).fill(credentials.email);
    await this.page.locator('form input').nth(1).fill(credentials.password);
    await this.page.getByRole('button', { name: /Sign In|Đăng nhập/i }).click();
    await this.page.waitForURL(/\/($|\?)/, { timeout: 15_000 });
  }
}

module.exports = { CheckoutPage, CartPage, HomePage, LoginPage };

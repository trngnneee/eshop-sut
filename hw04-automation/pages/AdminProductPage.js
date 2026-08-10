/** @typedef {import('@playwright/test').Page} Page */
/** @typedef {import('@playwright/test').Locator} Locator */

const ADMIN_BASE_URL =
  process.env.ADMIN_BASE_URL ||
  process.env.BASE_URL_ADMIN ||
  'http://localhost:5174';

class AdminProductPage {
  /** @param {Page} page */
  constructor(page) {
    this.page = page;
    this.baseURL = ADMIN_BASE_URL;
  }

  async goto() {
    await this.page.goto(this.baseURL + '/');
  }

  loginHeading() {
    return this.page.getByRole('heading', { name: /Admin Login/i });
  }

  emailInput() {
    return this.page.getByPlaceholder('Email');
  }

  passwordInput() {
    return this.page.getByPlaceholder('Password');
  }

  loginButton() {
    return this.page.getByRole('button', { name: /^Login$/i });
  }

  navProducts() {
    return this.page.getByText('Sản phẩm', { exact: true });
  }

  logout() {
    return this.page.getByText('Đăng xuất', { exact: true });
  }

  productsHeading() {
    return this.page.getByRole('heading', { name: /Quản lý Sản phẩm/i });
  }

  nameInput() {
    return this.page.getByPlaceholder('Tên sản phẩm');
  }

  priceInput() {
    return this.page.getByPlaceholder('Giá tiền');
  }

  imageUrlInput() {
    return this.page.getByPlaceholder('URL Ảnh');
  }

  descriptionInput() {
    return this.page.getByPlaceholder('Mô tả');
  }

  categorySelect() {
    return this.page.locator('form').filter({ has: this.nameInput() }).locator('select');
  }

  saveButton() {
    return this.page.getByRole('button', { name: /Lưu sản phẩm/i });
  }

  cancelEditButton() {
    return this.page.getByRole('button', { name: /Hủy sửa/i });
  }

  /**
   * @param {string} productName
   */
  productRow(productName) {
    return this.page.getByRole('row').filter({ hasText: productName });
  }

  /**
   * @param {string} productName
   */
  priceCell(productName) {
    return this.productRow(productName).locator('td').nth(2);
  }

  /**
   * @param {string} productName
   */
  editButton(productName) {
    return this.productRow(productName).getByRole('button', { name: /^Sửa$/ });
  }

  /**
   * @param {string} productName
   */
  deleteButton(productName) {
    return this.productRow(productName).getByRole('button', { name: /^Xóa$/ });
  }

  /**
   * @param {string} token
   */
  async injectAdminToken(token) {
    await this.goto();
    await this.page.evaluate((t) => {
      localStorage.setItem('adminToken', t);
    }, token);
    await this.page.reload();
    await this.navProducts().waitFor({ state: 'visible', timeout: 15_000 });
  }

  /**
   * @param {{ email: string, password: string }} creds
   */
  async loginWithForm(creds) {
    await this.goto();
    await this.emailInput().fill(creds.email);
    await this.passwordInput().fill(creds.password);
    const dialogPromise = this.page
      .waitForEvent('dialog', { timeout: 5_000 })
      .then(async (d) => {
        await d.accept();
        return d.message();
      })
      .catch(() => null);
    await this.loginButton().click();
    await dialogPromise;
    await this.navProducts().waitFor({ state: 'visible', timeout: 15_000 });
  }

  async openProducts() {
    await this.navProducts().click();
    await this.productsHeading().waitFor({ state: 'visible', timeout: 10_000 });
  }

  /**
   * @param {{ name: string, price: number|string, description?: string, imageUrl?: string, categoryId?: number|string }} data
   */
  async fillProductForm(data) {
    await this.nameInput().fill(String(data.name ?? ''));
    await this.priceInput().fill(String(data.price ?? ''));
    if (data.imageUrl !== undefined) {
      await this.imageUrlInput().fill(String(data.imageUrl));
    }
    if (data.description !== undefined) {
      await this.descriptionInput().fill(String(data.description));
    }
    if (data.categoryId !== undefined && data.categoryId !== null) {
      await this.categorySelect().selectOption(String(data.categoryId));
    }
  }

  /**
   * Click save and accept any alert; optionally capture POST/PUT status.
   * @returns {Promise<number|undefined>}
   */
  async saveProduct() {
    const responsePromise = this.page
      .waitForResponse(
        (res) =>
          /\/api\/products(\/\d+)?$/.test(res.url()) &&
          ['POST', 'PUT'].includes(res.request().method()),
        { timeout: 15_000 },
      )
      .catch(() => null);

    const dialogPromise = this.page
      .waitForEvent('dialog', { timeout: 10_000 })
      .then(async (dialog) => {
        await dialog.accept();
        return dialog.message();
      })
      .catch(() => null);

    await this.saveButton().click();
    const [response] = await Promise.all([responsePromise, dialogPromise]);
    return response ? response.status() : undefined;
  }

  /**
   * @param {string} productName
   */
  async startEdit(productName) {
    await this.editButton(productName).click();
    await this.cancelEditButton().waitFor({ state: 'visible', timeout: 5_000 });
  }

  /**
   * @param {string} productName
   */
  async deleteProduct(productName) {
    const responsePromise = this.page
      .waitForResponse(
        (res) =>
          /\/api\/products\/\d+$/.test(res.url()) &&
          res.request().method() === 'DELETE',
        { timeout: 15_000 },
      )
      .catch(() => null);
    const dialogPromise = this.page
      .waitForEvent('dialog', { timeout: 5_000 })
      .then(async (d) => {
        await d.accept();
        return d.message();
      })
      .catch(() => null);
    await this.deleteButton(productName).click();
    await Promise.all([responsePromise, dialogPromise]);
  }

  /**
   * Resolve JSON logical targets.
   * @param {string} target
   * @param {{ productName?: string, siblingName?: string }} ctx
   */
  target(target, ctx = {}) {
    switch (target) {
      case 'productRow':
        return this.productRow(ctx.productName || '');
      case 'priceCell':
        return this.priceCell(ctx.productName || '');
      case 'siblingRow':
        return this.productRow(ctx.siblingName || '');
      case 'productsHeading':
        return this.productsHeading();
      default:
        throw new Error(`Unknown AdminProductPage target: ${target}`);
    }
  }
}

module.exports = {
  AdminProductPage,
  ADMIN_BASE_URL,
};

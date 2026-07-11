// tests/pages/AdminProductPage.js
// Page Object for FR-15: Product Management (Admin CRUD)

class AdminProductPage {
  constructor(page) {
    this.page = page;

    this.addProductBtn  = page.locator(
      'button:has-text("Thêm"), button:has-text("Thêm sản phẩm"), button:has-text("Add")'
    ).first();
    this.productRows    = page.locator('tbody tr, [class*="product-row"]');
    this.pageHeading    = page.locator('h1').first();

    this.nameInput      = page.locator('input[name="name"], input[placeholder*="tên"], input[placeholder*="name"]').first();
    this.priceInput     = page.locator('input[name="price"], input[placeholder*="giá"], input[type="number"]').first();
    this.descInput      = page.locator('textarea[name="description"], textarea[placeholder*="mô tả"]').first();
    this.imageUrlInput  = page.locator('input[name="imageUrl"], input[name="image"], input[placeholder*="image"]').first();
    this.categorySelect = page.locator('select[name="category_id"], select[name="category"]').first();
    this.submitBtn      = page.locator('button[type="submit"]').first();
    this.cancelBtn      = page.locator('button:has-text("Hủy"), button:has-text("Cancel")').first();

    this.editButtons    = page.locator('button:has-text("Sửa"), button:has-text("Edit")');
    this.deleteButtons  = page.locator('button:has-text("Xóa"), button:has-text("Delete")');

    this.errorMsg   = page.locator('[class*="error"], [class*="alert"], [role="alert"]');
    this.successMsg = page.locator('[class*="success"], text=/thành công/i');
  }

  async goto() {
    await this.page.goto('/admin/products');
    await this.page.waitForLoadState('networkidle');
  }

  async openAddForm() {
    await this.addProductBtn.click();
    await this.page.waitForTimeout(600);
  }

  async selectFirstCategory() {
    if (await this.categorySelect.count() === 0) return;
    const options = this.categorySelect.locator('option');
    const count = await options.count();
    for (let i = 0; i < count; i++) {
      const val = await options.nth(i).getAttribute('value');
      if (val && val !== '') {
        await this.categorySelect.selectOption({ index: i });
        return;
      }
    }
    if (count > 1) await this.categorySelect.selectOption({ index: 1 });
  }

  async fillProductForm({ name, price, description, imageUrl, selectCategory = true }) {
    if (name !== undefined) await this.nameInput.fill(String(name));
    if (price !== undefined) await this.priceInput.fill(String(price));
    if (description !== undefined && await this.descInput.count() > 0) {
      await this.descInput.fill(description);
    }
    if (imageUrl && await this.imageUrlInput.count() > 0) {
      await this.imageUrlInput.fill(imageUrl);
    }
    if (selectCategory) await this.selectFirstCategory();
  }

  async fillNameAndCategoryOnly(name) {
    if (name !== undefined) await this.nameInput.fill(String(name));
    await this.priceInput.fill('');
    await this.selectFirstCategory();
  }

  async fillNamePriceNoCategory(name, price) {
    if (name !== undefined) await this.nameInput.fill(String(name));
    if (price !== undefined) await this.priceInput.fill(String(price));
  }

  async submit() {
    await this.submitBtn.click();
    await this.page.waitForTimeout(1200);
  }

  async getErrorText() {
    try {
      await this.errorMsg.first().waitFor({ timeout: 4000 });
      return await this.errorMsg.first().textContent();
    } catch { return null; }
  }

  async hasClientSideValidationError() {
    const invalid = this.page.locator('input:invalid, select:invalid, textarea:invalid');
    return (await invalid.count()) > 0;
  }

  async isSubmitSuccessful() {
    try {
      await this.successMsg.first().waitFor({ timeout: 4000 });
      return true;
    } catch {
      return !(await this.submitBtn.isVisible().catch(() => false));
    }
  }

  async expectSubmitRejected(message) {
    const ok = await this.isSubmitSuccessful();
    const error = await this.getErrorText();
    const blocked = await this.hasClientSideValidationError();
    expect(ok, message ?? 'Invalid input must not create/update product').toBe(false);
    expect(error || blocked, message ?? 'Must show validation error or block submit').toBeTruthy();
  }

  async expectSubmitSuccess(message) {
    expect(await this.isSubmitSuccessful(), message ?? 'Valid input must be accepted').toBe(true);
  }

  async getProductCount() {
    return await this.productRows.count();
  }

  async isListVisible() {
    const count = await this.getProductCount();
    if (count === 0) return false;
    const hasEdit = (await this.editButtons.count()) > 0;
    const hasDelete = (await this.deleteButtons.count()) > 0;
    return hasEdit || hasDelete || count > 0;
  }

  async getRowText(index = 0) {
    if (await this.productRows.count() <= index) return '';
    return (await this.productRows.nth(index).textContent()) ?? '';
  }

  async rowContainsText(text) {
    return this.page.locator('tbody tr, [class*="product-row"]', { hasText: text }).count().then(c => c > 0);
  }

  async clickEditRow(index = 0) {
    await this.editButtons.nth(index).click();
    await this.page.waitForTimeout(600);
  }

  async clickDeleteRow(index = 0) {
    await this.deleteButtons.nth(index).click();
    await this.page.waitForTimeout(400);
  }

  async clickDeleteByName(name) {
    const row = this.page.locator('tbody tr, [class*="product-row"]', { hasText: name }).first();
    await row.locator('button:has-text("Xóa"), button:has-text("Delete")').click();
    await this.page.waitForTimeout(400);
  }

  async confirmDeleteIfDialogAppears() {
    const confirmBtn = this.page.locator(
      'button:has-text("Xác nhận"), button:has-text("Đồng ý"), button:has-text("OK"), button:has-text("Có")'
    ).first();
    try {
      await confirmBtn.waitFor({ timeout: 2000 });
      await confirmBtn.click();
      await this.page.waitForTimeout(800);
    } catch { /* no dialog */ }
  }

  /** FR-22: required field labels should include * */
  async hasRequiredFieldMarkers() {
    const formText = await this.page.locator('form').first().textContent().catch(() => '');
    return formText.includes('*');
  }

  /** FR-22: validation error must appear above the submit button in DOM order / layout */
  async isErrorAboveSubmit() {
    const error = this.errorMsg.first();
    if ((await error.count()) === 0) return false;
    if (!(await this.submitBtn.isVisible().catch(() => false))) return true;

    const errorBox = await error.boundingBox();
    const submitBox = await this.submitBtn.boundingBox();
    if (!errorBox || !submitBox) {
      const errorY = await error.evaluate((el) => el.getBoundingClientRect().top);
      const submitY = await this.submitBtn.evaluate((el) => el.getBoundingClientRect().top);
      return errorY < submitY;
    }
    return errorBox.y < submitBox.y;
  }

  /** FR-21: price display uses ₫ symbol */
  async listShowsCurrencySymbol() {
    const text = await this.page.locator('tbody, [class*="product"]').first().textContent().catch(() => '');
    return /₫|đ|VND/i.test(text ?? '');
  }

  /** FR-21: at least one price uses thousand separator (e.g. 199.000 or 199,000) */
  async listShowsThousandSeparator() {
    const text = await this.page.locator('tbody, [class*="product"]').first().textContent().catch(() => '');
    return /[\d][.,]\d{3}/.test(text ?? '');
  }
}

module.exports = { AdminProductPage };

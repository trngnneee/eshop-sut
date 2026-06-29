// tests/pages/AdminProductPage.js
// Page Object for FR-15: Product Management (Admin CRUD)

class AdminProductPage {
  constructor(page) {
    this.page = page;

    // ── List view ────────────────────────────────────────────────────────────
    this.addProductBtn  = page.locator(
      'button:has-text("Thêm"), button:has-text("Thêm sản phẩm"), button:has-text("Add")'
    ).first();
    this.productRows    = page.locator('tbody tr, [class*="product-row"]');

    // ── Add / Edit form ──────────────────────────────────────────────────────
    this.nameInput      = page.locator('input[name="name"], input[placeholder*="tên"], input[placeholder*="name"]').first();
    this.priceInput     = page.locator('input[name="price"], input[placeholder*="giá"], input[type="number"]').first();
    this.descInput      = page.locator('textarea[name="description"], textarea[placeholder*="mô tả"]').first();
    this.imageUrlInput  = page.locator('input[name="imageUrl"], input[name="image"], input[placeholder*="image"]').first();
    this.categorySelect = page.locator('select[name="category_id"], select[name="category"]').first();
    this.submitBtn      = page.locator('button[type="submit"]').first();
    this.cancelBtn      = page.locator('button:has-text("Hủy"), button:has-text("Cancel")').first();

    // ── Edit / Delete actions (per row) ─────────────────────────────────────
    this.editButtons    = page.locator('button:has-text("Sửa"), button:has-text("Edit")');
    this.deleteButtons  = page.locator('button:has-text("Xóa"), button:has-text("Delete")');

    // ── Feedback ─────────────────────────────────────────────────────────────
    this.errorMsg   = page.locator('[class*="error"], [class*="alert"], [role="alert"]');
    this.successMsg = page.locator('[class*="success"], text=/thành công/i');
  }

  async goto() {
    await this.page.goto('/admin/products');
    await this.page.waitForLoadState('networkidle');
  }

  async isAccessible() {
    await this.page.waitForTimeout(800);
    return this.page.url().includes('/admin');
  }

  async openAddForm() {
    await this.addProductBtn.click();
    await this.page.waitForTimeout(600);
  }

  async fillProductForm({ name, price, description = 'Test description', imageUrl = '', categoryIndex = 0 }) {
    if (name !== undefined)        await this.nameInput.fill(String(name));
    if (price !== undefined)       await this.priceInput.fill(String(price));
    if (description !== undefined && await this.descInput.count() > 0)
                                   await this.descInput.fill(description);
    if (imageUrl && await this.imageUrlInput.count() > 0)
                                   await this.imageUrlInput.fill(imageUrl);
    // Select first available category option
    if (await this.categorySelect.count() > 0) {
      const options = await this.categorySelect.locator('option').all();
      const nonEmpty = options.filter(async o => (await o.getAttribute('value')) !== '');
      if (nonEmpty.length > 0) {
        await this.categorySelect.selectOption({ index: categoryIndex + 1 }); // skip blank option
      }
    }
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

  async isSubmitSuccessful() {
    try {
      await this.successMsg.first().waitFor({ timeout: 4000 });
      return true;
    } catch {
      // Also treat a redirect back to the list as success
      return !(await this.submitBtn.isVisible().catch(() => false));
    }
  }

  async getProductCount() {
    return await this.productRows.count();
  }

  async clickEditFirst() {
    await this.editButtons.first().click();
    await this.page.waitForTimeout(600);
  }

  async clickDeleteFirst() {
    await this.deleteButtons.first().click();
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
}

module.exports = { AdminProductPage };

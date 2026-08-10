import { Page, Locator, expect } from '@playwright/test';

export const ADMIN_URL = 'http://localhost:5174';

export class AdminCategoriesPage {
  readonly page: Page;
  readonly nameInput: Locator;
  readonly addButton: Locator;
  readonly table: Locator;
  readonly rows: Locator;

  constructor(page: Page) {
    this.page = page;
    this.nameInput = page.getByPlaceholder('Tên danh mục mới');
    this.addButton = page.getByRole('button', { name: 'Thêm mới' });
    this.table = page.locator('table');
    this.rows = page.locator('table tbody tr');
  }

  /** Mở admin (token đã được bơm sẵn vào localStorage) và vào tab Danh mục. */
  async gotoCategoriesTab() {
    await this.page.goto(`${ADMIN_URL}/`);
    await this.openCategoriesTab();
  }

  async openCategoriesTab() {
    await this.page.getByText('Danh mục', { exact: true }).click();
    await expect(this.table).toBeVisible();
  }

  async openProductsTab() {
    await this.page.getByText('Sản phẩm', { exact: true }).click();
  }

  /** Ô (cell) khớp chính xác tên danh mục. */
  cellByName(name: string): Locator {
    return this.page.getByRole('cell', { name, exact: true });
  }

  rowByText(text: string): Locator {
    return this.rows.filter({ hasText: text });
  }

  /**
   * Thêm danh mục và chờ POST + GET refresh hoàn tất để tránh assert vào lúc bảng chưa cập nhật.
   * Timeout ngắn + catch: nếu SUT chặn submit phía client (không phát sinh request) thì bỏ qua.
   */
  async addCategory(name: string) {
    await this.nameInput.fill(name);
    const postDone = this.page
      .waitForResponse(
        (r) => r.url().includes('/api/categories') && r.request().method() === 'POST',
        { timeout: 5_000 },
      )
      .catch(() => null);
    await this.addButton.click();
    if (await postDone) {
      await this.page
        .waitForResponse(
          (r) => r.url().includes('/api/categories') && r.request().method() === 'GET',
          { timeout: 5_000 },
        )
        .catch(() => null);
    }
  }
}

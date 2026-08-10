import { Page, Locator, expect } from '@playwright/test';

export class CheckoutPage {
  readonly page: Page;
  readonly totalInput: Locator;
  readonly couponInput: Locator;
  readonly applyButton: Locator;
  readonly couponError: Locator;
  readonly couponSuccess: Locator;
  readonly savingLine: Locator;
  readonly finalLine: Locator;
  readonly grandTotal: Locator;

  constructor(page: Page) {
    this.page = page;
    this.totalInput = page.locator('input[type="number"]');
    this.couponInput = page.getByPlaceholder('Nhập mã giảm giá...');
    this.applyButton = page.getByRole('button', { name: 'Áp dụng' });
    this.couponError = page.locator('p.text-red-600');
    this.couponSuccess = page.locator('.text-green-700');
    this.savingLine = this.couponSuccess.locator('p', { hasText: 'Tiết kiệm:' });
    this.finalLine = this.couponSuccess.locator('p', { hasText: 'Thành tiền:' });
    this.grandTotal = page.locator('span', { hasText: 'Tổng thanh toán:' });
  }

  async goto() {
    await this.page.goto('/checkout');
  }

  /** Chờ AuthContext load xong user (header hiện "Chào, ...") để user_id được gửi kèm khi áp mã. */
  async waitForLoggedInUser() {
    await expect(this.page.locator('header')).toContainText('Chào,');
  }

  async applyCoupon(total: number, code: string) {
    await this.totalInput.fill(String(total));
    await this.couponInput.fill(code);
    await this.applyButton.click();
  }
}

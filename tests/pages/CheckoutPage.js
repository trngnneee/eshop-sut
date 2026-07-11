// tests/pages/CheckoutPage.js
// Page Object for FR-08: Checkout — aligned with tests/test-cases/checkout/

class CheckoutPage {
  constructor(page) {
    this.page = page;

    this.productLines = page.locator('ul.list-disc li');
    this.totalInput = page.locator('input[type="number"]').first();
    this.totalDisplay = page.locator('text=/Tổng thanh toán/i');
    this.placeOrderBtn = page.locator(
      'button:has-text("Xác Nhận Thanh Toán"), button:has-text("Đặt hàng"), button:has-text("Thanh toán")'
    ).first();
    this.successMessage = page.getByText(/thanh toán thành công/i);
    this.pageHeading = page.locator('h1, h2').filter({ hasText: /xác nhận|thanh toán|đơn hàng/i });
    this.couponInput = page.locator('input[placeholder*="mã"], input[placeholder*="coupon"]');
    this.applyCouponBtn = page.locator('button:has-text("Áp dụng")');
  }

  async goto() {
    await this.page.goto('/checkout');
    await this.page.waitForLoadState('networkidle');
  }

  async isOnCheckoutPage() {
    return this.page.url().includes('/checkout');
  }

  async getProductLineCount() {
    return this.productLines.count();
  }

  async getProductLineTexts() {
    const n = await this.getProductLineCount();
    const texts = [];
    for (let i = 0; i < n; i++) {
      texts.push(await this.productLines.nth(i).textContent());
    }
    return texts;
  }

  async getTotalDisplayText() {
    const inputVal = await this.totalInput.inputValue().catch(() => null);
    if (inputVal) return inputVal;
    const display = await this.totalDisplay.textContent().catch(() => null);
    return display;
  }

  async isTotalEditable() {
    const count = await this.totalInput.count();
    if (count === 0) return false;
    const isDisabled = await this.totalInput.isDisabled();
    const isReadonly = await this.totalInput.getAttribute('readonly');
    return !isDisabled && isReadonly === null;
  }

  async setTotalValue(value) {
    await this.totalInput.fill(String(value));
  }

  async placeOrder() {
    await this.placeOrderBtn.click();
    await this.page.waitForTimeout(2500);
  }

  async isOrderSuccessful() {
    try {
      await this.successMessage.waitFor({ timeout: 6000 });
      return true;
    } catch {
      return /thanh toán thành công/i.test(await this.page.textContent('body') ?? '');
    }
  }
}

module.exports = { CheckoutPage };

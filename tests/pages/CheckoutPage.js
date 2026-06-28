// tests/pages/CheckoutPage.js
// Page Object for FR-08: Checkout
// (FR-09 coupon tests reuse the inline CheckoutPage from CartPage.js;
//  this file provides a fuller object for the FR-08 spec tests.)

class CheckoutPage {
  constructor(page) {
    this.page = page;

    // Order items list displayed on checkout page
    this.orderItemRows  = page.locator(
      '[class*="checkout-item"], [class*="order-item"], [class*="cart-item"], tbody tr'
    );
    // Total amount display (must be read-only, calculated by backend)
    this.totalAmount    = page.locator('[class*="total"], [class*="Total"]').last();
    // Submit / place order button
    this.placeOrderBtn  = page.locator(
      'button:has-text("Đặt hàng"), button:has-text("Thanh toán"), button:has-text("Place Order"), button[type="submit"]'
    ).first();
    // Success confirmation
    this.successMessage = page.locator(
      '[class*="success"], text=/thành công/i, text=/đặt hàng thành công/i, [role="alert"]'
    );
    // Coupon section
    this.couponInput    = page.locator(
      'input[placeholder*="mã"], input[placeholder*="coupon"], input[name="coupon"]'
    );
    this.applyCouponBtn = page.locator('button:has-text("Áp dụng"), button:has-text("Apply")');
    // Error / redirect elements
    this.errorMsg       = page.locator('[class*="error"], [class*="alert"], [role="alert"]');
  }

  async goto() {
    await this.page.goto('/checkout');
    await this.page.waitForLoadState('networkidle');
  }

  async isAccessible() {
    // Returns true if the checkout page actually loaded (not redirected to login)
    await this.page.waitForTimeout(1000);
    return this.page.url().includes('/checkout');
  }

  async getItemCount() {
    return await this.orderItemRows.count();
  }

  async getTotalText() {
    try { return await this.totalAmount.textContent(); } catch { return null; }
  }

  async placeOrder() {
    await this.placeOrderBtn.click();
    await this.page.waitForTimeout(2500);
  }

  async isOrderSuccessful() {
    try {
      await this.successMessage.first().waitFor({ timeout: 6000 });
      return true;
    } catch {
      // Also accept redirect to /orders or /order-history
      return this.page.url().match(/order(s|\/history|\/success)?/i) !== null;
    }
  }

  async isTotalEditable() {
    // The total amount field must NOT be editable (FR-08)
    const totalInput = this.page.locator('input[name*="total"], input[id*="total"]');
    const count = await totalInput.count();
    if (count === 0) return false;          // displayed as text, not input → correct
    const isDisabled = await totalInput.first().isDisabled();
    const isReadonly = await totalInput.first().getAttribute('readonly');
    return !isDisabled && isReadonly === null;  // true = editable = bug
  }

  async getErrorText() {
    try {
      await this.errorMsg.first().waitFor({ timeout: 4000 });
      return await this.errorMsg.first().textContent();
    } catch { return null; }
  }

  async applyCoupon(code) {
    await this.couponInput.fill(code);
    await this.applyCouponBtn.click();
    await this.page.waitForTimeout(1000);
  }
}

module.exports = { CheckoutPage };

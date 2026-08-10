import { test, expect } from '@playwright/test';
import { CheckoutPage } from '../pages/CheckoutPage';
import { registerUser, loginToken, getCouponIds, recordCouponUsage } from '../utils/api';
import data from '../data/fr09-coupon.json';

// FR-09 — Mã giảm giá (áp tại trang Checkout)
// Data-driven: toàn bộ test case đọc từ data/fr09-coupon.json
// Mỗi lần chạy đăng ký 1 user mới qua API để lượt dùng coupon không dây sang các lần chạy khác.

const fmt = (n: number) => n.toLocaleString('en-US'); // khớp locale en-US đặt trong config

test.describe(data.feature, () => {
  let token: string;
  let couponIds: Record<string, number>;

  test.beforeAll(async ({ request }, testInfo) => {
    const email = `coupon_${testInfo.project.name}_${Date.now()}@sut.test`;
    await registerUser(request, email, 'Secret123!');
    token = await loginToken(request, email, 'Secret123!');
    couponIds = await getCouponIds(request, token);
  });

  for (const tc of data.cases) {
    test(`${tc.id} [${tc.type}] ${tc.title}`, async ({ page, request }, testInfo) => {
      let pageToken: string | null = null;

      if (tc.auth === 'user') {
        pageToken = token;
      } else if (tc.auth === 'fresh-user-with-usage') {
        // Kịch bản C5: user riêng đã dùng coupon đủ số lần cho phép
        const email = `usage_${testInfo.project.name}_${Date.now()}@sut.test`;
        await registerUser(request, email, 'Secret123!');
        pageToken = await loginToken(request, email, 'Secret123!');
        for (let i = 0; i < (tc.preUsage ?? 0); i++) {
          await recordCouponUsage(request, pageToken, couponIds[tc.code.toUpperCase()]);
        }
      }

      if (pageToken) {
        await page.addInitScript((t) => localStorage.setItem('token', t), pageToken);
      }

      const checkout = new CheckoutPage(page);
      await checkout.goto();
      if (pageToken) {
        await checkout.waitForLoggedInUser();
      }

      if (tc.expected.outcome === 'button-disabled') {
        await checkout.totalInput.fill(String(tc.total));
        await expect(checkout.couponInput).toHaveValue('');
        await expect(checkout.applyButton).toBeDisabled();
        return;
      }

      await checkout.applyCoupon(tc.total, tc.code);

      if (tc.expected.outcome === 'applied') {
        await expect(checkout.couponSuccess).toBeVisible();
        await expect(
          checkout.savingLine,
          `số tiền giảm phải là ${fmt(tc.expected.discount!)} ₫`,
        ).toContainText(`${fmt(tc.expected.discount!)} ₫`);
        await expect(
          checkout.finalLine,
          `thành tiền phải là ${fmt(tc.expected.final!)} ₫`,
        ).toContainText(`${fmt(tc.expected.final!)} ₫`);
        await expect(
          checkout.grandTotal,
          'dòng Tổng thanh toán phải cập nhật theo thành tiền',
        ).toContainText(`${fmt(tc.expected.final!)} ₫`);
      } else {
        // rejected — spec yêu cầu từ chối kèm thông báo lý do
        await expect(checkout.couponError).toBeVisible();
        await expect(checkout.couponError).toContainText(tc.expected.errorContains!);
        await expect(checkout.couponSuccess).toBeHidden();
      }
    });
  }
});

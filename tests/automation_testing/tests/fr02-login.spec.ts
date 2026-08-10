import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { registerUser } from '../utils/api';
import data from '../data/fr02-login.json';

// FR-02 — Đăng nhập & Khóa tài khoản
// Data-driven: toàn bộ test case đọc từ data/fr02-login.json
//
// Traceability — các TC fail-đúng-kỳ-vọng đã được xác nhận là bug của SUT:
//   FR02-UI01        → issue #390 (heading "Đăng Ký" sai)
//   FR02-UI02 + TC07 → issue #391 (ô email type="text", không validate)
//   FR02-UI03        → issue #392 (ô mật khẩu không che ký tự)
//   FR02-LK01        → issue #393 (bộ đếm tăng +2/lần thay vì +1)
//   FR02-LK03        → issue #394 (khóa 180s thay vì 30s)

test.describe(data.feature, () => {
  // ---- Nhóm 1: các ca đăng nhập (positive / negative / edge) ----
  for (const tc of data.loginCases) {
    test(`${tc.id} [${tc.type}] ${tc.title}`, async ({ page }) => {
      const login = new LoginPage(page);
      await login.goto();
      await login.fillCredentials(tc.email, tc.password);

      switch (tc.expected.outcome) {
        case 'blocked': {
          // Spec FR-02: input phải được validate HTML5 → submit không gửi request
          await login.submitButton.click();
          expect(
            await login.isBlockedByHtml5Validation(),
            'form phải bị HTML5 validation chặn, không được gửi request',
          ).toBe(true);
          await expect(page).toHaveURL(/\/login$/);
          break;
        }
        case 'success': {
          const resp = await login.submitAndWaitLogin();
          expect(resp.status(), 'đăng nhập hợp lệ phải trả 200').toBe(200);
          await expect(page).toHaveURL('/');
          await expect(page.locator('header')).toContainText(tc.expected.greeting!);
          // Spec: JWT token phải được lưu phía client
          const token = await page.evaluate(() => localStorage.getItem('token'));
          expect(token, 'JWT token phải được lưu ở localStorage').toBeTruthy();
          break;
        }
        case 'error': {
          const resp = await login.submitAndWaitLogin();
          expect(resp.status(), 'đăng nhập sai phải trả 401').toBe(tc.expected.status);
          await expect(login.errorBox).toBeVisible();
          await expect(login.errorBox).toContainText(tc.expected.errorContains!);
          await expect(page).toHaveURL(/\/login$/);
          break;
        }
      }
    });
  }

  // ---- Nhóm 2: kiểm tra giao diện trang login theo spec ----
  for (const ui of data.uiChecks) {
    test(`${ui.id} [${ui.type}] ${ui.title}`, async ({ page }) => {
      const login = new LoginPage(page);
      await login.goto();
      switch (ui.check) {
        case 'heading':
          await expect(login.heading).toHaveText(ui.expected);
          break;
        case 'email-type':
          await expect(login.emailInput).toHaveAttribute('type', ui.expected);
          break;
        case 'password-type':
          await expect(login.passwordInput).toHaveAttribute('type', ui.expected);
          break;
        case 'forgot-link':
          await expect(page.getByRole('link', { name: ui.expected })).toBeVisible();
          break;
      }
    });
  }

  // ---- Nhóm 3: kịch bản khóa tài khoản (mỗi ca dùng 1 user mới đăng ký riêng) ----
  for (const lk of data.lockoutScenarios) {
    test(`${lk.id} [${lk.type}] ${lk.title}`, async ({ page, request }, testInfo) => {
      test.setTimeout(120_000); // có kịch bản chờ 31s theo spec khóa 30 giây
      const password = 'Secret123!';
      const email = `lockout_${testInfo.project.name}_${Date.now()}@sut.test`;
      await registerUser(request, email, password);

      const login = new LoginPage(page);
      await login.goto();

      for (let i = 0; i < lk.wrongAttempts; i++) {
        await login.fillCredentials(email, 'SaiMatKhau1!');
        const resp = await login.submitAndWaitLogin();
        // Spec: mỗi lần sai chỉ tăng bộ đếm; chấp nhận 401 (sai) hoặc 403 (đã khóa)
        // để kịch bản đi tiếp tới assertion chính phía dưới.
        expect.soft([401, 403], `lần sai thứ ${i + 1} phải bị từ chối`).toContain(resp.status());
      }

      if (lk.waitSeconds > 0) {
        await page.waitForTimeout(lk.waitSeconds * 1000);
      }

      await login.fillCredentials(email, password);
      const finalResp = await login.submitAndWaitLogin();

      if (lk.expected.outcome === 'success') {
        expect(
          finalResp.status(),
          'theo spec (bộ đếm +1/lần, khóa 30s) lần đăng nhập đúng này phải thành công',
        ).toBe(200);
        await expect(page).toHaveURL('/');
      } else {
        expect(finalResp.status(), 'tài khoản bị khóa → API phải trả 403').toBe(
          lk.expected.status,
        );
        // Spec: có thông báo lỗi phù hợp, không lộ chi tiết nguyên nhân
        await expect(login.errorBox).toBeVisible();
        await expect(page).toHaveURL(/\/login$/);
      }
    });
  }
});

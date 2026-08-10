import { Page, Locator, Response } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly heading: Locator;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorBox: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heading = page.locator('h2');
    // Label của SUT không gắn htmlFor/id với input nên không dùng được getByLabel;
    // neo theo div chứa label tương ứng.
    this.emailInput = page
      .locator('form > div')
      .filter({ has: page.locator('label', { hasText: 'Username' }) })
      .locator('input');
    this.passwordInput = page
      .locator('form > div')
      .filter({ has: page.locator('label', { hasText: 'Mật khẩu' }) })
      .locator('input');
    this.submitButton = page.getByRole('button', { name: 'Sign In' });
    this.errorBox = page.locator('.bg-red-100');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async fillCredentials(email: string, password: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
  }

  /** Submit và chờ response của POST /api/login (dùng khi kỳ vọng request được gửi đi). */
  async submitAndWaitLogin(): Promise<Response> {
    const [resp] = await Promise.all([
      this.page.waitForResponse(
        (r) => r.url().includes('/api/login') && r.request().method() === 'POST',
      ),
      this.submitButton.click(),
    ]);
    return resp;
  }

  /** true nếu form đang bị HTML5 validation chặn (còn ít nhất 1 input không hợp lệ). */
  async isBlockedByHtml5Validation(): Promise<boolean> {
    return this.page.evaluate(() =>
      Array.from(document.querySelectorAll<HTMLInputElement>('form input')).some(
        (i) => !i.checkValidity(),
      ),
    );
  }
}

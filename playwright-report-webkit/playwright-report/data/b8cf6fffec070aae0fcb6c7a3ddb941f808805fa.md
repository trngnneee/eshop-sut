# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: fr01_registration.spec.ts >> FR-01: Account Registration Suite >> TC05 - Đăng ký với email sai cú pháp RFC thiếu domain/kí tự @ (SRS: Form phải chặn lại)
- Location: tests\fr01_registration.spec.ts:11:9

# Error details

```
Error: SRS Requirement: Email input must have type="email" for format validation

expect(received).toBe(expected) // Object.is equality

Expected: "email"
Received: "text"
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - link "EShop" [ref=e5] [cursor=pointer]:
      - /url: /
    - navigation [ref=e6]:
      - link "Giỏ hàng" [ref=e7] [cursor=pointer]:
        - /url: /cart
      - link "Đăng nhập" [ref=e8] [cursor=pointer]:
        - /url: /login
      - link "Đăng ký" [ref=e9] [cursor=pointer]:
        - /url: /register
  - main [ref=e10]:
    - generic [ref=e11]:
      - heading "Đăng Ký Tài Khoản" [level=2] [ref=e12]
      - generic [ref=e13]:
        - generic [ref=e14]:
          - generic [ref=e15]: Họ Tên
          - textbox [ref=e16]: Le Van C
        - generic [ref=e17]:
          - generic [ref=e18]: Email
          - textbox [ref=e19]: invalidemailformat
        - generic [ref=e20]:
          - generic [ref=e21]: Mật khẩu
          - textbox [active] [ref=e22]: ValidPass123
          - paragraph [ref=e23]: "Yêu cầu: Tối thiểu 8 ký tự, có chữ hoa, chữ thường, số và ký tự đặc biệt."
        - button "Đăng Ký" [ref=e24] [cursor=pointer]
        - generic [ref=e25]:
          - text: Đã có tài khoản?
          - link "Đăng nhập" [ref=e26] [cursor=pointer]:
            - /url: /login
  - contentinfo [ref=e27]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | import testData from './data/fr01_registration.json';
  3  | 
  4  | test.describe('FR-01: Account Registration Suite', () => {
  5  |   test.beforeEach(async ({ page }) => {
  6  |     await page.goto('/register');
  7  |     await page.waitForLoadState('domcontentloaded');
  8  |   });
  9  | 
  10 |   for (const tc of testData) {
  11 |     test(`${tc.id} - ${tc.description}`, async ({ page }) => {
  12 |       test.info().annotations.push({
  13 |         type: 'Run by',
  14 |         description: '23127486 - Phan Quoc Thinh',
  15 |       });
  16 | 
  17 |       const nameInput = page.locator('input[type="text"]').first();
  18 |       const emailInput = page.locator('input').nth(1);
  19 |       const passwordInput = page.locator('input[type="password"]');
  20 |       const submitBtn = page.getByRole('button', { name: 'Đăng Ký' });
  21 | 
  22 |       // Pattern 1: Interactive State Assertion
  23 |       await expect(submitBtn).toBeVisible();
  24 |       await expect(submitBtn).toBeEnabled();
  25 | 
  26 |       let emailToFill = tc.email;
  27 |       if (tc.type === 'positive' && tc.email && !tc.email.includes('timestamp')) {
  28 |         emailToFill = `user_${tc.id.toLowerCase()}_${Date.now()}@eshop.com`;
  29 |       }
  30 | 
  31 |       if (tc.name) await nameInput.fill(tc.name);
  32 |       if (emailToFill) await emailInput.fill(emailToFill);
  33 |       if (tc.password) await passwordInput.fill(tc.password);
  34 | 
  35 |       if (tc.id === 'TC01' || tc.id === 'TC02') {
  36 |         // Positive Cases: Expect successful registration and redirection to /login
  37 |         await submitBtn.click();
  38 |         // Pattern 2: Navigation & Page State Assertion
  39 |         await expect(page).toHaveURL(/.*\/login/, { timeout: 5000 });
  40 |       } else if (tc.id === 'TC03') {
  41 |         // HTML5 required validation on Name
  42 |         const isValid = await nameInput.evaluate((el: HTMLInputElement) => el.checkValidity());
  43 |         // Pattern 3: HTML5 Constraint Validation Assertion
  44 |         expect(isValid).toBeFalsy();
  45 |         await submitBtn.click();
  46 |         await expect(page).toHaveURL(/.*\/register/);
  47 |       } else if (tc.id === 'TC04') {
  48 |         // HTML5 required validation on Email
  49 |         const isValid = await emailInput.evaluate((el: HTMLInputElement) => el.checkValidity());
  50 |         expect(isValid).toBeFalsy();
  51 |         await submitBtn.click();
  52 |         await expect(page).toHaveURL(/.*\/register/);
  53 |       } else if (tc.id === 'TC05') {
  54 |         // BUG-002: Email input is type="text" instead of type="email"
  55 |         const emailType = await emailInput.getAttribute('type');
> 56 |         expect(emailType, 'SRS Requirement: Email input must have type="email" for format validation').toBe('email');
     |                                                                                                        ^ Error: SRS Requirement: Email input must have type="email" for format validation
  57 |         await submitBtn.click();
  58 |         await expect(page).toHaveURL(/.*\/register/);
  59 |       } else if (tc.id === 'TC06') {
  60 |         // HTML5 required validation on Password
  61 |         const isValid = await passwordInput.evaluate((el: HTMLInputElement) => el.checkValidity());
  62 |         expect(isValid).toBeFalsy();
  63 |         await submitBtn.click();
  64 |         await expect(page).toHaveURL(/.*\/register/);
  65 |       } else if (tc.id === 'TC07' || tc.id === 'TC08' || tc.id === 'TC09' || tc.id === 'TC10') {
  66 |         // Negative Password Policy Cases
  67 |         await submitBtn.click();
  68 |         // Pattern 4: Text Content Match Assertion
  69 |         const errorBanner = page.locator('.bg-red-100, .text-red-700, p.text-red-500');
  70 |         await expect(errorBanner).toBeVisible();
  71 |         await expect(errorBanner).toContainText('Mật khẩu quá yếu!');
  72 |         await expect(page).toHaveURL(/.*\/register/);
  73 |       } else if (tc.id === 'TC11') {
  74 |         // BUG-003: Duplicate email should be rejected by backend
  75 |         await submitBtn.click();
  76 |         const errorBanner = page.locator('.bg-red-100, .text-red-700, p.text-red-500');
  77 |         await expect(errorBanner, 'SRS Requirement: SUT must show error when registering existing email').toBeVisible({ timeout: 3000 });
  78 |         await expect(page).toHaveURL(/.*\/register/);
  79 |       } else if (tc.id === 'TC12') {
  80 |         // BUG-001: Strong password with symbols should be accepted
  81 |         await submitBtn.click();
  82 |         await expect(page, 'SRS Requirement: Valid strong password with symbols must be accepted').toHaveURL(/.*\/login/, { timeout: 3000 });
  83 |       }
  84 |     });
  85 |   }
  86 | });
  87 | 
```
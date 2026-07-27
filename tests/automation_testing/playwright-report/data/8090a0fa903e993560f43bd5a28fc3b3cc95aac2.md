# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: profile.spec.js >> FR-04 — Quản lý hồ sơ cá nhân >> TC-PROFILE-001: Cập nhật hồ sơ thành công với dữ liệu hợp lệ theo spec FR-04
- Location: e2e/profile.spec.js:29:5

# Error details

```
Error: Update with spec-valid data must show the success alert

expect(received).toBe(expected) // Object.is equality

Expected: "Cập nhật thành công!"
Received: "Số điện thoại không hợp lệ. Vui lòng nhập đúng 9-10 chữ số."
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - link "EShop" [ref=e5]:
      - /url: /
    - navigation [ref=e6]:
      - link "Giỏ hàng" [ref=e7]:
        - /url: /cart
      - generic [ref=e8]:
        - link "Chào, Test User" [ref=e9]:
          - /url: /profile
        - button "Thoát" [ref=e10] [cursor=pointer]
  - main [ref=e11]:
    - generic [ref=e12]:
      - generic [ref=e13]:
        - heading "Hồ sơ của bạn" [level=2] [ref=e14]
        - generic [ref=e15]:
          - generic [ref=e16]:
            - generic [ref=e17]: Email (Không đổi)
            - textbox [disabled] [ref=e18]: test@eshop.com
          - generic [ref=e19]:
            - generic [ref=e20]: Họ Tên
            - textbox [ref=e21]: Nguyen Van Test
          - generic [ref=e22]:
            - generic [ref=e23]: Số điện thoại
            - 'textbox "VD: 0912345678" [ref=e24]': "0912345678"
          - generic [ref=e25]:
            - generic [ref=e26]: Địa chỉ giao hàng
            - textbox "Nhập địa chỉ của bạn" [ref=e27]: 227 Nguyễn Văn Cừ, Phường 4, Quận 5, TP.HCM
          - button "Cập nhật" [ref=e28] [cursor=pointer]
      - generic [ref=e29]:
        - heading "Lịch sử đơn hàng" [level=2] [ref=e30]
        - paragraph [ref=e31]: Bạn chưa có đơn hàng nào.
  - contentinfo [ref=e32]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  1  | // @ts-check
  2  | // FR-04 — Quản lý hồ sơ cá nhân (Pool A) — Data-driven Playwright suite.
  3  | // Test data lives in ../data/profile.json (no hardcoded inline data).
  4  | const { test, expect } = require('@playwright/test');
  5  | const path = require('path');
  6  | const fs = require('fs');
  7  | 
  8  | const API_BASE_URL = 'http://localhost:3000';
  9  | const dataFile = path.join(__dirname, '..', 'data', 'profile.json');
  10 | const testCases = JSON.parse(fs.readFileSync(dataFile, 'utf-8'));
  11 | 
  12 | // Precondition helper: log in through the API and inject the JWT into
  13 | // localStorage before any page script runs, so FR-04 tests do not depend
  14 | // on the login UI (which has its own known defects).
  15 | async function loginViaApi(page, request, credentials) {
  16 |   const res = await request.post(`${API_BASE_URL}/api/login`, { data: credentials });
  17 |   expect(res.ok(), 'Precondition: API login must succeed').toBeTruthy();
  18 |   const { token } = await res.json();
  19 |   await page.addInitScript((t) => localStorage.setItem('token', t), token);
  20 | }
  21 | 
  22 | // The SUT's labels are not linked to inputs via htmlFor/id, so scope each
  23 | // field by its immediate parent <div> that directly contains the label.
  24 | const fieldIn = (page, labelText, control = 'input') =>
  25 |   page.locator(`div:has(> label:text-is("${labelText}")) ${control}`);
  26 | 
  27 | test.describe('FR-04 — Quản lý hồ sơ cá nhân', () => {
  28 |   for (const tc of testCases) {
  29 |     test(`${tc.id}: ${tc.name}`, async ({ page, request }) => {
  30 |       await loginViaApi(page, request, tc.login);
  31 |       await page.goto('/profile');
  32 | 
  33 |       // Assertion pattern 1 — visibility: profile form is rendered for a logged-in user.
  34 |       await expect(page.getByRole('heading', { name: 'Hồ sơ của bạn' })).toBeVisible();
  35 | 
  36 |       await fieldIn(page, 'Họ Tên').fill(tc.profile.name);
  37 |       await fieldIn(page, 'Số điện thoại').fill(tc.profile.phone);
  38 |       await fieldIn(page, 'Địa chỉ giao hàng', 'textarea').fill(tc.profile.shippingAddress);
  39 | 
  40 |       // alert() blocks the page's JS, so the dialog must be accepted
  41 |       // concurrently with the click — awaiting the click first deadlocks.
  42 |       const [dialog] = await Promise.all([
  43 |         page.waitForEvent('dialog').then(async (d) => { await d.accept(); return d; }),
  44 |         page.getByRole('button', { name: 'Cập nhật' }).click(),
  45 |       ]);
  46 |       const alertMessage = dialog.message();
  47 | 
  48 |       // Assertion pattern 2 — exact value equality on the alert message.
> 49 |       expect(alertMessage, 'Update with spec-valid data must show the success alert').toBe(tc.expected.alert);
     |                                                                                       ^ Error: Update with spec-valid data must show the success alert
  50 | 
  51 |       if (tc.expected.persisted) {
  52 |         // Reload so AuthContext re-fetches GET /api/users/me from the server.
  53 |         await page.reload();
  54 | 
  55 |         // Assertion pattern 3 — input value assertion: data persisted across reload.
  56 |         await expect(fieldIn(page, 'Họ Tên')).toHaveValue(tc.profile.name);
  57 |         await expect(fieldIn(page, 'Số điện thoại')).toHaveValue(tc.profile.phone);
  58 |         await expect(fieldIn(page, 'Địa chỉ giao hàng', 'textarea')).toHaveValue(tc.profile.shippingAddress);
  59 | 
  60 |         // Assertion pattern 4 — text content: navbar greeting reflects the new name.
  61 |         await expect(page.getByRole('link', { name: /Chào,/ })).toContainText(tc.profile.name);
  62 |       }
  63 |     });
  64 |   }
  65 | });
  66 | 
```
# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: login.spec.ts >> FR-02 Login UI standards >> TC-LOGIN-021: Trường input có name/autocomplete chuẩn để tương thích trình quản lý mật khẩu
- Location: tests\login.spec.ts:133:9

# Error details

```
Error: expect(locator).toHaveAttribute(expected) failed

Locator:  locator('div').filter({ hasText: /^Username$/ }).locator('input')
Expected: "username"
Received: ""
Timeout:  5000ms

Call log:
  - Expect "toHaveAttribute" with timeout 5000ms
  - waiting for locator('div').filter({ hasText: /^Username$/ }).locator('input')
    13 × locator resolved to <input value="" required="" type="text" class="w-full border p-2 rounded"/>
       - unexpected value "null"

```

```yaml
- textbox
```

# Test source

```ts
  96  |       let dialogAppeared = false;
  97  |       page.on('dialog', async (dialog) => {
  98  |         dialogAppeared = true;
  99  |         await dialog.dismiss();
  100 |       });
  101 | 
  102 |       await page.goto('/login');
  103 |       await fillLoginForm(page, c.email, c.password);
  104 |       await submitLogin(page);
  105 | 
  106 |       if (c.expectedOutcome === 'success') {
  107 |         // Assertion pattern 1: URL navigation
  108 |         await expect(page).toHaveURL(HOME_URL);
  109 |         // Assertion pattern 2: element visibility
  110 |         await expect(page.getByRole('button', { name: 'Thoát' })).toBeVisible();
  111 |       } else {
  112 |         // Assertion pattern 1 (negated): stays on the login page
  113 |         await expect(page).toHaveURL(/\/login/);
  114 |         if (c.expectedErrorContains) {
  115 |           // Assertion pattern 3: text content
  116 |           await expect(page.getByText(c.expectedErrorContains, { exact: false })).toBeVisible();
  117 |         }
  118 |       }
  119 | 
  120 |       if (c.caseId === 'TC-LOGIN-016') {
  121 |         // Security oracle for the XSS case: no JS dialog must ever fire.
  122 |         expect(dialogAppeared).toBe(false);
  123 |       }
  124 |     });
  125 |   }
  126 | });
  127 | 
  128 | // ---------------------------------------------------------------------------------
  129 | // Shape B - UI/UX/accessibility standards (7 cases)
  130 | // ---------------------------------------------------------------------------------
  131 | test.describe('FR-02 Login UI standards', () => {
  132 |   for (const c of uiCases) {
  133 |     test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
  134 |       testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
  135 |       if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });
  136 | 
  137 |       // Session-lifecycle cases deliberately send a wrong-password attempt or otherwise
  138 |       // touch the account's login_attempts counter - never do that against the shared
  139 |       // seed account (test@eshop.com), or a lockout here breaks every later case in this
  140 |       // describe block that also logs in as that account. Give these a disposable account.
  141 |       const sessionLifecycleCases = ['TC-LOGIN-042', 'TC-LOGIN-043', 'TC-LOGIN-046'];
  142 |       let email = c.email;
  143 |       let password = c.password;
  144 |       if (sessionLifecycleCases.includes(c.caseId)) {
  145 |         email = `${c.caseId.toLowerCase()}@eshop.com`;
  146 |         password = c.caseId === 'TC-LOGIN-046' ? 'WrongPassword1!' : 'Test1234!';
  147 |         await deleteUserByEmail(email).catch(() => undefined);
  148 |         await ensureFreshAccount(request, email, c.caseId === 'TC-LOGIN-046' ? 'ValidPassword1!' : password);
  149 |       }
  150 | 
  151 |       await page.goto('/login');
  152 | 
  153 |       switch (c.check) {
  154 |         case 'form-standards': {
  155 |           await expect(page.getByRole('heading')).toHaveText(/Đăng Nhập|Đăng nhập/i);
  156 |           await expect(page.getByText('Email', { exact: false })).toBeVisible();
  157 |           const pwInput = page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input');
  158 |           await expect(pwInput).toHaveAttribute('type', 'password');
  159 |           await expect(page.getByRole('button', { name: 'Đăng nhập' })).toBeVisible();
  160 |           break;
  161 |         }
  162 |         case 'loading-state': {
  163 |           await fillLoginForm(page, c.email!, c.password!);
  164 |           const button = page.getByRole('button', { name: /Sign In|Đăng nhập/ });
  165 |           await button.click();
  166 |           await expect(button).toBeDisabled();
  167 |           break;
  168 |         }
  169 |         case 'password-toggle': {
  170 |           const toggle = page.getByRole('button', { name: /hiện mật khẩu|show password|toggle password/i });
  171 |           await expect(toggle).toBeVisible();
  172 |           break;
  173 |         }
  174 |         case 'route-guard': {
  175 |           await fillLoginForm(page, c.email!, c.password!);
  176 |           await submitLogin(page);
  177 |           await expect(page).toHaveURL(HOME_URL);
  178 |           await page.goto('/login');
  179 |           await expect(page).not.toHaveURL(/\/login/);
  180 |           break;
  181 |         }
  182 |         case 'no-credentials-in-url': {
  183 |           await fillLoginForm(page, c.email!, c.password!);
  184 |           await submitLogin(page);
  185 |           await expect(page).not.toHaveURL(new RegExp(c.password!.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
  186 |           break;
  187 |         }
  188 |         case 'tab-order': {
  189 |           const emailInput = page.locator('div').filter({ hasText: /^Username$/ }).locator('input');
  190 |           await page.keyboard.press('Tab');
  191 |           await expect(emailInput).toBeFocused();
  192 |           break;
  193 |         }
  194 |         case 'autofill-attributes': {
  195 |           const emailInput = page.locator('div').filter({ hasText: /^Username$/ }).locator('input');
> 196 |           await expect(emailInput).toHaveAttribute('autocomplete', 'username');
      |                                    ^ Error: expect(locator).toHaveAttribute(expected) failed
  197 |           break;
  198 |         }
  199 |         case 'offline-submit': {
  200 |           await fillLoginForm(page, c.email!, c.password!);
  201 |           await page.context().setOffline(true);
  202 |           await submitLogin(page);
  203 |           await page.waitForTimeout(1000);
  204 |           await expect(page.locator('body')).toBeVisible();
  205 |           await page.context().setOffline(false);
  206 |           break;
  207 |         }
  208 |         case 'session-persist-reload': {
  209 |           await fillLoginForm(page, email!, password!);
  210 |           await submitLogin(page);
  211 |           await expect(page).toHaveURL(HOME_URL);
  212 |           // Assertion pattern: reload the page and confirm the session survived it -
  213 |           // token lives in localStorage (not React state), so a real reload rehydrates it.
  214 |           await page.reload();
  215 |           await expect(page.getByRole('button', { name: 'Thoát' })).toBeVisible();
  216 |           const tokenAfterReload = await page.evaluate(() => localStorage.getItem('token'));
  217 |           expect(tokenAfterReload).toBeTruthy();
  218 |           break;
  219 |         }
  220 |         case 'logout-clears-session': {
  221 |           await fillLoginForm(page, email!, password!);
  222 |           await submitLogin(page);
  223 |           await expect(page).toHaveURL(HOME_URL);
  224 |           await page.getByRole('button', { name: 'Thoát' }).click();
  225 |           // Assertion pattern 1: UI reverts to the logged-out link
  226 |           await expect(page.getByRole('link', { name: 'Đăng nhập' })).toBeVisible();
  227 |           // Assertion pattern 2: the token is actually gone from storage, not just hidden in the UI
  228 |           const tokenAfterLogout = await page.evaluate(() => localStorage.getItem('token'));
  229 |           expect(tokenAfterLogout).toBeNull();
  230 |           break;
  231 |         }
  232 |         case 'invalid-token-auto-logout': {
  233 |           await page.goto('/');
  234 |           await page.evaluate(() => localStorage.setItem('token', 'not-a-real-jwt-string'));
  235 |           await page.reload();
  236 |           // The AuthContext effect fires GET /api/users/me with the bad token, gets a
  237 |           // non-2xx, and calls logout() - the header must show the guest state again.
  238 |           await expect(page.getByRole('link', { name: 'Đăng nhập' })).toBeVisible();
  239 |           const tokenAfter = await page.evaluate(() => localStorage.getItem('token'));
  240 |           expect(tokenAfter).toBeNull();
  241 |           break;
  242 |         }
  243 |         case 'password-autocomplete': {
  244 |           const pwInput = page.locator('div').filter({ hasText: /^Mật khẩu$/ }).locator('input');
  245 |           await expect(pwInput).toHaveAttribute('autocomplete', 'current-password');
  246 |           break;
  247 |         }
  248 |         case 'loading-resets-after-failure': {
  249 |           await fillLoginForm(page, email!, password!);
  250 |           const button = page.getByRole('button', { name: /Sign In|Đăng nhập/ });
  251 |           await button.click();
  252 |           // Assertion pattern: after the failed request settles, the button must be
  253 |           // interactive again (not stuck disabled forever) so the user can retry.
  254 |           await expect(button).toBeEnabled();
  255 |           await expect(page).toHaveURL(/\/login/);
  256 |           break;
  257 |         }
  258 |         case 'forged-token-rejected': {
  259 |           // A structurally valid JWT (3 dot-separated base64url parts) signed with the
  260 |           // wrong secret - jwt.verify() on the backend must reject it just like garbage.
  261 |           const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  262 |           const payload = Buffer.from(JSON.stringify({ id: 1, email: 'forged@eshop.com', exp: Math.floor(Date.now() / 1000) + 3600 })).toString('base64url');
  263 |           const forgedToken = `${header}.${payload}.forged-signature-not-valid`;
  264 |           await page.goto('/');
  265 |           await page.evaluate((t) => localStorage.setItem('token', t), forgedToken);
  266 |           await page.reload();
  267 |           await expect(page.getByRole('link', { name: 'Đăng nhập' })).toBeVisible();
  268 |           const tokenAfter = await page.evaluate(() => localStorage.getItem('token'));
  269 |           expect(tokenAfter).toBeNull();
  270 |           break;
  271 |         }
  272 |         default:
  273 |           throw new Error(`Unknown UI check "${c.check}" for ${c.caseId}`);
  274 |       }
  275 |     });
  276 |   }
  277 | });
  278 | 
  279 | // ---------------------------------------------------------------------------------
  280 | // Shape C - account lockout state machine (12 cases)
  281 | // Uses the API for the repeated wrong-password setup steps (fast + deterministic) and
  282 | // a direct DB fixture to simulate "the lock window has elapsed" instead of sleeping for
  283 | // the real ~3 minutes; the decisive outcome of each case is still checked exactly the
  284 | // way a user would see it (through the login form, or through admin-visible state).
  285 | // ---------------------------------------------------------------------------------
  286 | test.describe('FR-02 Account lockout behavior', () => {
  287 |   for (const c of lockoutCases) {
  288 |     test(`${c.caseId}: ${c.description}`, async ({ page, request }, testInfo) => {
  289 |       testInfo.annotations.push({ type: 'Run by', description: STUDENT_ID });
  290 |       if (c.bugRef) testInfo.annotations.push({ type: 'Bug ref', description: c.bugRef });
  291 | 
  292 |       const email = `lockout-${c.caseId.toLowerCase()}@eshop.com`;
  293 |       const correctPassword = 'ValidPassword1!';
  294 |       const wrongPassword = 'WrongPassword1!';
  295 | 
  296 |       await deleteUserByEmail(email).catch(() => undefined);
```
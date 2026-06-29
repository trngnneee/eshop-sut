# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: forgot-password.spec.js >> FR-03 · Forgot Password — Step 2: Password domain >> TC-FORGOT-018 · DT · Confirm password mismatch → rejected
- Location: tests\e2e\forgot-password.spec.js:272:3

# Error details

```
Error: Confirm-password field required (FR-03)

expect(received).toBe(expected) // Object.is equality

Expected: true
Received: false
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
      - heading "Quên Mật Khẩu" [level=2] [ref=e12]
      - generic [ref=e13]:
        - generic [ref=e14]: "Mã OTP của bạn là: 3371"
        - generic [ref=e15]:
          - generic [ref=e16]: Mã OTP (4 số)
          - textbox [ref=e17]
        - generic [ref=e18]:
          - generic [ref=e19]: Mật khẩu mới
          - textbox [ref=e20]
        - button "Đặt lại mật khẩu" [ref=e21] [cursor=pointer]
        - button "← Quay lại" [ref=e22] [cursor=pointer]
  - contentinfo [ref=e23]: © 2026 EShop SUT. Dành cho mục đích kiểm thử.
```

# Test source

```ts
  174 | 
  175 |   test('TC-FORGOT-008 · DT · OTP 7 digits → rejected', async ({ page }) => {
  176 |     const { fp } = await goToStep2(page);
  177 |     await fp.resetPassword(FORGOT.otpWrongLength7, FORGOT.newPwdValid, FORGOT.newPwdValid);
  178 |     await expectRejected(fp, page, '7-digit OTP must be rejected (SD-O04)');
  179 |   });
  180 | 
  181 |   test('TC-FORGOT-009 · DT · Wrong OTP value → rejected', async ({ page }) => {
  182 |     const { fp } = await goToStep2(page);
  183 |     await fp.resetPassword(FORGOT.otpAllZeros, FORGOT.newPwdValid, FORGOT.newPwdValid);
  184 |     await expectRejected(fp, page, 'Wrong OTP must be rejected (SD-O05)');
  185 |   });
  186 | 
  187 |   test('TC-FORGOT-010 · DT · OTP for email A used with email B → rejected via API', async ({ page }) => {
  188 |     const { body } = await requestOtpViaAPI(page, FORGOT.registeredEmail);
  189 |     expect(body.resetToken, 'Must obtain OTP for test@eshop.com').toBeTruthy();
  190 |     const response = await resetPasswordViaAPI(
  191 |       page,
  192 |       FORGOT.adminEmail,
  193 |       body.resetToken,
  194 |       FORGOT.newPwdValid
  195 |     );
  196 |     expect(response.ok(), 'OTP must not reset password for a different email (SD-O07)').toBe(false);
  197 |   });
  198 | 
  199 |   test('TC-FORGOT-027 · BVA · OTP 5 digits (length min−) → rejected', async ({ page }) => {
  200 |     const { fp } = await goToStep2(page);
  201 |     await fp.resetPassword(FORGOT.otpWrongLength5, FORGOT.newPwdValid, FORGOT.newPwdValid);
  202 |     await expectRejected(fp, page, '5-digit OTP (min−) must be rejected');
  203 |   });
  204 | 
  205 |   test('TC-FORGOT-028 · BVA · Valid 6-digit OTP → reset succeeds', async ({ page }) => {
  206 |     const { fp, otp } = await goToStep2(page);
  207 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  208 |     await fp.resetPassword(otp, FORGOT.newPwdValid, FORGOT.newPwdValid);
  209 |     await expectResetSuccess(fp, page);
  210 |   });
  211 | 
  212 |   test('TC-FORGOT-029 · BVA · OTP 7 digits (length max+) → rejected', async ({ page }) => {
  213 |     const { fp } = await goToStep2(page);
  214 |     await fp.resetPassword(FORGOT.otpWrongLength7, FORGOT.newPwdValid, FORGOT.newPwdValid);
  215 |     await expectRejected(fp, page, '7-digit OTP (max+) must be rejected');
  216 |   });
  217 | });
  218 | 
  219 | // ─────────────────────────────────────────────────────────────────────────────
  220 | test.describe('FR-03 · Forgot Password — Step 2: Password domain', () => {
  221 | 
  222 |   test('TC-FORGOT-011 · DT · Empty new password → rejected', async ({ page }) => {
  223 |     const { fp, otp } = await goToStep2(page);
  224 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  225 |     await fp.resetPassword(otp, '', FORGOT.newPwdValid);
  226 |     await expectRejected(fp, page, 'Empty new password must be rejected (SD-P01)');
  227 |   });
  228 | 
  229 |   test('TC-FORGOT-012 · DT · Password too short (7 chars) → rejected', async ({ page }) => {
  230 |     const { fp, otp } = await goToStep2(page);
  231 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  232 |     await fp.resetPassword(otp, FORGOT.newPwdTooShort, FORGOT.newPwdTooShort);
  233 |     await expectRejected(fp, page, 'Password under 8 chars must be rejected (SD-P02, FR-01)');
  234 |   });
  235 | 
  236 |   test('TC-FORGOT-013 · DT · Password missing uppercase → rejected', async ({ page }) => {
  237 |     const { fp, otp } = await goToStep2(page);
  238 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  239 |     await fp.resetPassword(otp, FORGOT.newPwdNoUpper, FORGOT.newPwdNoUpper);
  240 |     await expectRejected(fp, page, 'Password without uppercase must be rejected (SD-P03, FR-01)');
  241 |   });
  242 | 
  243 |   test('TC-FORGOT-014 · DT · Password missing lowercase → rejected', async ({ page }) => {
  244 |     const { fp, otp } = await goToStep2(page);
  245 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  246 |     await fp.resetPassword(otp, FORGOT.newPwdNoLower, FORGOT.newPwdNoLower);
  247 |     await expectRejected(fp, page, 'Password without lowercase must be rejected (SD-P04, FR-01)');
  248 |   });
  249 | 
  250 |   test('TC-FORGOT-015 · DT · Password missing digit → rejected', async ({ page }) => {
  251 |     const { fp, otp } = await goToStep2(page);
  252 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  253 |     await fp.resetPassword(otp, FORGOT.newPwdNoDigit, FORGOT.newPwdNoDigit);
  254 |     await expectRejected(fp, page, 'Password without digit must be rejected (SD-P05, FR-01)');
  255 |   });
  256 | 
  257 |   test('TC-FORGOT-016 · DT · Password missing special char → rejected', async ({ page }) => {
  258 |     const { fp, otp } = await goToStep2(page);
  259 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  260 |     await fp.resetPassword(otp, FORGOT.newPwdNoSpecial, FORGOT.newPwdNoSpecial);
  261 |     await expectRejected(fp, page, 'Password without special char must be rejected (SD-P06, FR-01)');
  262 |   });
  263 | 
  264 |   test('TC-FORGOT-017 · DT · Empty confirm password → rejected', async ({ page }) => {
  265 |     const { fp, otp } = await goToStep2(page);
  266 |     expect(await fp.hasConfirmPasswordField(), 'Confirm-password field required (FR-03)').toBe(true);
  267 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  268 |     await fp.resetPassword(otp, FORGOT.newPwdValid, '');
  269 |     await expectRejected(fp, page, 'Empty confirm password must be rejected (SD-C01)');
  270 |   });
  271 | 
  272 |   test('TC-FORGOT-018 · DT · Confirm password mismatch → rejected', async ({ page }) => {
  273 |     const { fp, otp } = await goToStep2(page);
> 274 |     expect(await fp.hasConfirmPasswordField(), 'Confirm-password field required (FR-03)').toBe(true);
      |                                                                                           ^ Error: Confirm-password field required (FR-03)
  275 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  276 |     await fp.resetPassword(otp, FORGOT.newPwdValid, FORGOT.newPwdAlt);
  277 |     await expectRejected(fp, page, 'Mismatched passwords must be rejected (SD-C02, FR-03)');
  278 |   });
  279 | });
  280 | 
  281 | // ─────────────────────────────────────────────────────────────────────────────
  282 | test.describe('FR-03 · Forgot Password — Step 2: Password BVA', () => {
  283 | 
  284 |   test('TC-FORGOT-030 · BVA · New password length 7 (min−) → rejected', async ({ page }) => {
  285 |     const { fp, otp } = await goToStep2(page);
  286 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  287 |     await fp.resetPassword(otp, FORGOT.newPwdMin7, FORGOT.newPwdMin7);
  288 |     await expectRejected(fp, page, 'Password of 7 chars (min−) must be rejected (FR-01)');
  289 |   });
  290 | 
  291 |   test('TC-FORGOT-031 · BVA · New password length 8 (min) → reset succeeds', async ({ page }) => {
  292 |     const { fp, otp } = await goToStep2(page);
  293 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  294 |     await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin8);
  295 |     await expectResetSuccess(fp, page);
  296 |   });
  297 | 
  298 |   test('TC-FORGOT-032 · BVA · New password length 9 (min+) → reset succeeds', async ({ page }) => {
  299 |     const { fp, otp } = await goToStep2(page);
  300 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  301 |     await fp.resetPassword(otp, FORGOT.newPwdMin9, FORGOT.newPwdMin9);
  302 |     await expectResetSuccess(fp, page);
  303 |   });
  304 | 
  305 |   test('TC-FORGOT-033 · BVA · New password length 49 (max−) → reset succeeds', async ({ page }) => {
  306 |     const { fp, otp } = await goToStep2(page);
  307 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  308 |     await fp.resetPassword(otp, FORGOT.pwdMax49, FORGOT.pwdMax49);
  309 |     await expectResetSuccess(fp, page);
  310 |   });
  311 | 
  312 |   test('TC-FORGOT-034 · BVA · New password length 50 (max) → reset succeeds', async ({ page }) => {
  313 |     const { fp, otp } = await goToStep2(page);
  314 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  315 |     await fp.resetPassword(otp, FORGOT.pwdMax50, FORGOT.pwdMax50);
  316 |     await expectResetSuccess(fp, page);
  317 |   });
  318 | 
  319 |   test('TC-FORGOT-035 · BVA · New password length 51 (max+) → rejected', async ({ page }) => {
  320 |     const { fp, otp } = await goToStep2(page);
  321 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  322 |     await fp.resetPassword(otp, FORGOT.pwdMax51, FORGOT.pwdMax51);
  323 |     await expectRejected(fp, page, 'Password of 51 chars (max+) must be rejected');
  324 |   });
  325 | });
  326 | 
  327 | // ─────────────────────────────────────────────────────────────────────────────
  328 | test.describe('FR-03 · Forgot Password — Step 2: Confirm-password BVA', () => {
  329 | 
  330 |   test('TC-FORGOT-036 · BVA · Confirm password length 7 (min−) → rejected', async ({ page }) => {
  331 |     const { fp, otp } = await goToStep2(page);
  332 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  333 |     await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin7);
  334 |     await expectRejected(fp, page, 'Confirm at min− with new at min must be rejected');
  335 |   });
  336 | 
  337 |   test('TC-FORGOT-037 · BVA · Confirm password length 8 (min) → reset succeeds', async ({ page }) => {
  338 |     const { fp, otp } = await goToStep2(page);
  339 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  340 |     await fp.resetPassword(otp, FORGOT.newPwdMin8, FORGOT.newPwdMin8);
  341 |     await expectResetSuccess(fp, page);
  342 |   });
  343 | 
  344 |   test('TC-FORGOT-038 · BVA · Confirm password length 9 (min+) → reset succeeds', async ({ page }) => {
  345 |     const { fp, otp } = await goToStep2(page);
  346 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  347 |     await fp.resetPassword(otp, FORGOT.newPwdMin9, FORGOT.newPwdMin9);
  348 |     await expectResetSuccess(fp, page);
  349 |   });
  350 | 
  351 |   test('TC-FORGOT-039 · BVA · Confirm password length 49 (max−) → reset succeeds', async ({ page }) => {
  352 |     const { fp, otp } = await goToStep2(page);
  353 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  354 |     await fp.resetPassword(otp, FORGOT.pwdMax49, FORGOT.pwdMax49);
  355 |     await expectResetSuccess(fp, page);
  356 |   });
  357 | 
  358 |   test('TC-FORGOT-040 · BVA · Confirm password length 50 (max) → reset succeeds', async ({ page }) => {
  359 |     const { fp, otp } = await goToStep2(page);
  360 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  361 |     await fp.resetPassword(otp, FORGOT.pwdMax50, FORGOT.pwdMax50);
  362 |     await expectResetSuccess(fp, page);
  363 |   });
  364 | 
  365 |   test('TC-FORGOT-041 · BVA · Confirm password length 51 (max+) → rejected', async ({ page }) => {
  366 |     const { fp, otp } = await goToStep2(page);
  367 |     if (!otp) test.skip(true, 'OTP not visible on screen');
  368 |     await fp.resetPassword(otp, FORGOT.pwdMax50, FORGOT.pwdMax51);
  369 |     await expectRejected(fp, page, 'Confirm password of 51 chars (max+) must be rejected');
  370 |   });
  371 | });
  372 | 
  373 | // ─────────────────────────────────────────────────────────────────────────────
  374 | test.describe('FR-03 · Forgot Password — Cross-boundary BVA', () => {
```
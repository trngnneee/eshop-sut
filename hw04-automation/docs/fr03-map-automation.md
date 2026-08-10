# Feature A — FR-03 · Map automation

**Student ID:** 23127271  
**Inputs:** `fr03-model-data.md` · JSON · `ForgotPassword.jsx`  
**Date:** 2026-08-07  

> Map locks locators / setup / journey actions. Implementation lands in **Generate**.

---

## 1. Runtime

| Surface | Default |
| --- | --- |
| Web | `BASE_URL` → `http://localhost:5173` |
| API | `API_BASE_URL` → `http://localhost:3000` |

---

## 2. Locators (`pages/ForgotPasswordPage.js`)

Prefer role / label / placeholder.

| Logical | Strategy |
| --- | --- |
| Email | label / placeholder Email |
| Submit request | button Gửi / Tiếp tục (SUT text) |
| OTP | OTP / mã xác nhận input |
| New password | password input(s) |
| Confirm password | second password / confirm label (may be absent → defect) |
| Back to login | exact **Quay lại đăng nhập** (not only "← Quay lại") |
| Step indicator | text matching Bước 1 / 2 |
| Dialogs | `page.on('dialog')` + `Promise.all` with click |

---

## 3. Setup / cleanup

| Flag | Action |
| --- | --- |
| `createUser` | `registerUser` unique email via `helpers/auth-api.js` |
| Cleanup | Prefer unique users; no shared-seed mutation |

---

## 4. Journey → actions

| Journey | Actions |
| --- | --- |
| `requestOnly` | goto forgot → fill email → submit |
| `fullReset` | request → fill OTP/password[/confirm] → submit → assert login |
| `requestThenInspect` | request → inspect step-2 / OTP banner |
| `uiContract` | open page → assert attribute / indicator |
| `backToLogin` | open page → click back-to-login |

---

## 5. Expect vocabulary → Playwright

| Type | Implementation sketch |
| --- | --- |
| `visible` / `hidden` / `containText` / `attribute` | standard expect |
| `dialog` / `dialogMatches` | captured dialog message |
| `url` | `toHaveURL` |
| `apiLogin` | helper POST login status |
| `otpLength` | parse demo OTP length == 6 |

---

## 6. Files for Generate

- `helpers/load-test-data.js`, `helpers/auth-api.js`
- `pages/ForgotPasswordPage.js`
- `tests/fr03-forgot-password.spec.js`
- `playwright.config.js` / matrix runner (shared)

## Next

**Generate** then **Verify** (`docs/fr03-verify-chromium.md`).

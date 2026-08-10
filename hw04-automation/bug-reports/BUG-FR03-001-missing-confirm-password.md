# BUG-FR03-001 — Missing confirm-password field on reset step

| Field | Value |
| --- | --- |
| Feature | FR-03 Forgot password (Web) |
| Severity | High |
| Environment | frontend-web `ForgotPassword.jsx` · localhost:5173 |
| Found by | TC-FORGOT-010 (Chromium / Firefox / WebKit) |
| Date | 2026-08-07 |

## Spec

README FR-03 Step 2: user enters OTP, **new password**, and **confirm new password**; the two password fields must match.

## Steps

1. Open `/forgot-password`.
2. Request OTP for a registered email.
3. Observe step-2 form fields.

## Expected

A confirm-password field (`type="password"`) is visible and required.

## Actual

Only one password input (“Mật khẩu mới”). No confirm field / label.

## Evidence

Playwright failure screenshot for TC-FORGOT-010 under `test-results/fr03-forgot-password/<browser>/`.

## GitHub Issue

https://github.com/trngnneee/eshop-sut/issues/372

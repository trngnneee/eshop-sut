# Bug Report — FR-02 (Login & Account Lockout)

**Student ID:** 23127207 · Reproduced by: `HW4/tests/login.spec.ts`, `HW4/tests/login-api.spec.ts`
**Environment:** Chromium, Firefox, WebKit (Playwright) — all 3 browsers reproduce every bug below identically (server-side logic, browser-independent).
**Execution evidence:** all 3 browsers ran the full 137-case suite and produced the identical
**105 passed / 32 failed / 137 total**. (No new bugs were found in the final boundary/robustness
volume pass — see `ai-review-login.md` §3e; every new case either confirmed correct handling of a
malformed input or reproduced an already-listed bug's failure pattern.)

> **GitHub Issues status:** all 8 new findings below have been filed as real GitHub Issues
> (#318–#321, #333–#335, #338) via `gh issue create`, with screenshot evidence attached. The
> already-known bugs below (#1–#12) were never filed as GitHub Issues even in HW02 (confirmed:
> zero `FR02`/`login` hits in `tests/issues_list.txt`) and remain open to file separately if
> needed.

## A. Already-known bugs reproduced by this automation run

| # | Bug ID | Title | Reproducing case(s) | Evidence |
|---|---|---|---|---|
| 1 | BUG-FR02-A-01 | Failed-login counter increments by 2 instead of 1 | TC-LOGIN-002, TC-LOGIN-023, TC-LOGIN-024 | `login_attempts` reads 2 after a single wrong password |
| 2 | BUG-FR02-A-02 | Lockout duration is 180s, not the spec'd ~30s | TC-LOGIN-025 | Measured `locked_until - triggerTime` ≈ 180013ms |
| 3 | BUG-FR02-A-04 | Login page heading reads "Đăng Ký" instead of "Đăng Nhập" | TC-LOGIN-004 | `getByRole('heading')` text mismatch |
| 4 | BUG-FR02-A-05 | Email field labeled "Username" instead of "Email" | TC-LOGIN-004 | Label text assertion |
| 5 | BUG-FR02-A-06 | Submit button reads "Sign In" instead of "Đăng nhập" | TC-LOGIN-004 | Button text assertion |
| 6 | BUG-FR02-A-07 | Password input has `type="text"` (not masked) | TC-LOGIN-004 | `toHaveAttribute('type','password')` fails |
| 7 | BUG-FR02-A-09 | Email is not trimmed server-side | TC-LOGIN-005 | Login with padded email fails instead of succeeding |
| 8 | BUG-FR02-A-11 | Submit button has no loading/disabled state | TC-LOGIN-009 | Button remains enabled right after click |
| 9 | BUG-FR02-A-12 | No show/hide password toggle | TC-LOGIN-010 | Toggle control not found |
| 10 | BUG-FR02-A-14 | No route guard on `/login` while already authenticated | TC-LOGIN-012 | Re-visiting `/login` does not redirect away |
| 11 | BUG-FR02-A-15 | Bad tab order / missing `autocomplete` attributes | TC-LOGIN-020, TC-LOGIN-021, TC-LOGIN-045 | Focus order wrong; `autocomplete` attribute absent on both the email field and (confirmed in a later pass) the password field (`current-password`) |
| 12 | BUG-FR02-A-17 | Password reset does not clear lockout state | TC-LOGIN-030 | Login with the new password still returns 403 while locked |

## B. New defects found by this automation pass

### NEW-BUG-LOGIN-01 — `POST /api/login` returns HTTP 500 for non-JSON Content-Type
- **Severity:** Medium
- **Steps:** `POST /api/login` with `Content-Type: text/plain` and a JSON-encoded string body.
- **Expected:** A graceful `4xx` validation error.
- **Actual:** HTTP 500 (unhandled exception — `req.body` is `undefined` because Express's JSON
  body-parser skips non-JSON content types, so destructuring `{ email, password }` throws).
- **Reproduced by:** `TC-API-004` (`tests/login-api.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/319 (screenshot attached)

### NEW-BUG-LOGIN-02 — Login response leaks the user's plaintext password — **High severity**
- **Severity:** High (security / data exposure)
- **Steps:** `POST /api/login` with valid credentials.
- **Expected:** Response body must not contain the password field.
- **Actual:** `response.user.password` contains the plaintext password value.
- **Reproduced by:** `TC-API-006` (`tests/login-api.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/318 (screenshot attached)

### NEW-BUG-LOGIN-03 — Identical JWTs for rapid consecutive logins
- **Severity:** Low
- **Steps:** Two `POST /api/login` calls with the same valid credentials within the same second.
- **Expected:** Each login issues a distinguishable token.
- **Actual:** Tokens are byte-identical (payload only has second-resolution `iat`, no `exp`/`jti`).
- **Reproduced by:** `TC-JWT-006` (`tests/login-api.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/320 (screenshot attached)

### NEW-BUG-LOGIN-04 — Email lookup is case-sensitive
- **Severity:** Medium
- **Steps:** Register with a lowercase email, then log in using the same email fully uppercased with the correct password.
- **Expected:** Login succeeds (email should be treated case-insensitively).
- **Actual:** Login fails with "Invalid email or password" (SQLite default `=` comparison is case-sensitive; no `LOWER()`/`COLLATE NOCASE` normalization).
- **Reproduced by:** `TC-LOGIN-028` (`tests/login.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/321 (screenshot attached)

### NEW-BUG-LOGIN-05 — Duplicate email registration silently creates an unreachable second account
- **Severity:** High (data integrity)
- **Steps:** `POST /api/register` twice with the same email but different passwords/names.
- **Expected:** The second registration is rejected (e.g. `409 Conflict`).
- **Actual:** Both succeed with `200`. `users.email` has no `UNIQUE` constraint and the handler
  never checks for an existing row; `SELECT * FROM users WHERE email = ?` always resolves to the
  first-inserted row, so the second account can never log in with the password its owner chose.
- **Reproduced by:** `TC-API-008` (`tests/login-api.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/333 (screenshot attached)

### NEW-BUG-LOGIN-06 — `POST /api/register` accepts an empty-string password
- **Severity:** High (security — no password policy)
- **Steps:** `POST /api/register` with `password: ""`, then log in with the same empty password.
- **Expected:** Registration rejects an empty/too-short password with a `4xx` error.
- **Actual:** `200` on both register and the subsequent login — no validation exists at all.
- **Reproduced by:** `TC-API-009` (`tests/login-api.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/334 (screenshot attached)

### NEW-BUG-LOGIN-07 — Password-reset token is a brute-forceable 4-digit number
- **Severity:** High (security — account takeover via brute force)
- **Steps:** `POST /api/forgot-password` with a valid email; inspect the returned `resetToken`.
- **Expected:** A cryptographically random token resistant to brute-forcing.
- **Actual:** Always a 4-digit decimal string (`Math.floor(1000 + Math.random() * 9000)`) — only
  9000 possible values, with no rate limit on `/api/reset-password` and no stored expiry.
- **Reproduced by:** `TC-API-010` (`tests/login-api.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/335 (screenshot attached)

### NEW-BUG-LOGIN-08 — Privilege escalation via `PUT /api/users/me` — **CRITICAL**
- **Severity:** Critical (privilege escalation / mass assignment, OWASP A01/A04)
- **Steps:** Register + log in as a brand-new regular user, then `PUT /api/users/me` with
  `{"role":"admin"}`.
- **Expected:** A user can never change their own `role` via a self-profile-update endpoint.
- **Actual:** `200 Profile updated`; a follow-up `GET /api/users/me` confirms `role: "admin"` —
  the account is genuinely, persistently promoted to admin.
- **Evidence:** The handler destructures `role` straight from `req.body` and writes it to the
  database whenever present, with no restriction at all.
- **Reproduced by:** `TC-API-011` (`tests/login-api.spec.ts`), all 3 browsers.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/338 (screenshot attached)

## How the 8 new issues above were filed

Installed `gh` CLI locally (`winget install --id GitHub.cli`), authenticated via
`gh auth login` (browser device-flow — no token ever typed anywhere), then filed each with:

```bash
gh issue create --repo trngnneee/eshop-sut --title "<title>" --body "<body>" --label bug
```

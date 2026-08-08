# Bug Report — FR-02 (Login & Account Lockout)

**Student ID:** 23127207 · Reproduced by: `HW4/tests/login.spec.ts`, `HW4/tests/login-api.spec.ts`
**Environment:** Chromium, Firefox, WebKit (Playwright) — all 3 browsers reproduce every bug below identically (server-side logic, browser-independent).

> **GitHub Issues status:** this environment has no `gh` CLI installed and no `GITHUB_TOKEN`
> configured, so issues could not be filed automatically (HW02's own `tests/create_github_issues.py`
> requires the same `GITHUB_TOKEN` env var and was not re-runnable here either). The
> already-known bugs below (#1–#9) were never filed as GitHub Issues even in HW02 (confirmed:
> zero `FR02`/`login` hits in `tests/issues_list.txt`). Titles/bodies below are ready to paste
> into `https://github.com/trngnneee/eshop-sut/issues/new`, or run with a supplied token — see
> the bottom of this file.

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
| 11 | BUG-FR02-A-15 | Bad tab order / missing `autocomplete` attributes | TC-LOGIN-020, TC-LOGIN-021 | Focus order wrong; `autocomplete` attribute absent |
| 12 | BUG-FR02-A-17 | Password reset does not clear lockout state | TC-LOGIN-030 | Login with the new password still returns 403 while locked |

## B. New defects found by this automation pass

### NEW-BUG-LOGIN-01 — `POST /api/login` returns HTTP 500 for non-JSON Content-Type
- **Severity:** Medium
- **Steps:** `POST /api/login` with `Content-Type: text/plain` and a JSON-encoded string body.
- **Expected:** A graceful `4xx` validation error.
- **Actual:** HTTP 500 (unhandled exception — `req.body` is `undefined` because Express's JSON
  body-parser skips non-JSON content types, so destructuring `{ email, password }` throws).
- **Reproduced by:** `TC-API-004` (`tests/login-api.spec.ts`), all 3 browsers.
- **Suggested GitHub issue title:** `[BUG][Login][API] POST /api/login trả về HTTP 500 khi Content-Type không phải application/json`

### NEW-BUG-LOGIN-02 — Login response leaks the user's plaintext password — **High severity**
- **Severity:** High (security / data exposure)
- **Steps:** `POST /api/login` with valid credentials.
- **Expected:** Response body must not contain the password field.
- **Actual:** `response.user.password` contains the plaintext password value.
- **Reproduced by:** `TC-API-006` (`tests/login-api.spec.ts`), all 3 browsers.
- **Suggested GitHub issue title:** `[BUG][Login][Security] Response đăng nhập thành công lộ password dạng plaintext trong JSON`

### NEW-BUG-LOGIN-03 — Identical JWTs for rapid consecutive logins
- **Severity:** Low
- **Steps:** Two `POST /api/login` calls with the same valid credentials within the same second.
- **Expected:** Each login issues a distinguishable token.
- **Actual:** Tokens are byte-identical (payload only has second-resolution `iat`, no `exp`/`jti`).
- **Reproduced by:** `TC-JWT-006` (`tests/login-api.spec.ts`), all 3 browsers.
- **Suggested GitHub issue title:** `[BUG][Login][Security] Hai lần đăng nhập liên tiếp trong cùng 1 giây sinh ra JWT giống hệt nhau`

### NEW-BUG-LOGIN-04 — Email lookup is case-sensitive
- **Severity:** Medium
- **Steps:** Register with a lowercase email, then log in using the same email fully uppercased with the correct password.
- **Expected:** Login succeeds (email should be treated case-insensitively).
- **Actual:** Login fails with "Invalid email or password" (SQLite default `=` comparison is case-sensitive; no `LOWER()`/`COLLATE NOCASE` normalization).
- **Reproduced by:** `TC-LOGIN-028` (`tests/login.spec.ts`), all 3 browsers.
- **Suggested GitHub issue title:** `[BUG][Login] Tra cứu Email khi đăng nhập phân biệt chữ hoa/thường`

## How to file these on GitHub once a token is available

```bash
export GITHUB_TOKEN=<personal-access-token-with-repo-scope>
python tests/create_github_issues.py   # HW02's existing script, adapt bug_dir/bug_files
# or, per-issue:
gh issue create --repo trngnneee/eshop-sut --title "<title above>" --body-file <bug-file>.md --label bug,FR-02,login
```

# AI Review & Gap Analysis — FR-02 (Login & Account Lockout)

**Student ID:** 23127207 · **Feature:** FR-02 — Pool A · **Spec files:** `tests/login.spec.ts`, `tests/login-api.spec.ts`
**Data files:** `test-data/login-cases.json` (31), `test-data/login-ui-cases.json` (14), `test-data/login-lockout-cases.json` (13), `test-data/login-api-cases.json` (11) — **69 test cases total**

## 1. Where this suite came from

HW02 (branch `HW2-Khoa`) already produced 80 manually-designed FR-02 test-case documents
(`tests/test-cases/login/*.md`, copied for reference into `docs/hw02-reference/`) and 19
confirmed bug reports (`BUG-FR02-A-01..19`). Task 1 of HW04 asked to *convert* designed test
cases into automation, not invent new ones — so the AI was driven to select, group into
data-driven "shapes", and convert a representative ~63-case subset of that pool (full detail
of which cases were selected and why is in `prompt-log.md`), rather than starting from a blank
page.

## 2. What the first AI draft got wrong or missed

The very first AI-generated script (commit `43fefdf`, before this review pass) covered a single
case (`TC-LOGIN-001`) with a hardcoded single-object JSON file. Reviewing it against the full
80-case HW02 pool surfaced these concrete gaps:

| # | What the AI missed | Why it missed it | Fix applied |
|---|---|---|---|
| 1 | Data file was one JSON **object**, not an array — not actually "data-driven" for more than 1 case | The initial prompt only asked to automate the one happy-path case, so the AI never designed a schema that could scale | Redesigned as 4 typed arrays (`login-cases.json`, `-ui-cases.json`, `-lockout-cases.json`, `-api-cases.json`) with a runtime loader that rejects duplicate/missing `caseId`s |
| 2 | No account isolation strategy for negative cases | The AI was never told that `login_attempts` increments **by 2** per failed attempt (a real SUT bug, `BUG-FR02-A-01`) — it had not read `backend/server.js`, so it did not realize two negative cases sharing the seeded `test@eshop.com` account would silently lock each other out | Every case that submits a *wrong* password against a real account now registers its own throwaway account first (`accountMode: "fresh"` / per-case lockout emails), so cases never contaminate each other regardless of execution order |
| 3 | Lockout/timing cases were not attempted at all | A naive approach would `page.waitForTimeout(180000)` per case — the AI defaulted to "not automatable" for anything timing-related | Added `tests/utils/db.ts`, a thin wrapper around the backend's own SQLite file, used only to fast-forward `locked_until` into the past (simulating "the lock window elapsed") and to read `login_attempts`/`locked_until` as a second oracle — this is the same direct-DB-inspection technique HW02's own `test_fr02_advanced.py` already used |
| 4 | Only one assertion pattern (`toHaveURL`) was exercised end-to-end | The original script had 3 *declared* patterns but only one feature (login) ever ran them | The full suite now exercises `toHaveURL`, `toBeVisible`/`toBeDisabled`, `toHaveText`/`toContainText`, `toHaveAttribute`, `toBeFocused`, plus response/JWT-payload assertions in the API spec — 6+ distinct patterns |
| 5 | Selectors depended on the visible Vietnamese/English label text (`hasText: /^Username$/`) | The SUT's `Login.jsx` has no `<label for>`, so `getByLabel` silently fails; the AI's first instinct (before being corrected) was to fall back to brittle CSS (`input:nth-of-type(1)`) | Kept the container-text locator strategy (still label-adjacent, not positional), which survives DOM reordering |
| 6 | No handling for JS `dialog` events on the XSS case | AI did not realize an un-dismissed `confirm()`/`alert()` dialog hangs a Playwright test forever | Added a `page.on('dialog', ...)` guard that auto-dismisses and records whether it fired, asserted explicitly in `TC-LOGIN-016` |

## 3. Execution results (Chromium, first full run)

**46 passed / 17 failed** out of 63. Every failure was triaged individually against the known
bug list and the actual `backend/server.js` logic — **none were caused by a flaw in the
automation itself** (see the fix log for the two script bugs that *were* found and corrected
during triage, both path-resolution typos in `require()` calls, fixed before this run).

### 3.1 Failures that reproduce already-known HW02 bugs

| Case(s) | Confirms | Evidence |
|---|---|---|
| TC-LOGIN-002, TC-LOGIN-023, TC-LOGIN-024 | `BUG-FR02-A-01` — counter increments by 2, not 1 | Attempts read as 2 after 1 failure; account already locked after only 2 failures |
| TC-LOGIN-025 | `BUG-FR02-A-02` — lock duration is 180000ms, not the spec'd ~30000ms | `durationMs` measured at 180013ms |
| TC-LOGIN-005 | `BUG-FR02-A-09` — email is not trimmed server-side | Login with padded email fails instead of succeeding |
| TC-LOGIN-004 | `BUG-FR02-A-04..08` — heading says "Đăng Ký", label says "Username", button says "Sign In", password field is `type="text"` | Combined UI-standards assertions fail |
| TC-LOGIN-009 | `BUG-FR02-A-11` — submit button has no loading/disabled state | Button remains enabled immediately after click |
| TC-LOGIN-010 | `BUG-FR02-A-12` — no show/hide password toggle | Toggle button not found |
| TC-LOGIN-012 | `BUG-FR02-A-14` — no route guard on `/login` when already authenticated | Page stays on `/login` instead of redirecting |
| TC-LOGIN-020, TC-LOGIN-021 | `BUG-FR02-A-15` — bad tab order / missing `autocomplete` attributes | Focus doesn't land on the email field first; `autocomplete="username"` missing |
| TC-LOGIN-030 | `BUG-FR02-A-17` — password reset does not clear the lockout state | Login with the *new* password is still blocked (403) |

### 3.2 New defects found by this automation pass (not in the original 19)

| ID | Severity | Finding | Case |
|---|---|---|---|
| NEW-BUG-LOGIN-01 | Medium | `POST /api/login` returns HTTP 500 (unhandled exception) when `Content-Type` is not `application/json`, instead of a graceful 4xx | TC-API-004 |
| NEW-BUG-LOGIN-02 | **High** | Successful login response body includes the user's **plaintext password** (`user.password`) | TC-API-006 |
| NEW-BUG-LOGIN-03 | Low | Two logins issued within the same second produce byte-identical JWTs (only second-resolution `iat`, no `exp`/`jti`) | TC-JWT-006 |
| NEW-BUG-LOGIN-04 | Medium | Email lookup is case-sensitive (`WHERE email = ?` with default SQLite BINARY collation) — the same account cannot log in with a different letter case | TC-LOGIN-028 |

These four are logged in `docs/bug-report-login.md` and were filed as real GitHub Issues
(#318–#321) with screenshot evidence.

## 3b. Third pass — session-lifecycle coverage (69 cases total)

The first two passes covered a single login attempt end-to-end but never touched what happens
*after* a successful login — reload, logout, or a corrupted/forged token — even though
`AuthContext.jsx`'s `useEffect` (rehydrate-from-`localStorage` + auto-logout-on-401/403) is a
distinct piece of logic from the login form itself. Six cases were added to close that gap:

| Case | Check | Result |
|---|---|---|
| `TC-LOGIN-042` | Session survives a real page reload (token rehydrated from `localStorage`) | **Passes** — positive confirmation |
| `TC-LOGIN-043` | Clicking "Thoát" clears the token from `localStorage`, not just the UI | **Passes** |
| `TC-LOGIN-044` | A garbage (non-JWT) string in `localStorage.token` triggers auto-logout on load | **Passes** — `AuthContext`'s `.catch(() => logout())` handles this correctly |
| `TC-LOGIN-045` | Password field has `autocomplete="current-password"` | **Fails** — same root cause as `BUG-FR02-A-15` (the SUT never sets `autocomplete` on any auth input); not filed as a separate issue |
| `TC-LOGIN-046` | Loading state resets (button re-enabled) after a *failed* login, not just before submit | **Passes** |
| `TC-LOGIN-047` | A structurally-valid JWT signed with the wrong secret is rejected by the backend, triggering auto-logout | **Passes** — `jwt.verify()` correctly rejects a bad signature |

**Script bug found and fixed while adding these:** `TC-LOGIN-046` initially sent a wrong-password
attempt against the shared seed account `test@eshop.com` (the same account several other UI-standard
cases in this describe block also log into with the *correct* password). That wrong attempt
increments the account's `login_attempts` by 2 towards a lockout, which then made every later case
sharing that account fail for the wrong reason — the exact same class of shared-mutable-state bug
documented in `ai-review-cart.md` §3 and `ai-review-dashboard.md` §2, just in a third feature. Fixed
by giving all three session-lifecycle cases that touch the login counter (`042`, `043`, `046`) a
disposable per-case account instead of the shared seed one.

## 4. Cases not automated

| Case | Reason |
|---|---|
| TC-LOGIN-006, TC-LOGIN-011 | Superseded by `TC-JWT-001` (checks the same "no `exp` claim" defect via direct JWT decode, which is a stronger and faster oracle than manipulating client clocks) |
| TC-LOGIN-008 (rate limiting) | No rate limiter exists to test against (confirmed absent per `BUG-FR02-A-10`); a meaningful automated check would need a fixed request budget/time window that would make the suite slow and flaky for a boundary that doesn't exist yet |
| TC-LOGIN-019 (JWT `alg: none` bypass) | Targets the general auth *middleware*, not the `/api/login` endpoint itself; would need a raw unsigned-token forgery helper out of scope for this feature's automation |
| TC-LOGIN-022 (oversized payload / DoS) | Low value for a functional suite and prone to environment-specific timeouts; recommended as a manual/perf-testing follow-up instead |
| TC-LOGIN-027 (multi-device session sync) | Lock state is stored server-side per account, so it is inherently shared across clients; already exercised indirectly by `TC-LOCK-BVA-005` (concurrent requests) |

## 5. Assertion pattern inventory

`toHaveURL`, `toBeVisible`, `toContainText`/`toHaveText`, `toBeDisabled`/`toBeEnabled`,
`toHaveAttribute`, `toBeFocused`, `page.evaluate()` + `expect(x).toBeTruthy()/toBeNull()` (direct
`localStorage` inspection), `expect(status).not.toBe(...)`, `expect(payload).toHaveProperty(...)` —
**9 distinct patterns** across the two spec files (requirement: ≥3).

## 6. Execution evidence (final, all 3 browsers, 69 cases)

Chromium, Firefox, and WebKit each produced the identical **51 passed / 18 failed / 69 total**.
Reports: `HW4/reports/login/{chromium,firefox,webkit}/index.html`, each labeled `Run by: 23127207`
with an ISO timestamp.

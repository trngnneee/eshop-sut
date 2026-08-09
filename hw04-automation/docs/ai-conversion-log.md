# AI conversion log — Feature A FR-03 (HW04 Task 1)

Student ID: **23127271**  
Feature: FR-03 Forgot password and password reset (two steps)  
Tool: Cursor Agent (Grok) · Date: 2026-08-07  
Sources: `Repo/eshop-sut/README.md` FR-03/FR-01/FR-22, HW02 Feature A, `2026.HW04.Automation Testing_En.pdf` Task 1

## Requirement ledger

| Feature | Source | Case IDs | Count | Data file | Spec file | Browsers | Reports |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| FR-03 (Feature A) | README FR-03 + HW02 + HW04 PDF | TC-FORGOT-001…014 | 14 | `test-data/fr03-forgot-password.json` | `tests/fr03-forgot-password.spec.js` | Chromium, Firefox, WebKit | `reports/html/fr03-forgot-password/<browser>/` |

HW04 Task 1 also requires Features B and C (≥12 each) for a full 9-cell matrix. This log covers **Feature A only**.

## Traceability

| Requirement | Case IDs | Automated title focus |
| --- | --- | --- |
| FR-03 Step 1 registered email → OTP | 001, 014 | OTP banner / full reset |
| FR-03 email rejection | 002, 003, 004 | empty / invalid / unregistered |
| FR-03 OTP validity | 005, 006, 007, 014 | wrong / empty / length 5 / length 6 |
| FR-01 password strength on reset | 008, 009 | short / missing uppercase |
| FR-03 confirm password | 010 | confirm field present |
| FR-03 / FR-22 step indicator | 011 | "Bước 1 / 2" |
| FR-03 back to login | 012 | Quay lại đăng nhập → `/login` |
| FR-22 email `type="email"` | 013 | email input attribute |

## Stage trace

### 1. Analyze

**Prompt intent:** Extract FR-03 actors, preconditions, state transitions, inputs, outputs from README and cross-check HW04 Task 1 (≥12 cases, data-driven, ≥3 assertion patterns, 3 browsers, labeled HTML reports).

**Outcome:**
- Two-step flow: email → OTP + new password + confirm (spec).
- Spec: 6-digit OTP, step indicator, back-to-login, FR-01 password rules, confirm match.
- Observed SUT gaps (from `ForgotPassword.jsx` / backend): 4-digit OTP, no confirm field, no step indicator, no login back-link, email `type="text"`, client password regex requires whitespace and rejects `@$!`, backend stores plaintext password and issues 4-digit token.
- Seed user must not be mutated — unique API-registered accounts per run.

### 2. Design

**Prompt intent:** Propose ≥12 uniquely identified cases (positive / negative / boundary / validation / UI).

**Outcome:** 14 cases TC-FORGOT-001…014 covering happy path, request failures, OTP failures, password strength, and UI contract rules from the spec (not the defective SUT).

### 3. Review

**Prompt intent:** Remove duplicates; map every expected result to an observable oracle; keep spec oracles even when SUT is defective.

**Outcome:**
- Happy-path oracle: success dialog + `/login` + API login with new password.
- Negative oracles: dialog text, stay on forgot-password, or initial password still works.
- Spec-only UI oracles (010–014) intentionally fail against current SUT → product defects, not softened.

### 4. Model data

**Prompt intent:** External JSON schema; map every case ID to one record; no inline case arrays in the spec.

**Outcome:** `test-data/fr03-forgot-password.json` with `journey`, `inputs`, and `expected.assertions[]` vocabulary. Loader rejects unknown journeys/assertion types, duplicate IDs, and fewer than 12 records.

### 5. Map automation

**Prompt intent:** Stable locators, setup/cleanup, isolation, assertion patterns.

**Outcome:**
- Page object `pages/ForgotPasswordPage.js` (`getByRole` / label / form inputs).
- Setup: `registerUser` when `setup.createUser` is true; unique email per run.
- Dispatcher in spec by `journey` + assertion `type` (no per-ID branching).
- Assertion patterns: visibility/hidden, text, attribute, URL, plain value (dialog / OTP length / API status).

### 6. Generate

**Files under `SoftwareTesting-HW/HW4/23127271/`:**
- `test-data/fr03-forgot-password.json` (14 cases)
- `helpers/load-test-data.js`, `helpers/auth-api.js`
- `pages/ForgotPasswordPage.js`
- `tests/fr03-forgot-password.spec.js`
- `playwright.config.js`, `scripts/run-matrix.js`
- `docs/ai-conversion-log.md`, `README.md`

### 7. Verify and repair

**Prompt intent:** List tests → Chromium sample → full 3-browser matrix; confirm `Run by: 23127271` in each report.

**Outcome (executed 2026-08-07):**
- Discovery: 14 cases × 3 projects = **42** listed tests.
- Chromium smoke after repair: **9 passed / 5 failed** (failures = 010–014 product defects only).
- Repairs applied: dialog `Promise.all` to avoid sync `alert()` deadlock; end-state assertions for happy path; tightened "Quay lại đăng nhập" locator; skip confirm fill when only one password field.
- Matrix: Chromium / Firefox / WebKit each **9 pass / 5 fail**; all three `index.html` contain visible `Run by: 23127271` (title + header + meta).
- Manifest: `reports/run-manifest.json` (cell exitCode 1 expected while spec defects remain).

## Assertion pattern ledger

| Pattern | API | Demonstrated in |
| --- | --- | --- |
| Visibility / hidden | `toBeVisible` / `toBeHidden` | 001, 002, 010, 011 |
| Text content | `toContainText` | 001, 010, 011, 014 |
| Attribute | `toHaveAttribute` | 001, 010, 013 |
| Navigation | `toHaveURL` | 001, 005, 012 |
| Plain value | `toBe` / `toMatch` | dialogs, OTP length, API login status |

## Known product defects exercised by failing oracles

| Case | Spec expectation | SUT observation |
| --- | --- | --- |
| 010 | Confirm password field | Missing |
| 011 | Step indicator "Bước 1 / 2" | Missing |
| 012 | Quay lại đăng nhập → login | Only "← Quay lại" to step 1 |
| 013 | Email `type="email"` | `type="text"` |
| 014 | OTP 6 digits | OTP 4 digits |

---

## Feature B prep note (2026-08-09) — no FR-08 tests generated yet

Before starting FR-08 Checkout automation:

- Feature A HTML reports copied to `evidence/feature-a-fr03-frozen-2026-08-07/`.
- Live FR-03 report dirs locked with `EVIDENCE-LOCK.json` (matrix skips unless `FORCE_OVERWRITE=1`).
- Matrix runner supports `npm run test:matrix:fr08` and merge-safe combined manifest.
- Default Playwright report slug changed from `fr03-forgot-password` → `adhoc` to prevent accidental overwrite.
- Prep ledger: `docs/fr08-prep-ledger.md`.

Feature B Analyze→Generate stages will be appended below when implementation starts (this section must remain).

---

## Feature B — FR-08 Checkout (executed 2026-08-09)

### Requirement ledger (updated)

| Feature | Source | Case IDs | Count | Data file | Spec file | Browsers | Reports |
| --- | --- | --- | ---: | --- | --- | --- | --- |
| FR-03 (A) | done | TC-FORGOT-001…014 | 14 | `fr03-forgot-password.json` | `fr03-forgot-password.spec.js` | 3 | frozen |
| FR-08 (B) | README FR-08 + HW02 + HW04 PDF | TC-CHECKOUT-001…014 | 14 | `fr08-checkout.json` | `fr08-checkout.spec.js` | 3 | `reports/html/fr08-checkout/<browser>/` |

### Stage outcomes

1. **Analyze** — auth gate, non-editable total, line items, server recalc, cart clear; SUT defects confirmed in `Checkout.jsx` / `POST /api/checkout`.
2. **Design** — 14 cases (pos/neg/boundary/validation/state/API).
3. **Review** — keep spec oracles for 002/003/007/008/009; map to observable UI/API checks.
4. **Model data** — external JSON + FR-08 journey/assertion vocabulary in loader.
5. **Map automation** — SPA navigation after seed (in-memory cart); page objects; API helpers.
6. **Generate** — spec/data/pages/helpers; bug reports BUG-FR08-001…005.
7. **Verify** — Chromium 9/5; matrix 9 pass / 5 fail × 3 browsers; labels `Run by: 23127271`; `evidence:verify-fr03` OK.

### Assertion patterns (FR-08)

| Pattern | Used in |
| --- | --- |
| Visibility / hidden | 003, 005, 010, 011 |
| Text | 001 dialog, 004, 006, 014 |
| URL | 001, 002 |
| Count | 005, 013 |
| Plain / API / readonly | 007, 008, 012 |

### Product defects (not softened)

002 route guard · 003 empty cart · 007 editable total · 008 trusts client total · 009 cart not cleared

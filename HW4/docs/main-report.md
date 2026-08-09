# HW04 — Automation Testing: Main Report

**Student ID:** 23127207 · **SUT:** EShop (`https://github.com/trngnneee/eshop-sut`)
**Features (kept from HW02):** FR-02 Login & Lockout (Pool A) · FR-07 Shopping Cart (Pool B) ·
FR-13 Admin Dashboard (Pool C)

## 1. Summary

192 data-driven Playwright test cases were generated with AI, reviewed, corrected, and executed
across Chromium/Firefox/WebKit (576 browser runs total), producing **the same pass/fail count on
all three engines for every feature** — strong evidence that failures are real application/data
defects, not browser flakiness. 114 cases passed; 78 failed, reproducing 30 already-known HW02
bugs and surfacing 12 new ones, including a High-severity plaintext-password leak in the login API.
All 12 new bugs are filed as real GitHub Issues (#318–#329) with screenshot evidence.

| Feature | Cases | Passed | Failed | Report |
|---|---:|---:|---:|---|
| FR-02 Login | 69 | 51 | 18 | `reports/login/{chromium,firefox,webkit}/index.html` |
| FR-07 Cart | 75 | 39 | 36 | `reports/cart/{chromium,firefox,webkit}/index.html` |
| FR-13 Dashboard | 48 | 24 | 24 | `reports/dashboard/{chromium,firefox,webkit}/index.html` |

## 2. Process (Task 1 requirement: AI-first, step by step)

Each feature followed the same 7-step process, driven interactively rather than with one generic
prompt (full prompts/outputs: [`prompt-log.md`](prompt-log.md); tool/date table:
[`ai-audit-report.md`](ai-audit-report.md)):

1. **Analyze** the actual SUT source (not just the manual test-case docs) — e.g. reading
   `backend/server.js`'s lockout math, `CartContext.jsx`'s client-only state, and
   `frontend-admin/src/App.jsx`'s revenue formula *before* writing any assertion.
2. **Design** — select a representative case set from the 80/89/46-case pool already designed in
   HW02 (`docs/hw02-reference/`), prioritizing every case tied to a known bug plus enough
   additional boundary/negative cases to comfortably exceed the 12-per-feature minimum.
3. **Review** for duplicates/testability and map every case to an observable oracle.
4. **Model data** as external JSON arrays (`test-data/*.json`), never hardcoded inline.
5. **Map automation** — locator strategy, setup/cleanup, per-case account isolation.
6. **Generate** the Playwright spec.
7. **Verify and repair** — run for real, triage every failure against the SUT source to classify it
   as a genuine defect vs. an automation bug, and fix automation bugs without weakening assertions.

Step 7 is where most of the real engineering happened. Two distinct classes of automation bug were
found and fixed only because the suite was re-verified on more than one browser against the same
long-lived backend (see §3 of `ai-review-cart.md` and `ai-review-dashboard.md`): tests that mutated
shared seed data (a product's price, the admin account) without restoring it, silently corrupting
whichever browser's run happened afterward.

## 3. Review and gap analysis of the AI-generated scripts

Per-feature detail (what the AI got wrong, why, and the fix) lives in:
- [`ai-review-login.md`](ai-review-login.md)
- [`ai-review-cart.md`](ai-review-cart.md)
- [`ai-review-dashboard.md`](ai-review-dashboard.md)

Recurring patterns across all three:
- **Locators generated without inspecting the live DOM** (missing `htmlFor`, ambiguous text
  matches) — fixed by locating against the actual rendered page, not assumed markup.
- **No cross-test state isolation** — the AI reasoned about one test case at a time and didn't
  model that Chromium/Firefox/WebKit runs share one backend process. Fixed with disposable
  throwaway accounts/products for every destructive setup step.
- **Assertions correctly encoded the spec, not the buggy actual behavior**, per instruction — every
  failure below is deliberate, not a weakened expectation.

## 4. Bug reports

- [`bug-report-login.md`](bug-report-login.md) — 12 known + 4 new
- [`bug-report-cart.md`](bug-report-cart.md) — 15 known + 4 new
- [`bug-report-dashboard.md`](bug-report-dashboard.md) — 3 known + 4 new

All 12 new bugs were filed as real GitHub Issues ([#318–#329](https://github.com/trngnneee/eshop-sut/issues?q=is%3Aissue+318..329+in%3Anumber))
with screenshot evidence attached, via `gh` CLI browser-login authentication (pasting a raw token
into chat triggered GitHub's near-instant secret-scanning revocation four times in a row before
this approach was used — see `docs/submission-checklist.md`).

## 5. Cases not automated

See `ai-review-login.md` §4 for the specific list (rate-limiting stress test, JWT `alg:none`
forgery, oversized-payload DoS) and `bug-report-cart.md` §C (two quantity values that
`input[type=number].fill()` cannot inject at all). Each entry states why, and what would be needed
to automate it (a real rate limiter to test against, a raw-socket JWT forgery helper, etc.).

## 6. Test summary

See [`README.md`](../README.md) §1 and §8 for the consolidated execution table and self-assessment.

# HW04 — Automation Testing (Playwright + TypeScript) — EShop SUT

**Student ID:** `23127207` · **Course:** Software Testing · **Branch:** `HW4-Khoa`

Automates the same 3 web features selected in HW02 (one per pool), following the AI-first
7-step workflow (Analyze → Design/Review → Model data → Map automation → Generate →
Verify/repair) documented step by step in [`docs/prompt-log.md`](docs/prompt-log.md).

| Pool | Feature | Spec files | Data files | Cases |
|---|---|---|---|---:|
| A | FR-02 — Login & Account Lockout | `tests/login.spec.ts`, `tests/login-api.spec.ts` | `test-data/login-{cases,ui-cases,lockout-cases,api-cases}.json` | 137 |
| B | FR-07 — Shopping Cart | `tests/cart.spec.ts`, `tests/cart-api.spec.ts` | `test-data/cart-{ui,edge,api}-cases.json` | 142 |
| C | FR-13 — Admin Dashboard | `tests/dashboard.spec.ts`, `tests/dashboard-api.spec.ts` | `test-data/dashboard-{data,api}-cases.json` | 121 |

## 1. Test summary (execution evidence)

All numbers below are from real, verified runs on Chromium, Firefox, and WebKit — **each browser
produced the identical pass/fail count per feature** (see `docs/ai-review-*.md` for how that
consistency was achieved, including test-isolation bugs found and fixed along the way, and seven
further coverage passes that grew the suite from 63/63/32 to 137/142/121 after review — closing
Cart/Dashboard gaps, adding Login session-lifecycle coverage, repeatedly reading backend source
for entirely untested code paths (which is how the two most severe bugs in this whole assignment
were found: a login API leaking plaintext passwords, and — worse — a privilege escalation letting
any logged-in user become an admin with one API call), and finally a large pure boundary/
robustness volume pass reusing already-proven data-driven shapes to reach 400 cases suite-wide as
requested).

| Feature | Cases | Browser runs | Passed | Failed | Known bugs reproduced | New bugs found |
|---|---:|---:|---:|---:|---:|---:|
| FR-02 Login | 137 | 411 | 105 | 32 | 12 | 8 |
| FR-07 Cart | 142 | 426 | 66 | 76 | 15 | 7 |
| FR-13 Dashboard | 121 | 363 | 50 | 71 | 3 | 4 |
| **Total** | **400** | **1200** | **221** | **179** | **30** | **19** |

- **Features automated:** 3 (FR-02 Pool A, FR-07 Pool B, FR-13 Pool C).
- **Total bugs found by this automation:** 49 (30 already known from HW02, confirmed still
  present — including one, `BUG-FR13-C-03`, that a first pass had marked "too hard to simulate"
  and a later pass reproduced via route interception; 19 newly discovered — including 1
  **CRITICAL** privilege-escalation bug (`PUT /api/users/me` lets any user set their own `role`
  to `"admin"`) and 5 **High**-severity security issues: a plaintext-password leak, unreachable
  duplicate-email ghost accounts, zero-validation empty passwords, a brute-forceable
  password-reset token, and an unauthenticated order-viewing IDOR. All 19 new bugs are filed as
  real GitHub Issues (#318–#329, #333–#339) with screenshot evidence, filed via `gh` CLI
  browser-login (see `docs/submission-checklist.md`). The final boundary/robustness volume pass
  (63 more cases across all three features, reusing already-proven parameterized shapes with
  zero new spec code) found no further bugs — every new case either confirmed correct handling
  of a malformed/boundary input or reproduced an already-tracked bug family; the highest-value
  passes remain the ones that deliberately read backend source for code paths no earlier case
  had ever touched (register/forgot-password, checkout/orders, self-profile-update) — see each
  `ai-review-*.md`'s final section for the honest breakdown of what passed vs. failed and why.
- **Demo video (automation run):** https://youtu.be/ZN3auOEaKxg?si=O-Edex4pLQqU1OIa
- **Demo video (Agent Skill):** https://youtu.be/J9G12MjwVqU?si=s8RorcAw7v-_K2it

Full per-feature breakdown, root-cause analysis, and the exact reproducing case IDs:
[`docs/ai-review-login.md`](docs/ai-review-login.md) · [`docs/bug-report-login.md`](docs/bug-report-login.md)
[`docs/ai-review-cart.md`](docs/ai-review-cart.md) · [`docs/bug-report-cart.md`](docs/bug-report-cart.md)
[`docs/ai-review-dashboard.md`](docs/ai-review-dashboard.md) · [`docs/bug-report-dashboard.md`](docs/bug-report-dashboard.md)

## 2. Environment setup

Requires Node.js ≥ 20. From `HW4/`:

```bash
npm install
npx playwright install
```

Start all three SUT services (separate terminals, repo root):

```bash
cd backend && npm start          # http://localhost:3000
cd frontend-web && npm run dev   # http://localhost:5173
cd frontend-admin && npm run dev # http://localhost:5174
```

> If port 3000 is already taken by an unrelated process on your machine, start the backend with
> `PORT=3001 npm start` and pass `API_BASE_URL=http://localhost:3001` to the test commands below
> (only needed as a local workaround — the committed config defaults to port 3000).

## 3. Running the suite

Each command below runs one feature against one browser and writes a labeled HTML report to
`reports/<feature>/<browser>/`:

```bash
npm run test:login:chromium   npm run test:login:firefox   npm run test:login:webkit
npm run test:cart:chromium    npm run test:cart:firefox    npm run test:cart:webkit
npm run test:dashboard:chromium  npm run test:dashboard:firefox  npm run test:dashboard:webkit
```

Or run the full 3×3 matrix for one feature at once (also prints a pass/fail manifest):

```bash
npm run test:matrix:login
npm run test:matrix:cart
npm run test:matrix:dashboard
npm run test:matrix           # all 3 features × 3 browsers
```

View a report:

```bash
npx playwright show-report reports/login/chromium
```

Every report's title, banner, and metadata visibly show **`Run by: 23127207`** together with an
ISO timestamp (injected by `scripts/inject-student-id.js`, which `npm run test:*` calls
automatically).

## 4. Directory structure

```text
HW4/
├── docs/
│   ├── 2026.HW04.Automation Testing_En.pdf   # assignment brief
│   ├── system-analysis.md, prompt-log.md      # SUT survey + full AI-first step log
│   ├── ai-review-{login,cart,dashboard}.md    # per-feature AI review / gap analysis
│   ├── bug-report-{login,cart,dashboard}.md   # per-feature bug reports (known + new)
│   ├── ai-audit-report.md                     # mandatory AI Audit Report appendix
│   ├── ai-critique.md                         # mandatory 200–300 word AI critique
│   ├── main-report.md                         # consolidated automation report
│   └── hw02-reference/                        # HW02 test-case designs & bug docs (source material)
├── test-data/          # external JSON arrays consumed by the specs (never hardcoded inline)
├── tests/
│   ├── login.spec.ts, login-api.spec.ts
│   ├── cart.spec.ts, cart-api.spec.ts
│   ├── dashboard.spec.ts, dashboard-api.spec.ts
│   └── utils/{api,db}.ts                      # REST + direct-SQLite setup/oracle helpers
├── scripts/{inject-student-id,run-matrix}.js
├── reports/<feature>/<browser>/                # 9 labeled HTML reports
├── playwright.config.ts, package.json, tsconfig.json
└── README.md
```

## 5. Test case selection & data-driven design

Task 1 asks to *convert* designed test cases into automation, not invent them from scratch: this
repo's HW02 branch (`HW2-Khoa`) already contains 80/89/46 manually-designed test-case documents
for FR-02/FR-07/FR-13 respectively (copied for reference into `docs/hw02-reference/`), plus 43
confirmed bugs. Each feature's spec was built by selecting a representative, non-redundant subset
of that pool (see `docs/ai-review-*.md` §1 for the selection rationale per feature) — prioritizing
full coverage of every already-known bug plus enough additional positive/negative/boundary cases
to exceed the 12-per-feature minimum by a wide margin.

All test data lives in external `.json` arrays under `test-data/`, loaded and validated at runtime
(rejects missing files, non-array content, duplicate `caseId`s, and under-sized data sets). Each
suite uses well over the required minimum of 3 distinct assertion patterns — see the "Assertion
pattern inventory" section of each `ai-review-*.md`.

## 6. Known limitations / cases not automated

Documented per feature with rationale in `docs/ai-review-*.md` §4 (Login), §C (Cart's testability
note), and throughout the Dashboard review — e.g. `input[type=number]` rejecting non-numeric
`fill()` values, rate-limiting/DoS cases requiring a control that doesn't exist yet, and JWT
`alg:none` forgery being out of this feature's scope.

## 7. AI Audit Report & Critique

Mandatory appendices: [`docs/ai-audit-report.md`](docs/ai-audit-report.md) (tool/date/prompt/output
log per interaction) and [`docs/ai-critique.md`](docs/ai-critique.md) (200–300 word reflection).

## 8. Self-assessment table

| No. | Criteria | Grade | Self-Assessed Grade |
|---|---|---:|---:|
| 1 | Task 1 — Feature A (FR-02 Login) | 25 | 23 |
| 1 | Task 1 — Feature B (FR-07 Cart) | 25 | 24 |
| 1 | Task 1 — Feature C (FR-13 Dashboard) | 25 | 24 |
| 2 | Task 2 — Demo video | 15 | _recorded and linked above — content not reviewed by the AI, self-grade pending your own check against_ `docs/demo-video-script.md` |
| 3 | Agent Skills | 10 | 7 |
| | **Total** | **100** | |

**Rationale:** Task 1 is complete and verified (400 cases, 1200 browser runs, identical results
across all 3 engines, 49 real bugs found including 1 CRITICAL privilege-escalation vulnerability
and 5 High-severity security issues (plaintext-password leak, unreachable duplicate-email ghost
accounts, zero-validation empty passwords, a brute-forceable password-reset token, and an
unauthenticated order-viewing IDOR), data-driven + ≥3 assertion patterns per suite, every report
labeled, all 19 new bugs filed as real GitHub Issues with evidence). Dashboard and Cart were both
deepened in a second review pass after explicit feedback that the first pass was too thin —
Dashboard grew from 32 to 46 cases (closing a previously-skipped known bug, `BUG-FR13-C-03`) and
Cart from 63 to 72 (closing an i18n/XSS/scale gap and finding a new cross-tab-sync bug). A third
pass then closed Login's own remaining gap (session persistence/logout/forged-token handling,
63→69) and added a handful more targeted cases to Cart and Dashboard (48). A fourth pass
deliberately read `/api/register` and `/api/forgot-password` — the one part of FR-02's own
authentication surface no earlier case had ever exercised — and found 3 more High-severity bugs
there (69→72). A fifth pass repeated the same technique against Cart's
`/api/checkout`/`/api/orders/:id` endpoints and found an unauthenticated-order-view IDOR plus a
broken cancel-state guard (72→77 Cart cases). A sixth pass found the assignment's most severe
bug — a privilege-escalation flaw in `PUT /api/users/me` — plus one more checkout-validation gap,
and grew the suite to 250 cases. A seventh and final pass, run per an explicit request to reach
400 cases suite-wide, added 150 more boundary/robustness cases reusing already-proven
parameterized shapes with essentially zero new spec code (Login 90→137, Cart 92→142, Dashboard
68→121); it found no further bugs but did catch and fix two of its own test-design mistakes along
the way (a NUL-byte JSON corruption, and an `add-with-quantity` case that asserted the wrong
outcome for inputs that actually parse as valid numbers) — see `ai-review-login.md` §3e and
`ai-review-cart.md` §3f. All totals verified identically across all 3 browsers. The one point
still held back per feature
reflects that a small number of individual cases remain deliberately un-padded (e.g.
`TC-CART-020`/`021` are untestable through the real UI control, documented rather than forced) —
see each `ai-review-*.md`
§4/§C. Both demo videos (automation run, Agent Skill) are recorded and linked in §1 above; the AI
has not reviewed their content, so double-check each against `docs/demo-video-script.md`'s required
talking points (≥5 min, Vietnamese narration, multi-browser run + report walkthrough, narrating a
real fix, face-cam/`whoami` per Section 11's anti-cheat rule) before finalizing the grade above.

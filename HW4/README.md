# HW04 — Automation Testing (Playwright + TypeScript) — EShop SUT

**Student ID:** `23127207` · **Course:** Software Testing · **Branch:** `HW4-Khoa`

Automates the same 3 web features selected in HW02 (one per pool), following the AI-first
7-step workflow (Analyze → Design/Review → Model data → Map automation → Generate →
Verify/repair) documented step by step in [`docs/prompt-log.md`](docs/prompt-log.md).

| Pool | Feature | Spec files | Data files | Cases |
|---|---|---|---|---:|
| A | FR-02 — Login & Account Lockout | `tests/login.spec.ts`, `tests/login-api.spec.ts` | `test-data/login-{cases,ui-cases,lockout-cases,api-cases}.json` | 63 |
| B | FR-07 — Shopping Cart | `tests/cart.spec.ts`, `tests/cart-api.spec.ts` | `test-data/cart-{ui,edge,api}-cases.json` | 63 |
| C | FR-13 — Admin Dashboard | `tests/dashboard.spec.ts`, `tests/dashboard-api.spec.ts` | `test-data/dashboard-{data,api}-cases.json` | 32 |

## 1. Test summary (execution evidence)

All numbers below are from real, verified runs on Chromium, Firefox, and WebKit — **each browser
produced the identical pass/fail count per feature** (see `docs/ai-review-*.md` for how that
consistency was achieved, including two test-isolation bugs found and fixed along the way).

| Feature | Cases | Browser runs | Passed | Failed | Known bugs reproduced | New bugs found |
|---|---:|---:|---:|---:|---:|---:|
| FR-02 Login | 63 | 189 | 46 | 17 | 12 | 4 |
| FR-07 Cart | 63 | 189 | 29 | 34 | 15 | 3 |
| FR-13 Dashboard | 32 | 96 | 15 | 17 | 2 | 3 |
| **Total** | **158** | **474** | **90** | **68** | **29** | **10** |

- **Features automated:** 3 (FR-02 Pool A, FR-07 Pool B, FR-13 Pool C).
- **Total bugs found by this automation:** 39 (29 already known from HW02, confirmed still
  present; 10 newly discovered — including 1 **High**-severity security issue: the login API
  leaks the user's plaintext password in its response body).
- **Demo video:** _[fill in the unlisted YouTube link once recorded — see_
  `docs/demo-video-script.md` _for the required talking points]_.

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
| 1 | Task 1 — Feature B (FR-07 Cart) | 25 | 23 |
| 1 | Task 1 — Feature C (FR-13 Dashboard) | 25 | 22 |
| 2 | Task 2 — Demo video | 15 | _pending — record before submission_ |
| 3 | Agent Skills | 10 | 7 |
| | **Total** | **100** | |

**Rationale:** Task 1 is complete and verified (158 cases, 474 browser runs, identical results
across all 3 engines, 39 real bugs found including a High-severity plaintext-password leak,
data-driven + ≥3 assertion patterns per suite, every report labeled). Points held back reflect
gaps this document is honest about: Dashboard's suite (32 cases) is smaller than Login/Cart because
the admin dashboard UI genuinely only exposes two metrics — padding it further would violate
"quality over completion." The demo video has not been recorded yet (requires the student's own
voice/face-cam per Section 11's anti-cheat rule). The Agent Skill
(`.agents/skills/playwright-skill/playwright-skill.md`) predates this run and needs a final pass
to reflect the actual implemented workflow (see Phase 3 of the working plan) before it is submitted
as a finished deliverable.

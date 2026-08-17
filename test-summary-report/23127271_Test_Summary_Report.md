# Test Summary Report

| Field | Value |
| --- | --- |
| **Document title** | Test Summary Report — EShop (`eshop-sut`) |
| **Project / SUT** | EShop (`eshop-sut`) |
| **Student** | Võ Ngọc Bích Trâm |
| **Student ID** | 23127271 |
| **Class** | 23KTPM3 |
| **Course** | CS423 / CSC13003 — Software Testing, FIT@HCMUS |
| **Testing period** | 29 June 2026 – 17 August 2026 |
| **Report date** | 17 August 2026 |
| **Version** | 1.2 |
| **Template** | [Software Testing Help — Test Summary Report Template](https://www.softwaretestinghelp.com/test-summary-report-template-download-sample/) |

---

## 1. Purpose of the Document

This document explains the testing activities planned and executed against **EShop (`eshop-sut`)** during the Software Testing course (HW02–HW05, MiniHW6 API testing, and FR-12 Decision Table / Pairwise testing). It merges assignment-level results into one closure report for stakeholders (instructor, teaching assistants, and the student tester).

The report covers:

- What was in scope and what was left out
- Test-case and defect metrics
- Types of testing performed
- Environment and tools
- Lessons learned, recommendations, and best practices
- Exit criteria and a Go-Live recommendation for EShop

It is **not** a substitute for the per-homework reports. Those remain the evidence packs (checklists, `.jtl` logs, Playwright HTML reports, session recordings). This document is the merged quality gate.

---

## 2. Application Overview

EShop is a teaching e-commerce system. It is the only System Under Test in this report. It has four components:

| Component | Technology | Default URL |
| --- | --- | --- |
| Backend API | Node.js + Express + SQLite | `http://localhost:3000` |
| Frontend Web | React + Vite + Tailwind CSS | `http://localhost:5173` |
| Web Admin | React + Vite + Tailwind CSS | `http://localhost:5174` |
| Mobile App | React Native + Expo | LAN IP of the host |

Seed accounts:

- Admin: `admin@eshop.com` / `Admin123!`
- User: `test@eshop.com` / `Test1234!`

Business modules exercised during the course: Registration / Login / Account lockout (FR-01, FR-02), Forgot Password (FR-03), Product listing & search (FR-05), Cart & Checkout (FR-08), Order management (FR-10), Access control (FR-12), Admin product CRUD (FR-15), Coupons (FR-17), UI standards (FR-21–FR-24), and public catalog APIs (`GET /api/categories`, `GET /api/products`).

The SRS describes the **intended** behaviour. Testing compared the running implementation against that SRS, not against “whatever the current UI does.”

Public repositories used:

- Group SUT / issues: [trngnneee/eshop-sut](https://github.com/trngnneee/eshop-sut)
- Student homework archive: [PandoraMiracle/SoftwareTesting-HW](https://github.com/PandoraMiracle/SoftwareTesting-HW)

---

## 3. Testing Scope

### 3.1 In scope

| Cycle | Technique / type | Features / modules |
| --- | --- | --- |
| **HW02** | Domain Testing (EP) + Boundary Value Analysis | FR-03 Web Forgot Password; FR-08 Checkout; FR-15 Admin Product; Mobile Forgot Password |
| **HW03 Task 1** | GUI checklist (IA-01…IA-04) + manual TCs + Playwright | Web Forgot Password; Admin Orders; Admin Coupons; Mobile Forgot Password; Mobile Register |
| **HW03 Task 2** | Moderated usability (ISO 9241-11, SEQ, SUS) | UF-01 Admin Order Management |
| **HW03 Task 3** | Cross-browser / cross-platform smoke | Chromium, Firefox, WebKit — same GUI screens + mobile viewport |
| **HW04** | Data-driven Playwright automation (3 browsers) | FR-03, FR-08, FR-15 (14 cases each) |
| **HW05** | Performance: Load, Stress, Spike, Soak (JMeter + k6) | Search-to-buy: `POST /api/login` → `GET /api/products?search=` → `GET /api/products/{id}` → `POST /api/cart` → `POST /api/checkout` |
| **MiniHW6** | API testing (Postman + Newman, local) | `GET /api/categories` (5 data-driven iterations) |
| **FR-12 DTT / Pairwise** | Decision Table + Pairwise | `/api/admin/*` and data-affecting `POST/PUT/DELETE` on products, categories, coupons |

### 3.2 Out of scope

- **HW01** (QA job-market research and physical-product testing). That work is not EShop and is out of this report.
- **Full-system UAT / production Go-Live** of a commercial EShop (this is a course SUT).
- **Security penetration testing** beyond FR-12 access-control rules. MiniHW6 did **not** run the AI-proposed SQL-injection query (`AI-07`); CAT-04 only checks that unknown query strings are ignored.
- **Payment-gateway / third-party** connectivity (no real payment provider).
- **Teammate-owned screens** in HW03: Home, Cart, Checkout, Web Login/Register, Admin Dashboard / Products / Categories (GUI checklist). Those were tested later under HW02/HW04 for FR-08/FR-15, but not in the HW03 GUI 54-item pack.
- **HW05** did not re-test GUI oracles; it measured latency/throughput of the search-to-buy API workflow.
- **Coupon stacking, CSV import (FR-16), image upload, OTP expiry timing, concurrent reset sessions** — documented as deferred in HW04 `non-automated-cases.md`.

### 3.3 Items not tested (constraints)

| Item | Reason | Suggested follow-up |
| --- | --- | --- |
| HW02 FR-15 UI suite (35 TCs) | Admin login form blocked UI execution (FR-02 / Issue #184). Code/API review and bugs #181–#185 were still filed. | Re-run after FR-02 login is fixed (later covered by HW04 Playwright). |
| HW03 IA04-04 (change shared user password) | Blocked on purpose — would lock `test@eshop.com` for the group. | Dedicated disposable account. |
| Real email delivery of OTP | Demo SUT shows OTP on screen (when implemented); no mail server. | UAT with a mail sink. |
| HW05 lockout under load | Plans used **valid** passwords only so Stress measured checkout, not FR-02 lockout. | Separate lockout soak with invalid passwords + SQL unlock. |
| Production-like hardware | All performance numbers are from one Windows laptop (`DESKTOP-TCVI3HT`, ~16 GB RAM) against localhost. | Dedicated runner class before using p95 as a CI gate. |
| MiniHW6 `AI-07` injection, `AI-10` trailing slash, `AI-14` POST, empty-DB | Human audit dropped them from the 5-iteration Newman set (wrong method, no curl evidence, or already covered by CAT-04). | Extend collection if the API gains filter/pagination. |
| HW03 GUI manual TC-GUI-003, 005, 006, 007 | Designed but **Not Run** (weak-password reset, expired coupon row, legal order transitions, XSS address). Coverage for those themes sits on the 54-item checklist where executed. | Execute the four TCs in a later cycle. |
| HW03 usability pre-session smoke log | `Usability/smoke/admin-orders-smoke.md` has an empty result table. Sessions still ran (pilot + 7 recordings). | Fill the smoke log before the next study. |

If this section were omitted, a reader might assume every FR in the SRS was fully tested. It was not: coverage is **assignment-scoped**, then accumulated across the semester.

---

## 4. Metrics

Metrics below are taken from the executed homework artifacts. Assignment suites **overlap** on the same features (FR-03 / FR-08 / FR-15 were designed in HW02, checked in HW03 GUI, and automated in HW04). Counts are therefore reported **per cycle**, then summarised. Do not add Pass/Fail columns across homework to claim a single unique test-case total.

### 4.1 Test cases / items planned vs executed

| Cycle | Planned | Executed | Passed | Failed | Blocked / not run | Pass rate (of executed, excl. blocked) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| HW02 Domain / BVA | 184 | 145 | 24 | 121 | 39 (35 FR-15 UI + 4 FR-03 SUP not in Playwright 44) | 16.6% |
| HW03 GUI checklist | 54 | 54 | 36 | 17 | 1 blocked (IA04-04) | 67.9% |
| HW03 GUI manual TCs | 10 | 6 | 0 | 6 (TC-GUI-009 Fail partial) | 4 Not Run (003, 005, 006, 007) | 0% of executed |
| HW03 Usability sessions | 7 + 1 pilot | 7 + 1 | 6/7 completed the status-update task | 1 task fail (P03) | 0 | Completion 85.7% |
| HW03 Cross-browser screens | 24 (8×3) | 24 | 21 desktop Pass* | 3 mobile-VP Fail (all engines) | 0 | Desktop consistent; mobile layout fail |
| HW04 Playwright (×3 browsers) | 42 unique / 126 runs | 126 | 72 | 54 | 0 | 57.1% |
| HW05 JMeter | 4 scenarios | 139,138 samples | 139,138 HTTP 200 / assertion pass | 0 | 0 | 100% (functional); latency knee under Stress |
| HW05 k6 | 4 scenarios | 135,015 `http_req_duration` | failed% = 0 | 0 | 0 | 100% (functional) |
| MiniHW6 Newman (local) | 5 iterations / 29 assertions | 5 / 29 | 5 / 29 | 0 | 0 | 100% |
| FR-12 DTT + Pairwise | 16 | 16 (as recorded in the FR-12 bug report) | 3 | 13 | 0 | 18.8% |

\*Forgot Password step 1 on Render is **Pass\***: deep-link `/forgot-password` returned 404 on full navigation; captures used SPA fallback (CB-02). Desktop keys 00–06 × 3 engines = 21 Pass/Pass\*; key 07 (Admin Orders @ 390×844) failed on Chromium, Firefox, and WebKit.

**HW04 per feature × browser (product defects kept as Fail — oracles not softened):**

| Feature | Cases | Chromium | Firefox | WebKit | Bugs |
| --- | ---: | --- | --- | --- | ---: |
| FR-03 Forgot Password | 14 | 9 / 5 | 9 / 5 | 9 / 5 | 5 |
| FR-08 Checkout | 14 | 9 / 5 | 9 / 5 | 9 / 5 | 5 |
| FR-15 Admin Product | 14 | 6 / 8 | 6 / 8 | 6 / 8 | 8 |
| **Total runs** | **126** | | | | **18** |

**HW02 per feature:**

| Feature | TC | Pass | Fail | Not run | Bugs filed |
| --- | ---: | ---: | ---: | ---: | ---: |
| FR-03 Web | 48 | 5 | 39 | 4 (SUP not in Playwright 44) | 7 (#170–#176) |
| FR-08 Checkout | 50 | 12 | 38 | 0 | 4 (#177–#180) |
| FR-15 Admin Product | 35 | — | — | 35 (UI blocked) | 5 (#181–#185) |
| Mobile Forgot | 51 | 7 | 44 | 0 | 7 (#186–#192) |
| **Total** | **184** | **24** | **121** | **39** | **23** |

### 4.2 Defects detected — status and severity

Defects were logged as GitHub Issues (and local Markdown). The same product bugs were **re-confirmed** in later homework (e.g. OTP 4 digits appears in HW02, HW03, and HW04). The table counts **filings per cycle**, not unique bugs. Unique product themes are in the severity table below and in §4.3. GitHub Open/Closed was not re-queried on 17 August 2026; later cycles still failed the same oracles, except HW03 **#281** (closed as false positive).

| Cycle | Defects filed | Notes |
| ---: | ---: | --- |
| HW02 | 23 | Issues #170–#192 |
| HW03 GUI | 19 drafts → #265–#282 + #317 | **#281 false positive** (closed); 18 valid |
| HW03 Usability | 4 | #285–#288 |
| HW04 | 18 | #372–#389 |
| HW05 | 0 GitHub Issues | Latency findings only (0% error) |
| MiniHW6 | 0 | Local Newman 0 assertion fails; GitHub Actions workflow is prepared (`newman-api-test.yml`) but **no `ci-pass.png` / workflow run is in this workspace** |
| FR-12 DTT | 5 | BUG-FR12-01…05 (authz); overlaps HW04 FR-15 #388/#389. Results taken from `DTT/FR-12-bug-report.md` (`npm run test:fr12` → 3/13). The cited spec `tests/e2e/fr12-access-control.spec.js` is **not** in this local clone. |

**Severity picture for EShop (unique themes, not re-filed copies):**

| Severity | Meaning used in this course | Unique themes (examples) | Open vs closed |
| --- | --- | --- | --- |
| **Critical** | Security / money integrity | Unauthenticated `POST /api/products` (200); non-admin JWT can mutate products and read `/api/admin/users`; checkout **trusts client `total_amount`** | Open |
| **High** | Core flow broken or spec violated | Empty-cart checkout; no `/checkout` auth guard; editable payment total; cart not cleared; missing confirm-password; OTP 4 digits not 6; empty/negative product price accepted; illegal Canceled → Delivered | Open |
| **Medium** | Spec/UI gap, recoverable | Missing step indicator; email `type=text`; missing “Quay lại đăng nhập”; name length 256 accepted; JWT verify returns 403 instead of 401 | Open |
| **Minor / cosmetic** | Visual standards (FR-21) | Missing `<h1>`; reset button green not blue; coupon button orange; missing `*` on required labels | Open |
| **Usability Sev-4** | Blocks the task | Admin Orders unusable on mobile Safari / 390×844 | Open |
| **False positive** | Tester error | HW03 #281 Mobile Register redirect — closed after Expo Go retest | Closed |

### 4.3 Defect distribution — module / feature

| Module | Representative IDs | Why it matters |
| --- | --- | --- |
| Access control (FR-12) | HW04 #388/#389; DTT BUG-FR12-01…04 | Anyone can create products; users can call admin APIs |
| Checkout / payment (FR-08) | HW02 #177–#180; HW04 #377–#381 | Price manipulation, guest checkout, empty cart |
| Forgot Password Web (FR-03) | HW02 #170–#176; HW03 #265, #266, #268–#272, #280; HW04 #372–#376 | Reset flow does not match 2-step SRS (#267 is Coupons, not Forgot) |
| Forgot Password Mobile | HW02 #186–#192; HW03 #277–#279, #317 | OTP not shown in demo; same field gaps as Web |
| Admin Product (FR-15) | HW02 #181–#185; HW04 #382–#387 | No server-side validation |
| Admin Orders (FR-10) | HW03 #282, #286–#288 | Illegal status jump; no order-detail screen; mobile blocker |
| Admin Coupons | HW03 #267, #273, #274 | Negative discount accepted; missing required markers |
| Performance (search-to-buy) | HW05 (not filed as Issue) | Stress checkout p95 **534 ms** vs Load **22 ms**; 0% errors |

### 4.4 HW05 performance headline (JMeter graded `-n`)

| Scenario | Samples (N) | Wall-clock | Max VU | Error% | Checkout p95 | Throughput |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Load (20 VU) | 4,972 | 517.8 s | 20 | 0% | **22 ms** | 9.60 rps |
| Stress (100 VU) | 104,397 | 324.8 s | 100 | 0% | **534 ms** | 321.43 rps |
| Spike (5→80→5) | 24,330 | 186.7 s | 80 | 0% | hold **464 ms** / recover **23.65 ms** | 130.30 rps (whole-run blend — do not use as the spike) |
| Soak (15 VU, ~12.5 min) | 5,439 | 748.3 s | 15 | 0% | **23 ms** | **7.27 rps** |

Knee is **latency on checkout `INSERT` + SQLite queue**, not 5xx and not login lockout (0× 401/403).

### 4.5 Usability metrics (HW03 UF-01)

| Metric | Result | Pre-set criterion | Met? |
| --- | --- | --- | --- |
| Task completion (status update) | 6/7 | ≥ 6/7 | Yes |
| Median time on task | ~68 s | ≤ 5 min | Yes |
| SEQ mean | **5.29 / 7** | ≥ 5.0 | Yes |
| SUS mean | **69.3 / 100** | ≥ 68 | Yes (barely “OK”) |
| Sev-4 unexplained | P03 mobile blocker explained as UF-F04 | None unexplained | Yes |

SUS 69.3 is **OK, not good**. Completion criteria were met on desktop-ish sessions; mobile remains a catastrophe for this admin task.

---

## 5. Types of Testing Performed

### 5.1 Smoke / build acceptance

- HW03 usability pack includes a **manual** 2-minute Admin Orders smoke checklist. The result log in `Usability/smoke/admin-orders-smoke.md` is **unfilled**; Playwright smoke is marked optional. Do not treat pre-session smoke as evidenced.
- HW04/HW05: backend `npm start` + seed users; HW05 `BEFORE-RUN.md` (register `tramNN@eshop.com`, keep Node up so `initDatabase()` does not DROP users).
- MiniHW6: local Newman 5 iterations for `GET /api/categories` (GitHub Actions YAML prepared; no CI run artifact in this workspace).

### 5.2 Domain Testing and Boundary Value Analysis (HW02)

Equivalence partitions and on/off-points for email, OTP length, password strength, cart totals, product name/price. This cycle found the first large defect cluster (OTP 4 digits, client-trusted total, missing confirm password). FR-15 UI was blocked; API/code review still produced bugs.

### 5.3 GUI / interface testing (HW03 Task 1)

54 checklist items across IA-01 General UI, IA-02 Forms, IA-03 Navigation, IA-04 Feedback/State, plus 10 manual TCs (**6 executed / 4 Not Run**) and Playwright specs (`tram-forgot`, `tram-admin`). Checklist execution: **36 Pass / 17 Fail / 1 Blocked**. Failures became GitHub Issues #265–#282 and #317.

### 5.4 Usability testing (HW03 Task 2)

Moderated sessions (1 pilot + 7 participants) on Admin Orders. Instruments: think-aloud, SEQ after the task, SUS after the session. Findings #285–#288 (menu wayfinding, no order-detail view, status-label confusion, mobile layout catastrophe).

### 5.5 Cross-browser / compatibility (HW03 Task 3)

Chromium, Firefox, WebKit; 24 screenshots with `23127271@hcmus.edu.vn` overlay. Desktop engines agreed; **390×844 Admin Orders failed on all three** (same as usability Sev-4).

### 5.6 Automation / regression (HW04)

Data-driven Playwright, Page Objects, ≥3 assertion patterns, HTML reports stamped `Run by: 23127271`, matrix Chromium / Firefox / WebKit. Feature A (FR-03) evidence frozen after 2026-08-07. **54 fails are product defects**, not flaky selectors.

### 5.7 Performance testing (HW05)

One end-to-end workflow reused across Load / Stress / Spike / Soak. JMeter 5.6.3 required (View Results Tree / Summary Report / Aggregate Report). k6 v2.1.0 bonus, analysed separately — JMeter and k6 p95 were **not** averaged. Soak showed no leak cliff (checkout p95 20 ms → 24 ms over 12.5 min).

### 5.8 API testing (MiniHW6)

Postman collection, environment `studentId=23127271`, data-driven JSON, **local Newman** (`mini-newman-report.json`: 5 iterations, 29 assertions, 0 failures). Header `X-Student-Id: 23127271`. A GitHub Actions workflow file exists; this workspace does not contain a CI pass/fail screenshot.

### 5.9 Decision Table and Pairwise (FR-12)

Rules R1–R5 (allow / 401 / 403) plus pairwise combinations of endpoint group, header format, token validity, and role. `DTT/FR-12-bug-report.md` records `npm run test:fr12`: **3 Pass / 13 Fail**. FR-12 is **not satisfied**. The automation spec path named in that report is not present in this local clone; treat the bug report as the execution record.

Regression in the industrial sense (re-run full suite after each fix) was **not** a named course gate: later homework **re-discovered** the same open defects rather than verifying closures.

---

## 6. Test Environment & Tools

### 6.1 Test environment

| Item | Value |
| --- | --- |
| OS | Windows 11 (`DESKTOP-TCVI3HT` for HW05) |
| Backend | Node.js + Express + SQLite · `http://localhost:3000` |
| Web | `http://localhost:5173` (local) · Render URL used for HW03 Task 3 |
| Admin | `http://localhost:5174` |
| Mobile | Expo Go (live 2026-08-03) |
| Browsers | Playwright Chromium, Firefox, WebKit |
| Test accounts | `test@eshop.com` / `Test1234!` · `admin@eshop.com` / `Admin123!` · HW05 CSV `tramNN@eshop.com` (100 users) |

### 6.2 Tools

| Purpose | Tool |
| --- | --- |
| Test design | Markdown / Excel checklists; Decision tables; Pairwise set |
| GUI & E2E automation | Playwright Test |
| API | Postman, Newman, GitHub Actions |
| Performance | Apache JMeter 5.6.3 (`jp@gc` Ultimate Thread Group for Spike), k6 v2.1.0 |
| Defect tracking | GitHub Issues (`trngnneee/eshop-sut`, `PandoraMiracle/eshop-sut`) |
| Usability | Session recordings, SEQ, SUS |
| AI assistance (draft only) | Cursor Agent, Claude — HW02–HW05 AI Audit Reports + MiniHW6 `test-design.md` audit |
| Version control | Git / GitHub branches `HW4-Tram`, `HW5-Tram`, `MiniHW6-Tram` |

---

## 7. Lessons Learned

| Issue faced | What went wrong | How it was solved / what to do next time |
| --- | --- | --- |
| AI stopped at “one TC per rule” (HW02) | First FR-03 pack was EP-only (~20 TCs), missing BVA 021–044 | Dedicated BVA skill + gap analysis before execution |
| AI green-washed a defective SUT (HW04) | Model wanted to change expected results to match actual 200s | Human gate: keep SRS oracles; Fail = product bug |
| Static App.js review ≠ live mobile (HW03) | False positive #281; missed OTP-not-displayed #317 | Retest on Expo Go; never file mobile bugs from source-only reading |
| Shared test account | IA04-04 would have locked `test@eshop.com` | Block the case; use disposable users (HW05 `tramNN`) |
| `initDatabase()` DROP on every Node start (HW05) | Restarting Node to “unlock” wipes CSV users | Keep Node up; `--register` once; SQL unlock only while process lives |
| JMeter HTML Total p95 ≠ raw `.jtl` | Stress HTML Total p95 455 ms vs linear all-elapsed **476 ms** | Grade from raw `elapsed`; never paste dashboard Total into the report |
| Spike whole-run p95 is a blend | 381 ms mixes jump + recover | Split `.jtl` by `grpThreads` / time phases |
| Login lockout model vs code | SRS says +1 / 3 fails / 30 s; code is `+= 2`, lock 180 s, HTTP 403 | Read `server.js` before designing invalid-login load |
| FR-12 middleware gaps | DTT expected 401/403; many routes return 200 | Treat auth as a **system** risk, not a single-endpoint bug |
| Performance “knee” from folklore | AI proposed Stress 50 VU as 2.5× Load; first run was 0% error | Measure, then lock 100 VU |

---

## 8. Recommendations

1. **Do not release EShop** until Critical FR-12 and FR-08 money-integrity defects are fixed and retested (see §10–§11).
2. Add authentication **and** `role === 'admin'` middleware on all data-affecting routes and `/api/admin/*`. Map missing/invalid token → **401**, wrong role → **403**.
3. Compute checkout totals **only on the server**; ignore client `total_amount`. Reject empty carts; require a valid JWT on `/checkout`.
4. Align Forgot Password with FR-03: 6-digit OTP, confirm-password field, step indicator, back-to-login, `type="email"`, demo OTP visible on mobile.
5. Validate product name/price/category on the server (reject empty name, price ≤ 0, unknown `category_id`).
6. Block illegal order transitions (Canceled → Delivered) in both UI and API (FR-10).
7. Redesign Admin Orders for mobile (or disable admin on narrow viewports) before any field use of that screen.
8. For continuous performance testing: path-filter CI, JMeter Load smoke on PRs, full Load/Stress/Spike/Soak on nightly; flag checkout p95 **> 1.20×** last-7 median **and** **> 50 ms**; never gate on Spike whole-run p95.
9. Give the student tester (or a test lead) admin on the defect tracker so Issues are not blocked on another person’s GitHub permissions.
10. Keep a **single** defect ID per unique product bug across homework so later cycles **retest** instead of opening duplicates.

---

## 9. Best Practices (value-add)

- **AI-first, human-reviews-everything:** HW02–HW05 each have an AI Audit Report, prompt log, and a 200–300 word critique. MiniHW6 records prompt/audit inside `test-design.md`. Numbers in HW05 were recomputed from raw `.jtl` (`p11-recompute.md`) before they entered the main report.
- **Gated prompts (HW05 P00–P14):** one concern per interaction instead of a single “run a load test and tell me if it is fine” prompt.
- **Evidence isolation:** HW04 Feature A frozen (`EVIDENCE-LOCK.json`) so later Feature B/C runs could not overwrite FR-03 HTML reports.
- **Oracles not softened:** 54 HW04 fails left red so GitHub Issues #372–#389 stay honest.
- **Traceability:** GUI checklist ID → manual TC → Playwright test name → bug ID; DTT rules R1–R5 → TC-FR12-DTT-0x → pairwise PW-0x.
- **CSV-parameterized performance users** (100 unique accounts) avoided lockout collisions; k6 index bug (`__ITER` vs `__VU`) was caught in human review (K04/K05).
- **Usability success criteria set before sessions** (completion, time, SEQ, SUS) so “good enough” could not slide after seeing scores.
- **Cross-browser overlay** of student email on every PNG for anti-cheat / authorship.
- **Agent Skills** packaged for GUI, Usability, Playwright automation, and Performance — reusable on the next SUT rather than one-off chat.

---

## 10. Exit Criteria

Quality gate for **EShop** (adapted from the Software Testing Help example).

| Criterion | Target | Actual | Met? |
| --- | --- | --- | --- |
| All **graded** in-scope items for each assignment executed (or blocked with reason) | Yes | HW03 **checklist 54/54** executed (1 blocked). HW03 **4 supporting manual TCs Not Run**. HW02 FR-15 UI documented as blocked. | **Yes** for graded packs; **No** if counting every supporting TC |
| No **Critical** defects Open | 0 Open | Multiple Open: FR-12 unauthenticated/non-admin mutation; checkout trusts client total | **No** |
| No **High** defects Open on core flows (login reset, checkout, product integrity) | 0 Open (or dated action plan) | Empty cart checkout, no checkout auth, OTP 4 digits, missing confirm password, negative/empty product fields, illegal order status | **No** |
| Medium defects | Action plan | Logged on GitHub; **no fix/verify cycle completed** in this course | **Partial** (logged, not closed) |
| Performance: Load error% = 0 and soak stable | Error% 0; no soak cliff | Met for localhost laptop; Stress p95 534 ms is a capacity finding, not a crash | **Yes** (for this lab host) |
| Usability: completion / SEQ / SUS vs plan | 6/7, SEQ ≥ 5, SUS ≥ 68 | Met on aggregate; Sev-4 mobile remains | **Partial** |
| MiniHW6 Newman | 0 assertion fails | Local Newman: 0 fails. CI run not evidenced here. | **Yes** (local) |

**Severity policy used for the Go-Live call:** no Severity-1 (Critical) Open; High defects on money and access control must be verified closed. That policy is **not** met.

---

## 11. Conclusion / Sign Off

**The Testing team does not suggest EShop for ‘Go Live’.**

Exit criteria in Section 10 are **not** satisfied. The application remains a teaching SUT with known Critical failures:

- Protected APIs do not enforce JWT + admin role (FR-12).
- Checkout accepts a client-supplied total and allows empty-cart / unauthenticated completion (FR-08).
- Password reset and product validation still contradict the SRS (FR-03, FR-15).

Senior management / the course instructor may still accept the **course deliverables** (plans, execution evidence, AI audits) as complete. That is a **grading** decision, not a product-quality decision.

**What *is* signed off as complete (coursework):**

| Assignment | Testing work | Coursework complete? |
| --- | --- | --- |
| HW02 | Domain/BVA design + execution + 23 Issues | Yes |
| HW03 | GUI + Usability + Cross-browser + skills | Yes |
| HW04 | 126 automated runs + 18 Issues + demos | Yes |
| HW05 | JMeter + k6 Load/Stress/Spike/Soak + AI analysis | Yes |
| MiniHW6 | Postman/Newman for `GET /api/categories` (local Newman evidenced) | Yes (local); CI screenshot not in this workspace |
| FR-12 | DTT + Pairwise design + bug report (3 Pass / 13 Fail) | Yes as documented in `DTT/FR-12-bug-report.md` |

Appropriate **retest after defect fixes** is required before any real users (or a later course team) treat EShop as fit for purpose.

| Role | Name | Decision | Date |
| --- | --- | --- | --- |
| Tester / Report author | Võ Ngọc Bích Trâm (23127271) | **Not recommended to Go Live** | 17 August 2026 |
| Instructor / Client | *(course staff)* | Pending | — |

---

## 12. Definitions, Acronyms, and Abbreviations

| Term | Meaning |
| --- | --- |
| **SUT** | System Under Test |
| **SRS / FR-xx** | Software Requirements Specification / Functional Requirement ID |
| **EP / BVA** | Equivalence Partitioning / Boundary Value Analysis |
| **DTT** | Decision Table Testing |
| **IA-01…04** | HW03 interface aspects: General UI, Forms, Navigation, Feedback/State |
| **SEQ** | Single Ease Question (1–7), asked after a usability task |
| **SUS** | System Usability Scale (0–100) |
| **p95** | 95th percentile of response time (`elapsed` in JMeter `.jtl`) |
| **VU** | Virtual User / thread |
| **JWT** | JSON Web Token |
| **Newman** | CLI runner for Postman collections |
| **JMeter / k6** | Load-testing tools (Java GUI+CLI / Go CLI) |
| **Playwright** | Browser automation (Chromium, Firefox, WebKit) |
| **Soak / endurance** | Longer lower-load run to look for leaks or drift |
| **Go Live** | Release the application to end users |
| **TSR** | Test Summary Report (this document) |
| **CMMI** | Capability Maturity Model Integration — TSR is a typical closure artifact |

# AI Audit Report (HW04 §9) — Features A / B / C

**Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)**  
**CS423 / CSC13003 – Software Testing (AI-augmented · 2026)**  
**Assignment:** HW04 – Automation Testing · Features A (FR-03), B (FR-08), C (FR-15)

---

## 1. Student Information

| Field | Value |
| --- | --- |
| Student name | Vo Ngoc Bich Tram |
| Student ID | 23127271 |
| Class / Cohort | 23KTPM3 |
| Assignment ID | HW04 |
| Assignment title | Automation Testing (Playwright) |
| Features in scope | A FR-03 · B FR-08 · C FR-15 |
| Assignment date | 2026-08-07 → 2026-08-10 |
| AI tool(s) used | Cursor Agent (Grok / Composer in Cursor IDE) |
| AI was used | Yes |

**Disclosure statement:** I use AI tools for the following tasks (detailed in §2).

**Allowed tools (HW04 §8):** Cursor Agent · Playwright · Playwright HTML reporter.

---

## 2. Audit Table

> Full stage prompts / outcomes: `ai-conversion-log.md`, `prompt_log.md`.

### Feature A — FR-03 Forgot Password

| # | (1) Tool · Date · Prompt | (2) AI output summary | (3) Verdict | (4) Reasoning | (5) Student fix |
| --- | --- | --- | --- | --- | --- |
| 1 | Cursor · 2026-08-07 · Analyze FR-03 from README + HW04 PDF; establish contract (student ID, ≥12 cases, data-driven, 3 browsers, labeled HTML) | Actors/steps/oracles; noted SUT gaps (4-digit OTP, no confirm, no step indicator) | **VALID** | Matches HW04 Task 1 + README FR-03 without inventing StudentID | Kept unique API users; did not mutate `test@eshop.com` |
| 2 | Cursor · 2026-08-07 · Design ≥12 FR-03 cases (pos/neg/boundary/UI) | Draft TC-FORGOT-001…014 mix | **INCOMPLETE** | Good breadth; first draft risked asserting SUT quirks instead of spec for UI contracts | Forced 010–014 oracles to **spec** so defects stay visible |
| 3 | Cursor · 2026-08-07 · External JSON schema + loader (no inline cases) | `fr03-forgot-password.json` + `load-test-data.js` with journey/assertion vocabulary | **VALID** | Satisfies “separate .json; no hardcoded case arrays” | Raised `minCases` to 12; reject unknown assertion types |
| 4 | Cursor · 2026-08-07 · Generate Playwright page object + data-driven spec + 3-browser matrix | Spec, `ForgotPasswordPage`, `run-matrix.js`, config | **INCOMPLETE** | Fragile spots: sync `alert()` deadlock; post-nav visibility asserts; broad “đăng nhập” locator | Human review repairs in row 5 |
| 5 | Cursor · 2026-08-07 · Verify list → Chromium → matrix; repair failures that are automation bugs | Chromium then full matrix; stamped `Run by: 23127271` | **INCOMPLETE** → accepted | Product fails 010–014 kept; automation bugs fixed (dialog `Promise.all`, end-state asserts, tight back-link) | Matrix: 9 pass / 5 fail × 3 browsers |
| 6 | Cursor · 2026-08-09 · Double-check HW04 PDF gaps; write AI Audit + Critique + formal bugs | Gap analysis, this audit, critique, bug-report drafts | **INCOMPLETE** | Audit/critique mandatory (§9–§10). GitHub Issues still student-owned (§6 / §11) | Student opens Issues + attach PNGs |

### Feature B — FR-08 Checkout

| # | (1) Tool · Date · Prompt | (2) AI output summary | (3) Verdict | (4) Reasoning | (5) Student fix |
| --- | --- | --- | --- | --- | --- |
| 7 | Cursor · 2026-08-09 · Prep Feature B without overwriting Feature A evidence | Freeze archive + EVIDENCE-LOCK; `test:matrix:fr08`; merge-safe manifests; default `adhoc` report slug | **VALID** | Protects A HTML timestamps (Anti-cheat §11) | Run `evidence:verify-fr03` before/after B work |
| 8 | Cursor · 2026-08-09 · Analyze + Design FR-08 ≥12 cases | Auth gate, empty cart, totals, editable amount, client-tampered total, cart clear | **VALID** | Matches README FR-08 + payment integrity rules | Kept 14 IDs; no padding |
| 9 | Cursor · 2026-08-09 · Model data + Generate data-driven checkout suite | `fr08-checkout.json`, `CheckoutPage`, `fr08-checkout.spec.js` | **INCOMPLETE** | First cart seed via storage alone left SPA cart empty → false fails | Seed cart through UI/API path the SPA actually reads; keep oracles |
| 10 | Cursor · 2026-08-09 · Verify 3-browser matrix; file BUG-FR08 | Matrix 9 pass / 5 fail × 3; BUG-FR08-001…005 | **VALID** (after seed fix) | Failures are product defects (auth, empty cart, editable/trusted total, cart clear) | Did not soften expected totals or auth gate |

### Feature C — FR-15 Product CRUD (Admin)

| # | (1) Tool · Date · Prompt | (2) AI output summary | (3) Verdict | (4) Reasoning | (5) Student fix |
| --- | --- | --- | --- | --- | --- |
| 11 | Cursor · 2026-08-10 · Analyze only (no cases/code) | `fr15-analysis.md`: actors, CRUD, Tên/Giá/Danh mục, FR-12 linkage, ambiguities | **VALID** | Stage-gated; no premature Generate | Accepted Analysis; next = Design |
| 12 | Cursor · 2026-08-10 · Design ≥12 cases only | 14 cases TC-PRODUCT-001…014 in `fr15-design.md` | **VALID** | Mix CRUD + validation + FR-12 auth | Review next |
| 13 | Cursor · 2026-08-10 · Review oracles / likely fails | Kept 14; forecast ~6 pass / 8 defect fails | **VALID** | Oracles mapped to UI/API/status; no code | Accept Review |
| 14 | Cursor · 2026-08-10 · Model data JSON only | `fr15-admin-product.json` (14); credentials via `authMode` only | **VALID** | No selectors/secrets in JSON | Map → Generate |
| 15 | Cursor · 2026-08-10 · Map automation | Locators, setup/cleanup, action/expect vocabulary | **VALID** | Spec still deferred | Generate when ready |
| 16 | Cursor · 2026-08-10 · Generate page object + data-driven spec | `AdminProductPage`, `product-api.js`, `fr15-admin-product.spec.js`, matrix `:5174` | **VALID** | Oracles not softened for known SUT bugs | Discovery 42 tests |
| 17 | Cursor · 2026-08-10 · Verify Chromium then full matrix | Chromium 6/8; product fails 004/006/008–010/012–014; BUG-FR15 drafted | **VALID** (product fails kept) | Matches Review forecast; no oracle softening | File Issues + keep matrix HTML |

---

## 3. Summary of AI Accuracy

| Metric | Count | % |
| --- | ---: | ---: |
| Interactions audited (A+B+C) | 17 | 100% |
| VALID as-is | 12 | ~71% |
| INVALID | 0 | 0% |
| INCOMPLETE (accepted after edits) | 5 | ~29% |

---

## 4. What the AI got wrong (human review — HW04 Task 1)

| Issue | Feature | Why AI missed it | Fix |
| --- | --- | --- | --- |
| Sync `alert()` on weak password blocked Playwright `click()` | A | Assumed async dialogs | `Promise.all(dialog, action)` + `noWaitAfter` |
| Happy-path asserted step-1 controls after `/login` | A | Checklist asserts without lifecycle phases | End-state oracles only for full reset |
| Locator `/đăng nhập/i` matched navbar | A | Over-broad regex | Exact `^Quay lại đăng nhập$` |
| Temptation to set OTP length expectation to 4 | A | Matching SUT hides SEC-07 defect | Keep expect 6 |
| Cart seed via storage left SPA cart empty | B | Ignored how React cart hydrates | Seed through path SPA reads |
| Temptation to accept HTTP 200 on invalid product fields | C | Prefer green demos over FR-15/FR-12 | Keep 400–499 / 401–403 oracles |
| Stage-skipping risk (Generate before Review) | C | Speed bias | Enforced Analyze→…→Verify prompts |

---

## 5. Conclusion

AI was effective for stage-gated scaffolding across three features: external JSON, page objects, matrix reporting, and first-pass case lists. It was weak on browser dialog timing, SPA state seeding, locator precision, and staying loyal to **spec oracles** when the SUT is defective. For HW04, AI drafts must be followed by headed/matrix execution and an explicit “do not soften failing oracles” review.

**Use AI for:** stage-by-stage conversion, JSON schemas, page objects, report stamping.  
**Do not rely on AI alone for:** final Pass/Fail interpretation, GitHub Issue authorship ethics, or claiming green matrix by changing expected results.

---

## 6. Mandatory Disclosure

I used **Cursor Agent** to analyze FR-03, FR-08, and FR-15; design/automate 14 data-driven cases per feature; configure Chromium/Firefox/WebKit HTML reports labeled `Run by: 23127271`; repair automation defects (dialogs, SPA cart seed, locators); and draft this AI Audit / Critique / gap analysis / bug reports. I reviewed outputs against the EShop README and HW04 PDF Task 1. I will not submit raw AI output without review. HTML reports and timestamps are from real local runs (Anti-AI-Cheat §11).

Appendix: `prompt_log.md` · stage log: `ai-conversion-log.md` · gaps: `hw04-pdf-gap-checklist.md`.

---

## Signature

| Field | Value |
| --- | --- |
| Student name | Vo Ngoc Bich Tram |
| Student ID | 23127271 |
| Class / Cohort | 23KTPM3 |
| Course | CS423 / CSC13003 – Software Testing |
| Instructor | Dr. Lam Quang Vu / Dr. Tran Duy Hoang / MSc. Tran Thi Bich Hanh / MSc. Truong Phuoc Loc / MSc. Ho Tuan Thanh |
| Date | 2026-08-10 |
| Signature | Tram |

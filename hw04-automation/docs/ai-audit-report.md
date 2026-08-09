# AI Audit Report (HW04 §9) — Feature A FR-03

**Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)**  
**CS423 / CSC13003 – Software Testing (AI-augmented · 2026)**  
**Assignment:** HW04 – Automation Testing · Feature A only

---

## 1. Student Information

| Field | Value |
| --- | --- |
| Student name | Vo Ngoc Bich Tram |
| Student ID | 23127271 |
| Class / Cohort | 23KTPM3 |
| Assignment ID | HW04 |
| Assignment title | Automation Testing (Playwright) |
| Feature in scope | Feature A — FR-03 Forgot Password (Web) |
| Assignment date | 2026-08-07 → 2026-08-09 |
| AI tool(s) used | Cursor Agent (Grok / Composer in Cursor IDE) |
| AI was used | Yes |

**Disclosure statement:** I use AI tools for the following tasks (detailed in §2).

**Allowed tools (HW04 §8):** Cursor Agent · Playwright · Playwright HTML reporter.

---

## 2. Audit Table

> Full stage prompts / outcomes: `ai-conversion-log.md`, `prompt_log.md`.

| # | (1) Tool · Date · Prompt | (2) AI output summary | (3) Verdict | (4) Reasoning | (5) Student fix |
| --- | --- | --- | --- | --- | --- |
| 1 | Cursor · 2026-08-07 · Analyze FR-03 from README + HW04 PDF; establish contract (student ID, ≥12 cases, data-driven, 3 browsers, labeled HTML) | Actors/steps/oracles; noted SUT gaps (4-digit OTP, no confirm, no step indicator) | **VALID** | Matches HW04 Task 1 + README FR-03 without inventing StudentID | Kept unique API users; did not mutate `test@eshop.com` |
| 2 | Cursor · 2026-08-07 · Design ≥12 FR-03 cases (pos/neg/boundary/UI) | Draft TC-FORGOT-001…014 mix | **INCOMPLETE** | Good breadth; first draft risked asserting SUT quirks instead of spec for UI contracts | Forced 010–014 oracles to **spec** so defects stay visible |
| 3 | Cursor · 2026-08-07 · External JSON schema + loader (no inline cases) | `fr03-forgot-password.json` + `load-test-data.js` with journey/assertion vocabulary | **VALID** | Satisfies “separate .json; no hardcoded case arrays” | Raised `minCases` to 12; reject unknown assertion types |
| 4 | Cursor · 2026-08-07 · Generate Playwright page object + data-driven spec + 3-browser matrix | Spec, `ForgotPasswordPage`, `run-matrix.js`, config | **INCOMPLETE** | Fragile spots: sync `alert()` deadlock; post-nav visibility asserts; broad “đăng nhập” locator | Human review repairs in row 5 |
| 5 | Cursor · 2026-08-07 · Verify list → Chromium → matrix; repair failures that are automation bugs | Chromium then full matrix; stamped `Run by: 23127271` | **INCOMPLETE** → accepted | Product fails 010–014 kept; automation bugs fixed (dialog `Promise.all`, end-state asserts, tight back-link) | Matrix: 9 pass / 5 fail × 3 browsers |
| 6 | Cursor · 2026-08-09 · Double-check HW04 PDF gaps; write AI Audit + Critique + formal bugs | Gap analysis, this audit, critique, bug-report drafts | **INCOMPLETE** | Audit/critique mandatory (§9–§10). GitHub Issues still student-owned (§6 / §11) | Student must open Issues + attach PNGs |

---

## 3. Summary of AI Accuracy

| Metric | Count | % |
| --- | ---: | ---: |
| Interactions audited (Feature A) | 6 | 100% |
| VALID as-is | 2 | ~33% |
| INVALID | 0 | 0% |
| INCOMPLETE (accepted after edits) | 4 | ~67% |

---

## 4. What the AI got wrong (human review — HW04 Task 1)

| Issue | Why AI missed it | Fix |
| --- | --- | --- |
| Sync `alert()` on weak password blocked Playwright `click()` | Model assumed async dialogs like API errors | `Promise.all(dialog, action)` + `noWaitAfter` |
| Happy-path asserted step-1 controls after `/login` | Generated “checklist” asserts without lifecycle phases | End-state oracles only for full reset |
| Locator `/đăng nhập/i` matched navbar, false Pass on 012 | Over-broad regex; ignored exact FR-03 label | Exact `^Quay lại đăng nhập$` → real Fail |
| Initial slice had 1 case only | Optimized for a demo slice, not HW04 ≥12 | Expanded to 14 external records |
| Temptation to set OTP length expectation to 4 | Matching SUT would hide SEC-07 / FR-03 defect | Keep expect 6 → TC-FORGOT-014 fails honestly |

---

## 5. Conclusion

AI was effective for scaffolding data-driven Playwright, matrix reporting, and first-pass case lists. It was weak on browser dialog timing, locator precision, and staying loyal to the **spec oracle** when the SUT is defective. For HW04, AI drafts must be followed by headed/matrix execution and an explicit “do not soften failing oracles” review.

**Use AI for:** stage-by-stage conversion, JSON schemas, page objects, report stamping.  
**Do not rely on AI alone for:** final Pass/Fail interpretation, GitHub Issue authorship ethics, or claiming green matrix by changing expected results.

---

## 6. Mandatory Disclosure

I used **Cursor Agent** to analyze FR-03, design/automate 14 data-driven cases, configure Chromium/Firefox/WebKit HTML reports labeled `Run by: 23127271`, repair automation defects, and draft this AI Audit / Critique / gap analysis. I reviewed outputs against the EShop README and HW04 PDF Task 1. I will not submit raw AI output without review. HTML reports and timestamps are from real local runs (Anti-AI-Cheat §11).

Appendix: `prompt_log.md` · stage log: `ai-conversion-log.md` · gaps: `hw04-fr03-gap-analysis.md`.

---

## Signature

| Field | Value |
| --- | --- |
| Student name | Vo Ngoc Bich Tram |
| Student ID | 23127271 |
| Class / Cohort | 23KTPM3 |
| Course | CS423 / CSC13003 – Software Testing |
| Instructor | Dr. Lam Quang Vu / Dr. Tran Duy Hoang / MSc. Tran Thi Bich Hanh / MSc. Truong Phuoc Loc / MSc. Ho Tuan Thanh |
| Date | 2026-08-09 |
| Signature | Tram |

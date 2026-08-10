Faculty of Information Technology (FIT) – Ho Chi Minh City University of Science (HCMUS)

CS423 / CSC13003 – Software Testing (AI-augmented · 2026)

AI POLICY · TEMPLATES — 2026 v1.0

# AI Audit Report — HW04 Task 1: Automation Testing

Mandatory appendix for every AI-assisted homework (HW#01–HW#06, and Seminar).

Adapted from Med Kharbach, PhD (2026) — AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0. This adaptation is prepared for FIT@HCMUS – CS423 / CSC15003 Software Testing course.

## 1. Student Information

| Field | Value |
| --- | --- |
| Student name (printed): | DANG TRUONG NGUYEN |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Assignment ID (e.g., HW#00, HW#02): | HW04 — Task 1 (Automation Testing) |
| Assignment date: | 10/08/2026 |
| AI tool(s) used: | Claude Code (Claude Fable 5) |
| AI tool(s) used: | [X] Yes  [ ] No |

## 2. Instructions (read before filling)

- Add one row per AI-generated artifact (test case, script, checklist, OpenAPI spec, JMeter plan, etc.).
- Paste the verbatim prompt — DO NOT paraphrase.
- Paste the verbatim AI output (or include a labelled screenshot in the report).
- Tag the verdict: VALID / INVALID / INCOMPLETE.
- Reasoning must cite a course slide, ISTQB section, or technical RFC.
- Show the corrected artifact with the change highlighted.
- Sample rows are in italic — replace them before submission.

## 3. Audit Table — one row per artifact

| (1) Prompt + Tool | (2) AI Output | (3) Verdict | (4) Reasoning (ISTQB) | (5) Student Fix |
| --- | --- | --- | --- | --- |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ0 · Task-1 work plan<br>__Prompt (verbatim):__<br>hãy viết plan cho task 1 vào folder plan trước, sau đó t sẽ đọc theo plan và cần biết làm gì | `plan/task1-plan.md` — 8-section plan: grading checklist (≥12 TC/feature, data-driven .csv/.json, ≥3 assertion patterns, 3 browsers/9 runs, "Run by: StudentID" + ISO timestamp), feature-selection table, environment setup, per-feature 8-step AI-first workflow, 10-hour timeline, 6 candidate assertion patterns, deliverables list, anti-cheat notes. | VALID | ISTQB FL – test planning: a test plan defines scope, approach, deliverables and exit criteria before execution. The plan mapped every graded requirement of the assignment to a concrete step, so work could be checked against it. | Accepted as-is; used it to drive the whole Task 1 (features FR-02/FR-09/FR-14 filled in from the suggestion row in section 1 of the plan). |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ1 · Test-case design + data files (40 TC)<br>__Prompt (verbatim):__<br>lấy FR 2, 9 14, hãy setup môi trường và viết code playwright cho 3 feat đó đi<br><br>(AI was then driven step-by-step: read SRS sections FR-02/09/14 → read frontend/backend source → design TC → emit data files) | 3 data files: `data/fr02-login.json` (15 TC: 8 login cases, 4 UI checks, 3 lockout scenarios), `data/fr09-coupon.json` (13 TC covering all 5 coupon conditions C1–C5 + boundaries), `data/fr14-category.json` (12 TC: view/create/delete/persist/integration/XSS). Positive, negative and edge types tagged per row. | INCOMPLETE | ISTQB FL – black-box techniques: equivalence partitioning and boundary value analysis (FR09-TC04/05 sit exactly on `min_order_amount`; FR02-LK01 sits exactly under the 3-attempt threshold). Initial design reused the shared `test@eshop.com` account for lockout scenarios, violating test-case independence (ISTQB: tests must be repeatable and order-independent). | Redesigned stateful scenarios to register a **fresh user per test via API** (lockout, coupon-usage) and to snapshot + clean categories in `afterEach`, so the shared SQLite backend is never polluted across the 3 browser runs; set `workers: 1`. |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ2 · Page Objects & selectors<br>__Prompt:__ (same session, step: derive selectors from real JSX source, not guesses) | `pages/LoginPage.ts`, `pages/CheckoutPage.ts`, `pages/AdminCategoriesPage.ts` — locators anchored on roles, placeholders and structural `form > div` blocks; helper methods `submitAndWaitLogin()`, `applyCoupon()`, `addCategory()`. | INCOMPLETE | ISTQB FL – maintainability of test automation (Page Object pattern isolates locator churn). The AI's first instinct was `getByLabel()`, which silently fails here: the SUT's `<label>` elements have no `htmlFor`/`id` association — an accessibility defect of the SUT that generic AI patterns assume away. | Verified every locator against the real JSX (`Login.jsx`, `Checkout.jsx`, admin `App.jsx`); replaced `getByLabel()` with label-anchored structural locators and documented the reason in code comments. |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ3 · Spec files (data-driven test scripts)<br>__Prompt:__ (same session, step: loop over JSON rows, ≥3 assertion patterns, no hardcoded data) | `tests/fr02-login.spec.ts`, `tests/fr09-coupon.spec.ts`, `tests/fr14-category.spec.ts` — pure loops over the JSON rows dispatching on `outcome`/`action`; 7 assertion patterns (URL, visibility/state, text, attribute/value, count, API response status, soft). | INCOMPLETE | ISTQB FL – test oracles: the UI shows one generic error for both wrong-password and locked-account, so a UI-only oracle cannot verify FR-02's lockout behaviour. ISTQB AuT – flaky-wait avoidance: assertions must synchronise on events, not timers. | Added an API-level oracle (`waitForResponse` → assert 401 vs 403); made the lockout loop tolerant (`expect.soft([401,403])`) because the SUT's +2 counter bug flips the status mid-scenario; made `addCategory()` await the POST + refresh GET before counting rows to remove a race that could produce a false pass. |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ4 · Multi-browser config + branded HTML report<br>__Prompt (verbatim):__<br>23127438 Đặng Trường Nguyên<br>fix đi | `playwright.config.ts` — 3 projects (Chromium/Firefox/WebKit), `webServer` auto-starting backend + 2 frontends, HTML reporter with `title: "Run by: 23127438 — <ISO>"` + metadata, `STUDENT_ID` env override; 4 HTML reports regenerated (`reports/all`, `reports/fr02-login`, `reports/fr09-coupon`, `reports/fr14-category`). | INCOMPLETE | ISTQB FL – configuration management & reporting: execution evidence must be attributable and reproducible. The reporter's title claim had to be verified, not trusted: the report stores it inside a base64-embedded zip, invisible to a plain grep. | Decoded the embedded `report.json` of all 4 reports and confirmed `options.title` and `metadata` carry "Run by: 23127438" + ISO timestamp; fixed the broken vite `.bin` shim by invoking `node node_modules/vite/bin/vite.js` directly; killed a stale "Hello World" server squatting port 3000 that made the first run's login API return non-JSON. |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ5 · Execution, triage & summary report<br>__Prompt (verbatim):__<br>t push lên git r, giờ hãy viết 1 file report md tổng hợp từ các result trước, sau đó viết bug report theo chuẩn template rổi đẩy lên github issue sử dụng gh | Full 3-browser run: 120 executions (40 TC × 3), **81 passed / 39 failed**, the 39 fails = the same 13 TC on all 3 browsers; `REPORT.md` with per-TC result tables, 9-bug summary, and a 7-point review of what the AI got wrong and why. | VALID | ISTQB FL – test monitoring & control + defect triage: a failed test is only a defect after analysis. Cross-browser consistency (identical 13 fails on 3 engines) was used as the argument separating SUT defects from flaky automation. | Reviewed each of the 13 failing TC against the SRS to confirm every failure traces to a spec violation (9 distinct root causes), not to script error; confirmed 0 flaky tests (no fail was browser-specific). |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ6 · Bug reports / GitHub issues (#390–398)<br>__Prompt:__ (same message as GĐ5 — "viết bug report theo chuẩn template rồi đẩy lên github issue sử dụng gh") | 9 issues following the repo's `bug_report.md` template (Found by TC / Requirement / Severity–Priority / Environment / Steps / Expected / Actual / Evidence + code location), labelled `type: bug`, `status: new`, `found-by: test-case`, each with a failure screenshot. | INCOMPLETE | ISTQB FL – defect management: reports must be reproducible and traceable both ways (TC ↔ issue). The AI's batch-creation script had an off-by-one (zsh arrays are 1-indexed), so the first `gh` run paired each issue title with the previous bug's body — structurally valid, factually wrong. | Caught the title/body mismatch by spot-checking issue #390, repaired all 8 bodies with `gh issue edit`, created the missing 9th issue, and re-verified content and severity of every issue against the SRS before accepting. |
| __Tool:__ Claude Code (Claude Fable 5)<br>__Artifact:__ GĐ7 · Cloudinary evidence-hosting script<br>__Prompt (verbatim):__<br>viết 1 script upload cloudinary và map lại, rồi sửa trên github issue<br>project: dnqinxiwo<br>api key: […]<br>api secret: […]<br>ko hard code, chạy trong runtime và lưu lại script đó để làm bằng chứng | `scripts/upload-screenshots-cloudinary.mjs` — dependency-free Node script: signed Cloudinary upload of the 9 screenshots, writes `bugs/cloudinary-map.json`, then rewrites image links in every `found-by: test-case` issue via `gh`. Ran clean: 9/9 uploaded, 9/9 issues updated, image URLs verified HTTP 200. | VALID | ISTQB FL – test evidence & tool support: evidence must stay accessible independent of repo history; secrets management follows the 12-factor principle (config in environment, never in code) — the script refuses to run without the env vars. | Accepted after verifying: credentials only via env at runtime, mapping file committed as evidence, one issue and one Cloudinary URL spot-checked (HTTP 200). Secret will be rotated after submission since it transited the AI session. |

## 4. Summary of AI Accuracy

Aggregate the verdicts from Section 3 and complete the table below.

| Metric | Count | Percentage |
| --- | --- | --- |
| Total AI-generated artifacts audited | 8 | 100% |
| VALID (correct, accepted as-is) | 3 | 37.5% |
| INVALID (wrong; rejected) | 0 | 0% |
| INCOMPLETE (acceptable after edits) | 5 | 62.5% |

## 5. Conclusion — When should AI be used (or not)?

Write 80–150 words describing patterns you observed. Where did AI shine? Where did AI fail? What is your recommendation for using AI in this kind of work in the future?

AI was strongest where the work was mechanical and verifiable: scaffolding the Playwright project, converting 40 designed test cases into data-driven loops, and generating template-conform bug reports — hours of typing became minutes. It was weakest wherever correctness depended on facts outside its assumptions: it reached for `getByLabel()` on a page whose labels are not associated with inputs, did not anticipate that three browser runs share one stateful SQLite backend, and its issue-creation loop silently mispaired titles and bodies because of zsh's 1-indexed arrays. None of these failures were visible in the code's appearance — they surfaced only through execution and inspection of real artifacts (DOM, database, created issues). My recommendation: let AI draft everything, but gate every artifact behind a runtime check the human designs; review effort should concentrate on environment assumptions, shared state, and off-by-one boundaries, because that is where plausible-looking AI output actually breaks.

## 6. Mandatory Disclosure (paste verbatim)

"The Task-1 work plan, test data files, Page Objects, Playwright specs, multi-browser configuration, summary report, bug reports and the Cloudinary evidence script were initially generated by Claude Code under my step-by-step direction; I reviewed and corrected them (test isolation redesign, locator fixes, API-level oracles, report-title verification, issue title/body repair) and I take full responsibility for the final artifacts. Section 5 reflects my own analysis. The detailed AI Audit Report is attached as Appendix A. I confirm I did not use AI to generate any artifact listed in the prohibited category: the HTML reports are real executions containing 'Run by: 23127438' with ISO timestamps, and the demo video is recorded and narrated by me."

## Signature

| Student name (printed): | DANG TRUONG NGUYEN |
| --- | --- |
| Student ID: | 23127438 |
| Class / Cohort: | 23KTPM3 |
| Course: | CS423 / CSC13003 – Software Testing |
| Instructor: | Msc. Tran Thi Bich Hanh |
| Date: | 10/08/2026 |
| Signature: | ![signature](./signature.png) |

## References

- Kharbach, M. (2026). AI Use Policy Templates for Higher Education. CC BY-NC-SA 4.0.
- ISTQB Foundation Level Syllabus (latest version).
- Hardman, P. (2025). A Post-AI Learning Taxonomy.
- Fuster Rabella, M. (2025). OECD Education Working Paper No. 338.
- Perkins, M., Roe, J., & Furze, L. (2025). AI Assessment Scale.
- Anthropic (2025). Building reliable AI test agents — engineering blog.
- DeepEval & Promptfoo documentation — testing frameworks for LLM systems.

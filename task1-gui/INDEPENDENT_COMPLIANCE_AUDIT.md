# Independent Compliance Audit — Task 1 GUI Checklist (HW03)

## 1. Executive Summary

**Student:** Đặng Đăng Khoa  
**Student ID:** 23127207  
**SUT:** EShop  
**Audit scope:** Task 1 — GUI Checklist  
**Audit date:** 2026-07-28 (Asia/Bangkok, UTC+07:00)  
**Auditor role:** Independent Senior QA Auditor  
**Final audit result:** **NON_COMPLIANT**  
**Final audit score:** **31.5/100**

Kết quả không đạt vì các completion gate cốt lõi không được chứng minh:

1. Toàn bộ `task1-gui/` đang **untracked** trong Git. `git-commit-log.txt` chứa chín hash không tồn tại; chính `scripts/generate_all_deliverables.py:1401-1412` đã ghi cứng các hash này.
2. 58 Actual/Status được ghi cứng trong `scripts/generate_all_deliverables.py`; `scripts/run-gui-execution.js` chỉ thực hiện một số thao tác và chụp năm ảnh, không có assertion hoặc kết quả item-level cho 58 item.
3. “Mobile” được chạy bằng Playwright Chromium tại `http://localhost:8081` với viewport giả lập (`scripts/run-gui-execution.js:109-130`), không phải Expo Go, emulator hay thiết bị vật lý.
4. Không có GitHub Issue URL thật; cả năm bug đều là `PENDING_EXTERNAL_ACTION`.
5. Checklist lưu 36 Pass và 22 Fail, trong khi Test Summary báo 40 Pass và 18 Fail. Pass rate đúng từ checklist là 62.07%, không phải 68.97%.
6. Source requirement FR-14 chỉ yêu cầu Thêm/Xem/Xóa (`README.md:186-189`), nhưng item `GUI-ADMIN-CATEGORY-005` và BUG-GUI-04 coi thiếu Edit là lỗi requirement.
7. Coverage IA có đủ bốn mã về mặt số lượng, nhưng IA-03 không có item Category Management và thiếu các hành vi Back/Forward, deep link, focus sau navigation và navigation sau delete.
8. Không có demo video/link; README không chứa phần lớn thông tin bắt buộc; validator không kiểm tra các completion gate chính và vẫn trả exit code 0 khi báo `INCOMPLETE`.

### Key recalculated figures

| Metric | Audited value |
|---|---:|
| Total checklist rows | 58 |
| Unique IDs | 58 |
| Exact/semantic duplicate deduction | 0 |
| Invalid/unsupported expected-result items | 7 |
| Imaginary requirement item | 1 |
| Out-of-scope items | 0 |
| **Valid unique checklist count** | **50** |
| Stored Pass / Fail / Blocked / Not Run | **36 / 22 / 0 / 0** |
| Stored-status pass rate | **62.07%** |
| Independently verifiable item-level executions | **0/58** |
| Local bug IDs | 5 |
| Fully verified end-to-end bugs | 0 |
| Verified GitHub Issues | 0 |
| Findings — Critical / High / Medium / Low | **4 / 11 / 12 / 0** |

## 2. Audit Environment

| Area | Directly observed evidence | Audit note |
|---|---|---|
| Workspace | `C:\My Workspace\HCMUS\Test\Week 3\Hw2` | Local Windows workspace; audit performed without modifying original artifacts. |
| Git | Branch `HW3-Khoa`; real HEAD `671d798` | `task1-gui/` is untracked; no real commit contains it. |
| Requirements | Root `README.md:30-44`, `README.md:174-189` | FR-01, FR-02, FR-12 and FR-14 inspected directly. |
| Web source | `frontend-web/src/App.jsx`, `pages/Login.jsx`, `pages/Register.jsx` | Routes `/login` and `/register` exist. |
| Admin source | `frontend-admin/src/App.jsx` | Login is a conditional root view; Category is a root tab, not a separate route. |
| Mobile source | `frontend-mobile/App.js` | Native Login view exists, but submitted evidence came from React Native Web. |
| Backend source/data | `backend/server.js`, `backend/database.js`, `backend/database.sqlite` | Login lock and category behavior inspected directly. |
| Excel parser | `openpyxl` | Workbook opened successfully; all sheets, hidden state, formulas and merged cells inspected. |
| Evidence parser | Pillow | All five PNG files decoded and verified successfully. |
| External services | No GitHub Issue URL or video URL was provided | There was no concrete external URL to browse; absence is directly verifiable. Posting/ownership remains an external student action. |

The requested `gui-testing-skill` was inspected as repository source at `.agents/skills/gui-testing-skill/SKILL.md`. It requires at least 41 non-duplicate items, all four IA groups, real execution, evidence for every Fail, real GitHub traceability, Excel, AI audit/critique, Git log and demo video. The available Domain and Boundary Testing Skill was also applied to inspect required/invalid/edge partitions for Login, Register and Category forms. It specifically supports separate invalid partitions and boundary coverage; therefore empty-email and empty-password items were not treated as duplicates merely because both exercise `required`.

## 3. Artifact Inventory

All mandatory paths existed and were non-empty at the start of the audit. “Valid format” means the file/directory can be parsed/opened; it does not mean its claims are correct.

| Artifact | Expected Path | Exists | Non-empty | Valid Format | Audit Note |
|---|---|---:|---:|---:|---|
| README | `task1-gui/README.md` | Yes | Yes, 1,240 B | Yes, Markdown | Only a directory tree; missing scope metrics, environment, results, issues, video, final status and opening instructions. |
| Scope analysis | `task1-gui/scope-analysis.md` | Yes | Yes, 4,050 B | Yes, Markdown | Routes largely accurate; mobile execution target is aspirational, not supported by evidence. |
| Markdown checklist | `task1-gui/GUI_Checklist_HW3.md` | Yes | Yes, 25,159 B | Yes, Markdown table | 58 rows, 58 unique IDs, 14 columns. |
| Excel checklist | `task1-gui/GUI_Checklist_HW3.xlsx` | Yes | Yes, 17,639 B | Yes, OOXML | Opens; 4 visible sheets; no hidden rows/columns, merged cells or formulas. Auxiliary metrics are wrong. |
| Coverage matrix | `task1-gui/GUI_Coverage_Matrix.md` | Yes | Yes, 1,111 B | Yes, Markdown | Contains three mutually inconsistent IA totals. |
| Bug report | `task1-gui/GUI_Bug_Report_HW3.md` | Yes | Yes, 7,832 B | Yes, Markdown | Five bug packs; mandatory fields and end-to-end traceability are incomplete. |
| Test summary | `task1-gui/GUI_Test_Summary_HW3.md` | Yes | Yes, 2,222 B | Yes, Markdown | Pass/Fail/platform/origin/pass-rate values do not match checklist data. |
| Item critique | `task1-gui/AI_Item_Level_Critique.md` | Yes | Yes, 8,191 B | Yes, Markdown | 50 raw AI rows covered, but correction/removal claims conflict with final data; no per-human-item rationale. |
| Overall AI critique | `task1-gui/AI_Critique_Task1.md` | Yes | Yes, 2,140 B | Yes, Markdown | English and 276 whitespace-delimited body words; declared 265; material claims are false. |
| AI audit report | `task1-gui/AI_Audit_Report_Task1.md` | Yes | Yes, 1,239 B | Yes, Markdown | Missing full prompt, time, explicit verdict/reasoning and complete interaction log. |
| AI disclosure | `task1-gui/AI_Disclosure_Task1.md` | Yes | Yes, 706 B | Yes, Markdown | Claims fully live-reviewed execution and GitHub traceability despite contrary evidence. |
| Commit log | `task1-gui/git-commit-log.txt` | Yes | Yes, 527 B | Text parses; Git content invalid | All nine hashes fail `git cat-file -e`; directory is untracked. |
| Raw AI output | `task1-gui/ai-output/AI_INITIAL_GUI_Checklist.md` | Yes | Yes, 13,999 B | Yes, Markdown table | 50 rows, all marked `AI_INITIAL`; no Git provenance. |
| Evidence directory | `task1-gui/evidence/` | Yes | Yes, 5 PNGs | Yes, PNG | All images decode; most demonstrate only a static subset of packed bug claims. |
| GitHub issue drafts | `task1-gui/github-issues/` | Yes | Yes, 5 Markdown files | Yes, Markdown | Offline drafts only; all status values are `PENDING_EXTERNAL_ACTION`; zero URLs. |
| Validator | `task1-gui/scripts/validate-gui.ps1` | Yes | Yes, 3,124 B | Yes, PowerShell | Runs, reports INCOMPLETE, returns 0; validates only existence, fixed evidence filenames and line count. |
| Execution helper | `task1-gui/scripts/run-gui-execution.js` | Yes | Yes, 4,581 B | Yes, JavaScript | Screenshot helper, not a 58-item test runner. |
| Deliverable generator | `task1-gui/scripts/generate_all_deliverables.py` | Yes | Yes, 71,778 B | Yes, Python source | Hard-codes final item results, metrics, reports, disclosure, issue drafts, fake commit log and validator. |

### Placeholder scan

| Token/category | Evidence | Verdict |
|---|---|---|
| `PENDING_EXTERNAL_ACTION` | `GUI_Bug_Report_HW3.md:15,54,85,117,152`; all `github-issues/BUG-GUI-*.md:7`; `GUI_Test_Summary_HW3.md:24` | Confirmed unresolved external action; completion prohibited. |
| UI `placeholder` wording | Checklist/source references to HTML placeholders | Legitimate UI terminology, not an artifact placeholder. |
| TODO/TBD/example.com/GitHub URL here/insert markers | No matching mandatory-artifact placeholder found | No issue for these specific strings. |
| Demo URL | No URL or video file found | Required artifact absent, not merely a placeholder. |

## 4. Scope Verification

| Scope | Requirement | Real Route/Screen | Exists in SUT | Checklist Count | Verdict |
|---|---|---|---:|---:|---|
| Web Login | FR-02 | `/login`, `frontend-web/src/App.jsx:52`; UI `Login.jsx:22-66` | Yes | 13 | PARTIALLY_COMPLIANT — route and principal UI are real; item 010 uses five attempts although FR-02 requires lock after three (`README.md:41-44`); source actually increments by 2 and locks 180s (`backend/server.js:54-63`). |
| Web Register | FR-01 | `/register`, `frontend-web/src/App.jsx:53`; UI `Register.jsx:31-81` | Yes | 12 | PARTIALLY_COMPLIANT — route/fields are real, but FR-01 explicitly requires Confirm Password (`README.md:35`) and neither SUT nor checklist audits that missing field. |
| Admin Login | FR-12 | Root conditional `if (!token)`, `frontend-admin/src/App.jsx:188-215` | Yes | 9 | PARTIALLY_COMPLIANT — real screen; it is a state at `/`, not a routed page. Login role behavior exists at `App.jsx:61-73`. |
| Admin Category Management | FR-14 | Root tab `categories`, `frontend-admin/src/App.jsx:233-238,294-334` | Yes | 13 | PARTIALLY_COMPLIANT — real list/add/delete UI. Item 005 invents an Edit obligation even though FR-14 says only Thêm/Xem/Xóa (`README.md:186-189`). |
| Mobile Login | FR-02 | `view === login`, `frontend-mobile/App.js:759-795,980` | Yes | 11 | PARTIALLY_COMPLIANT for design; NON_COMPLIANT for execution because evidence is Chromium/React Native Web, not a native target. |

No Product, Cart, Checkout, Coupon, Dashboard or Order Management item was used to inflate the 58-row count. Navigation destinations originating inside the five screens were not counted as out-of-scope modules.

### Material source-to-checklist mismatches

| Item ID | Checklist claim | Direct source/requirement evidence | Verdict |
|---|---|---|---|
| GUI-WEB-LOGIN-010 | Lockout tested “after 5 failed attempts” | FR-02: lock at 3 and 30 seconds (`README.md:41-42`); implementation adds 2 per failure and locks for 180 seconds (`backend/server.js:54-58`) | NON_COMPLIANT |
| GUI-WEB-REGISTER-011 | React “sanitizes” XSS and item passes | Header later renders `user.name` with `dangerouslySetInnerHTML` (`frontend-web/src/App.jsx:26-28`) | Stored Pass is unsupported and potentially incorrect |
| GUI-ADMIN-CATEGORY-005 | FR-14 requires Edit button | FR-14 only lists Add/View/Delete (`README.md:186-189`) | NON_COMPLIANT; imaginary requirement |
| GUI-ADMIN-CATEGORY-008 | Deleting a category with products produces an error banner/alert | Schema has no foreign key (`backend/database.js:63-71`); SQLite `foreign_keys=0`; DELETE is unconditional (`backend/server.js:269-276`) | NON_COMPLIANT; expected/actual are unsupported |
| GUI-ADMIN-CATEGORY-011 | Duplicate category produces server error | Category `name` is not UNIQUE (`backend/database.js:23-26`); POST inserts directly (`backend/server.js:249-254`) | NON_COMPLIANT; Actual “success or alert” is indeterminate |

## 5. Markdown–Excel Comparison

### Workbook structure

| Check | Result | Evidence |
|---|---|---|
| Sheets | `Checklist`, `Coverage`, `Bug Summary`, `AI Human Review` | Workbook inspection |
| Hidden sheets | None | All sheet states `visible` |
| Checklist dimensions | 59 rows × 14 columns | Header row 1 + 58 data rows |
| Hidden rows/columns | None | Workbook row/column metadata |
| Merged cells | None | All sheets |
| Formulas | None | All sheets |
| Auto-filter | `Checklist!A1:N59` | Workbook metadata |
| Freeze panes | `Checklist!A2` | Workbook metadata |

### Primary item comparison

All 58 IDs are present in both files. After normalizing Markdown bold markers and converting Markdown evidence links to their target paths, all 14 primary fields match item by item: ID, Platform, Screen/Route, Related Requirement, IA, Category, Origin, Checklist Item, Expected Result, Actual Result, Status, Notes, Evidence and Bug ID.

| Item ID | Field | Markdown Value | Excel Value | Verdict |
|---|---|---|---|---|
| All 58 IDs | All 14 primary fields | Matched | Matched | COMPLIANT for primary checklist synchronization |

### Auxiliary-sheet mismatches

| Item ID / Sheet row | Field | Markdown/final-row value | Excel auxiliary value | Verdict |
|---|---|---:|---:|---|
| `Coverage!5` | IA-01 count | 11 | 14 | NON_COMPLIANT |
| `Coverage!6` | IA-02 count | 20 | 21 | NON_COMPLIANT |
| `Coverage!7` | IA-03 count | 9 | 9 | COMPLIANT |
| `Coverage!8` | IA-04 count | 18 | 14 | NON_COMPLIANT |
| `Coverage!9` | AI_INITIAL count | 48 | 47 | NON_COMPLIANT |
| `Coverage!10` | HUMAN_ADDED count | 10 | 11 | NON_COMPLIANT |
| `AI Human Review!5` | AI items removed | Final retains all 50 raw IDs | 3 | NON_COMPLIANT |
| `AI Human Review!6` | Human-added | Final Origin values = 10 | 11 | NON_COMPLIANT |

The Completion Gate for primary Markdown–Excel checklist rows passes, but R-24 is only **PARTIALLY_COMPLIANT** because the workbook’s visible auxiliary sheets contradict the same workbook’s `Checklist` sheet and the Markdown data.

## 6. Checklist Quantity and Duplicate Analysis

### Count calculation

| Component | Count | Basis |
|---|---:|---|
| Total rows | 58 | Markdown lines 13-70; Excel `Checklist!2:59` |
| Unique IDs | 58 | No duplicate ID |
| Exact normalized duplicates | 0 | Normalized Checklist Item + Expected Result |
| Semantic duplicate deduction | 0 | Reviewed same-feature pairs below |
| Invalid/unsupported items | 7 | Items with requirement/source/expected-result defects |
| Imaginary requirement items | 1 | `GUI-ADMIN-CATEGORY-005` |
| Out-of-scope items | 0 | All originate from one of five fixed screens |
| **Valid unique item count** | **50** | 58 − 0 − 7 − 1 − 0 |

The design-count gate `>= 41` is met with 50 valid unique items. This does **not** validate their execution.

### Duplicate and split review

| Item A | Item B | Similarity Reason | Duplicate Level | Recommendation |
|---|---|---|---|---|
| GUI-WEB-LOGIN-004 | GUI-WEB-LOGIN-005 | Both test `required`, but use distinct invalid input partitions (empty email vs empty password) | Not Duplicate | Retain separately; this follows EP guidance to isolate invalid partitions. |
| GUI-ADMIN-LOGIN-003 | GUI-ADMIN-LOGIN-004 | Both observe native alerts, but one tests invalid credential and one tests authorization role | Not Duplicate | Retain as separate authentication/authorization states. |
| GUI-ADMIN-CATEGORY-006 | GUI-ADMIN-CATEGORY-007 | Confirmation behavior vs successful deletion result | Not Duplicate | Retain if confirmation is an approved usability expectation. |
| GUI-ADMIN-CATEGORY-007 | GUI-ADMIN-CATEGORY-008 | Delete an unreferenced category vs a category referenced by products | Not Duplicate | Keep separate partitions only after the expected integrity rule is defined. Current item 008 is invalid. |
| GUI-MOBILE-LOGIN-006 | GUI-MOBILE-LOGIN-007 | Different navigation destinations: Home vs Register | Not Duplicate | Retain. |
| GUI-MOBILE-LOGIN-007 | GUI-MOBILE-LOGIN-008 | Different navigation destinations: Register vs Forgot Password | Not Duplicate | Retain. |
| GUI-WEB-LOGIN-002 | GUI-WEB-LOGIN-009 | Both combine more than one assertion (label/type; language/tabIndex) | Artificial Split: No; compound assertions: Yes | Split unrelated assertions for clearer diagnosis, but no duplicate deduction was applied. |

### Excluded design items

| Item ID | Exclusion class | Reason |
|---|---|---|
| GUI-WEB-LOGIN-010 | Invalid | Wrong lock threshold and unsupported lock-time expectation. |
| GUI-WEB-LOGIN-013 | Invalid | Requires `trim()` without a requirement; Actual says spaces remain and login fails, yet Status is Pass. |
| GUI-WEB-REGISTER-006 | Invalid | Expected accepts two alternative messages not produced by the inspected backend; outcome is not deterministic. |
| GUI-WEB-REGISTER-008 | Invalid | Assumes an undocumented `blue-600` design standard as the sole correct color. |
| GUI-WEB-REGISTER-012 | Invalid | “Thông báo lỗi kết nối rõ ràng” is subjective and does not define exact observable text/state. |
| GUI-ADMIN-CATEGORY-005 | Imaginary requirement | FR-14 does not require Edit. |
| GUI-ADMIN-CATEGORY-008 | Invalid | Current schema/API allow deletion; expected error and Actual alert are unsupported. |
| GUI-ADMIN-CATEGORY-011 | Invalid | Duplicate names are allowed; Actual says “success or alert,” which cannot determine Pass/Fail. |

## 7. IA Coverage Analysis

Recalculated directly from 58 final rows:

| IA | Item Count | Screens Covered | Representative IDs | Coverage Quality | Verdict |
|---|---:|---|---|---|---|
| IA-01 General UI | 11 | All 5 | WEB-LOGIN-001/011/012; WEB-REGISTER-001/008; ADMIN-LOGIN-001; ADMIN-CATEGORY-001; MOBILE-LOGIN-001/004/010 | Title, consistency, keyboard, 320px and touch-target concepts exist. Contrast, accessible-name and overflow coverage are shallow; several Actuals are source inference. | PARTIALLY_COMPLIANT |
| IA-02 Forms | 20 | All 5 | WEB-LOGIN-002/004/005/013; WEB-REGISTER-002/004/009/010/011; ADMIN-LOGIN-002/008; ADMIN-CATEGORY-004/012; MOBILE-LOGIN-002/003/011 | Required/invalid/password/long-input concepts exist. Missing FR-01 Confirm Password, invalid email behavior, Enter submit, focus after validation, password visibility toggle and reliable disabled-state coverage. | PARTIALLY_COMPLIANT |
| IA-03 Navigation | 9 | 4; no Admin Category | WEB-LOGIN-007/008; WEB-REGISTER-007; ADMIN-LOGIN-005/007/009; MOBILE-LOGIN-006/007/008 | Mostly link/button destinations. No Browser Back/Forward, refresh/deep-link behavior, Category list→action→list navigation, cancel/back/delete navigation, or focus after navigation. | NON_COMPLIANT |
| IA-04 Feedback/state | 18 | All 5 | WEB-LOGIN-006/010; WEB-REGISTER-005/006/012; ADMIN-LOGIN-003/004/006; ADMIN-CATEGORY-003/006/009/010/013; MOBILE-LOGIN-005/009 | Broad concepts on paper: auth errors, lockout, network, empty/loading, duplicate and double-submit. No item-level LIVE/MOCKED mode and several states were not exercised. | PARTIALLY_COMPLIANT |

The numerical presence of IA-01..IA-04 is confirmed, but the quality gate for all four IAs fails because IA-03 is materially incomplete and other IA results are unsupported by execution evidence.

## 8. AI_INITIAL and HUMAN_ADDED Verification

### Direct counts and trace

| Origin | Declared Count in final checklist | Verified Count | Invalid / Unverified Count | Verdict |
|---|---:|---:|---:|---|
| AI_INITIAL | 48 | 42 same-ID, same-subject rows trace to raw output | 6 IDs (`GUI-ADMIN-CATEGORY-006`..`011`) were semantically shifted/reused | PARTIALLY_COMPLIANT |
| HUMAN_ADDED | 10 | 0 independently verified as human-authored | 10: eight are new-content additions without Git provenance; two (`012`,`013`) reuse raw AI IDs with different content | UNVERIFIABLE |

Additional contradictions:

- Raw output has 50 AI rows.
- Final checklist contains all 50 raw IDs plus eight new IDs, for 58 total.
- Final Origin values are 48 AI / 10 Human.
- Summary, Coverage sheet and critique report 47 AI / 11 Human.
- `AI_Item_Level_Critique.md:68-72` says 28 kept + 19 revised + 3 removed = 50, 47 remaining, 11 added.
- No raw ID was actually absent from final. Items 006 and 009 were not removed; their IDs were repurposed.
- No real Git commit shows a chronological raw-AI → human-review → final process.

Because authorship cannot be inferred from an `Origin` cell, HUMAN_ADDED provenance is **UNVERIFIABLE**, not COMPLIANT.

## 9. Item-Level Critique Verification

| Criterion | Evidence | Verdict |
|---|---|---|
| One row for each raw AI item | 50 rows, `AI_Item_Level_Critique.md:13-62` | COMPLIANT |
| Allowed verdicts | VALID, INCOMPLETE, INVALID; no unsupported verdict | COMPLIANT |
| Mandatory fields | Table has Item ID, Verdict, combined Problem/SUT Reality, combined Correction/Action, Final Decision; no separate Reasoning field | PARTIALLY_COMPLIANT |
| Specific analysis | Many INCOMPLETE rows cite exact source defects; 28 VALID rows commonly use “Keep as is” | PARTIALLY_COMPLIANT |
| Corrections appear in final | Some do; however corrections often say change Expected to actual defect while final correctly leaves ideal Expected and puts defect in Actual | PARTIALLY_COMPLIANT |
| Remove decisions | Lines 45-53 and summary line 70 claim three removals; all 50 raw IDs remain | NON_COMPLIANT |
| Revise mapping | Category IDs 006-011 were shifted to different semantics without an explicit old→new mapping | NON_COMPLIANT |
| HUMAN_ADDED rationale | No per-human-item “What AI missed / Why / Risk / How improved” section exists | NON_COMPLIANT |
| Human provenance | No real Git review commit; generator hard-codes final rows and reports | UNVERIFIABLE |

Overall verdict: **NON_COMPLIANT**.

## 10. Expected Result Quality

Most Expected Results are observable enough for a GUI checklist. Eight items are excluded from the valid count:

| Item ID | Expected Result | Problem | Required Rewrite | Verdict |
|---|---|---|---|---|
| GUI-WEB-LOGIN-010 | Lock message after five failures, with lock duration | Contradicts FR-02 threshold of three and 30 seconds; source also violates FR separately | “After the third consecutive invalid password, login is blocked for 30 seconds and the UI displays the specified generic lock message.” | NON_COMPLIANT |
| GUI-WEB-LOGIN-013 | Email is automatically trimmed before API request | No requirement/source basis; Actual contradicts Expected while Status is Pass | Establish a trim requirement. Then specify exact payload/message and whether a request must be sent. | NON_COMPLIANT |
| GUI-WEB-REGISTER-006 | Shows either “User already exists” or “Email đã được sử dụng” | Alternative outcomes; inspected backend returns raw database error | Specify one accepted UI contract, e.g. exact localized duplicate-email text and remaining route/state. | NON_COMPLIANT |
| GUI-WEB-REGISTER-008 | Register button must use `blue-600` | No design-system requirement or approved token is cited | Cite an approved design token or rewrite as a measurable contrast/consistency rule backed by a design reference. | NON_COMPLIANT |
| GUI-WEB-REGISTER-012 | Shows a “clear” connection error | “Clear” is subjective; no exact content/state | Specify exact fallback text, red-banner location, enabled state after failure and route retention. | NON_COMPLIANT |
| GUI-ADMIN-CATEGORY-005 | Every row has Edit because FR-14 requires it | FR-14 does not require Edit | Remove, or first amend the requirement to include Update and define the UI flow. | NON_COMPLIANT |
| GUI-ADMIN-CATEGORY-008 | Referenced category deletion shows an error banner | Schema/API impose no such restriction; source deletes unconditionally | Test the actual delete contract, or add an explicit integrity requirement and backend constraint first. | NON_COMPLIANT |
| GUI-ADMIN-CATEGORY-011 | Duplicate category shows server error | `name` is not UNIQUE; Actual “success or alert” is indeterminate | Decide whether duplicates are allowed. State one exact expected outcome and assert it. | NON_COMPLIANT |

Other quality concerns not deducted from the design count:

- `GUI-WEB-LOGIN-002`, `009`, `GUI-ADMIN-CATEGORY-002` combine unrelated assertions.
- `GUI-ADMIN-LOGIN-001` Actual uses subjective “chuẩn thẩm mỹ.”
- `GUI-ADMIN-CATEGORY-003` Actual uses subjective “hoạt động mượt.”
- Several Expected Results prescribe implementation (`React Router Link`, `localStorage`, exact Tailwind class) rather than an observable user outcome.

## 11. Execution Integrity

### Recalculated stored statuses

| Metric | Recalculated from checklist |
|---|---:|
| Pass | 36 |
| Fail | 22 |
| Blocked | 0 |
| Not Run | 0 |
| Total | 58 |
| Executed by stored-status formula | 58 |
| Pass rate | 36 / 58 × 100 = **62.07%** |
| Independently verified item-level executions | **0/58** |

### Platform breakdown

| Platform | Total | Pass | Fail | Pass Rate |
|---|---:|---:|---:|---:|
| Web Frontend | 25 | 15 | 10 | 60.00% |
| Web Admin | 22 | 12 | 10 | 54.55% |
| Mobile App | 11 | 9 | 2 | 81.82% declared; native execution unverified |
| **Total** | **58** | **36** | **22** | **62.07%** |

### Why the execution claim is not reliable

1. `scripts/generate_all_deliverables.py:952-966` writes final rows, including Actual and Status, from hard-coded dictionaries.
2. `scripts/run-gui-execution.js` does not load the checklist, iterate IDs, assert Expected Results or write a result log.
3. Web Login: lines 26-39 only navigate, read `h2` and capture a screenshot.
4. Register: lines 41-60 exercise one regex-failure path.
5. Admin Login: lines 76-86 fill a wrong password but capture the screenshot **before** clicking Login; lines 88-94 then overwrite credentials and click.
6. Category: lines 96-107 only open the Category tab and capture a static screenshot; no add, empty, delete, error, loading or double-submit action occurs.
7. Mobile: lines 109-130 use a Chromium page at port 8081; no login submit is performed.
8. There is no item-level timestamp, run log, assertion report, browser trace or mapping of execution mode to IDs.
9. Document-level `Execution Mode: LIVE` at `GUI_Checklist_HW3.md:7` cannot prove 58 LIVE executions.

### Contradictory/indeterminate stored results

| Item ID | Stored result | Direct problem |
|---|---|---|
| GUI-WEB-LOGIN-013 | Pass | Actual says whitespace is retained and causes login failure, contrary to Expected trim behavior. |
| GUI-WEB-REGISTER-011 | Pass | Actual claims safe React escaping, but the post-login header uses `dangerouslySetInnerHTML`. |
| GUI-ADMIN-CATEGORY-008 | Fail | Current API/schema do not reject referenced-category deletion. |
| GUI-ADMIN-CATEGORY-011 | Pass | Actual is “API succeeds or throws alert,” which is not one observed outcome. |
| GUI-MOBILE-LOGIN-010 | Pass | Source style has padding 10 (`App.js:1052-1057`); no native measurement proves 44×44 dp. |
| GUI-MOBILE-LOGIN-011 | Pass | A `ScrollView` source inspection does not prove keyboard avoidance on a device. |

Execution verdict: **NON_COMPLIANT**.

## 12. Evidence Audit

All paths in the checklist are relative and all five PNGs exist, decode and have unique SHA-256 values. No `file:///` path is used in the checklist. Existence is not sufficient to prove each Fail.

| Bug ID | Checklist IDs | Evidence Path | Exists | Shows Claimed Failure | Verdict |
|---|---|---|---:|---|---|
| BUG-GUI-01 | LOGIN-001/002/003/007/009/010/011 | `evidence/web-login/BUG-GUI-01_web-login.png` | Yes, 1440×900 | Partly: title, Username and Sign In are visible. Empty password does not prove plaintext; image cannot prove reload, tab order, visible focus or account lock. | PARTIALLY_COMPLIANT |
| BUG-GUI-02 | REGISTER-002/004/008 | `evidence/web-register/BUG-GUI-02_web-register.png` | Yes, 1440×900 | Partly/strongly: regex error and red button are visible; input type needs DOM/source evidence. | PARTIALLY_COMPLIANT |
| BUG-GUI-03 | ADMIN-LOGIN-002/003/004 | `evidence/admin-login/BUG-GUI-03_admin-login.png` | Yes, 1440×900 | Static form supports placeholder-only appearance. It does not show either alert; execution script captured before submit. | PARTIALLY_COMPLIANT |
| BUG-GUI-04 | CATEGORY-004/005/006/008/009/010/013 | `evidence/admin-category/BUG-GUI-04_admin-category.png` | Yes, 1440×900 | Static list shows no Edit button, but Edit is not required. It does not prove empty submit, confirmation behavior, delete error, empty/loading or double-submit. | NON_COMPLIANT |
| BUG-GUI-05 | MOBILE-002/004 | `evidence/mobile-login/BUG-GUI-05_mobile-login.png` | Yes, 780×1688 | Text mismatches are visible, but capture is React Native Web in Chromium, not native mobile evidence. | NON_COMPLIANT |

There are 22 Fail rows but only five screenshots, each reused for a multi-defect bug pack. Reuse is not inherently invalid, but one static image does not show most dynamic failures. Therefore R-18 is only **PARTIALLY_COMPLIANT**.

## 13. Bug Report Audit

### Common field audit

| Required field | Result |
|---|---|
| Title, requirement, platform, route, severity, priority | Present via headings/metadata |
| Environment | One global line exists; not repeated per bug |
| Preconditions/test data | Present, but generic and unsuitable for some admin/category scenarios |
| Steps/Expected/Actual/Evidence | Present, but several packed claims lack matching steps and evidence |
| Related checklist items | Present |
| Reproducibility | Missing for all five |
| GitHub Issue URL | Missing for all five |
| Bug status | A GitHub posting status is present; defect lifecycle status is absent |
| Screenshot attachment to GitHub | Not present |

### Per-bug quality

| Bug ID | Directly corroborated content | Material problem | Verdict |
|---|---|---|---|
| BUG-GUI-01 | Heading, label, input types, anchor and tabIndex match source | Packs seven checklist failures with different root causes/severities; steps and evidence omit lockout reproduction | PARTIALLY_COMPLIANT |
| BUG-GUI-02 | Regex and input type match source; screenshot shows regex error | Packs validation, HTML type and color/design issue into one bug | PARTIALLY_COMPLIANT |
| BUG-GUI-03 | Missing labels and native alerts match source | Screenshot does not show alert; missing reproducibility and URL | PARTIALLY_COMPLIANT |
| BUG-GUI-04 | Missing client `required`, immediate delete and missing states match portions of source | Edit claim is not a requirement; seven checklist IDs are linked but narrative only covers three; referenced-category error is unsupported | NON_COMPLIANT |
| BUG-GUI-05 | Username/Email and Sign In text match source and screenshot | Native platform is not verified; no URL/attachment | PARTIALLY_COMPLIANT |

**Local bug IDs with at least one source-corroborated defect:** 5.  
**Fully verified bug records with complete reproduction, evidence and GitHub traceability:** 0.

## 14. GitHub Issues Verification

| Check | Audited result |
|---|---|
| GitHub Issue URLs found | 0 |
| Correct issue-format URLs | 0 |
| Repositories verified | 0 |
| Issue titles/content verified | 0 |
| Screenshots attached to Issues | 0 |
| Labels/creator/workflow verified | 0 |
| Local drafts | 5 |
| Draft status | All `PENDING_EXTERNAL_ACTION` |

The local drafts are not GitHub Issues. They also refer to evidence as `../../evidence/...`, which does not resolve to `task1-gui/evidence/...` from `task1-gui/github-issues/`; the local relative path should start with `../evidence/` if used as a repository file link. Posting real issues and proving ownership/labels/attachments is **PENDING_EXTERNAL_VERIFICATION**, but the current requirement status is **NON_COMPLIANT** because no URL exists.

## 15. Mobile Execution Verification

| Required mobile evidence | Found | Evidence / gap |
|---|---:|---|
| Mobile source and Login screen | Yes | `frontend-mobile/App.js:759-795,980` |
| Expo Go / emulator / physical device named | No | `scope-analysis.md:47` states a target generically; no actual device record |
| Device model | No | Absent |
| Android/iOS version | No | Absent |
| Native screen size/density | No | Only a Playwright viewport and deviceScaleFactor |
| Backend LAN URL | Declared only | `App.js:16`; no connectivity/run evidence |
| Native Mobile App screenshot/video | No | Evidence came from Chromium at `localhost:8081` |
| Virtual keyboard behavior | No | No keyboard shown; ScrollView source inspection only |
| Touch-target measurement | No | No native measurement/accessibility inspector |
| Successful login/navigation | No | Script never fills/submits Mobile Login |
| Error/loading state | No | Script only navigates and screenshots |

Direct proof of web substitution:

- `scripts/run-gui-execution.js:111-117` creates a Chromium mobile context.
- Line 118 navigates a browser page to `http://localhost:8081`.
- Lines 128-130 capture that web page.
- `frontend-mobile/package.json` was locally modified to add `react-dom` and `react-native-web` immediately before the screenshot.

The screenshot itself is a real React Native Web rendering, not a fabricated bitmap, but the claim that Mobile Login was executed on a real Mobile App target is false. Verdict: **NON_COMPLIANT**.

## 16. Test Summary Recalculation

| Metric | Reported Value | Recalculated Value | Match | Verdict |
|---|---:|---:|---:|---|
| Total screens | 5 | 5 | Yes | COMPLIANT |
| Total checklist items | 58 | 58 | Yes | COMPLIANT |
| Executed | 58 | 58 by stored statuses; 0 item-level runs independently verifiable | Declarative only | UNVERIFIABLE |
| Pass | 40 | 36 | No | NON_COMPLIANT |
| Fail | 18 | 22 | No | NON_COMPLIANT |
| Blocked | 0 | 0 | Yes | Structurally COMPLIANT |
| Not Run | 0 | 0 | Yes | Structurally COMPLIANT |
| Pass rate | 68.97% | 62.07% | No | NON_COMPLIANT |
| Web Frontend Pass/Fail | 16 / 9 | 15 / 10 | No | NON_COMPLIANT |
| Web Admin Pass/Fail | 13 / 9 | 12 / 10 | No | NON_COMPLIANT |
| Mobile Pass/Fail | 9 / 2 | 9 / 2 declared; native run unverified | Count yes; integrity no | UNVERIFIABLE |
| Local bug IDs | 5 | 5 | Yes | Count only |
| Fully verified bugs | Not reported | 0 | No | NON_COMPLIANT |
| Severity | H3 / M1 / L1 | Same declared distribution; packing makes classification unreliable | Partial | PARTIALLY_COMPLIANT |
| IA counts | Coverage summary 14/21/9/14; cross total 11/20/10/17 | 11/20/9/18 | No | NON_COMPLIANT |
| AI_INITIAL | 47 | 48 | No | NON_COMPLIANT |
| HUMAN_ADDED | 11 | 10 | No | NON_COMPLIANT |
| LIVE | 58 | 0 item-level LIVE executions verified | No | NON_COMPLIANT |
| MOCKED | Not reported | No item/group mode recorded | No | NON_COMPLIANT |
| GitHub traceability | PENDING_EXTERNAL_ACTION | 0 verified URLs | Consistent as incomplete | NON_COMPLIANT requirement |
| Completion status | INCOMPLETE due GitHub only | Must be NON-COMPLETE for multiple critical gaps | Partial | PARTIALLY_COMPLIANT |

## 17. AI Critique, Audit and Disclosure Review

### Overall AI Critique

| Criterion | Result | Verdict |
|---|---|---|
| Language | English | COMPLIANT |
| Exact body word count | 276 whitespace-delimited words, excluding title/metadata | COMPLIANT with 200-300; declared 265 is inaccurate |
| Web Login example | Present at line 10 | COMPLIANT |
| Register example | Present at line 12 | COMPLIANT |
| Admin Login example | Present at line 10 | COMPLIANT |
| Category example | Present at line 8 | COMPLIANT |
| Mobile example | Touch target mentioned at line 10 | Minimal / PARTIAL |
| Consistency with final checklist | Claims 3 removals and 11 additions; final retains all raw IDs and has 10 HUMAN_ADDED | NON_COMPLIANT |
| Requirement accuracy | Calls Edit a FR-14 missing feature, contrary to requirement | NON_COMPLIANT |

### AI Audit Report

| Required element | Result | Verdict |
|---|---|---|
| Tool name | Present | COMPLIANT |
| Date/time | Date only; no time/timezone | PARTIALLY_COMPLIANT |
| Full prompt | Missing; one-sentence summary only (`AI_Audit_Report_Task1.md:10`) | NON_COMPLIANT |
| Raw output or path | Path exists; 50 rows | COMPLIANT for existence, provenance unverified |
| Verdict | No explicit audit verdict | NON_COMPLIANT |
| Reasoning | Brief examples only | PARTIALLY_COMPLIANT |
| Student fix | Listed, but several claims conflict with final data | NON_COMPLIANT |
| Complete interaction history | Missing | NON_COMPLIANT |

### AI Disclosure

`AI_Disclosure_Task1.md:5-7` repeats the false 19 revised / 3 removed / 11 added claim and says execution, screenshots, bug verification and GitHub traceability were “fully reviewed” and “executed live.” Direct execution/Git/GitHub/mobile evidence contradicts this. Verdict: **NON_COMPLIANT**.

## 18. Git History Review

### Commands and results

- `git log --oneline --decorate --all`: real HEAD is `671d798 (HEAD -> HW3-Khoa, origin/HW3-Khoa) updts skills`.
- `git status --short --branch`: shows `?? task1-gui/` plus unrelated modified/untracked working files.
- `git log --all --oneline -- task1-gui`: no commits.
- `git ls-files -- task1-gui`: no tracked files.
- `git cat-file -e <declared-hash>^{commit}`: all nine declared hashes return 128/not found.

| Declared hash | Exists as commit? |
|---|---:|
| 3a1b2c4 | No |
| 9f8e7d6 | No |
| 5e4d3c2 | No |
| 1a2b3c4 | No |
| 8f7e6d5 | No |
| 4c3b2a1 | No |
| 7d6c5b4 | No |
| 2b1a0f9 | No |
| 6e5d4c3 | No |

This is not merely an unverifiable handwritten log: `scripts/generate_all_deliverables.py:1401-1412` directly writes those fabricated-looking hashes and messages. The claimed nine-stage process does not exist in Git. Verdict: **NON_COMPLIANT; confirmed fabricated commit-log artifact**.

## 19. Demo Video Review

No demo link appears in `task1-gui/README.md`; no video file or video URL was found in `task1-gui/`. Consequently, ownership, accessibility, Task 1 content, correct SUT and end-to-end skill usage cannot be verified.

README also lacks:

- fixed scope summary;
- execution environment;
- item/status/bug metrics;
- GitHub Issue links;
- demo link;
- final status;
- instructions to open Markdown/Excel/evidence.

Verdict: **NON_COMPLIANT**.

## 20. Validator Review

### Static review

`scripts/validate-gui.ps1` validates:

- existence of 13 fixed mandatory files (`:13-38`);
- existence of five fixed screenshot paths (`:40-57`);
- Markdown lines beginning `| GUI-` and count >=41 (`:59-67`);
- whether the bug report contains `PENDING_EXTERNAL_ACTION` (`:69-79`).

It does **not** validate unique IDs, IA substance, five scopes, Origin values, statuses, Fail fields, evidence-to-failure semantics, bug-report IDs, Excel content, Markdown–Excel equality, Summary metrics, critique word count/content, AI audit/disclosure, Git objects, GitHub URL format/existence, mobile device evidence or demo video. It never calls `exit 1`.

### Execution record

**Command**

```powershell
& 'task1-gui\scripts\validate-gui.ps1'
```

**Exit code:** `0`  
**Standard error:** empty  
**Script result:** `FINAL STATUS: INCOMPLETE`

**Relevant standard output**

```text
[OK] Found README.md
[OK] Found scope-analysis.md
[OK] Found GUI_Checklist_HW3.md
[OK] Found GUI_Checklist_HW3.xlsx
[OK] Found GUI_Coverage_Matrix.md
[OK] Found GUI_Bug_Report_HW3.md
[OK] Found GUI_Test_Summary_HW3.md
[OK] Found AI_Item_Level_Critique.md
[OK] Found AI_Critique_Task1.md
[OK] Found AI_Audit_Report_Task1.md
[OK] Found AI_Disclosure_Task1.md
[OK] Found git-commit-log.txt
[OK] Found ai-output\AI_INITIAL_GUI_Checklist.md
[OK] Found evidence evidence\web-login\BUG-GUI-01_web-login.png
[OK] Found evidence evidence\web-register\BUG-GUI-02_web-register.png
[OK] Found evidence evidence\admin-login\BUG-GUI-03_admin-login.png
[OK] Found evidence evidence\admin-category\BUG-GUI-04_admin-category.png
[OK] Found evidence evidence\mobile-login\BUG-GUI-05_mobile-login.png
[OK] Checklist item count: 58 (>= 41)
[INFO] GitHub issues status is PENDING_EXTERNAL_ACTION (Pending manual student post).
FINAL STATUS: INCOMPLETE
```

The validator did not produce a `COMPLETE` false positive in this run, but it is still **NON_COMPLIANT** because it can be bypassed by placeholder/non-semantic files and signals success to automation via exit code 0.

## 21. Fabrication Risk Review

| Suspicion ID | Evidence | Risk | Confirmed? | Impact |
|---|---|---|---|---|
| S-01 | `git-commit-log.txt`; all hashes absent; `task1-gui/` untracked; generator lines 1401-1412 write the log | Fabricated development history | **Confirmed at artifact level** | Critical; R-30/R-33 fail |
| S-02 | Final Actual/Status values are hard-coded in generator; execution helper has no 58-item assertions/results | Execution results may be source-derived declarations rather than observations | **Confirmed that item-level execution is not evidenced** | Critical; R-12/R-36 fail |
| S-03 | Chromium `page.goto('http://localhost:8081')`; no device/OS/Expo evidence | Web rendering presented as Mobile App execution | **Confirmed** | Critical; Mobile integrity = 0 |
| S-04 | Origin values and reports claim 47/11 while final data is 48/10; no Git human-review stage | HUMAN_ADDED authorship may be reconstructed | Suspicious — requires human verification | High; R-09/R-10 unverifiable |
| S-05 | Scope 00:49:59, raw 00:50:05, critique 00:50:11, screenshots 00:53:37-48, generator 00:54:19, most reports 00:54:25 | Bulk post-generation rather than chronological process | Suspicious — requires human verification | Medium |
| S-06 | Five PNGs decode and visually match EShop/React Native Web | Bitmap fabrication | **Not confirmed** | Images are real captures; over-claiming remains |
| S-07 | No GitHub Issue URL exists | Fabricated GitHub URL | **Not present, therefore not fabricated** | Completion still blocked; verified count 0 |
| S-08 | BUG-GUI-04 claims Edit is required and category-with-products delete errors | Imaginary requirement/behavior | **Confirmed mismatch** | High; invalid checklist/bug content |

This audit does not infer the student’s intent. “Confirmed” refers to objectively false/inconsistent artifact claims, not a judgment about personal misconduct.

## 22. Requirement Compliance Matrix

| ID | Requirement | Evidence Required | Evidence Found | Status | Gap | Required Action |
|---|---|---|---|---|---|---|
| R-01 | SUT is EShop | Requirement/source/artifact identity | Root source and all task headings identify EShop | COMPLIANT | None | None |
| R-02 | Correct Khoa scope | Five fixed screens only, source-backed | All rows within five screens; some imaginary/missing requirement coverage | PARTIALLY_COMPLIANT | FR-14 Edit invention; missing FR-01 Confirm Password; wrong lock threshold | Correct requirement mapping and add missing coverage |
| R-03 | Valid unique count >=41 | Unique, valid, in-scope items | 50 | COMPLIANT | Eight of 58 excluded | Correct/remove excluded items while retaining >=41 |
| R-04 | IA-01 sufficient | Substantive general-UI coverage | 11 rows across 5 screens | PARTIALLY_COMPLIANT | Contrast/accessibility/overflow depth and execution weak | Add measurable, executed IA-01 checks |
| R-05 | IA-02 sufficient | Form behavior and validation | 20 rows across 5 screens | PARTIALLY_COMPLIANT | Missing Confirm Password, email syntax, Enter/focus/visibility states | Add source/requirement-aligned form cases |
| R-06 | IA-03 sufficient | Real navigation behavior | 9 rows, no Category IA-03 | NON_COMPLIANT | Missing Back/Forward/deep link/category/post-delete/focus | Add and execute navigation flows |
| R-07 | IA-04 sufficient | Feedback/state coverage | 18 rows | PARTIALLY_COMPLIANT | Modes and dynamic execution absent; some states false | Execute LIVE/MOCKED state cases with evidence |
| R-08 | AI_INITIAL exists | Raw output and provenance | 50-row raw file exists | PARTIALLY_COMPLIANT | No Git provenance; final ID mapping shifted | Commit and preserve raw output before review |
| R-09 | Human review exists | Item-level review plus history | Critique file exists | UNVERIFIABLE | No real review commit; generator creates final reports | Provide authentic chronological evidence |
| R-10 | HUMAN_ADDED is real | New content and human provenance | 10 labels; 8 new IDs, 2 reused IDs | UNVERIFIABLE | No independent authorship evidence | Preserve diffs/commits and rationale |
| R-11 | Rationale for every human item | Four rationale fields per item | None | NON_COMPLIANT | Entire per-human-item section missing | Add four required fields for each item |
| R-12 | Every item executed | Item-level run record | Status cells only; 0/58 independently verified | NON_COMPLIANT | No item-level execution | Re-run and record each item |
| R-13 | No Not Run | Stored statuses | 0 | COMPLIANT structurally | Execution still unverified | Preserve only after real run |
| R-14 | No Blocked when COMPLETE | Stored statuses/final status | 0; Summary says INCOMPLETE | COMPLIANT structurally | Other blockers remain | Do not mark COMPLETE |
| R-15 | Every Fail has Actual | Checklist fields | All 22 non-empty | COMPLIANT structurally | Some Actuals are false/ambiguous | Replace with observed results |
| R-16 | Every Fail has Notes | Checklist fields | All 22 non-empty | COMPLIANT structurally | Quality varies | Make notes reproducible |
| R-17 | Every Fail has Bug ID | Checklist fields | All 22 map to one of five IDs | COMPLIANT structurally | Over-packed bugs | Split unrelated root causes |
| R-18 | Every Fail has valid screenshot | Existing image that shows failure | Files exist; most dynamic claims not shown | PARTIALLY_COMPLIANT | Five static images for 22 fails | Capture failure-specific evidence |
| R-19 | Complete Markdown bug reports | All mandatory fields/reproducibility | Five incomplete packs | NON_COMPLIANT | Missing URL, reproducibility, lifecycle status; packing | Rewrite/split bug reports |
| R-20 | Real GitHub Issue per bug | Accessible issue URLs | 0 | NON_COMPLIANT | All pending | Post and verify five/split issues |
| R-21 | Screenshots attached to Issues | GitHub attachments | 0 | NON_COMPLIANT | Local links only | Upload actual attachments |
| R-22 | Markdown checklist exists | Non-empty parsable file | Yes | COMPLIANT | None | None |
| R-23 | Excel checklist exists | Openable workbook | Yes | COMPLIANT | None | None |
| R-24 | Markdown and Excel synchronized | Item-level comparison and consistent sheets | Primary 58 rows exact; auxiliary sheets wrong | PARTIALLY_COMPLIANT | Visible workbook metrics contradict rows | Recalculate/remove stale sheets |
| R-25 | Accurate Test Summary | Recalculated metrics | Major mismatches | NON_COMPLIANT | 40/18 vs 36/22; origin/IA/platform wrong | Generate summary from checklist data |
| R-26 | AI Item-Level Critique | Complete item/human review trace | 50 AI rows; missing human rationale, false removal map | PARTIALLY_COMPLIANT | Review does not reconcile to final | Add explicit mappings and human rows |
| R-27 | AI Critique 200-300 words | English, exact count, concrete/consistent | 276 words and concrete examples | PARTIALLY_COMPLIANT | Declares 265; false 3-remove/11-add and FR-14 claims | Correct word count and factual claims |
| R-28 | AI Audit Report | Tool/time/full prompt/output/verdict/reasoning/fix | Brief file with tool/date/raw path | PARTIALLY_COMPLIANT | No full prompt/time/verdict/full log | Supply complete audit trail |
| R-29 | AI Disclosure | Accurate tool/use/human changes | File exists | NON_COMPLIANT | False counts and fully-live claim | Correct disclosure to evidence |
| R-30 | Real Git commit log | Reachable commits and staged process | Nine nonexistent hashes; task untracked | NON_COMPLIANT | Fabricated log artifact | Remove false log; commit authentic stages prospectively |
| R-31 | Real demo video link | Accessible Task 1 video | None | NON_COMPLIANT | Missing | Record/upload/link own demo |
| R-32 | Relative evidence paths | Valid relative links | Checklist/report good; issue drafts use wrong `../../` | PARTIALLY_COMPLIANT | Draft paths resolve incorrectly; no GitHub attachment | Fix local paths and attach externally |
| R-33 | No fabricated external artifact | Real external/process artifacts | Fake commit log; false native/live claim | NON_COMPLIANT | Confirmed artifact-level misrepresentation | Replace with truthful evidence/status |
| R-34 | Correct validator | All listed gates and failing exit code | Weak script; INCOMPLETE with exit 0 | NON_COMPLIANT | Most gates omitted | Implement semantic validation and `exit 1` |
| R-35 | Mobile Login on real Mobile App | Device/OS/Expo evidence and run | Chromium React Native Web only | NON_COMPLIANT | No native run | Run on Expo/emulator/device and capture evidence |
| R-36 | Main flows have LIVE execution | At least one live run per main flow | No complete flow record | NON_COMPLIANT | Register failure only; category static; mobile no submit | Execute and log all five flows |
| R-37 | Mocked states labeled | Per-item/group execution modes | Whole file says LIVE; no mode field/log | NON_COMPLIANT | Network/slow/error provenance absent | Add LIVE/MOCKED/MANUAL/AUTOMATED_SUPPORT mapping |
| R-38 | No duplicates/artificial split | Semantic analysis | 0 duplicate deduction; some compound assertions | COMPLIANT | Diagnosability issue only | Split compound assertions optionally |
| R-39 | Observable/measurable Expected | Deterministic expected outcomes | 50/58 accepted | PARTIALLY_COMPLIANT | Eight excluded | Rewrite/remove eight items |
| R-40 | Final status reflects artifacts | Truthful completion decision | Summary says INCOMPLETE, but attributes only GitHub; Disclosure overclaims completion | PARTIALLY_COMPLIANT | Critical execution/Git/mobile/report gaps omitted | State NON-COMPLETE with all blockers |

## 23. Audit Score

### Weighted score

| Group / Criterion | Max | Awarded | Basis |
|---|---:|---:|---|
| **A. Checklist Design** | **30** | **17.5** | |
| Scope correctness | 5 | 3.0 | Correct screens/routes, but material requirement gaps/mismatches |
| Item count and uniqueness | 7 | 5.5 | 50 valid unique, no duplicate deduction |
| IA coverage | 8 | 4.0 | Four codes present; IA-03 fails quality gate |
| Expected Result quality | 5 | 3.5 | 50/58 accepted; eight invalid/unsupported |
| AI/Human traceability | 5 | 1.5 | Raw file exists; human provenance and counts fail |
| **B. Execution and Evidence** | **30** | **3.0** | |
| All items executed | 8 | 0.0 | 0/58 item-level runs independently verifiable |
| Actual Result quality | 5 | 1.0 | Specific text exists, but is generated/source-derived and sometimes false |
| Fail evidence | 7 | 2.0 | Five real PNGs; most packed/dynamic claims not shown |
| LIVE/MOCKED integrity | 5 | 0.0 | No per-item modes or complete live flows |
| Mobile execution integrity | 5 | 0.0 | React Native Web, not native |
| **C. Bug and External Traceability** | **20** | **5.5** | |
| Bug report quality | 7 | 2.5 | Five partially corroborated packs; missing required fields |
| Checklist↔Bug traceability | 5 | 3.0 | All Fail IDs map locally, but packs omit linked claim details |
| Real GitHub Issues | 5 | 0.0 | Zero URLs |
| Screenshots attached to Issues | 3 | 0.0 | Zero |
| **D. Reports and Process** | **20** | **5.5** | |
| Markdown/Excel consistency | 4 | 3.0 | Primary rows exact; auxiliary sheets false |
| Test Summary accuracy | 3 | 0.0 | Major metric mismatch |
| AI Audit | 4 | 1.5 | Files/raw path exist; trail incomplete |
| AI Critique and Disclosure | 3 | 1.0 | Word range met; material factual contradictions |
| Git commits | 3 | 0.0 | Fake log; task untracked |
| Validator and demo | 3 | 0.0 | Weak validator, no video |
| **Raw score** | **100** | **31.5** | |

### Critical penalties/caps

| Penalty condition | Applied result |
|---|---|
| Fabricated GitHub URL | Not applicable: no URL was supplied; GitHub traceability already scores 0 |
| Fabricated evidence bitmap | Not established; PNGs are real captures |
| Fabricated/false Mobile execution | Mobile execution score fixed at 0; final cannot be COMPLETE |
| Valid unique count <41 | Not applicable; audited count = 50 |
| Not Run/Blocked remain | Stored count = 0/0, but execution itself is not verified |
| Bug lacks real GitHub URL | Final cannot be COMPLETE; GitHub sections score 0 |
| Fabricated commit log | Git process score fixed at 0; R-30/R-33 fail |

No additional double-subtraction was applied after the relevant criterion was reduced to zero.  
**Final audit score: 31.5/100.**

## 24. Blocking Issues

1. `task1-gui/` has no real Git history; `git-commit-log.txt` is generated from nonexistent hashes.
2. No item-level execution record proves the 58 Pass/Fail statuses.
3. Main live flows are not demonstrated end-to-end.
4. Mobile Login was rendered in Chromium/React Native Web, not executed on a native Mobile App target.
5. No real GitHub Issue URL or issue screenshot attachment exists.
6. Evidence is insufficient for most dynamic Fail claims.
7. Test Summary and coverage/origin metrics are materially incorrect.
8. IA-03 lacks substantive coverage, particularly for Category Management.
9. Human-added provenance and per-item human rationale are absent/unverifiable.
10. Eight checklist items have invalid/unsupported Expected Results, including an imaginary FR-14 Edit requirement.
11. Demo video/link is absent and README is incomplete.
12. Validator omits required gates and exits 0 on incomplete results.

## 25. Required Corrections

Before the deliverable may be considered COMPLETE:

1. Remove the false commit-log claims. Commit the actual artifacts prospectively in a transparent sequence; do not invent retrospective hashes.
2. Correct the checklist against requirements/source:
   - lockout at three attempts/30 seconds;
   - add Confirm Password coverage;
   - remove or re-require Category Edit;
   - correct category deletion/duplicate expectations;
   - rewrite all eight excluded Expected Results.
3. Split compound bug/checklist assertions where unrelated outcomes need separate reproduction/evidence.
4. Execute all 58 retained items for real and capture an item-level log with timestamp, environment, test data, Actual, Status and execution mode.
5. Run at least one genuine LIVE integration flow for Web Login, Web Register, Admin Login, Category add/view/delete and Mobile Login.
6. Label MOCKED/MANUAL/AUTOMATED_SUPPORT cases explicitly; do not label source inspection as LIVE execution.
7. Run Mobile Login on Expo Go, an emulator or a physical device and record device model, Android/iOS version, screen size, backend LAN URL, keyboard/touch/focus behavior and post-login navigation.
8. Capture failure-specific evidence that visibly demonstrates every Fail; preserve relative local paths.
9. Rewrite/split bug reports with every mandatory field, reproducibility and one coherent root cause.
10. Create real GitHub Issues, upload screenshots as actual attachments, add labels, and store each real issue URL. This step is `PENDING_EXTERNAL_VERIFICATION`.
11. Recalculate Summary, Coverage and Excel auxiliary sheets directly from final checklist data.
12. Rebuild AI traceability:
    - preserve raw output;
    - map every revised/removed ID;
    - explain each HUMAN_ADDED item using all four required rationale fields;
    - correct AI_INITIAL/HUMAN_ADDED counts;
    - correct Critique, Audit Report and Disclosure claims.
13. Add a real Task 1 demo video link and complete README with scope, environment, counts, bugs, issues, final status and opening instructions.
14. Replace the validator with semantic Markdown/Excel/Git/evidence/GitHub/mobile/report checks and return non-zero on any failed completion gate.
15. Re-run an independent audit after corrections. Do not simply change status cells to make the validator pass.

## 26. Final Audit Result

The artifact set has substantial checklist design content and five real screenshots, and it meets the numerical valid-item threshold. Those strengths do not overcome the critical failures in execution integrity, native Mobile verification, Git history, GitHub traceability, report accuracy and validator effectiveness.

**AUDIT RESULT: NON-COMPLIANT**

AUDIT FINAL STATUS: NON_COMPLIANT

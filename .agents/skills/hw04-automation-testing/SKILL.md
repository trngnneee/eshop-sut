---
name: hw04-automation-testing
description: Complete the "HW04 - Automation Testing" homework (EShop SUT) end to end - selecting features, writing 12+ test cases per feature, driving Playwright automation script generation step-by-step (never one generic prompt), building data-driven CSV/JSON test data, configuring multi-browser runs with an HTML report stamped "Run by: {StudentID}", performing the mandatory human review / gap analysis of AI output, filing bug reports, and producing the AI Audit Report, AI Critique, README, and submission package required by the course. Use this whenever the user mentions HW04, "automation testing homework", EShop SUT, Playwright/Selenium test automation for a course assignment, an AI Audit Report, or asks to "do my automation testing homework" - even if they only paste the PDF or describe the task loosely.
---

# HW04 — Automation Testing (EShop SUT)

This skill operationalizes the HW04 assignment. It is a *workflow* skill: it does not
write all the scripts in one shot. The assignment explicitly forbids a single generic
prompt ("write all the automation scripts for this feature") — every artifact must be
produced through a disciplined, step-by-step, human-reviewed process, and that process
itself must be logged. This skill enforces that discipline.

Read the whole file before starting; the steps depend on each other (test data files
feed the scripts, the reporter config feeds the HTML report, the audit log feeds the
final report).

## 0. Collect the parameters up front

Before doing anything, get these from the user (ask only for what's missing — don't
re-ask if already given or inferable from context):

- **Student ID** (used to stamp `"Run by: {StudentID}"` in every HTML report)
- **Three features**, one each from Pool A, Pool B, Pool C (see `references/feature_pools.md`
  for the full FR list). If the user completed HW02, reuse those three; otherwise they
  must self-declare and state why HW02 is unavailable.
- **Tool stack**: Playwright (recommended) or Selenium 4+; Allure or the Playwright
  HTML reporter. Default to **Playwright + built-in HTML reporter** unless told otherwise
  — it needs the least setup to hit the "Run by: {StudentID}" + ISO timestamp requirement.
- **Repo location**: an existing `eshop-sut` clone/path, or "not cloned yet."
- **Which AI tool is "in use"**: for this session, that's Claude itself. Every
  interaction in this conversation counts as an auditable AI interaction — log it (see §6).

## 1. Scaffold the project (once, before feature work)

```
hw04-automation/
├── playwright.config.js        # from assets/playwright.config.template.js
├── package.json                 # from assets/package.json.template
├── data/                        # one file per feature, data-driven test data
├── tests/                       # one .spec.js file per feature
├── reports/                     # generated HTML reports land here (gitignored per-run,
│                                 # but the final ones for submission are kept)
└── docs/
    ├── report.md                 # main automation report (references/report_template.md)
    ├── ai-audit-report.md        # references/ai_audit_template.md
    ├── ai-critique.md            # 200-300 words, see §8
    ├── bug-report.md
    └── README.md                 # references/readme_template.md
```

Copy `assets/playwright.config.template.js` into `playwright.config.js` and replace
`{{STUDENT_ID}}` with the real student ID — this is what stamps every HTML report with
`Run by: {StudentID}` plus an ISO timestamp (a hard, TA-verified requirement in §11 of
the brief). Copy `assets/package.json.template` and adjust the project name.

## 2. Per feature: design the test cases FIRST, before touching the AI for code

For **each** of the three features, do this in order — do not skip to code generation:

1. Read the feature's functional requirement carefully (see `references/feature_pools.md`).
2. Design **at least 12 test cases** by hand or with AI help, covering a mix of
   positive, negative, and edge cases (any mix counts, but a suite of all-positive
   cases will read as shallow in review — aim for genuine variety: boundary values,
   invalid input, empty/duplicate data, state transitions, permission checks, etc.).
3. Write the test cases into a plain markdown/table list first — use
   `references/test_case_template.md` — this becomes both the traceability artifact
   in the final report and the literal thing you feed to the AI step by step in §3.
   Log this as the AI Audit interaction if the AI helped design them (see §6) — even
   test-case design counts as an "AI interaction" that must be logged.
4. Extract the test **data** (inputs/expected outputs) into `data/{feature}.csv` or
   `data/{feature}.json`. Hardcoded arrays inside the spec file are explicitly not
   accepted by the grader — this file must exist standalone and be imported.

## 3. Drive the AI through script generation step by step

The grading criteria explicitly penalize a single "write all the scripts" prompt. Work
through each test case (or small batches of related cases) in separate turns:

1. **Step A — scaffold**: ask for the page object / locators for the feature first,
   nothing else. Review the selectors before proceeding (see §5 for what "review"
   means).
2. **Step B — one behavior at a time**: for each test case or small group, prompt for
   just that test's automation, referencing the actual selectors/data file from Step A.
   Don't paste the whole test-case list into one mega-prompt.
3. **Step C — assertions pass**: explicitly ask for the assertion(s) for that case, and
   require **at least 3 distinct assertion patterns** across the suite as a whole (e.g.
   `toHaveText`, `toBeVisible`, `toHaveURL`, custom API/DB state checks, screenshot
   diffing, response-status checks — mix these, don't repeat one pattern 12 times).
4. **Step D — wire to data file**: convert any inline literals to reads from the
   `data/{feature}.csv|json` file (Playwright: iterate with `for (const row of data)`
   inside `test.describe`, or use `test.each`-style loops).

Log every one of these interactions per §6 as you go — don't try to reconstruct the log
afterward from memory.

## 4. Multi-browser execution

Each feature's spec must run on all 3 target browsers (Chromium/Firefox/WebKit, or
Chrome/Edge/Firefox), so 3 features × 3 browsers = **at least 9 browser runs**. In
Playwright this is `projects: [...]` in the config (already scaffolded in
`assets/playwright.config.template.js`). Run:

```bash
npx playwright test --reporter=html
npx playwright show-report reports/
```

Confirm the generated `reports/index.html` visibly shows `Run by: {StudentID}` and an
ISO timestamp somewhere in the title/header/footer — this is a hard, machine-checked
requirement, so open the file and actually look, don't assume the config worked.

## 5. Human review and gap analysis (mandatory, do not skip)

For each feature, after the suite runs, critically review what the AI produced. Write
this into `docs/report.md` under each feature. Look specifically for:

- **Fragile selectors** (text-based or nth-child selectors that will break vs.
  `data-testid`/role-based locators)
- **Weak or missing assertions** (e.g. only checking `toBeVisible` when the test claims
  to verify a value)
- **Missing edge cases** the AI didn't think of even though you asked
- **Flaky waits** (hardcoded `sleep`/`waitForTimeout` instead of proper auto-waiting or
  explicit state waits)

For each issue found: fix it, then write one or two sentences on **why** the AI likely
missed it (ambiguous prompt, insufficient context about the app's DOM, a generic
model tendency to over-trust happy-path flows, etc.). This section is graded — a report
that says "everything was perfect" will read as not having actually reviewed anything.

## 6. AI Audit Report — log as you go

Use `references/ai_audit_template.md`. For every AI interaction across §2–§5, append an
entry with: tool name, date/time, the prompt used, and the AI's output (or a faithful
summary if the output is long — link to the diff/commit instead of pasting hundreds of
lines). Do this immediately after each interaction, not retroactively; retroactive logs
are usually incomplete and read as such.

If the user says they did NOT use AI for some part, the declaration must say so
explicitly per the brief's required wording — see the template for the exact phrasing.

## 7. Bugs found

Whenever a failing assertion reveals a genuine product defect in EShop (not a flaky
test or bad selector — an actual bug), file it using the standard bilingual bug
template, in both places, with matching content:

- **On GitHub**: copy `assets/.github/ISSUE_TEMPLATE/bug_report.md` into the repo at
  `.github/ISSUE_TEMPLATE/bug_report.md` (once, at project setup) so "New Issue" offers
  it automatically. File one Issue per bug with a screenshot attached, using that exact
  template — this is the single source of truth for bug reports, don't maintain a
  separate local copy. Required fields: Found by Test Case, Requirement liên quan (the
  FR-xx it relates to), Severity/Priority (Critical/Major/Minor/Trivial and P0/P1/P2),
  Environment (OS/Browser/URL/Build), Steps to reproduce, Expected result, Actual
  result, Evidence.
- In the main report (§9), just link each filed Issue rather than re-typing its
  contents — see the Feature section's "Bugs Found" table in `references/report_template.md`.
- Note any test case that could not be automated at all and explain why (e.g. requires
  manual email verification, CAPTCHA, etc.) directly in `docs/report.md`.

## 8. AI Critique (200–300 words)

Write this last, after all three features are done, so it reflects the whole suite —
not one feature. It must answer: where the AI was wrong/biased/incomplete, why it
likely failed to catch the issue, and what principle was learned about collaborating
with AI. Keep it to 200–300 words — check the word count before finalizing.

## 9. README and submission package

Fill `references/readme_template.md` with the self-assessment table and the test
summary (feature count; test cases automated/executed/passed/failed; browser run
count; bug count; demo video link). Then assemble the submission zip per §14 of the
brief:

```
<StudentID>_HW04_AI_Automation_<SelfAssessedGrade>.zip
```
containing: main report (md+pdf), GitHub repo link, multi-browser HTML reports, demo
video link, AI Critique + AI Audit Report (md+pdf), git commit log (text file), bug
report with screenshots, README.md, and any supporting materials. Converting the
markdown report to PDF can be done with the `docx`/`pdf` skills if available.

## 10. Things this skill will NOT fabricate

Per the assignment's Anti-AI-Cheat Constraints (§11 of the brief), the HTML reports'
"Run by" + timestamp and the demo video's narration/face-cam/`whoami`+`hostname`
evidence must be **real, attributable execution evidence**. This skill will scaffold
configs and prompts to make producing that evidence easy, but it will not claim a run
happened, invent report contents, or write video-narration transcripts as if they were
already recorded — actually run the suite and record the video.

## Reference files

- `references/feature_pools.md` — full FR-01..FR-19 list by pool, for feature selection
- `references/ai_audit_template.md` — AI Audit Report format + example entry
- `references/report_template.md` — main report skeleton (per-feature sections matching §2–§5)
- `references/test_case_template.md` — test case design table (fill before generating scripts)
- `references/readme_template.md` — README with self-assessment table + summary stats
- `assets/.github/ISSUE_TEMPLATE/bug_report.md` — GitHub Issue template for filing bugs (bilingual VN/EN)
- `assets/playwright.config.template.js` — multi-browser config with `Run by:` stamping
- `assets/package.json.template` — minimal Playwright project setup
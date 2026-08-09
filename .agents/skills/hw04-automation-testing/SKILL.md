---
name: hw04-automation-testing
description: Complete the "HW04 - Automation Testing" homework (EShop SUT) for a single functional requirement (FR) end to end - just give the FR code/name (e.g. "FR-08 Checkout") and this skill runs the full pipeline (spec analysis -> test case design -> test data -> locators/page object -> automation scripts), pausing after each stage to log that stage's AI Audit entry and wait for the user's review/go-ahead before continuing. Also covers multi-browser HTML reports stamped "Run by: {StudentID}", bug filing via the repo's GitHub issue template, the AI Critique, and final submission packaging. Use this whenever the user mentions HW04, "automation testing homework", EShop SUT, an FR code for this course, or asks to test/automate a specific feature for this assignment.
---

# HW04 — Automation Testing (EShop SUT)

This skill runs a **gated pipeline per FR**: give it one feature requirement, it walks
through 4 stages in order, and after **every stage** it (a) writes that stage's AI
Audit Report entry, (b) shows the stage's output, and (c) **stops and asks whether to
continue** to the next stage. It never jumps ahead on its own — the assignment's
"human review" requirement means each stage's output must be looked at before the next
stage builds on it.

## 0. One-time setup (do this once per assignment, not per FR)

Ask only for what's missing (don't re-ask anything already established earlier in the
conversation):

- **Student ID** — stamps `"Run by: {StudentID}"` in every HTML report.
- **Tool stack** — default: Playwright + JavaScript + built-in HTML reporter (see
  `assets/playwright.config.template.js`, `assets/package.json.template`), unless the
  user asked for Selenium or Allure.
- **Repo location** — an existing `eshop-sut` clone/path, and whether spec docs
  (`README.md`, API docs, DB schema, etc.) are available to read from it. This skill
  needs to actually read the repo's spec files in Stage 1 — if the repo isn't cloned
  yet or docs aren't accessible, ask the user to provide the relevant spec text instead
  of guessing at the feature's behavior.

Scaffold the project if it doesn't exist yet:

```
hw04-automation/
├── playwright.config.js         # from assets/playwright.config.template.js
├── package.json                  # from assets/package.json.template
├── data/                         # one file per feature
├── tests/                        # one .spec.js file per feature
├── reports/                      # generated HTML reports
└── docs/
    ├── report.md                  # references/report_template.md
    ├── ai-audit-report.md         # references/ai_audit_template.md
    ├── ai-critique.md             # 200-300 words, written last, see §7
    └── README.md                  # references/readme_template.md
```

Replace `{{STUDENT_ID}}` in `playwright.config.js` with the real ID.

Also copy `assets/.github/ISSUE_TEMPLATE/bug_report.md` into the repo's
`.github/ISSUE_TEMPLATE/` once, so bug filing later (§6) is ready to use.

## 1. How to invoke: just give the FR

When the user says something like **"FR-08 Checkout"**, **"làm FR-02 Login giúp
tôi"**, or **"automate FR-15 Product management"**, run the pipeline below for that
FR, starting at Stage 1. Track which FR (of the three chosen) this is — Feature A, B,
or C — so output lands in the right section of `docs/report.md`.

If Pool A/B/C selection hasn't happened yet, resolve that first per
`references/feature_pools.md` before starting the pipeline.

### The stop-and-review contract (applies to every stage below)

After finishing a stage:
1. Append the AI Audit Report entry for that stage's interaction(s) to
   `docs/ai-audit-report.md` immediately (format: `references/ai_audit_template.md`).
2. Present the stage's output to the user in full (the test case table, the data file
   contents, the locators, or the generated script).
3. **Stop.** End your turn with something like: *"Stage N done and logged. Review the
   above — want me to continue to Stage N+1 (`<name>`), or change anything first?"*
4. Do not start the next stage until the user replies affirmatively (or with edits to
   apply first). If they ask for changes, apply them, re-log the correction as a new
   audit entry (don't silently edit the log), and ask again before moving on.

---

### Stage 1 — Spec analysis

Read the FR's actual behavior from the repo before designing anything:
- Search the `eshop-sut` repo's `README.md` and any docs/spec files for the FR's
  description, related routes/pages, and business rules (e.g. lockout thresholds,
  coupon rules, CRUD constraints, validation rules).
- If the repo isn't accessible, ask the user to paste the relevant spec section rather
  than inventing behavior — don't guess business rules that affect assertions later.
- Summarize: what the feature does, the UI flow, key business rules, and anything
  ambiguous or undocumented that will need a judgment call in test design.

This summary goes into `docs/report.md` under the feature's section (see
`references/report_template.md`) as a short "Spec Summary" note, and is the AI Audit
entry's "output" for this stage.

### Stage 2 — Test case design (≥12) + test data file

- Design **at least 12 test cases** using `references/test_case_template.md` — genuine
  mix of positive/negative/edge (boundary values, invalid input, empty/duplicate data,
  permission/state checks), grounded in the Stage 1 spec summary, not generic guesses.
- Write the test cases in both forms:
  1. a feature-level summary file at `docs/test-cases/FR-xx-test-cases.md`; and
  2. one standalone Markdown file per test case at
     `docs/test-cases/TC-FRxx-NN.md`, containing that case's metadata, steps,
     expected result, and suggested assertions.
- Extract the test data referenced by those cases into `data/{feature}.csv` or
  `data/{feature}.json` — this file is what the automation scripts will read from in
  Stage 4; hardcoded inline arrays in the script are not accepted per the assignment.
- Each test case's "Test Data (ref)" column must point to a row/key in that data file.

### Stage 3 — Locators / page object

- Generate the page object (locators for every element the 12 test cases interact
  with), based on the actual DOM of the feature's page(s) — ask the user to provide
  the relevant HTML/selector info if not already available, don't invent selectors
  blind.
- Prefer role-based or `data-testid` locators over text/CSS-position locators, since
  text-based selectors are a common AI-generated-script weakness the review step (§5)
  will need to catch.

### Stage 4 — Automation script generation

- Using the Stage 2 test cases, Stage 2 data file, and Stage 3 locators, generate the
  Playwright spec (`tests/{feature}.spec.js`) that loops over the data file and covers
  all 12+ cases.
- Use **at least 3 distinct assertion patterns** across the spec (e.g. `toHaveText`,
  `toHaveURL`, `toBeVisible` combined with a value check, an API/response-status check,
  etc.) — don't repeat one pattern for every case.
- This is the heaviest stage; it's fine to work through it in a few sub-turns internally
  (e.g. happy-path cases, then negative cases, then edge cases) rather than one giant
  generation — but only pause-and-ask-the-user once, at the end of the whole stage, not
  after every sub-turn. Log each sub-turn as its own AI Audit entry regardless.

---

## 2. After Stage 4 is approved: run, review, report

These happen once per FR, after the user has signed off on Stage 4's scripts — they are
not part of the gated pipeline above (no need to log/pause after each of these, but do
still update the report and audit log as you go).

### 2.1 Run multi-browser and check the report stamp

```bash
npx playwright test tests/{feature}.spec.js --reporter=html
npx playwright show-report reports/html
```

Confirm `reports/html/index.html` visibly shows `Run by: {StudentID}` + an ISO
timestamp. If not obviously visible, run `npm run stamp-report` (injects a banner via
`scripts/stamp-report.js`).

### 2.2 Human review / gap analysis (mandatory)

Now — with real execution results in hand — critically review what the AI produced
across Stages 3–4: fragile selectors, weak/missing assertions, missed edge cases, flaky
waits. For each issue found: fix it, and write one or two sentences on *why* the AI
likely missed it. Write this into `docs/report.md` §2.5 (per
`references/report_template.md`) for this feature.

### 2.3 Bugs found

If a failing assertion reveals a genuine EShop defect (not a flaky test or bad
selector), file a GitHub Issue using `.github/ISSUE_TEMPLATE/bug_report.md`, attach a
screenshot, and reference it from the feature's "Bugs Found" table in `docs/report.md`
— that Issue is the single source of truth, don't duplicate its content elsewhere. Note
any test case that couldn't be automated and why.

### 2.4 Move to the next FR

Once Feature A (or B, or C) is fully wrapped up (scripts run, reviewed, bugs filed),
tell the user this FR is complete and ask which FR to start next — then restart the
gated pipeline from Stage 1 for it.

---

## 3. After all three FRs are done

### 3.1 AI Critique (200–300 words)

Write this last, reflecting the whole suite (all three FRs), into `docs/ai-critique.md`.
Must answer: where the AI was wrong/biased/incomplete, why it likely failed to catch
the issue, and what principle was learned about collaborating with AI. Check the word
count (200–300) before finalizing.

### 3.2 README and submission package

Fill `references/readme_template.md` (self-assessment table + test summary: feature
count, test cases automated/executed/passed/failed, browser run count, bug count, demo
video link). Then assemble the submission zip per the brief's §14:

```
<StudentID>_HW04_AI_Automation_<SelfAssessedGrade>.zip
```
containing: main report (md+pdf), GitHub repo link, multi-browser HTML reports, demo
video link, AI Critique + AI Audit Report (md+pdf), git commit log (text file), any
bug-related materials, README.md, and other supporting materials. Use the `docx`/`pdf`
skills for markdown→PDF conversion if available.

## 4. What this skill will not fabricate

Per the assignment's Anti-AI-Cheat Constraints, the HTML reports' "Run by" + timestamp
and the demo video's narration/face-cam/`whoami`+`hostname` evidence must be real,
attributable execution evidence. This skill scaffolds configs/prompts to make producing
that evidence easy, but will not claim a run happened or invent report contents —
actually run the suite and record the video.

## Reference files

- `references/feature_pools.md` — full FR-01..FR-19 list by pool, for feature selection
- `references/test_case_template.md` — test case design table (Stage 2)
- `references/ai_audit_template.md` — AI Audit Report format + example entry (every stage)
- `references/report_template.md` — main report skeleton (per-feature sections)
- `references/readme_template.md` — README with self-assessment table + summary stats
- `assets/.github/ISSUE_TEMPLATE/bug_report.md` — GitHub Issue template for bugs (bilingual VN/EN)
- `assets/playwright.config.template.js` — multi-browser config with `Run by:` stamping
- `assets/package.json.template` — minimal Playwright project setup
- `scripts/stamp-report.js` — injects a visible "Run by: {StudentID}" banner into the HTML report if the reporter's metadata panel isn't obviously visible

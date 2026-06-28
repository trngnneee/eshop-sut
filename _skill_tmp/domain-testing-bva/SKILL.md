---
name: domain-testing-bva
description: >
  A Cursor Agent skill that applies Domain Testing and Boundary Value Analysis
  (BVA) techniques to any software feature. Use this skill whenever the user
  wants to design test cases using domain testing, equivalence partitioning,
  or boundary value analysis — especially for web/mobile features, form
  fields, e-commerce flows, or any numeric/string input. Triggers on phrases
  like "apply domain testing", "generate BVA test cases", "equivalence
  partitioning", "boundary analysis", "test this feature with domain testing",
  or any homework/assignment referencing HW02-style testing tasks.
  Always use this skill before writing any test case table or test plan.
---

# Domain Testing & Boundary Value Analysis Skill

This skill guides Claude through the **complete, step-by-step** methodology
for Domain Testing (DT) and Boundary Value Analysis (BVA) as taught in
software testing courses (ISTQB-aligned). It is designed for use on
real-world Systems Under Test (SUT) such as EShop or similar applications.

> ⚠️ **AI-First but Human-Reviewed**: Claude produces all artefacts; the
> student must review every result and correct any errors before submission.

---

## Workflow Overview

```
1. Understand the Feature
2. Identify Input Variables
3. Partition into Equivalence Classes  ← Domain Testing
4. Apply On/Off/In/Out Point Strategy  ← BVA
5. Combine into Test Cases (OCSN matrix)
6. Execute & Report Bugs
7. AI Gap Analysis
8. Generate AI Audit Log entry
```

Read `references/dt-theory.md` for the full theoretical background before
executing any step.

---

## Step 1 — Understand the Feature

Ask the user for (or read from context):
- Feature ID and name (e.g., FR-01 Account Registration)
- A URL or description of the SUT
- Any specification, wireframe, or acceptance criteria

Fetch the SUT's GitHub repository README if a link is provided. Look for:
- Input fields and their data types
- Business rules (min/max length, allowed characters, required fields)
- Expected success and failure messages

**Output**: A numbered list of all identified input variables with their
data types and known constraints.

---

## Step 2 — Identify Input Variables & Constraints

For each input field, document:

| # | Variable | Type | Constraints |
|---|----------|------|-------------|
| 1 | email | string | required, RFC 5322 format, max 254 chars |
| 2 | password | string | 8–32 chars, ≥1 uppercase, ≥1 digit |
| … | … | … | … |

If constraints are **not documented**, make reasonable assumptions and
**flag them explicitly** (these become investigation notes in the bug report).

---

## Step 3 — Domain Testing: Equivalence Partitioning

For each variable, define equivalence classes. Follow this structure:

### Valid Classes (should be accepted)
- Typical/nominal value in the middle of the valid range
- Edge of the valid range (covered more precisely in BVA)

### Invalid Classes (should be rejected)
- Below minimum
- Above maximum
- Wrong type / format
- Empty / null / whitespace-only
- Special characters (if restricted)
- SQL injection / XSS payload (security class)

**Rule**: Each class must be **mutually exclusive** and **collectively
exhaustive** for the domain they cover.

Use the template in `references/dt-theory.md → Equivalence Class Table`.

---

## Step 4 — BVA: On/Off/In/Out Points

For **every numeric or length-bounded variable**, generate the 4-point set:

| Point | Definition | Example (len 8–32) |
|-------|-----------|-------------------|
| **ON** | Exactly on the boundary | 8, 32 |
| **OFF** | One step outside the boundary | 7, 33 |
| **IN** | Well inside the valid range | 20 (midpoint) |
| **OUT** | Well outside the invalid range | 1, 100 |

For **string length**: unit = 1 character.
For **numeric values**: unit = 1 (integer) or smallest increment (float).
For **dates**: unit = 1 day.
For **sets/enums**: ON = valid member, OFF = non-member.

> Read `references/bva-points.md` for worked examples on different data types.

---

## Step 5 — Build the Test Case Table

Combine equivalence classes and BVA points into a unified test case table.

### Test Case ID Convention
```
TC-<FR>-DT-<seq>   (domain testing cases)
TC-<FR>-BVA-<seq>  (boundary value cases)
```
Example: `TC-FR01-DT-001`, `TC-FR01-BVA-003`

### Required Columns

| TC ID | Description | Preconditions | Input Data | Expected Result | Actual Result | Status |
|-------|-------------|---------------|------------|-----------------|---------------|--------|

- **Preconditions**: system state before the test (e.g., "user not logged in")
- **Input Data**: concrete values (never abstract like "valid email" — use
  `alice@example.com`)
- **Expected Result**: precise observable outcome
- **Actual Result**: filled during execution
- **Status**: Pass / Fail / Not Executed

### Coverage Targets
- At minimum **one test per equivalence class**
- At minimum **one test per BVA point per variable**
- Add combination tests when two variables interact (e.g., valid email +
  invalid password)

> Run `scripts/generate_tc_table.py` to scaffold the Markdown table
> automatically from a JSON variable definition file.

---

## Step 6 — Execution & Bug Reporting

### Executing Tests
1. Set up the SUT locally or access the deployed instance.
2. Run each test case in order; record Actual Result and Status.
3. Screenshot every **Fail** result immediately.

### Bug Report Format (per bug)

```markdown
## BUG-<FR>-<seq>: <Short Title>

| Field        | Value |
|--------------|-------|
| Related TC   | TC-FR01-DT-005 |
| Severity     | Critical / Major / Minor / Trivial |
| Priority     | High / Medium / Low |
| Steps to Reproduce | 1. … 2. … 3. … |
| Expected     | … |
| Actual       | … |
| Screenshot   | ![screenshot](./screenshots/bug-01.png) |
| GitHub Issue | https://github.com/…/issues/<n> |
```

Post each bug to the team's GitHub Issues page with the screenshot attached.

---

## Step 7 — AI Gap Analysis

After reviewing all AI-generated test cases, document:

1. **Missed test cases**: cases the AI did not generate that you added
   manually. For each one:
   - The TC ID you added
   - Why the AI missed it (prompt quality / AI limitation / feature complexity)

2. **Incorrect cases**: cases the AI generated with wrong expected results.
   - The original AI output
   - Your corrected version
   - Root cause of AI error

Use the template in `references/gap-analysis-template.md`.

---

## Step 8 — AI Audit Log Entry

At the end of each AI session, generate an audit entry:

```markdown
### AI Audit Entry — <Feature ID>

| Field       | Value |
|-------------|-------|
| Tool        | Claude Sonnet 4.6 / ChatGPT-4o / … |
| Date & Time | YYYY-MM-DD HH:MM (UTC+7) |
| Task        | Domain Testing / BVA / Bug Report |

**Prompt used:**
> (paste the exact prompt you sent)

**AI Output Summary:**
> (brief description of what the AI produced)

**Human Corrections Made:**
> (list changes you made after reviewing the output)
```

---

## Output Artefacts Checklist

- [ ] `report.md` — Main report with DT section and BVA section
- [ ] `test-cases-DT.md` — Domain Testing test case table
- [ ] `test-cases-BVA.md` — BVA test case table
- [ ] `bug-report.md` — All bugs with screenshots
- [ ] `ai-audit.md` — AI Audit Report (mandatory appendix)
- [ ] `ai-critique.md` — 200–300 word AI critique
- [ ] `git-log.txt` — Git commit log (one commit per feature step)
- [ ] `README.md` — Self-assessment table + test summary

---

## Reference Files

| File | When to Read |
|------|-------------|
| `references/dt-theory.md` | Before Step 3 — full EP theory & worked example |
| `references/bva-points.md` | Before Step 4 — BVA point types with examples |
| `references/gap-analysis-template.md` | Step 7 — AI gap analysis template |
| `references/report-structure.md` | When generating the final Markdown report |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate_tc_table.py` | Scaffold TC table from variables JSON |
| `scripts/audit_log_extractor.py` | Extract AI audit info from conversation |
| `scripts/bug_report_formatter.py` | Format bug entries and push to GitHub |

# Skill: Decision Table + Pairwise Test Design Agent

## Purpose
Use this skill to analyze one EShop feature, build a full decision table, remove impossible or redundant rules, apply pairwise reduction on the remaining valid combinations, and generate Markdown deliverables for Test Design, Test Cases, Test Run, Bug Report, Traceability Matrix, and AI Audit.

## Input Required
Ask the user for these inputs if they are missing:

```yaml
feature_id: "FR-XX"
feature_name: "<Tên chức năng>"
module: "<Web User | Web Admin | Mobile | API>"
requirement_text: "<Mô tả FR / user story / acceptance criteria>"
scope:
  in_scope:
    - "<luồng hoặc màn hình/API được test>"
  out_scope:
    - "<phần không test>"
actors:
  - "<Guest | User | Admin | ...>"
interfaces:
  - "<UI route hoặc API endpoint>"
known_constraints:
  - "<ràng buộc nghiệp vụ, role, trạng thái, dữ liệu>"
test_environment:
  browser_or_device: "<Chrome / Android Emulator / ...>"
  base_url: "<URL>"
  build_or_commit: "<commit hash nếu có>"
```

## Core Rules
1. Do not output a generic list of test cases immediately.
2. First extract conditions, actions, constraints, and assumptions.
3. Build the full decision table before pairwise reduction.
4. Do not merge two rules if they have different expected results.
5. Do not delete security, authorization, validation, or destructive-operation cases only because pairwise did not select them.
6. Pairwise reduces interaction combinations, not boundary values. Boundary values and invalid classes must still be explicitly represented where relevant.
7. Every generated test case must trace back to at least one decision rule ID and one requirement ID.
8. Every failed test case must be linkable to a bug report using `Found by Test Case` and `Related Bug`.

## Workflow

### Step 1 — Requirement Analysis
Create `tests/test-design/<FR-ID>/01-requirement-analysis.md`.

Output:
- Feature summary
- Actors and permissions
- Entry points: UI routes / API endpoints
- Preconditions
- Postconditions
- Data entities affected
- In-scope and out-of-scope
- Assumptions that need human confirmation

### Step 2 — Condition / Action Model
Create `tests/test-design/<FR-ID>/02-condition-action-model.md`.

Extract conditions as factors. For each factor, define values.

Condition table format:

| Condition ID | Condition / Factor | Values | Source / Reason | Risk |
|---|---|---|---|---|
| C01 | User authentication state | Logged in / Not logged in | Requirement | High |
| C02 | Role | User / Admin / Guest | Authorization rule | High |

Action table format:

| Action ID | Action / Expected Behavior | When triggered |
|---|---|---|
| A01 | Allow operation | Valid rule |
| A02 | Reject and show validation error | Invalid input |

### Step 3 — Full Decision Table
Create `tests/test-design/<FR-ID>/03-decision-table-full.md`.

Rules:
- If all conditions are Boolean, total theoretical rules = `2^n`.
- If conditions have discrete values, total theoretical rules = product of value counts.
- Use `Y/N`, explicit discrete values, or `-` only when a condition is truly irrelevant for that rule.
- Mark rules as `Valid`, `Invalid`, `Impossible`, or `Redundant`.

Decision table format:

| Rule ID | C01 | C02 | C03 | Action | Expected Result | Validity | Reason |
|---|---|---|---|---|---|---|---|
| R001 | Logged in | User | Valid input | A01 | Operation succeeds | Valid | Happy path |
| R002 | Not logged in | - | Valid input | A02 | Redirect to login | Valid | Auth required |

### Step 4 — Constraint Filtering
Create `tests/test-design/<FR-ID>/04-rule-filtering.md`.

Filtering table:

| Rule ID | Decision | Reason |
|---|---|---|
| R010 | Remove | Impossible because Guest cannot access admin page |
| R011 | Keep | Negative authorization case |

Keep all high-risk negative rules even if they look redundant.

### Step 5 — Pairwise Reduction
Create `tests/test-design/<FR-ID>/05-pairwise-reduction.md`.

Pairwise procedure:
1. Define pairwise factors from conditions that still vary after filtering.
2. Exclude impossible values according to constraints.
3. Generate a minimal set where every pair of values across any two factors appears at least once.
4. Add back mandatory rules:
   - all different expected result groups,
   - all high-risk auth/security cases,
   - all boundary/invalid equivalence classes,
   - all known bug-prone combinations.
5. Compare selected rules against full decision table and document coverage gaps.

Pairwise output format:

| Pairwise Case ID | Covered Rule ID(s) | C01 | C02 | C03 | Expected Action | Why selected |
|---|---|---|---|---|---|---|
| PW001 | R001 | Logged in | User | Valid input | A01 | Covers happy path + pairs |
| PW002 | R002 | Not logged in | - | Valid input | A02 | Mandatory auth negative |

Coverage review format:

| Pair | Covered by Pairwise Case | Status |
|---|---|---|
| C01=Logged in + C02=User | PW001 | Covered |
| C01=Not logged in + C03=Invalid input | PW002 | Covered |

### Step 6 — Generate Test Cases
Create one Markdown file per test case in `tests/test-cases/<FR-ID>/`.

Test case template:

```md
# TC-<MODULE>-DT-PW-001: <Short title>

## Requirement ID
<FR-ID>

## Module / Test Type / Technique
<Module> / Functional / Decision Table + Pairwise

## Source Design
- Decision Rule ID(s): Rxxx
- Pairwise Case ID: PWxxx

## Preconditions
- <Precondition 1>

## Test Data
| Field | Value | Class |
|---|---|---|
| <field> | <value> | Valid / Invalid / Boundary |

## Test Steps
1. <Step 1>
2. <Step 2>

## Expected Result
- <Expected result must be observable and pass/fail clear>

## Status / Related Bugs
Not Run / None
```

### Step 7 — Generate Test Run Template
Create `tests/test-runs/<FR-ID>-test-run.md`.

```md
# Test Run: <FR-ID> - <Feature Name>

| Test Case ID | Module | Tester | Date | Result | Related Bug | Note / Evidence |
|---|---|---|---|---|---|---|
| TC-XXX-DT-PW-001 | <module> | <name> | <date> | Not Run | None | |
```

Allowed results: `Pass`, `Fail`, `Blocked`, `Not Run`.

### Step 8 — Generate Bug Report Template
Create bug files only for failed executed tests in `tests/bug-report/<FR-ID>/`.

Bug report template:

```md
# BUG-<FR-ID>-001: <Bug title>

## Found by Test Case
TC-<MODULE>-DT-PW-001

## Requirement liên quan
<FR-ID>

## Severity / Priority
<Minor | Major | Critical> / <P0 | P1 | P2 | P3>

## Environment
- Browser / Device:
- OS:
- Base URL:
- Build / Commit:

## Preconditions
- <precondition>

## Steps to Reproduce
1. <step>
2. <step>

## Expected Result
<Expected behavior>

## Actual Result
<Actual behavior>

## Evidence
- Screenshot: `<path or GitHub issue attachment>`
- Video / Log: `<path or link>`

## Impact
<Business/user impact>

## Labels đề xuất
`type: bug`, `module: <module>`, `severity: <level>`, `priority: <level>`, `found-by: test-case`

## Retest Note
- Status: Not Retested
- Retest by:
- Retest date:
```

### Step 9 — Traceability Matrix
Create `tests/test-summary/traceability-matrix.md`.

```md
# Traceability Matrix

| Requirement | Decision Rule | Pairwise Case | Test Case | Result | Bug Issue | Status |
|---|---|---|---|---|---|---|
| FR-XX | R001 | PW001 | TC-XXX-DT-PW-001 | Not Run | None | Designed |
```

### Step 10 — AI Audit Snippet
Create `docs/ai-audit-log.md`.

```md
# AI Audit Log

| Tool | Date Time | Prompt Summary | Output Summary | Human Review / Correction |
|---|---|---|---|
| ChatGPT / Gemini / Claude | YYYY-MM-DD HH:mm | Generate decision table + pairwise test cases for FR-XX | Produced test design and test cases | Reviewed constraints, fixed expected results |
```

## Final Response Format
When the skill completes, return:

1. Folder tree of generated files.
2. Summary counts:
   - full decision rules,
   - rules removed as impossible/redundant,
   - pairwise cases selected,
   - final test cases generated,
   - bug reports created.
3. Short AI gap analysis: what may still be missing and what humans must review.
4. Checklist for submission.

## Quality Checklist
Before finalizing, verify:

- [ ] Requirement ID is present in every file.
- [ ] Every condition has values and source/reason.
- [ ] Full decision table exists before pairwise reduction.
- [ ] Impossible rules are documented, not silently removed.
- [ ] Pairwise selected cases cover all value pairs or explain exceptions.
- [ ] Expected result is specific and observable.
- [ ] Test case IDs are stable.
- [ ] Failed test cases have related bug reports.
- [ ] Traceability matrix connects Requirement → Rule → Pairwise Case → Test Case → Bug.
- [ ] AI audit log records prompt, output, and human correction.

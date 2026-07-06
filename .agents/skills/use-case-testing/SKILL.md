---
name: use-case-testing
description: Kỹ năng thiết kế, phát sinh, thực thi và báo cáo test case bằng Use Case Testing cho EShop. Use when Codex needs to read README/API/specs/user-flow descriptions, shortlist features suitable for Use Case Testing, wait for user confirmation, generate one Markdown file per test case, prepare test-run/summary/traceability artifacts, execute test cases, and create exactly one bug report for each failed test case.
---

# Use Case Testing Skill

## Core Contract

Use this skill for behavior that can be described as an actor pursuing a goal through a system interaction: main success scenario, alternate flows, exception flows, preconditions, postconditions, role/permission checks, and business-rule outcomes.

Do not force this technique onto pure value-boundary validation or explicit state machines. For those, recommend the existing domain/boundary or state-transition workflow unless the user confirms they want Use Case Testing anyway.

Follow the local EShop artifact style:

- Read the live requirement before generating: `README.md`, `api_specification.md`, relevant implementation files, and existing `tests/test-*` artifacts.
- Suggest candidate requirements first, then wait for user confirmation before writing test artifacts unless the user already explicitly confirms the target FR/feature in the prompt.
- Generate each test case as one Markdown file under `tests/test-cases/<module_name>/`.
- Prepare and keep synchronized: testcase files, summary, test-run, traceability matrix, and bug reports.
- When reporting defects for this workflow, create exactly one bug report file for each failed test case. Do not group multiple failed TCs into one bug.

## Workflow

### 1. Read Specs And Shortlist Candidates

Search with `rg` and inspect nearby implementation evidence. Build a candidate table with:

| FR | Feature | Evidence | Actors | Goal / Use case | Main flow | Alternate / exception flows | Fit | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

Rank as:

- `High`: explicit actors, user goals, step-by-step user/API flows, alternate/exception flows, role guards, preconditions, postconditions, or business-rule branches.
- `Medium`: implicit workflows such as checkout, cart, profile, order/admin actions, search, auth/session, or multi-screen UI behavior that can be modeled after reading code.
- `Low`: isolated field validation, simple display-only behavior, or dense condition matrices better served by boundary/decision-table testing.

Present the shortlist and ask the user to confirm the FRs/features to generate. Stop before file writes when confirmation is still missing.

### 2. Build The Use Case Model

After confirmation, derive and record:

- Primary actor, supporting actors, and unavailable/unauthorized actors.
- Goal, trigger, scope, interface, and frequency/risk if visible from specs.
- Preconditions and required fixtures/session state.
- Main success scenario as ordered steps.
- Alternate flows for valid variations.
- Exception flows for rejected/failed behavior.
- Postconditions and invariants after success or rejection.
- Business rules and referenced endpoints/screens.
- Assumptions and open questions, especially where README/API/code disagree.

Do not invent pass/fail execution results during design. Generation artifacts stay `Not Run / None` until real execution happens.

### 3. Design Coverage

Cover at minimum:

- Every selected use case at least once.
- Every main success scenario at least once.
- Every meaningful alternate flow at least once.
- Every exception flow/rejection path at least once.
- Every actor/role/permission branch that changes expected behavior.
- Every precondition failure that the requirement or implementation exposes.
- Every important postcondition/invariant.
- Cross-interface behavior when the same use case exists on web, admin, mobile, or API.

Prefer one assertion focus per TC. Setup steps may prepare shared fixtures, but each TC should validate one flow, guard, or postcondition.

### 4. Generate Artifacts

Before writing artifacts, read `references/project-artifact-templates.md` and use those templates.

Default artifact set:

- `tests/test-cases/<module_name>/<TC_ID>.md`
- `tests/test-summary/frNN-<module-name>-use-case-summary.md`
- `tests/test-runs/frNN-<module-name>-test-run.md`
- Updated `tests/test-summary/traceability-matrix.md`
- Optional reusable analysis/config note at `tests/test-configs/frNN-<module-name>-use-case-config.json`

Use these ID conventions:

- Use-case TC: `FR[NN]-UC[NN]-TC[NN]`, for example `FR07-UC01-TC01`.
- Flow-specific TC when useful: `FR[NN]-[FLOW_CODE]-TC[NN]`, for example `FR07-CART-TC01`, but keep the mapping to a use case and flow in the summary.
- Bug report: `BUG-FR[NN]-UC[NN]-TC[NN]` or `BUG-FR[NN]-[FLOW_CODE]-[NN]`, with exactly one `Found by Test Case` entry per bug file.

If an existing generator cannot model the use case cleanly, write the Markdown files manually with `apply_patch` while preserving the same artifact shapes.

Do not overwrite an existing test-run file that already contains real execution results unless the user explicitly requests regeneration.

### 5. Required Report Metrics

Every generated summary and every post-execution run report must make these counts explicit:

- Total test cases: count testcase files, summary index rows, and test-run rows; these must match.
- Test case coverage: map each TC to use case, flow type, actor, precondition, postcondition, and requirement bullet.
- Test case status: count `Not Run`, `Passed`, `Failed`, `Blocked`, and `Skipped`.
- Bug count: count bug report files for the selected FR/feature.
- Bug coverage: show whether every failed TC has exactly one bug report and whether every bug report maps to exactly one failed TC.

Use the labels `Total TC`, `TC Coverage`, `TC Status`, `Bug Count`, and `Bug Coverage` in the summary or run report so reviewers can find them quickly.

### 6. Execute Test Cases And Report Bugs

When the user asks to execute, run the project through existing local scripts, API calls, or UI flows as appropriate. Record actual results in:

- Each testcase `Status / Related bugs` section.
- The `tests/test-runs/...` execution table.
- The `Defect Log` section of the run sheet.

For each failed TC:

- Create exactly one bug report file under `tests/bug/FR-NN/`.
- Include exactly one related TC in `Found by Test Case`.
- Reuse the TC setup/steps/expected result; add observed actual result and evidence placeholder when evidence is not yet available.
- Sync the bug ID back into the testcase and test-run row.

If execution is blocked because servers, seed data, credentials, or browser/API access are unavailable, leave unexecuted cases as `Not Run` or `Blocked`, record the blocker, and do not invent pass/fail results.

### 7. Verify Before Finishing

Check:

- Candidate confirmation happened before artifact generation, or the prompt already contained an explicit confirmed FR/feature.
- Testcase file count equals the summary index count and test-run row count.
- Coverage tables mention every selected use case, main flow, alternate flow, exception flow, actor, and requirement bullet.
- Status totals equal `Total TC`.
- Every failed TC has exactly one bug file, and every bug file points to exactly one failed TC.
- Bug count equals failed TC count for this skill unless the user explicitly overrides the one-bug-per-TC rule.
- Testcase status, test-run result, defect log, and bug files agree.
- No placeholder TODOs remain in generated deliverables except intentional evidence placeholders.
- Skill structure validates with the global skill validator after editing this skill.

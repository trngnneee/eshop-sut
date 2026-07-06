---
name: state-transition-testing
description: Kỹ năng thiết kế và phát sinh test case bằng State Transition Testing cho EShop. Use when Codex needs to read README/API/specs, shortlist features whose behavior depends on states and transitions, wait for user confirmation, generate one Markdown file per test case, prepare test-run/summary/traceability artifacts, execute test cases, and create one bug report per failed test case.
---

# State Transition Testing Skill

## Core Contract

Use this skill for behavior where the expected result depends on `current_state + actor/action/input + guard_condition -> next_state` or a rejected transition that must keep the state unchanged.

Do not force this technique onto pure form/input validation, search filters, simple CRUD without lifecycle rules, or boundary-value checks. For those, recommend the existing domain/boundary or decision-table workflow instead.

Follow the local EShop artifact style:

- Read the live requirement before generating: `README.md`, `api_specification.md`, relevant implementation files, and existing `tests/test-*` artifacts.
- Suggest candidate requirements first, then wait for user confirmation before writing test artifacts unless the user already explicitly confirms the target FR/feature in the prompt.
- Generate each test case as one Markdown file under `tests/test-cases/<module_name>/`.
- Keep test-run, summary, traceability, and bug report files synchronized.
- When reporting defects for this workflow, create exactly one bug report file for each failed test case. Do not group multiple failed TCs into one bug.

## Workflow

### 1. Read Specs And Shortlist Candidates

Search the project with `rg` and inspect nearby implementation evidence. Build a candidate table with:

| FR | Feature | Evidence | State variables | Events/actions | Final/blocked states | Fit | Reason |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |

Rank as:

- `High`: explicit states, transitions, final states, role/action guards, lifecycle diagrams, or status APIs.
- `Medium`: implicit lifecycle/session/cart/checkout/order/payment/coupon usage behavior that can be modeled as states after reading code.
- `Low`: mostly input validation, simple CRUD, display-only behavior, or search/filter behavior.

Present the shortlist and ask the user to confirm the FRs/features to generate. Stop before file writes when confirmation is still missing.

### 2. Build The State Model

After confirmation, derive and show the model before or while generating artifacts:

- State variables: status/session/cart/order/payment/etc.
- Initial states and final states.
- Actors/roles and ownership constraints.
- Events/actions/API endpoints/UI actions.
- Valid transitions.
- Invalid transitions, blocked transitions, no-op transitions, skipped transitions, reverse transitions, and transitions out of final states.
- Guards: auth, role, ownership, required payload, allowed action source, and business conditions.
- Expected side effects and invariants.
- Assumptions and open questions, especially where README and implementation disagree.

For invalid transitions, the expected result must include both rejection and state unchanged.

Do not invent pass/fail execution results during design. Generation artifacts stay `Not Run / None` until real execution happens.

### 3. Design Coverage

Cover at minimum:

- Every valid transition at least once.
- Every meaningful invalid transition at least once.
- Every final state rejecting further transition.
- No-op transition such as `pending -> pending` when relevant.
- Skip-forward and reverse transitions when the state graph has ordering.
- Invalid state/action values such as unknown status, empty value, or `null`.
- Actor/permission guards such as admin-only transition and user-only cancel.
- Ownership/auth guards when endpoint behavior depends on the logged-in user.
- State/action value classes only when they affect transition acceptance, such as unknown status, empty status, `null`, missing transition action, or unsupported event.

Prefer one assertion focus per TC. Setup steps may traverse earlier valid states, but the TC should assert the target transition only.

### 4. Generate Artifacts

Before writing artifacts, read `references/project-artifact-templates.md` and use those templates.

Default artifact set:

- `tests/test-cases/<module_name>/<TC_ID>.md`
- `tests/test-summary/frNN-<module-name>-state-transition-summary.md`
- `tests/test-runs/frNN-<module-name>-test-run.md`
- Updated `tests/test-summary/traceability-matrix.md`
- Optional reusable config at `tests/test-configs/frNN-<module-name>-state-transition-config.json`

Use these ID conventions:

- State-transition TC: `FR[NN]-[STATE_CODE]-TC[NN]`, for example `FR10-S-TC01`.
- Bug report: `BUG-FR[NN]-[STATE_CODE]-[NN]`, with exactly one `Found by Test Case` entry per bug file.

If the existing generator fits the model, use it as a renderer and then manually review coverage. Do not include `boundary_cases` or any BVA testcase IDs in the config for this skill:

```bash
PYTHONPYCACHEPREFIX=/tmp/codex-pycache python .agents/skills/domain_and_boundary_testing/scripts/generate_test_cases.py --config tests/test-configs/<config>.json
```

Keep generated configs in `tests/test-configs/`. Do not write temporary configs inside `.agents/skills/`.

If the generator cannot model the feature cleanly, write the Markdown files manually with `apply_patch` while preserving the same artifact shapes.

Do not overwrite an existing test-run file that already contains real execution results unless the user explicitly requests regeneration.

### 5. Required Report Metrics

Every generated summary and every post-execution run report must make these counts explicit:

- Total test cases: count testcase files, summary index rows, and test-run rows; these must match.
- Test case coverage: map each TC to transition/class, state variable, actor, guard, final-state rule, and requirement bullet.
- Test case status: count `Not Run`, `Passed`, `Failed`, `Blocked`, and `Skipped`.
- Bug count: count bug report files for the selected FR/feature.
- Bug coverage: show whether every failed TC has exactly one bug report and whether every bug report maps to exactly one failed TC.

Use the labels `Total TC`, `TC Coverage`, `TC Status`, `Bug Count`, and `Bug Coverage` in the summary or run report so reviewers can find them quickly.

### 6. Execute Test Cases And Report Bugs

When the user asks to execute, run the project through existing local scripts or direct API/UI flows as appropriate. Record actual results in:

- Each testcase `Status / Related bugs` section.
- The `tests/test-runs/...` execution table.
- The `Defect Log` section of the run sheet.

For each failed TC:

- Create exactly one bug report file under `tests/bug/FR-NN/`.
- Include exactly one related TC in `Found by Test Case`.
- Reuse the TC steps and expected result; add the observed actual result and evidence placeholder when evidence is not yet available.
- Sync the bug ID back into the testcase and test-run row.

If execution is blocked because servers, seed data, credentials, or browser/API access are unavailable, leave unexecuted cases as `Not Run` or `Blocked`, record the blocker, and do not invent pass/fail results.

### 7. Verify Before Finishing

Check:

- Candidate confirmation happened before artifact generation, or the prompt already contained an explicit confirmed FR.
- Testcase file count equals the summary index count and test-run row count.
- Coverage tables mention every selected state variable, valid transition, invalid transition, final-state rejection, actor/permission guard, and requirement bullet.
- Status totals equal `Total TC`.
- Every failed TC has exactly one bug file, and every bug file points to exactly one failed TC.
- Bug count equals failed TC count for this skill.
- Testcase status, test-run result, defect log, and bug files agree.
- No placeholder TODOs remain in generated deliverables except intentional evidence placeholders.
- Skill structure validates with the global skill validator after editing this skill.

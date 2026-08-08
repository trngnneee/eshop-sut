# Test Case Template — <Feature name, e.g. FR-08 Checkout>

Fill this in **before** driving the AI for automation code (see SKILL.md §2). This
table is both the traceability artifact for the report and the literal thing fed to
the AI step by step in §3 — write it out fully first.

| TC ID | Type | Title | Preconditions | Steps | Test Data (ref) | Expected Result | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| TC-XXX-01 | Positive | ... | ... | 1. ...<br>2. ... | data row #1 | ... | High | Not Run |
| TC-XXX-02 | Negative | ... | ... | ... | data row #2 | ... | Medium | Not Run |
| TC-XXX-03 | Edge | ... | ... | ... | data row #3 | ... | Medium | Not Run |
| ... | | | | | | | | |

**Column notes**
- **TC ID**: `TC-<FEATURE>-NN`, e.g. `TC-CHECKOUT-01`. Keep IDs stable — the AI Audit
  Report, the automation spec, and any bug report all reference these IDs.
- **Type**: Positive / Negative / Edge. Aim for genuine variety across the 12+ cases —
  boundary values, invalid input, empty/duplicate data, permission checks, state
  transitions — not 12 near-identical happy-path variants.
- **Test Data (ref)**: don't inline values here if the case is data-driven — point to
  the row/key in `data/{feature}.csv|json` instead, so the table and the data file
  can't drift out of sync.
- **Expected Result**: the actual assertable outcome (visible text, URL, DB/API state),
  specific enough that the assertion pattern chosen for it is obvious.
- **Priority**: optional but useful when deciding what to automate first if time is
  short.
- **Status**: `Not Run` / `Pass` / `Fail` / `Blocked` / `Not Automated`. Update this
  after each browser run (§4 of SKILL.md) — this is what feeds the "executed/passed/
  failed" counts in the README test summary and the per-feature execution table in
  `report_template.md`. A case that fails should link to its bug (Bug ID) if the
  failure is a genuine product defect, not a test/script issue.

## Minimum coverage checklist
- [ ] At least 12 test cases total for this feature
- [ ] At least one Negative case
- [ ] At least one Edge case
- [ ] Every case's expected result is objectively checkable (no vague "works correctly")
- [ ] Every case maps to a row in the feature's data file (no hardcoded literals planned)
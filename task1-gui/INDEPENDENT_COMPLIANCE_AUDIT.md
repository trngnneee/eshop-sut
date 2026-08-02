# Independent Compliance Re-audit — Task 1 GUI Checklist

**Student:** Đặng Đăng Khoa — 23127207
**Re-audit date:** 2026-08-02 (Asia/Bangkok)
**Human-review status:** `HUMAN_REVIEWED`
**Verdict:** `STRUCTURALLY_READY_WITH_EXTERNAL_BLOCKERS`

## Outcome

The prior `NON_COMPLIANT` snapshot was superseded after a complete item-level reconciliation. The current source of truth contains 58 unique checklist items, 37 Pass, 20 Fail and 1 Blocked. All four IA groups are represented; origin is exactly 48 `AI_INITIAL` and 10 `HUMAN_ADDED`; all rows include Expected, Actual, Notes, execution mode, evidence ID, capture time and screenshot. Every Fail has a unique local Bug ID and evidence, while eligible existing GitHub defects are mapped to verified issue URLs.

This verdict is deliberately not `COMPLETE`. Local structural compliance cannot replace three external records: publication of remaining non-duplicate defects to GitHub, a public YouTube demo for the GUI-testing skill, and a native-device run for the soft-keyboard item. The validator reports those limitations separately from file/data failures.

## Recalculated metrics

| Metric | Current value | Audit result |
|---|---:|---|
| Checklist rows / unique IDs | 58 / 58 | Pass |
| Status | 37 Pass / 20 Fail / 1 Blocked | Pass |
| Origin | 48 AI_INITIAL / 10 HUMAN_ADDED | Pass |
| IA groups | IA-01, IA-02, IA-03, IA-04 | Pass |
| Item-level screenshots | 40 unique PNG files | Pass |
| Mock-controlled rows | 5, explicitly labelled | Pass |
| Human review | Confirmed 2026-08-02 | Pass |
| Native soft-keyboard run | 0 | External blocker |
| Task 1 public YouTube demo | Not supplied | External blocker |
| Pending GitHub mappings | Calculated by validator from final CSV | External blocker until zero |

## Evidence audit

- `results/Task1_Execution_Chrome.csv` is the machine-readable execution source.
- `GUI_Checklist_HW3.md` and `GUI_Checklist_HW3.xlsx` are regenerated from the same rows.
- `evidence/executed-chrome/` contains the referenced identity-overlaid screenshots. The validator checks existence, size and PNG signature.
- `results/Evidence_Index.csv` maps evidence IDs, checklist IDs, modes and capture times.
- `GUI_Bug_Report_HW3.md` separates each failed assertion and links its screenshot and GitHub disposition.
- `AI_Item_Level_Critique.md` covers all 58 IDs and records why each human-added case was retained.

Screenshots are evidence of the state visible at capture time; dynamic actions are also described in Actual/Notes. Mocked states are not counted as live backend observations. Expo Web at a narrow viewport is not claimed as a native Android/iOS run.

## Corrections to the old audit

| Old problem | Current disposition |
|---|---|
| Hard-coded 36/22 results and inconsistent 40/18 summary | Superseded by current 58-row execution data and consistent 37/20/1 metrics. |
| Five packed screenshots for all failures | Superseded by 40 current screenshots and an evidence index. |
| Invented FR-14 Edit Category requirement | Removed; Category item 005 now tests real tab navigation. |
| Invented duplicate-category rejection requirement | Removed; item 011 now tests deterministic Add/View behavior. |
| Wrong lockout boundary | Corrected to the written three-attempt/30-second requirement. |
| Weak validator returning success while incomplete | Replaced by semantic checks with exit 1 for structural failure and exit 2 for disclosed completion blockers. |
| Human review unconfirmed | Resolved by the student's explicit confirmation on 2026-08-02. |
| Fake/stale commit-history claims | Removed from current reports; only authentic repository history may be exported. |

## Open findings by severity

1. **High — Native evidence:** `GUI-MOBILE-LOGIN-011` is Blocked until a real eligible mobile target exposes the soft keyboard.
2. **High — GitHub traceability:** every remaining `PENDING_EXTERNAL_ACTION` must be replaced by an exact duplicate URL or a URL returned after creating a non-duplicate issue.
3. **High — Demo:** `Demo_Video_Link.md` must contain a real public YouTube URL showing the Task 1 skill workflow.

There are no hidden pilot, participant, device, issue, video or execution claims in this audit. Missing external evidence remains explicit.

## Validator status

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\task1-gui\scripts\validate-gui.ps1
powershell -ExecutionPolicy Bypass -File .\task1-gui\scripts\validate-gui.ps1 -StrictCompletion
```

The default validator is expected to pass when the package is structurally sound. Strict mode is expected to return exit code 2 while any disclosed external blocker remains. A strict nonzero result is not relabelled as completion.

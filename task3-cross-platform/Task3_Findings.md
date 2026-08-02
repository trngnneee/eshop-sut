# Task 3 — Severity-Ranked Findings

**Status:** `TECHNICAL_EXECUTION_REVIEWED_BY_AUTOMATION — THIRD_PLATFORM_PENDING`  
**Frequency denominator:** four executed environments unless otherwise stated; only Chrome/Firefox count toward the current 2/3 rubric platform total.

## Prioritized findings

| Rank | Finding | Type | Frequency | Severity | Evidence/checklist IDs | Recommended action |
|---:|---|---|---:|---|---|---|
| 1 | Login password is rendered as plaintext and the page uses incorrect login semantics (`Đăng Ký`, `Username`, `Sign In`). | Systemic GUI/software defect | 4/4 | Critical | `GUI-WEB-LOGIN-001/002/003/009`; each platform baseline screenshot | Use `type=password`; label the field Email; correct heading/button localization; retest accessibility and password-manager behavior. |
| 2 | Category delete has no confirmation and the backend permits deletion of a category referenced by a synthetic product. | Data-integrity software defect | 4/4 | High | `GUI-ADMIN-CATEGORY-006/008`; delete and in-use-delete evidence | Add referential-integrity validation, block in-use delete, and require a clear confirmation/impact message. |
| 3 | Lockout occurs at HTTP level but the web UI continues to show only the generic login failure message. | Feedback/software defect | 4/4 | High | `GUI-WEB-LOGIN-010`; observed HTTP sequence `401/401/403` | Surface the locked state and remaining duration without exposing account-enumeration details; align threshold/duration with FR-02. |
| 4 | Duplicate email registration is accepted with HTTP 200. | Validation/software defect | 4/4 | High | `GUI-WEB-REGISTER-006` | Add a unique email constraint and deterministic 409/validation feedback; retest concurrent registration. |
| 5 | Admin login lacks associated labels and uses native alerts for credential/authorization failures. | Accessibility and feedback defect | 4/4 | Medium | `GUI-ADMIN-LOGIN-002/003/004` | Add programmatic labels and an accessible inline error region; move focus to the error summary. |
| 6 | Category management lacks empty-name prevention, empty/loading states and double-submit protection. | Systemic form/state issue | 4/4 | Medium | `GUI-ADMIN-CATEGORY-004/009/010/013` | Enforce the required non-empty name, add explicit async states, and disable submission while pending. |
| 7 | Positive `tabIndex=1` places Sign In before the login inputs; browser focus sequences vary in detail but all violate the form’s natural order. | Cross-browser accessibility defect | 4/4 | Medium | `GUI-WEB-LOGIN-011`; keyboard evidence per platform | Remove positive tabindex and rely on DOM order; add visible `:focus-visible` styling and browser regression checks. |
| 8 | Expo Web mobile login uses `Username`/`Sign In`; the measured Sign In target is 39 CSS px high, below the 44 px checklist threshold. | Mobile UI consistency/accessibility defect | 4/4 Expo Web runs | Medium | `GUI-MOBILE-LOGIN-002/004/010` | Use consistent Vietnamese labels and raise the interactive target to at least 44×44 CSS px/dp. |
| 9 | Email whitespace is not normalized before login; forgot-password uses a full document navigation. | Resilience/navigation issue | 4/4 | Low | `GUI-WEB-LOGIN-007/013` | Trim the identifier before submission and use router navigation if SPA state preservation is required. |
| 10 | The inherited Task 1 checklist expects Category Edit and duplicate-name rejection, but the local FR-14 requires only Add/View/Delete and a non-empty name. | Test-design / requirement mismatch, not a confirmed SUT bug | 4/4 checklist mismatch | N/A | `GUI-ADMIN-CATEGORY-005/011`; `README.md` FR-14 | Correct or justify the two Expected Results before treating their Fail verdicts as defects. Preserve the execution evidence as a checklist audit trail. |

## Cross-platform consistency

- All 58 checklist IDs produced the same status on all four executed environments: 34 Pass, 23 Fail and 1 Not Observable per environment.
- The equality of statuses does not mean the engines behaved identically. Keyboard focus sequences differ, but `Sign In` with positive tabindex precedes the form inputs in every run.
- No failure was classified as browser-exclusive. The observed failures are therefore predominantly systemic application behavior.
- `GUI-MOBILE-LOGIN-011` remains `Not Observable` because Expo Web/headless desktop browsers do not display a real mobile soft keyboard. A physical/cloud device or Expo Go session is required.
- A checklist `Fail` means the observed result did not match the stored Task 1 Expected Result. It does not automatically establish a software bug; `GUI-ADMIN-CATEGORY-005/011` are explicitly retained as test-design mismatches.

## Issue handling

This Task 3 package records findings locally. It does not claim that new GitHub issues or comments were published. Existing Task 1/Task 2 issue mappings remain separate; duplicate search/publication should be completed only when an eligible third-platform run is available and the final cross-platform evidence set is approved.

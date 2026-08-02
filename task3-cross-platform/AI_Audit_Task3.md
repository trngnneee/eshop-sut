# AI Audit Report — Task 3

**Student:** Đặng Đăng Khoa — 23127207
**Date:** 2026-08-02
**Timezone:** Asia/Bangkok (UTC+7)
**Status:** `HUMAN_REVIEWED — BLOCKED_THIRD_REQUIRED_PLATFORM`

## Interaction 1 — Execute Task 3 with complete evidence

| Field | Value |
|---|---|
| AI tool | OpenAI Codex with local PowerShell, Node.js, Playwright, Chrome, Firefox, WebKit and Expo Web |
| Date/time | 2026-08-02, `TIME_NOT_EXPORTED` |
| User prompt | `thực hiện luôn task 3, chụp lại đầy đủ evidence` |
| AI output/use | Read the official nine-page HW03 PDF and the repository GUI-testing skill; identified the exact Chrome/Firefox/Safari-or-Android requirement and student-overlay constraint; inventoried installed browsers/cloud credentials/Android tooling; started the local EShop services; built a 58-item cross-platform runner; captured identity/platform/URL overlays; generated 232 result rows, 160 screenshots, matrices, findings, reports and validators. |
| Human/source control | No cloud credentials, macOS/Safari host, Android emulator or physical device existed. The AI did not rename WebKit as Safari or emulation as Android. The package therefore remains blocked at 2/3 eligible platforms. |

## Harness corrections

| Correction | Detection | Resolution | Evidence impact |
|---|---|---|---|
| Two navigation locators matched both header and form links; one XSS dialog listener remained active. | Initial Chrome run produced 55/58 rows and three scenario errors. | Scoped links to `main` and removed the unused listener. | Initial run was excluded; Chrome was rerun to 58/58 with zero scenario errors. |
| Mobile API proxy passed an unresolved Promise as `Content-Type`. | Mobile successful login returned backend 500 consistently; console log contradicted the intended live test. | Awaited `headerValue`, reran the seven Mobile screenshots for every environment and verified the synthetic name appeared in the header. | Final Mobile Login 009 is Pass on all environments; no false SUT bug retained. |
| Keyboard scenario clicked the page before pressing Tab, changing the starting focus. | A supplemental WebKit status differed while source inspection showed positive `tabIndex=1`. | Reran from a genuinely unfocused document and captured eight Tab targets; refined the check to compare positive-submit and first-input indices. | Final status is consistently Fail; evidence records engine-specific sequences without a false browser-only defect. |
| Three inherited Task 1 expectations asserted automatic whitespace normalization, Category Edit and duplicate-name rejection without requirement support. | Human review compared the expected results with FR-02/FR-14 and the retained runtime observations. | Corrected the expectations, updated the future runner and audibly reclassified the same three observations through `reconcile-task1-expectations.js`. | Per-platform totals changed from 34/23/1 to 37/20/1. Original screenshots and capture timestamps remain unchanged; JSON stores the reconciliation note. |

## Tools and data handling

| Tool | Purpose | Data handling |
|---|---|---|
| Playwright | Browser execution, assertions, screenshots, dialog/network observation | Synthetic accounts/categories/products; student identity only in required overlay |
| Google Chrome / Firefox | Two rubric-eligible local browser runs | Localhost only |
| Playwright WebKit / Pixel 7 emulation | Supplemental compatibility evidence | Explicitly labelled non-eligible |
| Expo Web | Execute the Mobile Login checklist in browser contexts | Hardcoded LAN API redirected to the local backend and disclosed |
| Node.js | Generate CSV/JSON, matrix and evidence index | No participant data |
| PowerShell | Service readiness, validator and file-integrity checks | No external publication |

## Anti-fabrication declaration

- No Safari, BrowserStack, LambdaTest, Sauce Labs, Android device, Expo Go device or physical-phone run is claimed.
- No screenshot is presented as coming from an unavailable platform.
- No participant data from Task 2 is used in Task 3.
- Synthetic test entities use `task3-*` identifiers and are cleaned after capture.
- Mocked states are explicitly marked in `execution_mode`.
- No GitHub issue/comment publication is claimed.

## Student review confirmation

The student confirmed in the project conversation that all human-review sections had been reviewed. This confirmation applies to the Task 3 evidence overlays, eligibility decision, findings, audit and critique; it does not waive the unavailable third-platform requirement.

- Review date: `2026-08-02`
- Student confirmation: `HUMAN_REVIEWED — confirmed by the student in chat`

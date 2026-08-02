# Task 3 — Cross-Browser / Cross-Platform Report

**Student:** Đặng Đăng Khoa
**Student ID:** 23127207
**Overlay email:** `23127207@student.hcmus.edu.vn`
**SUT:** EShop
**Report date/timezone:** 2026-08-02 — Asia/Bangkok (UTC+7)
**Status:** `BLOCKED_THIRD_REQUIRED_PLATFORM — LOCAL_EXECUTION_COMPLETE`

## Executive result

The 58-item Task 1 GUI checklist was re-executed against the local EShop SUT on four browser environments. Google Chrome 150 on Windows and Firefox 153 on Windows are valid current Task 3 platforms. Playwright WebKit 26.5 on Windows and Chromium Pixel 7 emulation were executed as supplemental compatibility checks but are not represented as Safari or real Android Chrome.

Each environment produced 58 result rows and 40 screenshots: 37 Pass, 20 Fail and 1 Not Observable. The combined dataset contains 232 rows and 160 PNG screenshots. Every row maps to an existing screenshot; every screenshot includes the student identity/email overlay, actual platform/engine, Windows/device declaration, SUT localhost URL, checklist IDs, observation and capture time.

The local evidence package is complete, but the rubric requires three eligible real/cloud/physical platforms. Only two are presently available. Task 3 therefore remains `BLOCKED_THIRD_REQUIRED_PLATFORM` rather than being falsely marked complete.

## Scope and execution design

The execution reused all 58 Task 1 IDs:

| Area | Checklist IDs | Items per platform |
|---|---|---:|
| Web Login | `GUI-WEB-LOGIN-001`–`013` | 13 |
| Web Register | `GUI-WEB-REGISTER-001`–`012` | 12 |
| Admin Login | `GUI-ADMIN-LOGIN-001`–`009` | 9 |
| Admin Category | `GUI-ADMIN-CATEGORY-001`–`013` | 13 |
| Mobile Login through Expo Web | `GUI-MOBILE-LOGIN-001`–`011` | 11 |
| Total |  | 58 |

Primary flows used the live local backend and frontends at `localhost:3000`, `localhost:5173`, `localhost:5174` and `localhost:8081`. Unique synthetic accounts, categories and products were created only where necessary and cleaned up after capture. Error/loading/empty/double-submit states that required deterministic timing or mutation prevention are explicitly labelled `MOCKED_*`; they are not presented as production/network observations.

## Platform results

| Platform | Eligible? | Browser version | Device/viewport | Pass | Fail | Not Observable | Evidence |
|---|---|---|---|---:|---:|---:|---:|
| Google Chrome / Windows | YES | 150.0.7871.187 | Desktop 1440×900 | 37 | 20 | 1 | 40 PNG |
| Firefox / Windows | YES | 153.0 | Desktop 1440×900 | 37 | 20 | 1 | 40 PNG |
| Playwright WebKit / Windows | NO — not Safari | 26.5 | Desktop 1440×900 | 37 | 20 | 1 | 40 PNG |
| Chromium Pixel 7 emulation | NO — not real Android | 151.0.7922.34 | Emulated Pixel 7 | 37 | 20 | 1 | 40 PNG |

Across all runs, 58/58 item statuses were consistent. The eligible Chrome + Firefox subtotal is 116 rows: 74 Pass, 40 Fail and 2 Not Observable. The consistency result indicates that the failures are systemic rather than isolated to one tested browser; it must not be used to claim Safari/Android compatibility.

The 20 Fail verdicts are checklist comparisons, not automatically 20 independent software defects. After human review corrected three unsupported Task 1 expectations (`GUI-WEB-LOGIN-013`, `GUI-ADMIN-CATEGORY-005`, `GUI-ADMIN-CATEGORY-011`), the retained observations were reclassified consistently on all four platforms. Screenshots and capture timestamps were not altered; `results/run-summary.json` records the reconciliation explicitly.

## Key findings

The severity-ranked register is in `Task3_Findings.md`. The highest-risk observations are:

1. Web Login displays the password as plaintext on every executed environment.
2. Category deletion has no confirmation and permits deleting a category referenced by a synthetic product.
3. Lockout is observable as HTTP `401/401/403`, but the UI does not distinguish the locked state.
4. Duplicate email registration returns HTTP 200.
5. Positive tabindex places Sign In before form inputs across the tested engines.

These are application-level failures seen consistently in Chrome, Firefox, WebKit and Chromium emulation. The test did not discover a fail that occurred on only one browser.

## Evidence integrity

- `Cross_Platform_Matrix.md` provides one row per Task 1 item with linked platform evidence.
- `Evidence_Index.md` enumerates all 160 screenshots and their supported item IDs.
- `results/Task3_Cross_Platform_Results.csv` stores one row per platform/item.
- Per-platform JSON files retain browser version, console messages, page errors and scenario-error counts.
- All four runs contain 58 unique expected IDs, no duplicate/unexpected IDs and zero harness scenario errors.
- A failed initial Chrome harness run was excluded after fixing three locator/dialog issues. A later mobile proxy defect was also fixed and the affected seven screenshots were rerun on all four environments. These corrections are disclosed in `AI_Audit_Task3.md`; the final indexed evidence is the corrected run only.

## Limitations

- No BrowserStack/LambdaTest/Sauce Labs credentials were configured.
- No macOS/Safari host, Android SDK/emulator/AVD or connected physical phone was available.
- Playwright WebKit on Windows is not Safari.
- Pixel 7 emulation is not a real/cloud Android Chrome device.
- Expo Web does not show a real soft keyboard, so `GUI-MOBILE-LOGIN-011` is `Not Observable` on every environment.
- Native JavaScript dialogs are browser-owned UI and do not appear in page screenshots; their observed text is recorded in the evidence overlay and machine-readable run log.
- The runner used localhost and an in-process route proxy for the mobile app’s hardcoded LAN API URL; this is disclosed in Mobile evidence actual results.

## Completion decision

The execution, result matrix, evidence index and local browser evidence are complete. The HW03 Task 3 rubric itself is not yet satisfied because only two of the required three eligible platforms exist. To close the gate, add one complete 58-item run from Safari on macOS, real/cloud Android Chrome, or Expo Go on a real phone. The screenshots must visibly retain the student name/ID/email, browser/OS/device and SUT URL/tunnel identity. Until then, the correct final state is `BLOCKED_THIRD_REQUIRED_PLATFORM`.

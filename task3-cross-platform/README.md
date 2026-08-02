# Task 3 — Cross-Browser / Cross-Platform

**Student:** Đặng Đăng Khoa — 23127207  
**Student email overlay:** `23127207@student.hcmus.edu.vn`  
**SUT:** EShop local frontend/admin/Expo Web  
**Current status:** `BLOCKED_THIRD_REQUIRED_PLATFORM — LOCAL_EXECUTION_COMPLETE`

## Outcome

The complete 58-item Task 1 checklist was executed on four local browser environments. Google Chrome on Windows and Firefox on Windows are the two rubric-eligible platforms currently evidenced. Playwright WebKit on Windows and Pixel 7 Chromium emulation were also executed, but are explicitly supplemental: WebKit is not Apple Safari, and responsive/device emulation is not a physical or cloud Android Chrome session.

| Environment | Eligibility | Items | Pass | Fail | Not Observable | Screenshots |
|---|---|---:|---:|---:|---:|---:|
| Google Chrome 150 / Windows | Eligible | 58 | 34 | 23 | 1 | 40 |
| Firefox 153 / Windows | Eligible | 58 | 34 | 23 | 1 | 40 |
| Playwright WebKit 26.5 / Windows | Supplemental only; not Safari | 58 | 34 | 23 | 1 | 40 |
| Chromium Pixel 7 emulation / Windows host | Supplemental only; not real Android | 58 | 34 | 23 | 1 | 40 |

Totals: 232 result rows and 160 screenshot files. All 58 checklist IDs have consistent Pass/Fail/Not Observable status across the four executed environments.

## Evidence rule

Every screenshot contains an in-page evidence overlay with:

- student full name, ID and student email;
- actual browser/engine version;
- Windows host and device/viewport declaration;
- the current `localhost` SUT URL;
- evidence ID and mapped Task 1 checklist IDs;
- observed state and UTC capture timestamp.

The overlay is an evidence annotation and does not alter the assertion result. Native JavaScript dialog text is captured by Playwright and written into the overlay/result JSON because a page-level screenshot cannot include browser-owned dialog chrome. Mocked empty/loading/network-error/double-submit states are labelled by `execution_mode`; primary login, registration, admin and mobile API-proxy flows use the live local SUT.

## Package map

| Artefact | Purpose |
|---|---|
| `Task3_Cross_Platform_Report.md` / `.pdf` | Main Task 3 report |
| `Task3_Findings.md` | Severity-ranked cross-platform findings |
| `Platform_Inventory.md` | Eligibility and environment boundary |
| `Cross_Platform_Matrix.md` | 58-item status/evidence matrix |
| `Evidence_Index.md` | Full index of 160 screenshots |
| `results/Task3_Cross_Platform_Results.csv` | 232 item-platform result rows |
| `results/*.json` | Per-platform diagnostics and machine-readable results |
| `results/Evidence_Index.csv` | Machine-readable screenshot index |
| `evidence/` | Platform-grouped PNG screenshots |
| `AI_Audit_Task3.md` / `.pdf` | AI interaction and anti-fabrication disclosure |
| `AI_Critique_Task3.md` / `.pdf` | 200–300 word critique awaiting student review |
| `git-commit-log.txt` | Text export of the repository history and worktree state |
| `scripts/run-task3.js` | Execution and capture runner |
| `scripts/summarize-task3.js` | Matrix/evidence-index generator |
| `scripts/validate-task3.ps1` | Structural and completion validator |
| `scripts/export-commit-log.ps1` | Reproducible UTF-8 Git history exporter |

## Completion boundary

Local execution and evidence generation are complete. Task 3 cannot truthfully be marked rubric-complete until one additional eligible platform is supplied through one of these routes:

1. Safari on macOS through BrowserStack/LambdaTest/Sauce Labs or a real Mac; or
2. Android Chrome through a cloud real-device session or a physical Android device; or
3. Expo Go on a real phone, if used as the third platform in place of Safari.

The third-platform screenshots must retain the same student identity, device/browser/OS and localhost/tunnel URL evidence. No cloud credentials or physical device were available in the current environment, so no third-platform result was fabricated.

## Commands

```powershell
node "task3-cross-platform/scripts/run-task3.js"
node "task3-cross-platform/scripts/summarize-task3.js"
powershell -NoProfile -ExecutionPolicy Bypass -File "task3-cross-platform/scripts/validate-task3.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File "task3-cross-platform/scripts/export-commit-log.ps1"
```

# Task 3 Platform Inventory

**Requirement source:** `HW3/2026.HW03.GUI Usability_En.pdf`, Task 3 and Anti-AI-Cheat Constraints  
**Required set:** at least three real/cloud/physical platforms covering Chrome, Firefox and Safari or Android Chrome  
**Current completion:** `2/3 ELIGIBLE — BLOCKED_THIRD_REQUIRED_PLATFORM`

| Platform ID | Browser/engine | OS/device evidence | Run type | Rubric eligible? | Evidence state |
|---|---|---|---|---|---|
| `chrome-windows` | Google Chrome 150.0.7871.187 | Windows host 10.0.26200; desktop 1440×900 | Real local installed browser | YES | 58/58 rows; 40 screenshots |
| `firefox-windows` | Firefox 153.0 | Windows host 10.0.26200; desktop 1440×900 | Local Playwright-distributed Firefox binary | YES | 58/58 rows; 40 screenshots |
| `webkit-windows` | Playwright WebKit 26.5 | Windows host 10.0.26200; desktop 1440×900 | Supplemental engine compatibility | NO — not Apple Safari | 58/58 rows; 40 screenshots |
| `android-chrome-emulation` | Chromium 151.0.7922.34 with Pixel 7 descriptor | Windows host; emulated Pixel 7 viewport/touch/user-agent | Supplemental responsive emulation | NO — not a real/cloud Android session | 58/58 rows; 40 screenshots |

## Availability checks

- Google Chrome executable: available locally.
- Playwright Firefox and WebKit binaries: available locally.
- Microsoft Edge: installed, but not used as a substitute because the rubric names Safari/Android Chrome.
- Safari executable/macOS host: unavailable.
- Android SDK, emulator and AVD: unavailable.
- BrowserStack, LambdaTest and Sauce Labs credentials: not configured in the execution environment.
- Physical Android/iOS device connection: unavailable to the automation environment.

## Non-substitution declaration

`webkit-windows` must not be renamed Safari. `android-chrome-emulation` must not be renamed physical Android Chrome. Both are useful compatibility runs and their screenshots are retained, but neither raises the rubric-eligible count above 2.


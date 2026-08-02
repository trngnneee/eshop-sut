# Task 1 — GUI Checklist Deliverables

**Student:** Đặng Đăng Khoa — 23127207
**SUT:** EShop
**Primary execution:** Google Chrome 150.0.7871.187 / Windows 10.0.26200, 2026-08-02
**Status:** `BLOCKED_REAL_MOBILE_SOFT_KEYBOARD_AND_PENDING_EXTERNAL_ITEMS`

## Outcome

- 58 unique items; IA-01 through IA-04 covered.
- 37 Pass, 20 Fail, 1 Blocked.
- 48 AI-initial and 10 human-added items, human-reviewed.
- 40 current Chrome screenshots with identity/email overlay.
- One source of truth: `results/Task1_Execution_Chrome.csv`.

## Completion boundary

1. `GUI-MOBILE-LOGIN-011` needs Expo Go or a physical/cloud phone.
2. Every `PENDING_EXTERNAL_ACTION` bug needs a real duplicate/new GitHub URL.
3. `Demo_Video_Link.md` needs a real public Task 1 GUI-skill YouTube URL.

No unavailable evidence is reconstructed to satisfy a validator.

## Commands

```powershell
python .\task1-gui\scripts\sync-current-execution.py
powershell -NoProfile -ExecutionPolicy Bypass -File .\task1-gui\scripts\validate-gui.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\task1-gui\scripts\validate-gui.ps1 -RequireComplete
powershell -NoProfile -ExecutionPolicy Bypass -File .\task1-gui\scripts\export-commit-log.ps1
```

# Technical Preflight — Not Participant Evidence

**Actor:** Automated/researcher technical check
**Participant evidence:** No
**Current status:** `PASS_WITH_PROVISIONAL_DEFECT`
**Finding label:** `PROVISIONAL`

## Purpose

Confirm that the selected flow can technically reach registration, login, profile update, persistence verification, and logout before recruiting a pilot participant. This check does not substitute for the required real-person pilot and is excluded from all participant metrics and SUS analysis.

## Planned assertions

1. A unique test account can be registered and redirects to `/login`.
2. That account can log in and reach the authenticated home page.
3. The profile page is discoverable through the authenticated header.
4. A specification-valid Vietnamese test phone (`0912345678`) is tested without silently changing it.
5. If the valid phone is rejected, fallback Card B (`912345678`) is tested only to determine whether the remaining flow is reachable.
6. Updated data persists after page reload.
7. Logout removes the authentication token and exposes the unauthenticated state.

## Environment and result

- Date/time: 2026-07-29 14:34:28–14:34:31 +07:00
- SUT snapshot: Git HEAD `671d798058fa782301f06b679dbec5523339f66f` with the existing dirty worktree
- Browser: Chromium headless through Playwright 1.62.0
- Unique non-participant test account: `ux.preflight.20260729073428665@example.com`
- Result JSON: `evidence/technical-preflight/result.json`
- Screenshots: `evidence/technical-preflight/`
- Overall result: `PASS_WITH_PROVISIONAL_DEFECT`
- Cleanup: technical-preflight users IDs `3`, `4`, and `5` were deleted after evidence capture; remaining `ux.preflight.%@example.com` users = `0`; guarded `users` auto-increment sequence restored from `5` to `2` (`MAX(users.id)=2`)

## Provisional observations to verify

| ID | Source-based observation before live check | Requirement / expected behaviour | Status |
| :--- | :--- | :--- | :--- |
| PF-01 | Login heading says “Đăng Ký”, username is not an email input, the password is visible text, and the submit control says “Sign In”. | FR-02, FR-21, FR-22, IA-01, IA-02 | `PROVISIONAL`; already covered by Task 1 BUG-GUI-01 |
| PF-02 | Live preflight rejected `0912345678` with “Số điện thoại không hợp lệ” and then saved successfully with fallback `912345678`. | FR-04 | `PROVISIONAL`; technically reproduced, participant observation still required |
| PF-03 | The logout control is labelled “Thoát”; when used from `/profile`, no redirect is requested and the same route renders “Vui lòng đăng nhập”. | FR-23 and IA-03/IA-04 | `PROVISIONAL`; observe participants before usability conclusion |

Do not convert these observations into participant counts or quotes.

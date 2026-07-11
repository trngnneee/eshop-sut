# Test Run ù FR-22 Mobile Forgot (Playwright Automation)

**Date:** 2026-06-29  
**Command:** `npm run test:mforgot` (alias: `npm run test:fr22`)  
**Project:** mobile-chromium ù Expo Web `http://localhost:8081`  
**Testing approach:** Black-box (UI + API as external interfaces)

## Summary

| Metric | Count |
| :--- | ---: |
| Automated TC | 14 |
| Pass | 3 |
| Fail | 11 |

## Results

| Test Case | Result | Bug | Note |
| :--- | :--- | :--- | :--- |
| TC-MFORGOT-SUP-001 | Fail | #24 | OTP token 4 digits, label says "4 s?" |
| TC-MFORGOT-SUP-002 | Fail | #20 | Demo message has no OTP on screen |
| TC-MFORGOT-SUP-003 | Fail | #26 | API accepts weak password `weakpass` |
| TC-MFORGOT-SUP-004 | Pass | None | OTP reuse correctly rejected |
| TC-MFORGOT-SUP-005 | Fail | #22 | No confirm-password field on Step 2 |
| TC-MFORGOT-SUP-006 | Fail | #21 | Validation via popup, not inline (FR-22) |
| TC-MFORGOT-SUP-007 | Fail | #27 | `Test1234+` accepted (should reject) |
| TC-MFORGOT-001 | Fail | #22, #24, #20 | Full flow blocked (confirm, OTP, demo) |
| TC-MFORGOT-004 | Pass | None | Invalid email rejected |
| TC-MFORGOT-010 | Pass | None | Unregistered email handled |
| TC-MFORGOT-019 | Fail | #23 | No Step Indicator on screen |
| TC-MFORGOT-020 | Fail | #25 | No "Quay l?i ??ng nh?p" control |
| TC-MFORGOT-028 | Fail | #24, #27 | OTP length + password validation |
| TC-MFORGOT-031 | Fail | #27 | Valid `Abc@1234` rejected |

## Mobile black-box bug reports (FR-22)

| # | Report | Defect |
| :---: | :--- | :--- |
| 20 | [issue-020](../bug-reports/issue-020-mobile-no-otp-demo.md) | Demo OTP not displayed on screen |
| 21 | [issue-021](../bug-reports/issue-021-mobile-alert-not-inline.md) | Validation error in popup, not inline |
| 22 | [issue-022](../bug-reports/issue-022-mobile-missing-confirm-password.md) | Step 2 missing confirm-password field |
| 23 | [issue-023](../bug-reports/issue-023-mobile-missing-step-indicator.md) | Step Indicator not shown |
| 24 | [issue-024](../bug-reports/issue-024-mobile-otp-four-digits.md) | OTP 4 digits, not 6 |
| 25 | [issue-025](../bug-reports/issue-025-mobile-no-back-to-login.md) | No return-to-login control |
| 26 | [issue-026](../bug-reports/issue-026-mobile-api-accepts-weak-password.md) | API accepts weak password |
| 27 | [issue-027](../bug-reports/issue-027-mobile-password-validation-fr01.md) | Password rules do not match FR-01 |

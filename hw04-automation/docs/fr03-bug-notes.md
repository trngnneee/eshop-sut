# Bug notes — FR-03 (from automation oracles)

Student: **23127271** · Feature A · Observed 2026-08-07 via Playwright matrix

These failures are **product defects** against `Repo/eshop-sut/README.md` FR-03 / FR-22 / SEC-07. Spec oracles were not weakened.

| Case | Spec expectation | SUT observation | Severity |
| --- | --- | --- | --- |
| TC-FORGOT-010 | Confirm-password field on step 2 | Only one password input | High |
| TC-FORGOT-011 | Step indicator e.g. "Bước 1 / 2" | Missing | Medium |
| TC-FORGOT-012 | Control "Quay lại đăng nhập" → `/login` | Only "← Quay lại" returns to step 1 | Medium |
| TC-FORGOT-013 | Email input `type="email"` | `type="text"` | Medium |
| TC-FORGOT-014 | Demo OTP is 6 digits | Backend issues 4-digit token; label says "(4 số)" | High |

Screenshots: Playwright `test-results/fr03-forgot-password/<browser>/` failure folders from the matrix run.

# Feature A — FR-03 · Verify

**Student ID:** 23127271  
**Date:** 2026-08-07  
**Result:** Chromium **9 pass / 5 fail**; matrix same × Firefox / WebKit  
**Reports:** `reports/html/fr03-forgot-password/<browser>/` · title `Run by: 23127271`

---

## Failure list (product defects — oracles kept)

| Case | Issue |
| --- | --- |
| TC-FORGOT-010 | Confirm-password field missing |
| TC-FORGOT-011 | Step indicator missing |
| TC-FORGOT-012 | Quay lại đăng nhập does not go to `/login` |
| TC-FORGOT-013 | Email `type=text` |
| TC-FORGOT-014 | OTP 4 digits not 6 |

Bug notes: `docs/fr03-bug-notes.md` · `bug-reports/BUG-FR03-001`…`005`.

## Targeted repairs applied (automation only)

- Dialog handling with `Promise.all` (avoid alert deadlock)
- Happy-path end-state assertions
- Tightened back-to-login locator
- Skip confirm fill when only one password field exists

## Evidence freeze (later)

`evidence/feature-a-fr03-frozen-2026-08-07/` + `EVIDENCE-LOCK.json` before Feature B.

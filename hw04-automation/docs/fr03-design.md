# Feature A — FR-03 · Design

**Student ID:** 23127271  
**Based on:** `docs/fr03-analysis.md`  
**Date:** 2026-08-07  

> No external JSON and no Playwright in this stage. **14** cases (≥12). Oracles follow **README FR-03 / FR-01 / FR-22**, not defective SUT.

---

## Traceability

| Requirement | Case IDs |
| --- | --- |
| Step 1 registered email → OTP / full reset | 001, 014 |
| Email rejection | 002, 003, 004 |
| OTP validity | 005, 006, 007, 014 |
| FR-01 password on reset | 008, 009 |
| Confirm password field | 010 |
| Step indicator | 011 |
| Back to login | 012 |
| Email `type=email` | 013 |

---

## Case ledger (14)

| ID | Category | Covered rule |
| --- | --- | --- |
| TC-FORGOT-001 | positive | Full reset; login with new password |
| TC-FORGOT-002 | negative | Empty email rejected |
| TC-FORGOT-003 | negative | Invalid email format rejected |
| TC-FORGOT-004 | negative | Unregistered email rejected |
| TC-FORGOT-005 | negative | Wrong OTP rejected |
| TC-FORGOT-006 | negative | Empty OTP rejected |
| TC-FORGOT-007 | boundary | OTP length 5 rejected |
| TC-FORGOT-008 | negative | Password shorter than 8 chars rejected |
| TC-FORGOT-009 | negative | Password missing uppercase rejected |
| TC-FORGOT-010 | validation | Confirm-password field present (FR-03) |
| TC-FORGOT-011 | ui | Step indicator "Bước 1 / 2" |
| TC-FORGOT-012 | ui | Quay lại đăng nhập → `/login` |
| TC-FORGOT-013 | validation | Email `type="email"` |
| TC-FORGOT-014 | boundary | Demo OTP exactly 6 digits |

---

## Case details (summary)

### TC-FORGOT-001 — Full happy path
- **Journey intent:** `fullReset` — request OTP → reset → login with new password.
- **Expected:** Success feedback; URL login; API login OK.

### TC-FORGOT-002…004 — Request-step negatives
- Empty / invalid format / unregistered email stay on request step with error feedback.

### TC-FORGOT-005…007 — OTP negatives / boundary
- Wrong, empty, length-5 OTP must not complete reset; original password still works if reset blocked.

### TC-FORGOT-008…009 — FR-01 password strength
- Short / no-uppercase new password rejected at reset.

### TC-FORGOT-010…014 — Spec UI / contract
- Confirm field, step indicator, back-to-login, email type, OTP length 6 — **spec oracles** even if SUT defective.

## Mix summary

Positive 1 · Negative 7 · Boundary 2 · Validation/UI 4 → **14**.

## Next

**Review** — dedupe + observable oracles (`docs/fr03-review.md`).

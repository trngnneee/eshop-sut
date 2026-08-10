# Feature A — FR-03 Forgot Password (Web) · Analyze only

**Student ID:** 23127271  
**Stage:** Analyze · Design → `fr03-design.md`  
**Date:** 2026-08-07  
**Sources:** `Repo/eshop-sut/README.md` FR-03 / FR-01 / FR-22 / SEC-07, HW02 Feature A, HW04 PDF Task 1  
**Tool:** Cursor Agent · skill `automation-testing`

> Scope lock: **analyze only**. No case IDs designed here, no external JSON, no Playwright code.

---

## 1. Contract (HW04 Task 1)

| Item | Value |
| --- | --- |
| Feature | A — FR-03 Forgot password and password reset (two steps) |
| App | Storefront `http://localhost:5173` |
| API | `http://localhost:3000` |
| Target later | ≥12 data-driven cases · JSON · 3 browsers · HTML `Run by: 23127271` |
| Paths | `test-data/fr03-forgot-password.json` · `tests/fr03-forgot-password.spec.js` · `reports/html/fr03-forgot-password/<browser>/` |

---

## 2. Actors

| Actor | Role |
| --- | --- |
| Registered user | Requests OTP via email; resets password with OTP + new password + confirm |
| Unregistered / guest | Must not obtain a usable OTP for an unknown email |
| System / API | Issues OTP; validates password rules (FR-01); persists new password |

---

## 3. Preconditions

1. API + Web running.
2. For happy path: a **registered** account (prefer unique API-registered user per run — do not mutate shared seed permanently).
3. User can open `/forgot-password` (or equivalent route from Login).

---

## 4. Operations & state transitions

```text
[Login] → Forgot password
    │
    ▼
 Step 1: enter email → request OTP
    │  reject: empty / invalid format / unregistered
    ▼
 Step 2: OTP + new password + confirm
    │  reject: wrong/empty/short OTP; weak password; confirm mismatch
    ▼
 Success → return to Login; login with new password works
```

---

## 5. Input rules (spec)

| Field | Rule |
| --- | --- |
| Email (step 1) | Required; valid format; must be registered |
| OTP (step 2) | **6 digits** (SEC-07 / FR-03 demo) |
| New password | FR-01 strength (≥8, uppercase, etc.) |
| Confirm password | Required; must match new password |
| UI contract | Step indicator "Bước 1 / 2"; email `type="email"`; control **Quay lại đăng nhập** → `/login` |

---

## 6. Outputs / feedback

- Dialog / inline error on reject; stay on forgot-password when invalid.
- Success: confirmation + navigate to login; API login with new password succeeds.
- Demo OTP may be shown in UI for the testing SUT — length must still be 6 per spec.

---

## 7. Ambiguities

| ID | Topic | Decision for later Design |
| --- | --- | --- |
| A1 | Exact dialog copy | Prefer stable substrings / `dialogMatches`, not full string equality |
| A2 | Confirm mismatch case | Covered by presence of confirm field (010) + FR-01 rejects; optional dedicated mismatch deferred |
| A3 | OTP expiry timing | Out of scope for this suite |

---

## 8. SUT observations (do not soften oracles later)

From `ForgotPassword.jsx` / backend at Analyze time:
- OTP is **4** digits; label may say "(4 số)".
- No confirm-password field on step 2.
- No step indicator "Bước 1 / 2".
- Back control returns to step 1, not Login.
- Email input `type="text"`.
- Client password regex quirks; backend may store plaintext / weak rules.

---

## 9. Environment

| Service | URL |
| --- | --- |
| Web | `http://localhost:5173` |
| API | `http://localhost:3000` |

## 10. Next stage

**Design** ≥12 distinct case IDs from this analysis (`docs/fr03-design.md`). Still no JSON/code.

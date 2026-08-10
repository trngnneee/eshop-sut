# Feature A — FR-03 · Review

**Student ID:** 23127271  
**Input:** `fr03-design.md` · `fr03-analysis.md`  
**Date:** 2026-08-07  

> Spec oracles **not** softened to match SUT.

---

## 1. Duplicate / overlap check

| Pair | Verdict |
| --- | --- |
| 002 empty vs 003 invalid format | Distinct invalid classes — **keep both** |
| 005 wrong OTP vs 006 empty vs 007 length 5 | Distinct — **keep all** |
| 008 short vs 009 no uppercase | Distinct FR-01 clauses — **keep both** |
| 001 full reset vs 014 OTP length | Complementary — **keep both** |
| Confirm mismatch dedicated case | Deferred — covered by 010 presence + strength cases |

**Result:** **14** IDs retained.

---

## 2. Observable oracle map

| ID | Channel | Oracle |
| --- | --- | --- |
| 001 | UI + API | Success dialog; `/login`; `apiLogin` with new password succeeds |
| 002–004 | UI | Error dialog/text; remain on forgot-password / not advanced incorrectly |
| 005–009 | UI + API | Reject reset; original password still authenticates when applicable |
| 010 | UI | Confirm-password control **visible** |
| 011 | UI | Text matching step indicator (e.g. Bước 1 / 2) |
| 012 | UI + URL | Back-to-login control → `/login` |
| 013 | UI | Email input `type="email"` |
| 014 | UI | Demo OTP length **6** (`otpLength`) |

---

## 3. Likely SUT defect failures (forecast)

| ID | Forecast |
| --- | --- |
| 010–014 | **Fail** — confirm missing, no indicator, back≠login, type=text, OTP 4 digits |
| 001–009 | **Pass** (probable) after sync-dialog / wait fixes |

## 4. Next

**Model data** → `test-data/fr03-forgot-password.json` + `docs/fr03-model-data.md`.

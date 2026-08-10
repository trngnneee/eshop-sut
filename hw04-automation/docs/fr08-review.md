# Feature B — FR-08 · Review

**Student ID:** 23127271  
**Date:** 2026-08-09  

> Spec oracles **not** softened.

---

## 1. Duplicate / overlap

| Pair | Verdict |
| --- | --- |
| 001 guest cart vs 002 direct URL | Distinct entry points — **keep both** |
| 005 lines vs 013 two lines vs 014 qty | Distinct — **keep** |
| 007 readonly vs 008 API tamper | UI vs server — **keep both** |
| 004 happy vs 009 cart clear | Complementary — **keep both** |

**Result:** 14 IDs retained.

---

## 2. Observable oracles

| ID | Oracle focus |
| --- | --- |
| 001 | Dialog / redirect toward login; URL |
| 002 | Guest direct checkout blocked (URL / dialog) |
| 003 | Empty cart cannot complete (dialog / stay) |
| 004 | Success path completes |
| 005 / 013 / 014 | Line visibility / count / qty text |
| 006 | Total text contains đồng formatting cue |
| 007 | `totalReadonly` — total control not editable |
| 008 | `orderTotalEquals` cart-computed total after tamper POST |
| 009 | `cartEmpty` after success |
| 010 / 011 | Heading / confirm button visible |
| 012 | `apiStatus` unauthorized |

---

## 3. Likely failures

**Fail:** 002, 003, 007, 008, 009 (known HW02/SUT defects).  
**Pass (probable):** 001, 004–006, 010–014.

## Next

**Model data** → `fr08-checkout.json` + `fr08-model-data.md`.

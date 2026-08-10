# Feature B — FR-08 · Verify

**Student ID:** 23127271  
**Date:** 2026-08-09  
**Result:** Chromium **9 pass / 5 fail**; matrix same × 3 browsers  
**Reports:** `reports/html/fr08-checkout/<browser>/` · `Run by: 23127271`  
**Guard:** `npm run evidence:verify-fr03` OK before/after

---

## Failures (oracles kept)

| Case | Defect |
| --- | --- |
| TC-CHECKOUT-002 | No auth guard on `/checkout` |
| TC-CHECKOUT-003 | Empty cart checkout allowed |
| TC-CHECKOUT-007 | Payment total editable |
| TC-CHECKOUT-008 | Backend trusts client total |
| TC-CHECKOUT-009 | Cart not cleared after checkout |

Bugs: `BUG-FR08-001`…`005`.

## Automation note

SPA cart seeding required navigation fix so seeded items survive until checkout inspect/confirm.

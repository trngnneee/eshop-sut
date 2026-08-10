# Feature B — FR-08 · Design

**Student ID:** 23127271  
**Based on:** `fr08-analysis.md`  
**Date:** 2026-08-09  

> **14** cases. Oracles follow README FR-08, not SUT defects.

---

## Traceability

| Requirement | Case IDs |
| --- | --- |
| Auth gate / guest | 001, 002, 012 |
| Empty cart blocked | 003 |
| Happy path | 004 |
| Line items visible | 005, 013, 014 |
| Total formatting / readonly | 006, 007 |
| Server recalc / anti-tamper | 008 |
| Cart cleared | 009 |
| Checkout chrome | 010, 011 |

---

## Case ledger (14)

| ID | Category | Covered rule |
| --- | --- | --- |
| TC-CHECKOUT-001 | negative | Guest from cart → login block |
| TC-CHECKOUT-002 | negative | Direct `/checkout` without login blocked |
| TC-CHECKOUT-003 | negative | Empty cart checkout blocked |
| TC-CHECKOUT-004 | positive | Logged-in + items completes checkout |
| TC-CHECKOUT-005 | validation | Line item(s) listed |
| TC-CHECKOUT-006 | validation | Total uses Vietnamese đồng formatting |
| TC-CHECKOUT-007 | validation | Total not directly editable |
| TC-CHECKOUT-008 | negative | Client-tampered `total_amount` rejected / ignored |
| TC-CHECKOUT-009 | state | Cart cleared after success |
| TC-CHECKOUT-010 | ui | Confirmation heading when checkout reachable |
| TC-CHECKOUT-011 | ui | Confirm payment button visible |
| TC-CHECKOUT-012 | negative | Unauthenticated API checkout rejected |
| TC-CHECKOUT-013 | boundary | Two distinct product lines |
| TC-CHECKOUT-014 | boundary | Quantity marker for single-unit line |

## Next

**Review** → `docs/fr08-review.md`.

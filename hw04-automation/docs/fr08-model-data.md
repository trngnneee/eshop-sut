# Feature B — FR-08 · Model data

**Student ID:** 23127271  
**File:** `test-data/fr08-checkout.json`  
**Cases:** 14 (`TC-CHECKOUT-001…014`)  
**Date:** 2026-08-09  

---

## Schema

Same HW04 pattern: `id`, `category`, `purpose`, `preconditions`, `setup`, `journey`, `inputs`, `expected.assertions[]`.

### `journey` vocabulary

| Journey | Used by |
| --- | --- |
| `guestCartCheckout` | 001 |
| `guestDirectCheckout` | 002 |
| `emptyCartCheckout` | 003 |
| `fullCheckout` | 004, 009 |
| `inspectCheckout` | 005–007, 010, 011, 013, 014 |
| `tamperTotalCheckout` | 008 |
| `apiCheckoutUnauthorized` | 012 |

### Assertion types

`visible` · `hidden` · `containText` · `dialogMatches` · `url` · `count` · `totalReadonly` · `orderTotalEquals` · `cartEmpty` · `apiStatus` (+ loader may allow `attribute` / `dialog`)

## Next

**Map** → `docs/fr08-map-automation.md`.

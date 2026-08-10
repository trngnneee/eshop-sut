# Feature A — FR-03 · Model data

**Student ID:** 23127271  
**File:** `test-data/fr03-forgot-password.json`  
**Cases:** 14 (`TC-FORGOT-001…014`)  
**Date:** 2026-08-07  

> Primitives + logical vocabulary only. Secrets stay in helpers/env.

---

## Schema (per case)

| Field | Notes |
| --- | --- |
| `id` / `category` / `purpose` / `preconditions` | Stable metadata |
| `setup` | Flags e.g. `createUser` |
| `journey` | Dispatcher key |
| `inputs` | email modes, OTP modes, password variants |
| `expected.assertions[]` | Typed oracles |

### `journey` vocabulary

| Journey | Used by |
| --- | --- |
| `fullReset` | 001, 005–009 |
| `requestOnly` | 002–004 |
| `requestThenInspect` | 010, 014 |
| `uiContract` | 011, 013 |
| `backToLogin` | 012 |

### Assertion types

`visible` · `hidden` · `containText` · `attribute` · `dialog` · `dialogMatches` · `url` · `apiLogin` · `otpLength`

---

## ID → record map

All 14 Design/Review IDs have exactly one JSON record. Loader rejects unknown journeys/assertions and fewer than 12 records.

## Next

**Map automation** → `docs/fr03-map-automation.md`.

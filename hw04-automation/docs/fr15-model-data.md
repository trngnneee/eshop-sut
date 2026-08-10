# Feature C — FR-15 · Model data

**Student ID:** 23127271  
**File:** `test-data/fr15-admin-product.json`  
**Cases:** 14 (`TC-PRODUCT-001…014`)  
**Date:** 2026-08-10  

> Primitives + logical vocabulary only. **No** CSS/XPath selectors, **no** passwords/tokens in JSON.

---

## Schema (per case)

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Stable case ID |
| `category` | string | positive / negative / boundary / state |
| `purpose` | string | Covered rule |
| `preconditions` | string | Human-readable |
| `setup` | object | Flags only: `authMode`, `seedProduct`, `seedSibling`, `ensureCategory`, `cleanupProduct` |
| `journey` | string | Dispatcher key (see below) |
| `inputs` | object | Primitives / modes (see below) |
| `expected.assertions[]` | array | Typed oracles with primitive params |

### `setup.authMode` (secrets stay in env/helpers)

| Value | Meaning |
| --- | --- |
| `admin` | Helper reads admin credentials from env or README seed defaults |
| `user` | Helper obtains non-admin JWT |
| `none` | No `Authorization` header |

### `journey` vocabulary

| Journey | Used by |
| --- | --- |
| `uiCreate` | 001 |
| `uiView` | 002 |
| `uiEdit` | 003 |
| `uiEditIsolation` | 004 |
| `uiDelete` | 005 |
| `apiCreate` | 006–014 |

### `inputs` modes (no giant strings / secrets)

| Key | Values |
| --- | --- |
| `nameMode` | `unique` · `empty` · `fixedLength` |
| `nameLength` / `nameChar` | For BVA 255/256 |
| `namePrefix` / `editNamePrefix` / `siblingNamePrefix` | Prefix only; helper adds unique suffix |
| `price` / `editPrice` / `siblingPrice` | numbers |
| `categoryMode` | `existingFirst` · `invalidId` · `literal` |
| `categoryId` | number when mode needs a literal/invalid id |

### Assertion types (logical targets, not selectors)

`apiStatus` · `apiProductExists` · `apiProductAbsent` · `apiProductFieldEquals` · `apiSiblingUnchanged` · `uiSiblingNameUnchanged` · `visible` · `hidden` · `containText`

Logical `target` keys only: `productRow`, `priceCell`, `siblingRow`.

---

## ID → record map

All 14 Design/Review IDs have exactly one JSON record. Loader validation (later Generate) must reject unknown journeys/assertions and `< 12` records.

## Next

**Map automation** done → `docs/fr15-map-automation.md`.  
**Generate** next (loader FR-15 allow-lists + `AdminProductPage` + `fr15-admin-product.spec.js`).

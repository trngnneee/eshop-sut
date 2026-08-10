# Feature C — FR-15 · Verify (Chromium smoke)

**Student ID:** 23127271  
**Date:** 2026-08-10  
**Command:** `npx playwright test tests/fr15-admin-product.spec.js --project=chromium`  
**Env:** API `:3000` · Admin `:5174` · `ADMIN_BASE_URL=http://localhost:5174`

> Spec oracles **not** changed to match defective SUT.

---

## Result summary

| | Count | IDs |
| --- | ---: | --- |
| **Passed** | **6** | 001, 002, 003, 005, 007, 011 |
| **Failed** | **8** | 004, 006, 008, 009, 010, 012, 013, 014 |
| Total | 14 | |

Matches Review forecast (~6 pass / 8 defect fails).

---

## Failure list (observed)

| ID | Assertion that failed | Observed | Classification |
| --- | --- | --- | --- |
| **004** | `uiSiblingNameUnchanged` | Row with sibling name **not found** after edit (mass-rename UI) | **Product defect** (`fakeMassUpdatedProducts`) |
| **006** | `apiStatus` 400–499 | `POST` returned **200** for empty name | **Product defect** (no server validation) |
| **008** | `apiStatus` 400–499 | `POST` returned **200** for name length 256 | **Product defect** |
| **009** | `apiStatus` 400–499 | `POST` returned **200** for `price: 0` | **Product defect** |
| **010** | `apiStatus` 400–499 | `POST` returned **200** for `price: -1` | **Product defect** |
| **012** | `apiStatus` 400–499 | `POST` returned **200** for `category_id: 999999` | **Product defect** |
| **013** | `apiStatus` 401–403 | `POST` without JWT returned **200** | **Product defect** (FR-12 / HW02 #182) |
| **014** | `apiStatus` 401–403 | `POST` with user JWT returned **200** | **Product defect** (FR-12 role gate) |

Note: For 004, `apiSiblingUnchanged` did not appear in the stack (failure stopped on UI). Sibling persistence in API may still be correct; UI oracle alone is enough to fail the case per Review.

---

## Targeted fixes — **do not** soften expected

### A. Keep as failing product evidence (no JSON/oracle change)

| Cases | Correct action |
| --- | --- |
| 006, 008, 009, 010, 012 | File/keep bug: server must reject invalid name/price/category (FR-15). |
| 013, 014 | File/keep bug: `POST/PUT/DELETE /api/products` need JWT + `role=admin` (FR-12). |
| 004 | File/keep bug: after edit, only target product UI row may change — remove `fakeMassUpdatedProducts`. |

**Forbidden:** changing `expected.assertions` min/max to accept `200`, removing `uiSiblingNameUnchanged`, or skipping these cases.

### B. Optional automation clarity (oracle unchanged)

| Issue | Proposed repair | Why safe |
| --- | --- | --- |
| 004 fail message is “element(s) not found” | Before edit, capture sibling **row index** (or row handle); after edit, `expect(row.nth(index)).toContainText(siblingName)` | Still requires original sibling name on that row; fails with clearer “got mass-renamed text” instead of missing locator |
| 004 dual oracle order | Run `apiSiblingUnchanged` then UI (or soft-collect both) so report shows API pass + UI fail | Does not weaken either check |
| Negative API cases leave junk rows if create wrongly succeeds | Cleanup already deletes `createdIds` — confirm afterEach always runs (it does) | Hygiene only |

### C. Environment (already handled this run)

| Issue | Fix applied / note |
| --- | --- |
| Missing Chromium binary | `npx playwright install chromium` |
| Admin SPA down | Started `frontend-admin` `npm run dev` on `:5174` |

---

## Next

1. Optionally apply **B** (004 locator-by-index) — still expects sibling name.  
2. Add `bug-reports/BUG-FR15-*` for the 8 defects.  
3. Full matrix: `npm run test:matrix:fr15` + `evidence:verify-fr03`.

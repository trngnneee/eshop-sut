# Feature C — FR-15 · Review

**Student ID:** 23127271  
**Stage:** Review (Model data done → `fr15-admin-product.json`; Generate not started)  
**Input:** `docs/fr15-design.md` (14 cases) · `docs/fr15-analysis.md`  
**Date:** 2026-08-10  

> No JSON / Playwright in this stage. Spec oracles **not** softened to match SUT.

---

## 1. Duplicate / overlap check

| Pair | Verdict | Action |
| --- | --- | --- |
| 001 Create vs 002 View | Near-overlap if 001 already asserts “row in list” | **Keep both.** Narrow oracles: **001** = persist via Create success (API record by unique name); **002** = UI Read of an existing product (name + price cell visible). Do not treat 002 as a second Create. |
| 003 Edit vs 004 Isolation | Complementary, not duplicate | **Keep both.** 003 → target A changed; 004 → sibling B unchanged (UI **and** API). |
| 009 price `0` vs 010 price `-1` | Distinct invalid classes under “> 0” | **Keep both** (not cosmetic padding). |
| 013 no JWT vs 014 non-admin JWT | Distinct FR-12 clauses | **Keep both** (existence of token ≠ `role=admin`). |
| 007 vs 008 (255 / 256) | Classic BVA pair | **Keep both.** |
| 012 missing + invalid category | Two inputs in one ID | **Keep one ID.** Primary input for automation later: **invalid** `category_id` (e.g. `999999`). Missing body field is the same rejection class — do not split into a 15th case. |
| FR-16 Import / FR-14 Category | Out of scope | **Not added.** |

**Result:** No IDs removed. Still **14** distinct logical cases. Refinements are oracle/channel clarifications only.

---

## 2. Observable oracle map

Prefer durable checks: HTTP status, API body fields, UI visibility / row text. Avoid brittle exact `alert()` copy (Analysis A1).

| ID | Channel | Observable oracle (pass criteria) |
| --- | --- | --- |
| **001** | UI Create + API verify | After Lưu: `GET /api/products` contains unique `name` with matching `price` and `category_id`. |
| **002** | UI Read | Product row visible: name text + price cell containing `₫` (FR-21 symbol; thousand-separator not required for this case). |
| **003** | UI Edit + API verify | `GET /api/products/:id` (or list filter) shows A’s **new** name/price; old name no longer on A. |
| **004** | UI + API | After editing A: **API** B.name/B.price unchanged **and** **UI** row for B still shows original name (spec). |
| **005** | UI Delete + API verify | Unique name/`id` absent from list and from `GET /api/products`. |
| **006** | API primary (UI secondary) | `POST /api/products` with `name=""` → **4xx** (or equivalent reject); product count for empty name stays 0. UI: empty name blocked before submit if exercised. |
| **007** | API or UI Create | Create with `name.length === 255` succeeds; record exists with that name. |
| **008** | API Create | `POST` with `name.length === 256` → **4xx** / reject; no row with that 256-char name. |
| **009** | API Create | `POST` with `price: 0` → reject; no stored product with that unique name and price 0. |
| **010** | API Create | `POST` with `price: -1` → reject; no stored product with that name. |
| **011** | API or UI Create | Create with `price: 1` succeeds; stored `price` is `1` (number or numeric string). |
| **012** | API Create | `POST` with `category_id: 999999` (or omitted) → reject; no product with that unique name. |
| **013** | API only | `POST /api/products` **without** `Authorization` → **401/403**; name not in catalog. |
| **014** | API only | `POST /api/products` with **user** JWT (`role=user`) → **403** (or authz failure); name not in catalog. |

### Locked decisions (from Analysis ambiguities)

| Ambiguity | Review decision |
| --- | --- |
| A1 error message text | Do **not** assert exact Vietnamese alert strings; assert reject + non-persistence. |
| A2 decimal vs integer price | Boundary happy path uses integer **`1`**. |
| A3 delete confirm | **Out of suite** (not FR-15). |
| A4 UI exists | Oracles assume Products tab CRUD UI present. |
| A5 FR-16 Import | Excluded from case set. |
| 004 UI vs API diverge | Assert **both**; UI failure alone still fails the case (spec: siblings unchanged on screen). |

---

## 3. Likely SUT defect failures (do not soften)

Based on Analysis §8 / HW02 #182–#183. Status = expected outcome **against current SUT** if oracles above are kept.

| ID | Likely result vs SUT | Why |
| --- | --- | --- |
| 001 | **Pass** (probable) | Create path works without validation for valid data. |
| 002 | **Pass** (probable) | List renders name + `₫`. |
| 003 | **Pass** (API); UI list may look wrong | PUT updates one `id`; list refresh uses mass-rename only after edit — assert API for A’s fields. |
| 004 | **Fail** (UI oracle) | `fakeMassUpdatedProducts` sets **every** row’s displayed name to A’s new name; API B may still be correct → case still **fails** on UI spec. |
| 005 | **Pass** (probable) | DELETE works. |
| 006 | **Fail** (API) | No server name validation; empty/`null` name may insert. UI `required` alone does not satisfy FR-15 if API accepts empty. |
| 007 | **Pass** (probable) | No max-length check ⇒ 255 accepted. |
| 008 | **Fail** | No client `maxLength` / server length check ⇒ 256 accepted. |
| 009 | **Fail** | API inserts `price: 0`. |
| 010 | **Fail** | API inserts negative price. |
| 011 | **Pass** (probable) | Positive price stored. |
| 012 | **Fail** | No category existence / required check on API. |
| 013 | **Fail** | `POST /api/products` has no `authenticateToken` (HW02 #182). |
| 014 | **Fail** | No admin-role gate on product mutate (FR-12). |

### Forecast summary

| | IDs | Count |
| --- | --- | ---: |
| Likely **pass** | 001, 002, 003*, 005, 007, 011 | ~6 |
| Likely **fail** (product defect) | 004, 006, 008, 009, 010, 012, 013, 014 | **8** |

\*003 pass if oracle is API-targeted update; do not require post-edit UI list purity (that belongs to 004).

Same policy as FR-03/FR-08: failing cases remain in the suite as defect evidence.

---

## 4. Coverage after Review

| Requirement | Case IDs | Oracle channel |
| --- | --- | --- |
| FR-15 Create | 001 | UI + API |
| FR-15 Read | 002 | UI |
| FR-15 Update | 003 | UI action + API |
| FR-15 edit isolation | 004 | UI + API |
| FR-15 Delete | 005 | UI + API |
| Name required / max 255 | 006, 007, 008 | API (+ UI for 006 secondary) |
| Price > 0 | 009, 010, 011 | API (+ UI ok for 011) |
| Category required/valid | 012 | API |
| FR-12 authz | 013, 014 | API |

**Count unchanged: 14.** Ready for Model data (still no code).

---

## 5. Next stage

Model data written: `test-data/fr15-admin-product.json` + `docs/fr15-model-data.md`.  
Not yet: Map automation · Generate · Verify.

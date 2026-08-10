# Feature C — FR-15 Product CRUD (Admin) · Design

**Student ID:** 23127271  
**Status:** Design (Review complete — see `fr15-review.md`; Model data not started)  
**Based on:** `docs/fr15-analysis.md`  
**Date:** 2026-08-10  

> No external JSON and no Playwright in this stage. Case count: **14** (≥12).  
> Oracles follow **README FR-15 / FR-12**, not current SUT defects.

---

## Traceability

| Requirement | Case IDs |
| --- | --- |
| FR-15 Create (Thêm) | 001 |
| FR-15 Read (Xem) | 002 |
| FR-15 Update (Sửa) | 003 |
| FR-15 Edit isolation (chỉ SP đó đổi) | 004 |
| FR-15 Delete (Xóa) | 005 |
| FR-15 Tên bắt buộc | 006 |
| FR-15 Tên max 255 | 007, 008 |
| FR-15 Giá > 0 | 009, 010, 011 |
| FR-15 Danh mục bắt buộc / hợp lệ | 012 |
| FR-12 Auth on product mutate | 013, 014 |

---

## Case ledger (14)

| ID | Category | Covered rule |
| --- | --- | --- |
| TC-PRODUCT-001 | positive | Create valid product |
| TC-PRODUCT-002 | positive | View / list shows created product |
| TC-PRODUCT-003 | positive | Edit updates target product fields |
| TC-PRODUCT-004 | state | Edit one product must not change siblings |
| TC-PRODUCT-005 | positive | Delete removes product |
| TC-PRODUCT-006 | negative | Empty name rejected |
| TC-PRODUCT-007 | boundary | Name length 255 accepted |
| TC-PRODUCT-008 | boundary | Name length 256 rejected |
| TC-PRODUCT-009 | negative | Price `0` rejected |
| TC-PRODUCT-010 | negative | Negative price rejected |
| TC-PRODUCT-011 | boundary | Smallest positive price (`1`) accepted |
| TC-PRODUCT-012 | negative | Missing / invalid category rejected |
| TC-PRODUCT-013 | negative | Unauthenticated `POST /api/products` rejected (FR-12) |
| TC-PRODUCT-014 | negative | Non-admin JWT cannot mutate products (FR-12) |

---

## Case details

### TC-PRODUCT-001 — Create valid product
- **Category:** positive  
- **Purpose:** Admin creates a product with valid name, price > 0, and existing category.  
- **Preconditions:** Admin logged in; ≥1 category seeded; unique product name for the run.  
- **Input ref:** `name` unique · `price` e.g. `150000` · `category_id` existing · optional description/image.  
- **Steps:** Open Admin → Sản phẩm → fill form → Lưu sản phẩm.  
- **Expected:** Product persisted; appears in list and/or `GET /api/products` with matching fields.  
- **Cleanup:** Delete created product (API or UI).

### TC-PRODUCT-002 — View product in list
- **Category:** positive  
- **Purpose:** Admin can view products (Read).  
- **Preconditions:** Admin logged in; known product exists (seed or setup Create).  
- **Input ref:** Existing product `name` / `id`.  
- **Steps:** Open Sản phẩm tab; locate product row.  
- **Expected:** Row visible with name and price (₫).  
- **Cleanup:** None if using seed; cleanup if setup-created.

### TC-PRODUCT-003 — Edit target product
- **Category:** positive  
- **Purpose:** Admin edits one product’s name/price/category successfully.  
- **Preconditions:** Admin logged in; product A exists.  
- **Input ref:** New name / new positive price / valid category for A.  
- **Steps:** Click Sửa on A → change fields → Lưu.  
- **Expected:** Product A fields updated in persistence (`GET /api/products/:id` or list after refresh from API).  
- **Cleanup:** Restore or delete A.

### TC-PRODUCT-004 — Edit isolation (siblings unchanged)
- **Category:** state  
- **Purpose:** When editing product A, product B keeps original name/price (FR-15).  
- **Preconditions:** Admin logged in; products A and B exist with distinct names.  
- **Input ref:** Edit A to new name; capture B’s name/price before edit.  
- **Steps:** Edit and save A; observe B in UI list **and** via API.  
- **Expected:** B unchanged in **API** and **UI** (spec). *Known SUT risk:* UI may rename all rows — keep UI+API oracle; do not soften.  
- **Cleanup:** Delete A/B if created for test.

### TC-PRODUCT-005 — Delete product
- **Category:** positive  
- **Purpose:** Admin deletes a product.  
- **Preconditions:** Admin logged in; disposable product exists.  
- **Input ref:** Product `id` / unique name.  
- **Steps:** Click Xóa on target row (or equivalent).  
- **Expected:** Product absent from list and `GET /api/products` (or empty/404 for id).  
- **Cleanup:** N/A (already deleted).

### TC-PRODUCT-006 — Empty name rejected
- **Category:** negative  
- **Purpose:** Name is required.  
- **Preconditions:** Admin logged in.  
- **Input ref:** `name=""` · valid price · valid category.  
- **Steps:** Attempt Create (UI and/or API).  
- **Expected:** Create fails; no new product with empty name. Prefer status/rejection over exact alert text (Analysis A1).  
- **Cleanup:** None.

### TC-PRODUCT-007 — Name length 255 accepted
- **Category:** boundary  
- **Purpose:** Max name length 255 is valid.  
- **Preconditions:** Admin logged in; unique 255-char name.  
- **Input ref:** `name` length 255 · price > 0 · valid category.  
- **Steps:** Create via UI or API.  
- **Expected:** Product created successfully.  
- **Cleanup:** Delete product.

### TC-PRODUCT-008 — Name length 256 rejected
- **Category:** boundary  
- **Purpose:** Name longer than 255 must be rejected.  
- **Preconditions:** Admin logged in.  
- **Input ref:** `name` length 256 · price > 0 · valid category.  
- **Steps:** Attempt Create.  
- **Expected:** Rejected; product not persisted with that name.  
- **Cleanup:** Delete if SUT wrongly accepts (defect evidence).

### TC-PRODUCT-009 — Price zero rejected
- **Category:** negative  
- **Purpose:** Price must be > 0; `0` invalid.  
- **Preconditions:** Admin logged in.  
- **Input ref:** valid name · `price=0` · valid category.  
- **Steps:** Attempt Create.  
- **Expected:** Rejected; no product stored with price 0.  
- **Cleanup:** As needed if SUT accepts (defect).

### TC-PRODUCT-010 — Negative price rejected
- **Category:** negative  
- **Purpose:** Negative price invalid.  
- **Preconditions:** Admin logged in.  
- **Input ref:** valid name · `price=-1` · valid category.  
- **Steps:** Attempt Create.  
- **Expected:** Rejected; no product with negative price.  
- **Cleanup:** As needed.

### TC-PRODUCT-011 — Minimal positive price accepted
- **Category:** boundary  
- **Purpose:** Smallest practical positive integer price accepted (Analysis A2: use integer `1` ₫).  
- **Preconditions:** Admin logged in.  
- **Input ref:** unique name · `price=1` · valid category.  
- **Steps:** Create.  
- **Expected:** Product created with price 1.  
- **Cleanup:** Delete product.

### TC-PRODUCT-012 — Missing / invalid category rejected
- **Category:** negative  
- **Purpose:** Category required and must exist in list.  
- **Preconditions:** Admin logged in.  
- **Input ref:** valid name · price > 0 · `category_id` missing or nonexistent (e.g. `999999`).  
- **Steps:** Attempt Create via API (UI always defaults a select — API exercises the rule cleanly).  
- **Expected:** Rejected; no product with invalid/missing category.  
- **Cleanup:** As needed.

### TC-PRODUCT-013 — Unauthenticated create blocked (FR-12)
- **Category:** negative  
- **Purpose:** Mutating product API requires JWT.  
- **Preconditions:** No `Authorization` header.  
- **Input ref:** Valid product body.  
- **Steps:** `POST /api/products` without token.  
- **Expected:** `401`/`403` (or equivalent auth failure); product not created.  
- **Cleanup:** Delete if wrongly created (defect — expected vs HW02 #182).

### TC-PRODUCT-014 — Non-admin cannot mutate (FR-12)
- **Category:** negative  
- **Purpose:** `role` must be `admin`, not merely any valid JWT.  
- **Preconditions:** Logged-in regular user token (`test@eshop.com` or API-registered user).  
- **Input ref:** Valid product body + user JWT.  
- **Steps:** `POST /api/products` (and optionally PUT/DELETE) with user token.  
- **Expected:** Forbidden; product not created/updated/deleted.  
- **Cleanup:** As needed if SUT allows (defect).

---

## Mix summary

| Category | IDs | Count |
| --- | --- | ---: |
| positive | 001, 002, 003, 005 | 4 |
| state | 004 | 1 |
| negative | 006, 009, 010, 012, 013, 014 | 6 |
| boundary | 007, 008, 011 | 3 |
| **Total** | | **14** |

Out of scope (do not count): FR-16 CSV Import, FR-14 Category CRUD, delete-confirm dialog (Analysis A3).

---

## Next stage

**Review** complete → `docs/fr15-review.md`.  
Next: **Model data** (still no Playwright until Generate).

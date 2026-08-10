# Feature C — FR-15 Product CRUD (Admin) · Analyze only

**Student ID:** 23127271  
**Stage:** Analyze (done) · Design recorded in `fr15-design.md`  
**Date:** 2026-08-10  
**Sources:** `Repo/eshop-sut/README.md` FR-15 (+ FR-12, FR-21, FR-22), HW02 Feature C notes, current SUT `frontend-admin` + `backend`  
**Tool:** Cursor Agent · skill `automation-testing/playwright-skill.md`

> Scope lock: this document records **analyze only**. No case IDs, no external JSON, no Playwright code.

---

## 1. Contract (HW04 Task 1)

| Item                            | Value                                                                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| Feature                         | C — FR-15 Quản lý sản phẩm (Admin CRUD)                                                                                 |
| App under test                  | Web Admin `http://localhost:5174`                                                                                       |
| API                             | `http://localhost:3000`                                                                                                 |
| Admin seed                      | `admin@eshop.com` / `Admin123!`                                                                                         |
| Target artifacts (later)        | ≥12 data-driven cases · JSON · 3 browsers · HTML `Run by: 23127271`                                                     |
| Planned paths (not created yet) | `test-data/fr15-admin-product.json` · `tests/fr15-admin-product.spec.js` · `reports/html/fr15-admin-product/<browser>/` |
| Evidence rule                   | **Do not** overwrite FR-03 / FR-08 reports; use `npm run test:matrix:fr15` only when implementing                       |

---

## 2. Actors

| Actor                        | Role in FR-15                                                                            |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| **Admin** (`role = 'admin'`) | May Add / View / Edit / Delete products via Admin UI and protected product-mutating APIs |
| **Regular user**             | Must **not** perform product Create/Update/Delete (FR-12)                                |
| **Unauthenticated client**   | Must **not** call mutating product APIs (FR-12)                                          |
| **System / API**             | Persist products; enforce input rules; ensure edit is scoped to one product ID           |

---

## 3. Preconditions

1. Backend API running (`localhost:3000`); Admin SPA on `5174`.
2. At least one **category** exists (seeded) so “Danh mục bắt buộc, chọn từ danh sách có sẵn” is testable.
3. Admin session: valid JWT with `role = 'admin'` (UI stores `adminToken` in `localStorage`).
4. For Edit / Delete: at least one product exists (seed or prior Create).
5. Isolation for later automation: prefer creating unique product names per run and cleaning up; avoid mutating seed catalog permanently when possible.

---

## 4. Operations & state transitions (CRUD)

```text
[Admin logged in]
        │
        ▼
  View list (Read)  ←── refresh after Create / Update / Delete
        │
        ├── Create ──► product appears in list (unique entity)
        ├── Edit    ──► only target product fields change
        └── Delete  ──► product removed from list / GET by id
```

| Operation         | Spec expectation (README FR-15)                         | Typical observable oracle (for later Design)                    |
| ----------------- | ------------------------------------------------------- | --------------------------------------------------------------- |
| **Create (Thêm)** | Valid name + positive price + category → product stored | New row in Admin list and/or `GET /api/products`                |
| **Read (Xem)**    | Admin can see product list/details                      | Table/list shows name, price, image; API returns records        |
| **Update (Sửa)**  | Only the edited product changes; others unchanged       | Target fields updated; sibling products’ names/prices unchanged |
| **Delete (Xóa)**  | Product removed                                         | Row gone from UI/API                                            |

Out of FR-15 scope for this feature slice (do not mix into FR-15 suite unless as dependency setup): CSV Import (**FR-16**), Category CRUD (**FR-14**), Coupon CRUD (**FR-17**).

---

## 5. Input rules (acceptance criteria)

| Field            | Rule                                                  | Boundary / validation notes                                                                     |
| ---------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Tên sản phẩm** | Required; max **255** characters                      | Empty rejected; length 255 accept / 256 reject (Design later)                                   |
| **Giá**          | Required; number **> 0** (strictly positive)          | `0`, negative, non-numeric rejected; smallest valid positive TBD in Design (e.g. `0.01` vs `1`) |
| **Danh mục**     | Required; must be chosen from **existing** categories | Missing / invalid `category_id` rejected                                                        |
| **Mô tả / Ảnh**  | Not constrained by FR-15 text                         | Optional for happy path unless UI marks required                                                |

Related cross-FRs that may appear as **supplementary** checks later (not core FR-15 fields):

| ID        | Relevance                                                                           |
| --------- | ----------------------------------------------------------------------------------- |
| **FR-12** | `POST/PUT/DELETE /api/products` require valid JWT **and** `role = 'admin'`          |
| **FR-21** | Price display uses `₫` with thousand separators                                     |
| **FR-22** | Required fields marked `*`; errors above submit; email `type="email"` on login form |

---

## 6. Outputs / feedback

- Success: persisted change reflected in product list (and API).
- Failure: reject invalid Create/Update; show suitable error (UI alert/message and/or HTTP 4xx).
- Edit isolation: after updating product A, product B must keep prior name/price/category.

---

## 7. Ambiguities (to resolve in Review, not invent in Analyze)

| #   | Ambiguity                                                                                                             | Impact                                                                      |
| --- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| A1  | Exact error **message text** for empty name / non-positive price / missing category                                   | Oracle should prefer stable HTTP status + field rejection over brittle copy |
| A2  | Whether price must be **integer VND** or allow decimals                                                               | Spec says “số dương (> 0)” only                                             |
| A3  | Whether Delete needs a **confirm dialog** (FR-24 mentions cart delete confirm; FR-15 silent)                          | Treat confirm as optional unless HW02/FR-24 is explicitly in scope          |
| A4  | HW02 #181 claimed “Admin product CRUD UI not implemented”; **current** Admin SPA has a Products tab with form + table | Analysis uses **current** SUT, not outdated issue title                     |
| A5  | FR-16 Import sits on the same Products tab — keep out of FR-15 case set                                               | Avoid counting Import rows toward FR-15’s ≥12                               |

---

## 8. SUT observations (code / behavior vs spec)

Inspected: `frontend-admin/src/App.jsx`, `backend/server.js` (product routes), seed in `database.js`.

| Area                    | Spec                        | Current SUT observation                                                                                                                                                                              |
| ----------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Admin UI CRUD           | Add/View/Edit/Delete        | Products tab exists: form (name, price, imageUrl, description, category select), list with Sửa/Xóa                                                                                                   |
| Name required           | Required                    | HTML `required` on name input only                                                                                                                                                                   |
| Name max 255            | Max 255                     | No `maxLength` / no server length check observed                                                                                                                                                     |
| Price > 0               | Required positive           | `type="number"` without `min` / `required`; API inserts body as-is                                                                                                                                   |
| Category required       | Must choose from list       | Defaults `category_id: 1`; no empty option / no server check for missing/invalid id                                                                                                                  |
| Edit isolation          | Only edited product changes | After PUT success, UI runs `fakeMassUpdatedProducts`: **all** list rows get the edited **name** (display corruption). API PUT appears to update one `id` only — UI oracle and API oracle may diverge |
| FR-12 on product mutate | JWT + admin role            | `POST/PUT/DELETE /api/products` have **no** `authenticateToken`; anyone can mutate. `authenticateToken` itself does **not** assert `role === 'admin'`                                                |
| FR-21 currency          | `₫` + thousands             | List shows `{price} ₫` without `toLocaleString()`                                                                                                                                                    |
| Admin login form        | FR-02/FR-22 email type      | Email input has no `type="email"` (placeholder only) — related to HW02 #184 risk for admin entry                                                                                                     |
| Delete confirm          | (not in FR-15)              | Immediate delete, no dialog                                                                                                                                                                          |

**Implication for later stages:** keep **spec oracles** even when SUT fails (same policy as FR-03/FR-08). Expected product-defect themes: missing API auth/role, missing server validation, mass-name UI after edit, currency formatting, possibly login field type.

---

## 9. Dependencies & environment

| Dependency           | Note                                                                                                  |
| -------------------- | ----------------------------------------------------------------------------------------------------- |
| Categories seed      | Needed for category select / valid `category_id`                                                      |
| Admin credentials    | Prefer seed admin; do not weaken password in tests                                                    |
| Feature A/B evidence | Frozen FR-03 locks + FR-08 reports must remain; matrix filter `fr15` / `C` only                       |
| Matrix runner        | `package.json` already has `test:matrix:fr15` / `test:matrix:c` pointing at slug `fr15-admin-product` |

### Safe commands when Feature C is implemented later

```powershell
cd SoftwareTesting-HW\HW4\23127271
npm run evidence:verify-fr03
npm run test:matrix:fr15
```

Avoid pointing `FEATURE_SLUG` at `fr03-forgot-password` or `fr08-checkout`, and avoid `FORCE_OVERWRITE=1` unless intentionally regenerating A.

---

## 10. Requirement ledger (Analysis snapshot)

| Feature   | Source               | Case IDs            | Count | Data file                   | Spec file                      | Browsers | Reports                                      |
| --------- | -------------------- | ------------------- | ----: | --------------------------- | ------------------------------ | -------- | -------------------------------------------- |
| FR-03 (A) | done                 | TC-FORGOT-001…014   |    14 | `fr03-forgot-password.json` | `fr03-forgot-password.spec.js` | 3        | **FROZEN**                                   |
| FR-08 (B) | done                 | TC-CHECKOUT-001…014 |    14 | `fr08-checkout.json`        | `fr08-checkout.spec.js`        | 3        | kept                                         |
| FR-15 (C) | README FR-15 + FR-12 | TC-PRODUCT-001…014 |    14 | TBD                         | TBD                            | 3        | `reports/html/fr15-admin-product/<browser>/` |

---

## 11. Next stage

Design is in `docs/fr15-design.md`. Remaining: **Review** → Model data → Map → Generate → Verify.  
Still no JSON / Playwright until those stages.

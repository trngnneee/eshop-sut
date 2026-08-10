# Feature C — FR-15 · Map automation

**Student ID:** 23127271  
**Stage:** Map (Generate / Verify **not started**)  
**Inputs:** `fr15-model-data.md` · `fr15-admin-product.json` · Admin SPA `App.jsx`  
**Date:** 2026-08-10  

> Skill separates **Map** from **Generate**. This file locks locators, setup/cleanup, journey actions, and expect vocabulary.  
> **Do not** treat this as implemented code — full spec/helpers land in **Generate**.

---

## 1. Runtime surfaces

| Surface | URL / key | Notes |
| --- | --- | --- |
| Admin UI | `ADMIN_BASE_URL` default `http://localhost:5174` | Separate from storefront `5173` |
| API | `API_BASE_URL` default `http://localhost:3000` | Shared with FR-03/FR-08 helpers |
| Admin token storage | `localStorage.adminToken` | Not `token` (storefront) |
| Credentials | `ADMIN_EMAIL` / `ADMIN_PASSWORD` or README seed | Never in JSON |
| User JWT (014) | `loginUser` / register unique user | `authMode: user` |

Generate must pass `baseURL` = Admin URL for UI journeys (matrix env or per-test `page.goto(ADMIN_BASE_URL)`).

---

## 2. Locators (page object plan: `pages/AdminProductPage.js`)

Prefer role / placeholder / text. CSS only as last resort for table cells.

### Login gate

| Logical | Locator strategy |
| --- | --- |
| `loginHeading` | `getByRole('heading', { name: /Admin Login/i })` |
| `emailInput` | `getByPlaceholder('Email')` |
| `passwordInput` | `getByPlaceholder('Password')` |
| `loginButton` | `getByRole('button', { name: /^Login$/i })` |

### Shell / nav

| Logical | Locator strategy |
| --- | --- |
| `navProducts` | `getByText('Sản phẩm', { exact: true })` (sidebar) |
| `logout` | `getByText('Đăng xuất', { exact: true })` |
| `productsHeading` | `getByRole('heading', { name: /Quản lý Sản phẩm/i })` |

### Product form

| Logical | Locator strategy |
| --- | --- |
| `nameInput` | `getByPlaceholder('Tên sản phẩm')` |
| `priceInput` | `getByPlaceholder('Giá tiền')` |
| `imageUrlInput` | `getByPlaceholder('URL Ảnh')` |
| `descriptionInput` | `getByPlaceholder('Mô tả')` |
| `categorySelect` | `locator('form select')` (only select on product form) |
| `saveButton` | `getByRole('button', { name: /Lưu sản phẩm/i })` |
| `cancelEditButton` | `getByRole('button', { name: /Hủy sửa/i })` |

### Product table (JSON targets)

| JSON `target` | Locator strategy |
| --- | --- |
| `productRow` | `getByRole('row').filter({ hasText: productName })` |
| `priceCell` | `productRow.locator('td').nth(2)` (Ảnh · Tên · **Giá** · Hành động) |
| `siblingRow` | `getByRole('row').filter({ hasText: siblingName })` |
| (actions) | Within row: `getByRole('button', { name: /^Sửa$/ })` · `getByRole('button', { name: /^Xóa$/ })` |

**Avoid:** XPath, `.nth(n)` for product identity (use name filter), sleeping for list refresh (wait on row / API).

---

## 3. Setup / cleanup (admin isolation)

### Setup helpers (planned: extend `helpers/auth-api.js` + small `helpers/product-api.js`)

| Flag / mode | Action |
| --- | --- |
| `authMode: admin` | `loginUser(adminCreds)` → token; for UI: inject `localStorage.adminToken` then goto Admin; for API: `Authorization: Bearer` |
| `authMode: user` | Register unique user **or** login seed user → JWT (must be `role=user`) |
| `authMode: none` | No header / clear `adminToken` |
| `ensureCategory` | `GET /api/categories` → pick first id; fail test if empty |
| `seedProduct` | `POST /api/products` with resolved unique name/price/category (even though API lacks auth — use for deterministic setup) |
| `seedSibling` | Second `POST` for product B |
| Resolve `nameMode` | `unique` → `prefix + '-' + Date.now()`; `empty` → `""`; `fixedLength` → `nameChar.repeat(nameLength)` |
| Resolve `categoryMode` | `existingFirst` · `invalidId`/`literal` use `inputs.categoryId` |

### UI session inject (mirror FR-08 pattern)

```text
goto ADMIN_BASE_URL → evaluate localStorage.setItem('adminToken', token)
→ reload → expect products nav or dashboard visible
```

Fallback: fill login form with env/seed admin if inject fails.

### Cleanup

| Flag | Action |
| --- | --- |
| `cleanupProduct: true` | After test (finally): `DELETE /api/products/:id` for all ids tracked in runtime (`createdIds`) |
| `cleanupProduct: false` | Only for delete journey (005) where absence is the oracle — still track accidental leftovers from failed asserts |
| Isolation | Unique name prefixes per case (`HW04-P00x-…`); workers=1 already in config |

**Do not** mutate FR-03/FR-08 artifacts; run via `test:matrix:fr15` only when Verify starts.

---

## 4. Journey → actions (dispatcher vocabulary)

No branching on case **ID** in Generate — only on `journey`.

| `journey` | Steps |
| --- | --- |
| `uiCreate` | Admin session → open Products → fill form from resolved inputs → click Lưu → capture create response if intercepted **or** verify via GET |
| `uiView` | Admin session → seed product (setup) → open Products → locate `productRow` |
| `uiEdit` | Seed A → open Products → Sửa on A → fill edit fields → Lưu → API read A |
| `uiEditIsolation` | Seed A+B → edit A → assert B UI + API |
| `uiDelete` | Seed product → Xóa → assert absent |
| `apiCreate` | Build body from inputs → `POST /api/products` with auth from `authMode` → store `createResponse` status + body |

Optional network intercept on UI save: `page.waitForResponse(/\/api\/products/)` for status when useful; primary persistence checks stay on GET list.

---

## 5. Expect vocabulary → Playwright / API checks

| Assertion `type` | Implementation sketch | Pattern family |
| --- | --- | --- |
| `visible` | `expect(resolveTarget(target)).toBeVisible()` | Visibility |
| `hidden` | `expect(resolveTarget(target)).toBeHidden()` | Visibility |
| `containText` | `expect(target).toContainText(value \| runtime[valueFrom])` | Text |
| `apiStatus` | `expect(runtime[on]).toBeGreaterThanOrEqual(min)` + `toBeLessThanOrEqual(max)` | Plain value |
| `apiProductExists` | GET products → find by name (+ price/category per `match`) → `expect(found).toBeTruthy()` | Plain / collection |
| `apiProductAbsent` | GET → `expect(found).toBeFalsy()` | Plain value |
| `apiProductFieldEquals` | GET by id/name → `expect(Number(field) or field).toEqual(expected)` | Plain value |
| `apiSiblingUnchanged` | Compare B snapshot before/after on listed `fields` | Plain value |
| `uiSiblingNameUnchanged` | `expect(siblingRow).toContainText(originalSiblingName)` | Text |

### ≥3 assertion patterns (HW04)

1. Visibility / hidden — 002, 005  
2. Text (`toContainText`) — 002, 004  
3. Plain / API status & field equality — 001, 006–014, 003  

---

## 6. Per-case map

| ID | Journey | Setup highlights | Primary expects |
| --- | --- | --- | --- |
| 001 | `uiCreate` | admin, ensureCategory, cleanup | `apiProductExists`, create OK status |
| 002 | `uiView` | admin, seedProduct | `visible` row, name text, `₫` in price cell |
| 003 | `uiEdit` | admin, seedProduct | API name/price = edited; old name absent on A |
| 004 | `uiEditIsolation` | admin, seed + sibling | `apiSiblingUnchanged` + `uiSiblingNameUnchanged` |
| 005 | `uiDelete` | admin, seed; cleanup false | `apiProductAbsent` + row `hidden` |
| 006 | `apiCreate` | admin, name empty | status 4xx + absent |
| 007 | `apiCreate` | nameLength 255 | 2xx + exists |
| 008 | `apiCreate` | nameLength 256 | 4xx + absent |
| 009 | `apiCreate` | price 0 | 4xx + absent |
| 010 | `apiCreate` | price -1 | 4xx + absent |
| 011 | `apiCreate` | price 1 | 2xx + price equals 1 |
| 012 | `apiCreate` | categoryId 999999 | 4xx + absent |
| 013 | `apiCreate` | authMode none | 401–403 + absent |
| 014 | `apiCreate` | authMode user | 401–403 + absent |

---

## 7. Files to create in **Generate** (not now)

| Path | Role |
| --- | --- |
| `helpers/load-test-data.js` | Extend FR-15 journeys + assertion allow-lists |
| `helpers/product-api.js` | list/create/update/delete/get categories; resolve name/category |
| `helpers/auth-api.js` | Reuse login; add `getAdminCredentials()` from env |
| `pages/AdminProductPage.js` | Locators + login/openProducts/fill/save/edit/delete |
| `tests/fr15-admin-product.spec.js` | `loadFeatureCases` → setup → `runJourney` → assert loop |
| Matrix | Already: `npm run test:matrix:fr15` / slug `fr15-admin-product` |

---

## 8. Stage gate

| Stage | Status |
| --- | --- |
| Analyze → Model data | Done |
| Map automation | Done |
| **Generate** | **Done** — see §7 files |
| Verify | Next — `npm run test:matrix:fr15` |

Map ≠ Generate: Generate added Playwright page object, helpers, and `fr15-admin-product.spec.js`.

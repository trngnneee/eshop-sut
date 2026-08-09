# Bug Report — FR-13 (Admin Dashboard)

**Student ID:** 23127207 · **Reproduced by:** `tests/dashboard.spec.ts`, `tests/dashboard-api.spec.ts`  
**Execution evidence:** Chromium, Firefox, and WebKit each ran the full 46-case suite and produced
the identical result **22 passed / 24 failed / 46**. Reports:
`HW4/reports/dashboard/{chromium,firefox,webkit}/index.html`, each labeled `Run by: 23127207` with
an ISO timestamp.

An earlier run's `admin-self-delete-blocked` case genuinely deleted the real seed admin account
(confirming the bug below) and broke every later dashboard case in that run — fixed by promoting a
disposable throwaway account to `role='admin'` instead; see `docs/ai-review-dashboard.md` §2.

> **GitHub Issues status:** all 4 new findings below have been filed as real GitHub Issues
> (#325–#327, #329) with screenshot evidence attached. Existing HW02 issue links for
> previously-known bugs (including `BUG-FR13-C-03`, reproduced below) are listed in
> `docs/hw02-reference/tests/issues_list.txt`.

## A. Known issue reproduced

### BUG-FR13-C-02 — Admin API routes lack role-based authorization

- **Severity:** High
- **Cases:** `TC-DASHBOARD-ACL-002`, `003`, `006`, `008`
- **Steps:** Register/login as a normal user, obtain its valid JWT, then call the admin users,
  admin orders, user-delete, or order-status endpoint.
- **Expected:** `403 Forbidden` for a valid non-admin token.
- **Actual:** Requests are accepted (the API tests receive successful behavior rather than `403`).
- **Evidence:** `backend/server.js` applies `authenticateToken` to the routes but never checks
  `req.user.role === 'admin'`.
- **Existing issue:** `https://github.com/trngnneee/eshop-sut/issues/157` (from the HW02 reference list).

### BUG-FR13-C-03 — Dashboard data load has no resilience to a failed sub-request

- **Severity:** Medium
- **Cases:** `TC-DASHBOARD-RESIL-001`
- **Steps:** Intercept and abort just the `GET /api/admin/orders` call (so login itself still
  succeeds), then observe the dashboard after login.
- **Expected:** The admin sees a clear error/retry message.
- **Actual:** No message appears; `App.jsx`'s `fetchData()` runs 5 sequential `axios.get` calls
  with one shared `catch` block that only handles `401`/`403` — any other failure (including one
  request being unreachable) breaks the chain silently.
- **Existing issue:** `https://github.com/trngnneee/eshop-sut/issues/158` (from the HW02 reference
  list; this run reproduces it with a browser-level repro instead of only static source review).

## B. New findings from the API run

### NEW-BUG-FR13-01 — Deleting a nonexistent user returns a false success

- **Severity:** Medium
- **Case:** `TC-DASHBOARD-USR-001`
- **Steps:** Authenticate, send `DELETE /api/admin/users/99999999`.
- **Expected:** HTTP `404` with an explicit “user not found” response.
- **Actual:** HTTP `200` and `{ "message": "User deleted" }` even though no row changed.
- **Evidence:** `backend/server.js` does not inspect `this.changes` in the delete callback.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/325 (screenshot attached)

### NEW-BUG-FR13-02 — Admin can delete its own account

- **Severity:** High
- **Case:** `TC-DASHBOARD-USR-002`
- **Steps:** Login as `admin@eshop.com`, read the admin user's ID, then send
  `DELETE /api/admin/users/<admin-id>` with that token.
- **Expected:** HTTP `400` and the current admin remains present.
- **Actual:** HTTP `200`; the admin row is deleted. Any later admin login then fails until the
  seed account is restored.
- **Evidence:** `backend/server.js` has no self-delete guard and the route currently performs a
  direct delete by ID.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/326 (screenshot attached)

### NEW-BUG-FR13-03 — Canceled orders can be resurrected as delivered

- **Severity:** High
- **Case:** `TC-DASHBOARD-ORD-002`
- **Steps:** Create an order, transition it to `canceled`, then call
  `PUT /api/admin/orders/<id>/status` with `{ "status": "delivered" }`.
- **Expected:** HTTP `400`; a terminal canceled order must remain canceled.
- **Actual:** HTTP `200`; the order changes to `delivered`.
- **Evidence:** The state-transition handler explicitly allows `currentStatus === "canceled"`
  with `status === "delivered"`.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/327 (screenshot attached)

### NEW-BUG-FR13-04 — `DELETE /api/admin/users/:id` never validates the id format

- **Severity:** Medium
- **Cases:** `TC-DASHBOARD-ACL-009` (non-numeric id), `TC-DASHBOARD-ACL-010` (SQL-injection-shaped
  id), `TC-DASHBOARD-USR-005` (negative id)
- **Steps:** `DELETE /api/admin/users/abc`, `DELETE /api/admin/users/1%20OR%201=1`, and
  `DELETE /api/admin/users/-1`, each with a valid admin token.
- **Expected:** HTTP `400` for a malformed id, in all three cases.
- **Actual:** HTTP `200` `{"message":"User deleted"}` for all three, even though nothing matched.
- **Evidence:** The route runs `DELETE FROM users WHERE id = ?` with the raw route parameter and
  never validates it is a positive integer before querying — a distinct root cause from
  `NEW-BUG-FR13-01` (that one is a *valid-format but nonexistent* id; this one is a *malformed* id
  that should never reach the query at all). The SQL-injection-shaped id did not delete other rows
  (parameterized query), but the endpoint still misreports success for an input it should reject.
- **GitHub Issue:** https://github.com/trngnneee/eshop-sut/issues/329 (screenshot attached)

## C. Known UI defect — confirmed on Chromium, Firefox, and WebKit

### BUG-FR13-C-01 — Dashboard revenue is doubled

- **Severity:** High
- **Cases:** Every data-driven case with at least one delivered order fails, including
  `TC-DASHBOARD-DT-001`, `BVA-002`, `DT-005`, `BVA-003`, `BVA-004`, `DT-006`, `DT-007`, `BVA-005`,
  `STATE-001`, and `BVA-006` — identically on all 3 browsers.
- **Steps:** Seed one or more delivered orders, open the admin dashboard, and compare the revenue
  card with the sum of `total_amount`.
- **Expected:** Revenue equals the sum of delivered order amounts, with invalid negative/null data
  handled according to the data-integrity rule.
- **Actual:** `frontend-admin/src/App.jsx` computes `sum + o.total_amount * 2`, so every delivered
  amount is doubled (e.g. a single 500,000₫ delivered order displays as 1,000,000₫). Negative
  amounts also produce negative revenue since there is no nonnegative-data guard.
- **Existing issue:** `https://github.com/trngnneee/eshop-sut/issues/156`.

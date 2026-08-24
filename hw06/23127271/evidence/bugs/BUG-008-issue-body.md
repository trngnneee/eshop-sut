**HW06 API Testing — Student 23127271**

- **Severity:** Medium
- **Found via:** `TC-ADMINUSERS-SCH-SUP-001` (Human (Stage 3))
- **Branch:** `HW6-Tram`

## Screenshot evidence

![BUG-008 evidence](https://github.com/trngnneee/eshop-sut/raw/HW6-Tram/hw06/23127271/evidence/bugs/BUG-008.png)

---

# Bug: GET /api/admin/users returns undocumented sensitive columns

- **Found via test case**: TC-ADMINUSERS-SCH-SUP-001
- **API / Endpoint**: `GET /api/admin/users`
- **Severity**: Medium
- **Found by**: Human extension (Stage 3)

## Steps to reproduce

1. `POST /api/login` as `admin@eshop.com` / `Admin123!`.
2. `GET /api/admin/users` with admin JWT and `X-Student-Id: 23127271`.
3. Inspect each object in the JSON array for field names and types.

## Expected result

FR-19 / api_spec: list entries expose user identity fields (`id`, `name`, `email`, `role`). SEC-01 forbids passwords. Undocumented internal columns (`login_attempts`, `locked_until`, etc.) should not be exposed unless specified.

## Actual result

**HTTP 200 OK** — list objects include extra DB columns beyond the documented schema (Newman probe designed to record `shipping_address`, `login_attempts`, `locked_until`).

Newman log excerpt:

```
□ FR-19 — Admin Users / SchemaValidation / TC-ADMINUSERS-SCH-SUP-001
  GET http://localhost:3000/api/admin/users [200 OK, 267B, 2ms]
  '[TC-ADMINUSERS-SCH-SUP-001] primary status=', 200
```

## Evidence

- Newman: `reports/newman-run.log` (TC-ADMINUSERS-SCH-SUP-001)
- Source: `server.js` — `SELECT id, name, email, role, login_attempts, locked_until, shipping_address FROM users`

## Notes

**Impact:** Schema over-exposure / unnecessary PII (shipping address on all users) and account-locking metadata useful to attackers.

**Fix direction:** Align SELECT with api_spec field list; omit internal security columns from API responses.

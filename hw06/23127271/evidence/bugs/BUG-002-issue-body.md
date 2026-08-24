**HW06 API Testing — Student 23127271**

- **Severity:** Critical
- **Found via:** `TC-ADMINUSERS-SEC-002` (AI (Stage 1))
- **Branch:** `HW6-Tram`

## Screenshot evidence

![BUG-002 evidence](https://github.com/trngnneee/eshop-sut/raw/HW6-Tram/hw06/23127271/evidence/bugs/BUG-002.png)

---

# Bug: Non-admin user receives HTTP 200 on DELETE /api/admin/users/:id

- **Found via test case**: TC-ADMINUSERS-SEC-002
- **API / Endpoint**: `DELETE /api/admin/users/:id`
- **Severity**: Critical
- **Found by**: AI-generated case (Stage 1)

## Steps to reproduce

1. Start EShop SUT at `http://localhost:3000`.
2. `POST /api/login` as `test@eshop.com` / `Test1234!` (role **user**).
3. Ensure a disposable user exists (Setup folder registers one; note `disposableUserId`).
4. Send `DELETE /api/admin/users/{disposableUserId}` with:
   - `Authorization: Bearer <user_token>`
   - `X-Student-Id: 23127271`

## Expected result

SEC-03 / FR-12: a user JWT must **not** delete accounts via the admin API. Target user must remain in `GET /api/admin/users` (as admin).

## Actual result

**HTTP 200 OK** with a JSON success-style body (~293B) when called with the **user** token.

Newman log excerpt:

```
□ FR-19 — Admin Users / Security / TC-ADMINUSERS-SEC-002
  DELETE http://localhost:3000/api/admin/users/<3> [200 OK, 293B, 3ms]
  '[TC-ADMINUSERS-SEC-002] primary status=', 200
```

## Evidence

- Newman: `reports/newman-run.log` (TC-ADMINUSERS-SEC-002)
- Postman request header confirmed: `Authorization: Bearer {{userToken}}`

## Notes

**Suspected root cause:** `DELETE /api/admin/users/:id` uses only `authenticateToken`, not an admin-role check (`server.js`).

**Collection defect (re-test):** The first Newman run used URL `.../users/<3>` (literal angle brackets from `<{{disposableUserId}}>` template). Fix the path to `.../users/{{disposableUserId}}` and re-run to confirm whether row deletion occurs. Even with a malformed id, returning **200** to a non-admin caller indicates missing authorization logic.

**Related:** BUG-001 (same missing admin guard on GET list).

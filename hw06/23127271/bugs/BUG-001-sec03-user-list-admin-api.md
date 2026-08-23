# Bug: Non-admin user can list all users via GET /api/admin/users

- **Found via test case**: TC-ADMINUSERS-SEC-SUP-002
- **API / Endpoint**: `GET /api/admin/users`
- **Severity**: Critical
- **Found by**: Human extension (Stage 3)

## Steps to reproduce

1. Start EShop SUT at `http://localhost:3000`.
2. `POST /api/login` with `email=test@eshop.com`, `password=Test1234!` (role **user**).
3. Send `GET /api/admin/users` with headers:
   - `Authorization: Bearer <user_token>`
   - `X-Student-Id: 23127271`

## Expected result

SEC-03 / FR-12: a regular user JWT must **not** retrieve the full user roster. The API spec §6.1 requires **admin** role for admin endpoints. No password fields in any returned data (SEC-01).

## Actual result

**HTTP 200 OK** — request succeeds with a JSON array of user records (Newman log ~267B response body).

Newman log excerpt:

```
□ FR-19 — Admin Users / Security / TC-ADMINUSERS-SEC-SUP-002
  GET http://localhost:3000/api/admin/users [200 OK, 267B, 3ms]
  '[TC-ADMINUSERS-SEC-SUP-002] primary status=', 200
```

## Evidence

- Newman: `reports/newman-run.log` (TC-ADMINUSERS-SEC-SUP-002 block)
- HTML report: `reports/newman-report.html`
- Postman collection uses `Bearer {{userToken}}` for this request (correct probe wiring)

## Notes

**Suspected root cause:** `server.js` registers `GET /api/admin/users` with only `authenticateToken` — no `role === 'admin'` guard. Any valid JWT can read the user list including internal columns (`login_attempts`, `locked_until`, `shipping_address`).

**Security impact:** Information disclosure + reconnaissance for privilege-escalation attacks (pairs with BUG-002).

# Bug: User can escalate to admin via PUT /api/users/me (role mass assignment)

- **Found via test case**: TC-PROFILE-SEC-007 (also TC-PROFILE-ST-007)
- **API / Endpoint**: `PUT /api/users/me`
- **Severity**: Critical
- **Found by**: AI-generated case (Stage 1)

## Steps to reproduce

1. `POST /api/login` as `test@eshop.com` / `Test1234!`.
2. Confirm `GET /api/users/me` shows `role: "user"`.
3. `PUT /api/users/me` with JSON body:

```json
{
  "name": "Nguyen Van A",
  "phone": "0912345678",
  "shipping_address": "123 Le Loi",
  "role": "admin"
}
```

4. `GET /api/users/me` again with the same token.

## Expected result

SEC-06 / FR-04: clients must **not** change `role` through profile update. `role` must remain `user`.

## Actual result

**HTTP 200 OK** on PUT (Newman log). The SUT accepts `role` in the request body and persists it (confirmed in `server.js`: `if (role) { query += ", role = ?"; }`).

Newman log excerpt:

```
□ FR-04 — Profile / Security / TC-PROFILE-SEC-007
  PUT http://localhost:3000/api/users/me [200 OK, 296B, 16ms]
  '[TC-PROFILE-SEC-007] primary status=', 200
```

## Evidence

- Newman: `reports/newman-run.log` (TC-PROFILE-SEC-007, TC-PROFILE-ST-007)
- Source: `Repo/eshop-sut/backend/server.js` — `app.put("/api/users/me", ...)` updates `role` when present

## Notes

**Security impact:** Full privilege escalation from user to admin, bypassing FR-12 admin-only APIs (compounds BUG-001/BUG-002).

**Fix direction:** Strip/ignore `role` (and other non-FR-04 fields) server-side; never UPDATE role from client profile PUT.

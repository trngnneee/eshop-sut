**HW06 API Testing — Student 23127271**

- **Severity:** Critical
- **Found via:** `TC-PROFILE-SCH-SUP-003` (Human (Stage 3))
- **Branch:** `HW6-Tram`

## Screenshot evidence

![BUG-004 evidence](https://github.com/trngnneee/eshop-sut/raw/HW6-Tram/hw06/23127271/evidence/bugs/BUG-004.png)

---

# Bug: GET /api/users/me exposes password hash (SEC-01 violation)

- **Found via test case**: TC-PROFILE-SCH-SUP-003 (also TC-PROFILE-SCH-SUP-001)
- **API / Endpoint**: `GET /api/users/me`
- **Severity**: Critical
- **Found by**: Human extension (Stage 3)

## Steps to reproduce

1. `POST /api/login` as `test@eshop.com` / `Test1234!`.
2. `GET /api/users/me` with `Authorization: Bearer <user_token>` and `X-Student-Id: 23127271`.
3. Inspect JSON keys in the response body.

## Expected result

SEC-01: responses must **not** include `password`, `password_hash`, or equivalent credential material. API spec documents profile fields only (`name`, `phone`, `shipping_address`, `email`, `role`).

## Actual result

**HTTP 200 OK** with a **446-byte** JSON body (vs ~296B for simple PUT responses), consistent with full `SELECT *` row serialization including sensitive columns.

Newman log excerpt:

```
□ FR-04 — Profile / SchemaValidation / TC-PROFILE-SCH-SUP-003
  GET http://localhost:3000/api/users/me [200 OK, 446B, 2ms]
  '[TC-PROFILE-SCH-SUP-003] primary status=', 200
```

## Evidence

- Newman: `reports/newman-run.log` (TC-PROFILE-SCH-SUP-003, TC-PROFILE-SCH-SUP-001)
- Source: `server.js` — `db.get("SELECT * FROM users WHERE id = ?", ...)` then `res.json(user)`

## Notes

**Security impact:** Credential hash disclosure enables offline cracking and violates SEC-01.

**Fix direction:** Return an explicit column whitelist; never serialize `password` / hash fields.

**Evidence attachment:** Screenshot of GET response with `password` value redacted before submission.

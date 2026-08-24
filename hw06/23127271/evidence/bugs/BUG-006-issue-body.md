**HW06 API Testing — Student 23127271**

- **Severity:** Medium
- **Found via:** `TC-PROFILE-SEC-SUP-004` (Human (Stage 3))
- **Branch:** `HW6-Tram`

## Screenshot evidence

![BUG-006 evidence](https://github.com/trngnneee/eshop-sut/raw/HW6-Tram/hw06/23127271/evidence/bugs/BUG-006.png)

---

# Bug: Profile PUT with Content-Type text/plain causes HTTP 500

- **Found via test case**: TC-PROFILE-SEC-SUP-004 (same pattern as TC-PROFILE-040)
- **API / Endpoint**: `PUT /api/users/me`
- **Severity**: Medium
- **Found by**: Human extension (Stage 3)

## Steps to reproduce

1. `POST /api/login` as `test@eshop.com` / `Test1234!`.
2. `PUT /api/users/me` with:
   - `Authorization: Bearer <user_token>`
   - `Content-Type: text/plain`
   - Body (raw JSON string): `{"name":"Hacked Via Plain","phone":"0912345678","shipping_address":"X"}`
3. Optionally `GET /api/users/me` to check whether profile changed.

## Expected result

SEC-02: with a valid JWT, malformed or non-JSON content types must **not** crash the server or apply unsafe parsing. Profile should remain unchanged if body is ignored. **No HTTP 500** with stack/SQL leak.

## Actual result

**HTTP 500 Internal Server Error** (~1.84kB body).

Newman log excerpt:

```
□ FR-04 — Profile / Security / TC-PROFILE-SEC-SUP-004
  PUT http://localhost:3000/api/users/me [500 Internal Server Error, 1.84kB, 2ms]
  '[TC-PROFILE-SEC-SUP-004] primary status=', 500
```

(TC-PROFILE-040 shows the same 500 pattern for `Content-Type: text/plain`.)

## Evidence

- Newman: `reports/newman-run.log` lines ~1558–1570, ~582–594

## Notes

**Suspected root cause:** Express body parser mismatch — destructuring `req.body` fields when body is empty/malformed leads to DB error and 500 response.

**Fix direction:** Return 400/415 for unsupported media type; do not UPDATE on unparseable body.

# Bug: Admin can delete own account (FR-19 self-delete not enforced)

- **Found via test case**: TC-ADMINUSERS-SEC-003
- **API / Endpoint**: `DELETE /api/admin/users/:id`
- **Severity**: High
- **Found by**: AI-generated case (Stage 1)

## Steps to reproduce

1. `POST /api/login` as `admin@eshop.com` / `Admin123!`.
2. `GET /api/users/me` → note `id` (admin self id, typically `1`).
3. `DELETE /api/admin/users/{admin_self_id}` with admin JWT.
4. `GET /api/admin/users` as admin (if token still valid) or observe login state.

## Expected result

FR-19: an admin must **not** delete their **own** account. Admin row must remain present in the user list.

## Actual result

**HTTP 200 OK** on DELETE when path id equals the logged-in admin (`DELETE .../1` in Newman run).

Newman log excerpt:

```
□ FR-19 — Admin Users / Security / TC-ADMINUSERS-SEC-003
  DELETE http://localhost:3000/api/admin/users/1 [200 OK, 293B, 2ms]
  '[TC-ADMINUSERS-SEC-003] primary status=', 200
```

Follow-up verify GET list also returned 200 (267B) — confirm whether admin row persists after re-test.

## Evidence

- Newman: `reports/newman-run.log` (TC-ADMINUSERS-SEC-003)
- Source: `server.js` — unconditional `DELETE FROM users WHERE id = ?` with no self-id guard

## Notes

**Business impact:** Accidental or malicious self-lockout of the only admin; breaks FR-19 lifecycle rule.

**Fix direction:** Reject DELETE when `req.params.id == req.user.id` (observe-only status not specified — any non-success preferred).

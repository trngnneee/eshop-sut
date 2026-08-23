# TC-ADMINUSERS-SEC-SUP-003: Race — parallel DELETE on same disposable user

## Requirement ID
FR-19 / SEC-02

## Module / Test type / Technique
admin-users / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-02

## Threat / probe
Race — parallel DELETE on same disposable user

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Disposable D registered.

## Test data
```json
{
  "sequence": [
    "DELETE /api/admin/users/D twice in parallel with admin JWT",
    "GET /api/admin/users"
  ]
}
```

## Test steps
1. DELETE /api/admin/users/D twice in parallel with admin JWT
2. GET /api/admin/users

## Expected result
D absent from final list exactly once removed. Second parallel DELETE may error or noop — not specified. No other user deleted; SEC-01 no password in responses. HTTP status is not specified — record actual without inventing codes.

## Type
Unspecified (concurrency)

## Why the AI missed this
Prompt quality — checklist concurrency item omitted from security generator; AI emitted sequential delete probes only (SEC-001/013), not double-delete idempotency side effects.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Parallel DELETE idempotency race.

## Status / Related bugs
Not Run / None

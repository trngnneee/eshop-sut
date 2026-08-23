# TC-ADMINUSERS-SEC-SUP-004: Negative path id -1

## Requirement ID
FR-19 / SEC-05

## Module / Test type / Technique
admin-users / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-05

## Threat / probe
Negative path id -1

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=admin@eshop.com password=Admin123!.
- Snapshot GET /api/admin/users count.

## Test data
```json
{
  "path": {
    "id": "-1"
  }
}
```

## Test steps
1. DELETE /api/admin/users/-1 with admin JWT.
2. GET /api/admin/users — compare count to snapshot.

## Expected result
Must not delete seed users or cause SQL/500 leak. List count unchanged except legitimate target. SEC-05 parameterized path parsing. HTTP status is not specified — record actual without inventing codes.

## Type
Boundary / injection

## Why the AI missed this
Model limitation — path SQLi cases used string tautologies (SEC-004/005/011); numeric boundary ids (-1, 0) as type-confusion deletes are a separate SEC-05 partition.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Negative path id SEC-05 boundary observe.

## Status / Related bugs
Not Run / None

# TC-PROFILE-SEC-SUP-005: Race — concurrent XSS vs SQLi PUT on same field

## Requirement ID
FR-04 / SEC-04 / SEC-05

## Module / Test type / Technique
profile / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-04

## Threat / probe
Race — concurrent XSS vs SQLi PUT on same field

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "sequence": [
    "PUT name=<script>alert(1)</script> (other fields FR-04-valid)",
    "PUT name=Nguyen' OR '1'='1 (parallel, no GET between)",
    "GET /api/users/me"
  ]
}
```

## Test steps
1. PUT name=<script>alert(1)</script> (other fields FR-04-valid)
2. PUT name=Nguyen' OR '1'='1 (parallel, no GET between)
3. GET /api/users/me

## Expected result
GET must return exactly one stored name value, not concatenated/corrupt. SEC-04/SEC-05: no server execution/SQL leak. email/role unchanged. Record winner. HTTP status is not specified — record actual without inventing codes.

## Type
Unspecified (concurrency)

## Why the AI missed this
API characteristic — in-memory/SQLite profile may last-write-win under race; AI never combined SEC-04 and SEC-05 payloads in parallel PUTs to detect torn or mixed malicious storage.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Parallel XSS vs SQLi race; SEC-04/05 observe.

## Status / Related bugs
Not Run / None

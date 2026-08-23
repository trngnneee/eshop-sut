# TC-PROFILE-SEC-SUP-002: Mass assignment — numeric id field in PUT body

## Requirement ID
FR-04 / SEC-06

## Module / Test type / Technique
profile / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-06

## Threat / probe
Mass assignment — numeric id field in PUT body

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- Note seed admin id=1, test user id=2.

## Test data
```json
{
  "body": {
    "name": "Nguyen Van A",
    "phone": "0912345678",
    "shipping_address": "123 Le Loi",
    "id": 1
  }
}
```

## Test steps
1. PUT /api/users/me with body including "id":1 plus FR-04-valid fields.
2. GET /api/users/me.

## Expected result
FR-04: PUT documents only name, phone, shipping_address. Client must not rebind profile to another user id — GET still shows test@eshop.com and original id. HTTP status is not specified — record actual without inventing codes.

## Type
Illegal / mass assignment

## Why the AI missed this
Model limitation — AI mapped SEC-06 to role/password/email/login_attempts only; primary-key id swap in profile body is a classic mass-assignment vector not listed in spec example JSON.

## Audit (human SUP)
- **Status:** INCOMPLETE
- **Reasoning:** Mass-assignment id probe valid but mis-tagged SEC-06 (role-only per README).

## Status / Related bugs
Not Run / None

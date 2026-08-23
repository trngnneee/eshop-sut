# TC-PROFILE-SEC-SUP-001: Race — concurrent PUT with role=admin vs valid profile

## Requirement ID
FR-04 / SEC-06

## Module / Test type / Technique
profile / Security / Human extension (SEC-SUP)

## Security requirement(s)
SEC-06

## Threat / probe
Race — concurrent PUT with role=admin vs valid profile

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- GET /api/users/me snapshot role=user.

## Test data
```json
{
  "sequence": [
    "PUT {\"name\":\"Valid Name\",\"phone\":\"0912345678\",\"shipping_address\":\"123 Le Loi\",\"role\":\"admin\"}",
    "PUT {\"name\":\"Race Name B\",\"phone\":\"0912345678\",\"shipping_address\":\"123 Le Loi\"} — fire immediately parallel",
    "GET /api/users/me"
  ]
}
```

## Test steps
1. PUT {"name":"Valid Name","phone":"0912345678","shipping_address":"123 Le Loi","role":"admin"}
2. PUT {"name":"Race Name B","phone":"0912345678","shipping_address":"123 Le Loi"} — fire immediately parallel
3. GET /api/users/me

## Expected result
SEC-06: role must remain user regardless of ordering. GET shows one coherent profile; role must not become admin. Record which PUT wins for name. HTTP status is not specified — record actual without inventing codes.

## Type
Unspecified (concurrency)

## Why the AI missed this
Prompt quality — security generator emitted one-shot SEC-06 probes (TC-PROFILE-SEC-007); checklist section 2 concurrency/race was never requested, so parallel privilege-escalation PUTs were absent.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** SEC-06 race on role field; concurrency observe.

## Status / Related bugs
Not Run / None

# TC-CART-SCH-SUP-002: POST line with extra user_id key — stored schema pollution

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Extra client keys persisted

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body": {
    "id": 1,
    "name": "Phone",
    "price": 100000,
    "quantity": 1,
    "user_id": 999,
    "role": "admin"
  }
}
```

## Test steps
1. POST with extra keys.
2. GET /api/cart — inspect line object keys.

## Expected result
Record whether GET line includes user_id/role keys. Canonical four fields should have correct types if present.

## Why the AI missed this
API characteristic — SUT pushes req.body verbatim; AI schema cases asserted four canonical keys but not extra properties persistence.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** additionalProperties on cart line from verbatim body store.

## Status / Related bugs
Not Run / None

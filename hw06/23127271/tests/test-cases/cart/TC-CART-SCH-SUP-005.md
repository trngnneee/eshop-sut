# TC-CART-SCH-SUP-005: Duplicate quantity keys — last-wins schema parse

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Duplicate JSON keys in POST

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.

## Test data
```json
{
  "body_raw": "{\"id\":1,\"name\":\"Dup\",\"price\":100000,\"quantity\":1,\"quantity\":5}"
}
```

## Test steps
1. POST raw JSON with duplicate quantity key.
2. GET /api/cart.

## Expected result
GET line quantity reflects parser last-wins or first-wins — record. id/name/price types unchanged.

## Why the AI missed this
Model limitation — domain SUP-003 covered duplicate keys for profile phone; cart POST duplicate quantity not mirrored in schema category.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Duplicate quantity key parser behavior.

## Status / Related bugs
Not Run / None

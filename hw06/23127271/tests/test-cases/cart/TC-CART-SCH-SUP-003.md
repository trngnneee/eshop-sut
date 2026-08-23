# TC-CART-SCH-SUP-003: Multi-line cart — each element same key set

## Requirement ID
FR-07

## Module / Test type / Technique
cart / Schema validation / Human extension (SCH-SUP)

## Schema aspect
Homogeneous line schema

## Preconditions
- EShop at http://localhost:3000.
- POST /api/login email=test@eshop.com password=Test1234!.
- POST full line id=1; POST minimal {id:2, quantity:1}.

## Test data
```json
{
  "sequence": [
    "POST full line",
    "POST minimal id=2",
    "GET /api/cart"
  ]
}
```

## Test steps
1. POST two different body shapes.
2. GET — diff keys per array element.

## Expected result
Array length 2 (or 1 if merge — record). Compare key sets of line[0] vs line[1]; document inconsistency if one lacks name/price.

## Why the AI missed this
Model limitation — AI validated types per line in isolation (SCH-004..006); heterogeneous keys across lines after different POST shapes not compared.

## Audit (human SUP)
- **Status:** VALID
- **Reasoning:** Heterogeneous line key sets across cart array.

## Status / Related bugs
Not Run / None

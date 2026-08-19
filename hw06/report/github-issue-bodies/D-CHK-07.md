## Defect

**Bug ID:** `D-CHK-07`  
**Found by Test Case:** `TC-API-CHECKOUT-031`  
**Module:** `orders`  
**Severity:** `critical`  
**Priority:** `P0`

## Expected result

Unauthenticated or unauthorized callers must receive HTTP 401/403 and must not read another user's order.

## Actual result

Full strict Newman IDOR probe observed an accessible order detail response without the required authorization boundary.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-full-suite.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-CHECKOUT-031`.

## Defect

**Bug ID:** `D-CHK-01`  
**Found by Test Case:** `TC-API-CHECKOUT-037`  
**Module:** `checkout`  
**Severity:** `critical`  
**Priority:** `P0`

## Expected result

The server must calculate the order total from the authenticated user's cart.

## Actual result

The client-total probe accepts a forged total and creates the order instead of recalculating from cart state.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-full-suite.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-CHECKOUT-037`.

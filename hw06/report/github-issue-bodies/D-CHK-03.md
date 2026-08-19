## Defect

**Bug ID:** `D-CHK-03`  
**Found by Test Case:** `TC-API-CHECKOUT-020`  
**Module:** `checkout`  
**Severity:** `major`  
**Priority:** `P1`

## Expected result

The cart should be empty after the order is created.

## Actual result

Full strict post-condition assertion failed because the cart still contained its item.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-full-suite.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-CHECKOUT-020`.

## Defect

**Bug ID:** `D-ADM-02`  
**Found by Test Case:** `TC-API-ORDER-STATUS-024`  
**Module:** `orders`  
**Severity:** `critical`  
**Priority:** `P0`

## Expected result

Canceled is terminal; canceled → delivered must return HTTP 400 and leave state unchanged.

## Actual result

Full strict and 25-row transition DDT both observed HTTP 200 for the forbidden transition.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-full-suite.json; hw06/newman/reports/03-ddt-order-status.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-ORDER-STATUS-024`.

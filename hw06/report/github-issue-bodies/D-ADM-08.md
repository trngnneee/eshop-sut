## Defect

**Bug ID:** `D-ADM-08`  
**Found by Test Case:** `TC-API-ORDER-STATUS-043`  
**Module:** `orders`  
**Severity:** `major`  
**Priority:** `P1`

## Expected result

A user may cancel only pending or confirmed orders; shipping should return HTTP 400.

## Actual result

The SUT catalog records that the user cancel endpoint accepts shipping; an isolated stateful probe is required.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`docs/hw06/02-sut-defect-catalog.md`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-ORDER-STATUS-043`.

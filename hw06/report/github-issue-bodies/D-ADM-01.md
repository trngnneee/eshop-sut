## Defect

**Bug ID:** `D-ADM-01`  
**Found by Test Case:** `TC-API-ORDER-STATUS-033`  
**Module:** `orders`  
**Severity:** `critical`  
**Priority:** `P0`

## Expected result

A non-admin token must receive HTTP 403.

## Actual result

Full strict Newman role-escalation assertion failed because the user token received HTTP 200.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-full-suite.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-ORDER-STATUS-033`.

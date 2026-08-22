## Defect

**Bug ID:** `D-ADM-06`  
**Found by Test Case:** `TC-API-ORDER-STATUS-044`  
**Module:** `orders`  
**Severity:** `minor`  
**Priority:** `P3`

## Expected result

An out-of-enum status value should be rejected as invalid input, distinct from a valid value used in a forbidden transition.

## Actual result

The transition DDT suite observed a state-transition error message for an out-of-enum value. The whitelist blocks it only as a side effect, so type errors and transition errors are indistinguishable to a caller.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/03-ddt-order-status.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-ORDER-STATUS-044`.

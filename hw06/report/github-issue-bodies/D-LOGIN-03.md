## Defect

**Bug ID:** `D-LOGIN-03`  
**Found by Test Case:** `TC-API-LOGIN-028`  
**Module:** `api`  
**Severity:** `critical`  
**Priority:** `P0`

## Expected result

Successful login response must not contain a password field or plaintext credential.

## Actual result

Full strict Newman assertion failed because the response contained the password field.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-full-suite.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-LOGIN-028`.

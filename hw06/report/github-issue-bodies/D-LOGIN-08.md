## Defect

**Bug ID:** `D-LOGIN-08`  
**Found by Test Case:** `TC-API-LOGIN-004`  
**Module:** `api`  
**Severity:** `minor`  
**Priority:** `P3`

## Expected result

A missing or wrong-typed email/password field should return HTTP 400 with a validation error, distinct from a credential rejection.

## Actual result

Strict Newman assertion failed: expected response to have status code 400 but got 401. Malformed bodies are treated as failed credentials instead of invalid input.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-full-suite.json; hw06/newman/reports/01-ddt-login.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-LOGIN-004`.

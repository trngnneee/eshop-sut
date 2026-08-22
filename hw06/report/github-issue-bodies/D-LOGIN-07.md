## Defect

**Bug ID:** `D-LOGIN-07`  
**Found by Test Case:** `TC-API-LOGIN-020`  
**Module:** `api`  
**Severity:** `minor`  
**Priority:** `P3`

## Expected result

A locked account should return the same generic message as any other failed login, so callers cannot distinguish which emails exist or are locked.

## Actual result

The data-driven login suite observed the lock-specific Vietnamese message instead of the generic failure text, and a different status code from the wrong-password path. This allows user enumeration.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/01-ddt-login.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-LOGIN-020`.

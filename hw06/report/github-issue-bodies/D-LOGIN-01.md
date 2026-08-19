## Defect

**Bug ID:** `D-LOGIN-01`  
**Found by Test Case:** `TC-API-LOGIN-018`  
**Module:** `api`  
**Severity:** `critical`  
**Priority:** `P0`

## Expected result

After two consecutive wrong-password attempts, a valid credential should still be accepted; the account should lock only at the documented threshold.

## Actual result

The canary/full Newman run observed HTTP 403 for the valid credential after two injected failures. This is the lockout-threshold defect.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/00-canary-suite.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-LOGIN-018`.

## Defect

**Bug ID:** `D-LOGIN-06`  
**Found by Test Case:** `TC-API-LOGIN-024`  
**Module:** `api`  
**Severity:** `major`  
**Priority:** `P1`

## Expected result

After lock expiry, a successful login should reset the consecutive-failure state.

## Actual result

The SUT catalog records that the counter remains after expiry; a timed stateful probe is required.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`docs/hw06/02-sut-defect-catalog.md`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-LOGIN-024`.

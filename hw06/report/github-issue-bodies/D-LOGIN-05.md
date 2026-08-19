## Defect

**Bug ID:** `D-LOGIN-05`  
**Found by Test Case:** `TC-API-LOGIN-030`  
**Module:** `api`  
**Severity:** `major`  
**Priority:** `P1`

## Expected result

Issued JWTs should use managed signing configuration and an expiration claim.

## Actual result

The SUT catalog identifies a hard-coded secret and missing expiry. Decode/signing follow-up is required for a complete runtime proof.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`docs/hw06/02-sut-defect-catalog.md`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-LOGIN-030`.

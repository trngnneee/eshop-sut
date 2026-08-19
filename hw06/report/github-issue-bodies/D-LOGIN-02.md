## Defect

**Bug ID:** `D-LOGIN-02`  
**Found by Test Case:** `TC-API-LOGIN-022`  
**Module:** `api`  
**Severity:** `major`  
**Priority:** `P1`

## Expected result

The lockout window should expire after the 30-second requirement.

## Actual result

The SUT defect catalog records a 180-second lock window. A timed probe is required to measure expiry without waiting in the smoke suite.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`docs/hw06/02-sut-defect-catalog.md`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-LOGIN-022`.

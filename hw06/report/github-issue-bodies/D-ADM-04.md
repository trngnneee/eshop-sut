## Defect

**Bug ID:** `D-ADM-04`  
**Found by Test Case:** `TC-API-ORDER-STATUS-041`  
**Module:** `orders`  
**Severity:** `major`  
**Priority:** `P2`

## Expected result

A failed UPDATE must return a controlled error, not a success message.

## Actual result

The callback ignores its database error argument; a nonexistent-order probe is required to demonstrate the false 200.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`docs/hw06/02-sut-defect-catalog.md`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-ORDER-STATUS-041`.

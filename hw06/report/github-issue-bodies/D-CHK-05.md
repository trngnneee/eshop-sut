## Defect

**Bug ID:** `D-CHK-05`  
**Found by Test Case:** `TC-API-CHECKOUT-042`  
**Module:** `checkout`  
**Severity:** `major`  
**Priority:** `P1`

## Expected result

A script-bearing shipping address must be rejected or neutralised before persistence, because the admin order screen renders this value.

## Actual result

The checkout DDT suite read the order back and found the payload persisted byte-for-byte, so the stored value reaches the admin view unchanged.

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`hw06/newman/reports/02-ddt-checkout.json`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `TC-API-CHECKOUT-042`.

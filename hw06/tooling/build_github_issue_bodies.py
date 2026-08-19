"""Create scrubbed GitHub issue bodies for the HW06 defect catalog.

The body files intentionally contain no credentials, JWTs, or raw Newman
request dumps. Local report paths identify the reproducible evidence.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "report" / "github-issue-bodies"

BUGS = [
    ("D-LOGIN-01", "Login failure counter increments twice and locks early", "critical", "P0", "api", "TC-API-LOGIN-018", "After two consecutive wrong-password attempts, a valid credential should still be accepted; the account should lock only at the documented threshold.", "The canary/full Newman run observed HTTP 403 for the valid credential after two injected failures. This is the lockout-threshold defect.", "hw06/newman/reports/00-canary-suite.json"),
    ("D-LOGIN-02", "Login lock duration is 180 seconds instead of 30 seconds", "major", "P1", "api", "TC-API-LOGIN-022", "The lockout window should expire after the 30-second requirement.", "The SUT defect catalog records a 180-second lock window. A timed probe is required to measure expiry without waiting in the smoke suite.", "docs/hw06/02-sut-defect-catalog.md"),
    ("D-LOGIN-03", "Login response exposes the plaintext password", "critical", "P0", "api", "TC-API-LOGIN-028", "Successful login response must not contain a password field or plaintext credential.", "Full strict Newman assertion failed because the response contained the password field.", "hw06/newman/reports/00-full-suite.json"),
    ("D-LOGIN-05", "JWT is hard-coded and has no expiration claim", "major", "P1", "api", "TC-API-LOGIN-030", "Issued JWTs should use managed signing configuration and an expiration claim.", "The SUT catalog identifies a hard-coded secret and missing expiry. Decode/signing follow-up is required for a complete runtime proof.", "docs/hw06/02-sut-defect-catalog.md"),
    ("D-LOGIN-06", "Login failure counter is not reset after lock expiry", "major", "P1", "api", "TC-API-LOGIN-024", "After lock expiry, a successful login should reset the consecutive-failure state.", "The SUT catalog records that the counter remains after expiry; a timed stateful probe is required.", "docs/hw06/02-sut-defect-catalog.md"),
    ("D-CHK-01", "Checkout trusts client-supplied total_amount", "critical", "P0", "checkout", "TC-API-CHECKOUT-037", "The server must calculate the order total from the authenticated user's cart.", "The client-total probe accepts a forged total and creates the order instead of recalculating from cart state.", "hw06/newman/reports/00-full-suite.json"),
    ("D-CHK-02", "Checkout accepts zero or negative total_amount", "major", "P1", "checkout", "TC-API-CHECKOUT-005", "Non-positive totals must be rejected with a controlled validation response.", "Full strict Newman assertion failed: zero total returned HTTP 200.", "hw06/newman/reports/00-full-suite.json"),
    ("D-CHK-03", "Cart is not cleared after successful checkout", "major", "P1", "checkout", "TC-API-CHECKOUT-020", "The cart should be empty after the order is created.", "Full strict post-condition assertion failed because the cart still contained its item.", "hw06/newman/reports/00-full-suite.json"),
    ("D-CHK-04", "Checkout succeeds with an empty cart", "major", "P2", "checkout", "TC-API-CHECKOUT-022", "An empty cart should not create a payable order.", "The SUT catalog records successful checkout with no cart items; an isolated empty-cart probe is required.", "docs/hw06/02-sut-defect-catalog.md"),
    ("D-CHK-07", "Order detail endpoint is vulnerable to IDOR", "critical", "P0", "orders", "TC-API-CHECKOUT-031", "Unauthenticated or unauthorized callers must receive HTTP 401/403 and must not read another user's order.", "Full strict Newman IDOR probe observed an accessible order detail response without the required authorization boundary.", "hw06/newman/reports/00-full-suite.json"),
    ("D-ADM-01", "Regular user can update order status through admin endpoint", "critical", "P0", "orders", "TC-API-ORDER-STATUS-033", "A non-admin token must receive HTTP 403.", "Full strict Newman role-escalation assertion failed because the user token received HTTP 200.", "hw06/newman/reports/00-full-suite.json"),
    ("D-ADM-02", "Canceled order can transition to delivered", "critical", "P0", "orders", "TC-API-ORDER-STATUS-024", "Canceled is terminal; canceled → delivered must return HTTP 400 and leave state unchanged.", "Full strict and 25-row transition DDT both observed HTTP 200 for the forbidden transition.", "hw06/newman/reports/00-full-suite.json; hw06/newman/reports/03-ddt-order-status.json"),
    ("D-ADM-03", "Admin cannot cancel an order in shipping", "major", "P2", "orders", "TC-API-ORDER-STATUS-015", "The documented transition matrix allows an admin to cancel a shipping order.", "The SUT catalog records HTTP 400 for shipping → canceled; an isolated stateful probe is required.", "docs/hw06/02-sut-defect-catalog.md"),
    ("D-ADM-04", "Admin status endpoint ignores database update errors", "major", "P2", "orders", "TC-API-ORDER-STATUS-041", "A failed UPDATE must return a controlled error, not a success message.", "The callback ignores its database error argument; a nonexistent-order probe is required to demonstrate the false 200.", "docs/hw06/02-sut-defect-catalog.md"),
    ("D-ADM-08", "User can cancel an order while it is shipping", "major", "P1", "orders", "TC-API-ORDER-STATUS-043", "A user may cancel only pending or confirmed orders; shipping should return HTTP 400.", "The SUT catalog records that the user cancel endpoint accepts shipping; an isolated stateful probe is required.", "docs/hw06/02-sut-defect-catalog.md"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for bug, title, severity, priority, module, tc, expected, actual, evidence in BUGS:
        body = f"""## Defect

**Bug ID:** `{bug}`  
**Found by Test Case:** `{tc}`  
**Module:** `{module}`  
**Severity:** `{severity}`  
**Priority:** `{priority}`

## Expected result

{expected}

## Actual result

{actual}

## Reproduction / evidence

Run the HW06 Newman collection against a reset EShop backend. The scrubbed local evidence reference is:

`{evidence}`

The request body in this issue intentionally omits credentials, JWTs, and other sensitive values. The exact case data is maintained in the local HW06 test-case table and Newman JSON report.

## Suggested fix

Validate the input/state transition at the API boundary, enforce the documented authorization/ownership rule, and add a regression assertion for `{tc}`.
"""
        (OUT / f"{bug}.md").write_text(body, encoding="utf-8")
    print(f"Wrote {len(BUGS)} scrubbed issue bodies to {OUT}")


if __name__ == "__main__":
    main()

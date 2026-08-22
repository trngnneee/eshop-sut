# Stage C — Security Checklist (SEC-01–SEC-07)

The assignment's spec defines security requirements SEC-01 through SEC-07
(consult the actual `api_specification.md` for the exact wording — the
numbering below is a common ordering; re-map if the real spec differs).
For each endpoint, walk every item and decide APPLIES / DOESN'T APPLY
before writing cases — record the "doesn't apply" verdicts too, they're
useful evidence for the audit and AI-critique write-up.

| Ref | Area | What to test |
|---|---|---|
| SEC-01 | **Injection** (SQL/NoSQL) | Submit parameter values containing typical injection metacharacters (quotes, comment sequences, boolean-tautology patterns) in every string input that reaches a query — search fields, login fields, filters. Expect the request to be rejected or safely escaped (never a 500 that leaks a query/stack trace, never an auth bypass). |
| SEC-02 | **Broken authentication** | Missing token, expired/malformed token, token for a different (revoked) session, wrong token type (e.g. refresh token used as access token). Expect consistent 401s with no distinguishing info between "wrong password" and "unknown user" on login endpoints (user-enumeration check). |
| SEC-03 | **IDOR / broken object-level authorization** | Authenticate as user A, request/modify a resource (order, cart, profile) owned by user B by guessing/incrementing its id. Expect 403/404, never the other user's data. |
| SEC-04 | **Broken function-level authorization / role escalation** | Authenticate as a regular user, call an admin-only endpoint directly. Also test a lower-privilege admin role (if the SUT has tiers) calling a higher-privilege action. Expect 403. |
| SEC-05 | **Mass assignment / over-posting** | Send extra fields in the body that shouldn't be client-settable (e.g. `role`, `isAdmin`, `price` on a customer-facing endpoint, `status` on a create-order call). Expect the server to ignore/reject them, not silently apply them. |
| SEC-06 | **Rate limiting / account lockout** | Repeated failed logins should trigger lockout per FR-02; repeated requests to sensitive endpoints should be throttled. Verify the lockout threshold and that it clears/expires as specified, and that lockout doesn't itself leak whether the account exists. |
| SEC-07 | **Sensitive data exposure / schema leakage** | Check that responses never include fields they shouldn't (password hashes, internal ids not meant for clients, other users' PII in list endpoints, verbose stack traces in error bodies). Cross-check against Stage D's schema so nothing extra sneaks through. |

## Writing the case

- `sec_ref` = the matching `SEC-0x`.
- `expected.status` = the safe outcome (usually 400/401/403/404, never 200
  with leaked/altered data, never a 500 with a stack trace).
- Note in `title` what invariant is being protected, not just the attack
  name — e.g. "Order detail request for another user's order id returns
  403, not the order" rather than just "IDOR test".
- Keep payload values illustrative and minimal — the goal is to prove the
  server-side control exists, not to build a working exploit chain.

## Cross-referencing

Some security cases are naturally also state-transition or domain-partition
cases (e.g. role escalation on a state-changing endpoint). Tag them under
whichever stage best captures the *primary* thing being verified and note
the overlap in the title so the audit reviewer isn't confused by an
apparent duplicate.

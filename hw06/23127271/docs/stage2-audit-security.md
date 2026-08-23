# Stage 2 — Human audit of AI security cases

**Rule used:** written SRS + `api_specification.md` + README SEC-01..SEC-07. Same standard as `docs/stage2-audit.md`. Human SEC-SUP cases are excluded (Source=Human).

| Label | Count |
|-------|------:|
| VALID | 31 |
| INVALID | 1 |
| INCOMPLETE | 5 |
| **Total (AI SEC)** | **37** |

## Labels

| Label | Meaning in this audit |
|-------|------------------------|
| VALID | Threat probe and oracle follow a written SEC/FR rule without inventing HTTP codes. |
| INVALID | Oracle asserted a mandatory reject/rule the spec does not state (e.g. cart price validation via FR-07/SEC-06). |
| INCOMPLETE | Probe is worth running but SEC tag or oracle over-claimed (wrong SEC mapping, undocumented side effect, implementation assumption). |

## Notable corrections

- **`TC-CART-SEC-006` (INVALID):** Dropped FR-07/SEC-06 mandatory price rejection; FR-08 checkout recalculation does not govern POST /api/cart storage.
- **`TC-PROFILE-SEC-008` / `TC-CART-SEC-008`:** Retagged mass-assignment oracles — SEC-06 is profile `role` only per README.
- **`TC-ADMINUSERS-SEC-003`:** Reframed as FR-19 self-delete, not SEC-03 role check.
- **`TC-PROFILE-SEC-012`:** Removed invented account-lockout bypass expectation.
- **`TC-CART-SEC-010`:** Removed SQLite backend assumption from oracle.

## Per-case table

| TC ID | Audit | Corrected type | Reasoning |
|-------|-------|----------------|-----------|
| TC-ADMINUSERS-SEC-001 | VALID | Security probe | SEC-02 unauthenticated DELETE. Target user must remain (D still in list). |
| TC-ADMINUSERS-SEC-002 | VALID | Security probe | SEC-03 / FR-12: admin DELETE requires role=admin, not merely a valid JWT. |
| TC-ADMINUSERS-SEC-003 | INCOMPLETE | FR-19 constraint | Self-delete rule is FR-19, not SEC-03 (caller already has admin role). Mis-tagged SEC requirement. |
| TC-ADMINUSERS-SEC-004 | VALID | Security probe | SEC-05 path SQLi OR tautology. Preventing mass delete via injection is a valid SEC-05 oracle. |
| TC-ADMINUSERS-SEC-005 | VALID | Security probe | SEC-05 stacked DELETE in path id. Oracle observes parameterized parsing. |
| TC-ADMINUSERS-SEC-006 | VALID | Security probe | SEC-01 / FR-19: admin list must not expose passwords. GET /api/admin/users is in FR-19 scope. |
| TC-ADMINUSERS-SEC-007 | VALID | Security probe | SEC-01 on DELETE error response for missing user. Missing-user behaviour is unspecified but password leak check is valid. |
| TC-ADMINUSERS-SEC-008 | VALID | Security probe | DELETE body is undocumented; probing unexpected JSON is a valid SEC-05 observe test. Path id authoritative oracle is reasonable. |
| TC-ADMINUSERS-SEC-010 | VALID | Security probe | SEC-02 empty Bearer token on DELETE. |
| TC-ADMINUSERS-SEC-011 | VALID | Security probe | SEC-05 percent-encoded SQLi in path id. |
| TC-ADMINUSERS-SEC-013 | VALID | Security probe | SEC-01 on successful DELETE response body. |
| TC-ADMINUSERS-SEC-014 | VALID | Security probe | SEC-05 SQLi Bearer + SEC-02 on admin DELETE. |
| TC-CART-SEC-001 | VALID | Security probe | SEC-02: cart APIs require JWT (api_spec section 4). Expect no line added when unauthenticated. |
| TC-CART-SEC-002 | VALID | Security probe | SEC-02 malformed JWT on POST /api/cart. Oracle is spec-aligned. |
| TC-CART-SEC-003 | VALID | Security probe | SEC-05 SQLi in cart line name. Oracle scoped to cart POST/GET side effects. |
| TC-CART-SEC-004 | VALID | Security probe | SEC-05 string id coercion probe. Observing parse/coerce behaviour without mandating reject is correct. |
| TC-CART-SEC-005 | VALID | Security probe | SEC-04 XSS in cart name. API literal-storage oracle matches SEC-04 scope. |
| TC-CART-SEC-006 | INVALID | Integrity observe (unspecified at cart POST) | Oracle claimed FR-07/SEC-06 requires cart POST to reject client price tampering. FR-08 mandates server-side checkout total; FR-07/example body does not forbid storing client price on add. SEC-06 is role-only on profile. |
| TC-CART-SEC-007 | VALID | Security probe / IDOR | Cross-user cart isolation is implied by per-user JWT-scoped cart. IDOR read probe is valid SEC-02 test. |
| TC-CART-SEC-008 | INCOMPLETE | Security probe / integrity | user_id mass assignment is a valid integrity probe, but SEC-06 applies only to profile role field per README. |
| TC-CART-SEC-010 | INCOMPLETE | Security probe | NoSQL-style string probe is valid SEC-05 observe, but oracle assumed SQLite backend which is not in the spec. |
| TC-CART-SEC-011 | VALID | Security probe / IDOR | IDOR-style POST with foreign user_id in body. Oracle correctly records cross-user cart binding. |
| TC-CART-SEC-012 | VALID | Security probe | SEC-05 SQLi + SEC-02 invalid Bearer on POST /api/cart. Combined probe is valid. |
| TC-PROFILE-SEC-001 | VALID | Security probe | SEC-05 SQLi in documented name field. Oracle observes injection side effects without inventing HTTP codes. |
| TC-PROFILE-SEC-002 | VALID | Security probe | SEC-05 UNION probe on name. Oracle is observe-only for SQL leaks. |
| TC-PROFILE-SEC-003 | VALID | Security probe | SEC-05 stacked DROP probe on shipping_address. Oracle correctly scoped to profile integrity. |
| TC-PROFILE-SEC-004 | VALID | Security probe | SEC-05 SQLi on phone field. Observing stored phone vs FR-04 format is a reasonable side-effect check. |
| TC-PROFILE-SEC-005 | VALID | Security probe | SEC-04 stored XSS probe on name. API-layer literal storage oracle matches SEC-04 testing scope. |
| TC-PROFILE-SEC-006 | VALID | Security probe | SEC-04 XSS event handler in shipping_address. Oracle is spec-aligned for API storage observe. |
| TC-PROFILE-SEC-007 | VALID | Security probe | SEC-06 explicitly forbids client role change; FR-04 repeats the same rule. |
| TC-PROFILE-SEC-008 | INCOMPLETE | Security probe / mass assignment | Probe is valid mass-assignment, but tagged SEC-06 (role-only per README). Password rule comes from FR-04 field list + SEC-01, not SEC-06. |
| TC-PROFILE-SEC-009 | VALID | Security probe | SEC-02: API spec section 2 requires JWT on PUT /api/users/me. Snapshot unchanged is the correct oracle. |
| TC-PROFILE-SEC-010 | VALID | Security probe | SEC-02 tampered JWT probe. Oracle requires no profile change without inventing status codes. |
| TC-PROFILE-SEC-011 | VALID | Security probe | FR-04: email must not change. Oracle allows reject-or-ignore and requires email unchanged. |
| TC-PROFILE-SEC-012 | INCOMPLETE | Security probe / mass assignment | Undocumented fields are worth probing, but 'account-lockout bypass' is not a written SRS/SEC rule. |
| TC-PROFILE-SEC-013 | VALID | Security probe | Combined SEC-05 (Auth header SQLi) and SEC-02 (invalid token) probe. Both requirements are written. |
| TC-PROFILE-SEC-014 | VALID | Security probe | SEC-04 polyglot/template literal probe. Oracle observes no server-side evaluation in JSON API. |

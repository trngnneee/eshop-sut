# Stage 2 — Human audit of AI state-transition cases

**Rule used:** only written SRS + `api_specification.md` text. Same standard as `docs/stage2-audit.md` for domain partitions.

| Label | Count |
|-------|------:|
| VALID | 33 |
| INVALID | 0 |
| INCOMPLETE | 9 |
| **Total** | **42** |

## Labels

| Label | Meaning in this audit |
|-------|------------------------|
| VALID | State transition and oracle follow a written rule. |
| INVALID | Oracle invented a reject/required/status rule the spec does not state. |
| INCOMPLETE | Transition is worth testing but expected result over-claimed (HTTP code, rollback, FR-10 side effect, etc.). |

## Notable corrections

- **`TC-CART-ST-013`:** Mislabelled illegal qty decrease — corrected to monotonic add/merge observe (no decrease API in spec).
- **`TC-CART-ST-011`:** Dropped mandatory order-status assertion; kept FR-08 cart-empty oracle only.
- **`TC-ADMINUSERS-ST-003` / ST-015:** Removed preferred 404/404 expectations for unspecified missing/repeat-delete behaviour.
- **`TC-PROFILE-ST-010`:** Removed assumed rollback of P1 on rejected invalid phone.

## Per-case table

| TC ID | Audit | Corrected type | Reasoning |
|-------|-------|----------------|-----------|
| TC-ADMINUSERS-ST-001 | VALID | Legal | FR-19 legal EXISTS to DELETED for a non-self user. |
| TC-ADMINUSERS-ST-002 | INCOMPLETE | Illegal | FR-19 self-delete prohibition is real. Generated title/oracle already avoids mandating HTTP 403 — audit confirms INCOMPLETE only because status is unspecified. |
| TC-ADMINUSERS-ST-003 | INCOMPLETE | Illegal repeat / Unspecified | Repeat DELETE on a gone user is a valid terminal-state probe. Preferring 404/4xx over silent 200 is not in the spec. |
| TC-ADMINUSERS-ST-004 | VALID | Legal | List cardinality N to N-1 follows from a successful FR-19 delete of one other user. |
| TC-ADMINUSERS-ST-005 | VALID | Legal | Sequential delete of two disposable users — both reach DELETED terminal state. |
| TC-ADMINUSERS-ST-006 | VALID | Illegal | FR-12 / SEC-03: non-admin must not use admin delete API. Oracle checks target still exists without inventing HTTP 403. |
| TC-ADMINUSERS-ST-007 | VALID | Illegal | SEC-02: protected admin API requires JWT. Oracle checks no delete occurred. |
| TC-ADMINUSERS-ST-008 | VALID | Legal | Register to EXISTS to DELETED lifecycle under FR-19. |
| TC-ADMINUSERS-ST-009 | VALID | Legal | Selective delete: other seed users remain while target id=3 is removed. |
| TC-ADMINUSERS-ST-010 | VALID | Illegal | Self-delete blocked (FR-19) with list stability — no collateral deletes. |
| TC-ADMINUSERS-ST-011 | INCOMPLETE | Legal consequence / Unspecified | Deleted account should not authenticate — reasonable consequence but FR-19 does not state login behaviour; HTTP 401/403 not specified. |
| TC-ADMINUSERS-ST-012 | VALID | Unspecified | Cascade delete with orders is correctly flagged unspecified; no invented requirement. |
| TC-ADMINUSERS-ST-013 | INCOMPLETE | Unspecified / guard | DELETE body is not documented. Path :id is the specified identifier (consistent with domain TC-ADMINUSERS-019). Body override rule is inferred, not written. |
| TC-ADMINUSERS-ST-014 | VALID | Legal | FR-19: delete user id=2 (not self). Admin id=1 must remain. |
| TC-ADMINUSERS-ST-015 | INCOMPLETE | Unspecified | Missing user id is not specified as invalid in FR-19. Expecting 404/4xx was invented (same as domain TC-ADMINUSERS-005 audit). |
| TC-CART-ST-001 | VALID | Legal | EMPTY to one line is the base cart state transition under authenticated POST /api/cart. |
| TC-CART-ST-002 | VALID | Legal | FR-07 merge when same product added again — core legal transition. |
| TC-CART-ST-003 | VALID | Legal | FR-07 merge applies to the same product; a different id is a separate line. |
| TC-CART-ST-004 | VALID | Legal | Merge on an existing line while another line stays unchanged — FR-07 in multi-line cart. |
| TC-CART-ST-005 | VALID | Legal | Adding a third distinct product extends MULTI state by one line. |
| TC-CART-ST-006 | VALID | Legal | Two POSTs of same id from empty must merge per FR-07, not create two rows. |
| TC-CART-ST-007 | VALID | Legal | Quantity accumulation via merge is FR-07. |
| TC-CART-ST-008 | VALID | Legal (idempotency) | Repeat POST with same id tests idempotent merge behaviour under FR-07. |
| TC-CART-ST-009 | VALID | Legal | Interleaved POST/GET checks observable cart consistency — no invented HTTP codes. |
| TC-CART-ST-010 | VALID | Legal (isolation) | Cart is scoped to the authenticated user (JWT). Another user's cart must not show the line. |
| TC-CART-ST-011 | INCOMPLETE | Legal (cross-endpoint FR-08) | FR-08 cart-clear after successful checkout is spec-backed. Generated oracle also asserted order status pending (FR-10) and assumed checkout success shape — not required for this cart transition test. |
| TC-CART-ST-012 | VALID | Legal | After cart is empty (post-checkout per FR-08), a new POST starts a fresh SINGLE line. |
| TC-CART-ST-013 | INCOMPLETE | Unspecified (monotonic add) | Mislabelled as illegal transition. Spec has no cart qty-decrease API; POST only adds/merges. Case is an observe-only monotonic-add probe, not a specified illegal transition. |
| TC-CART-ST-014 | VALID | Legal | Unequal merge operands 2+3 from empty — FR-07. |
| TC-CART-ST-015 | VALID | Legal / Unspecified | Session-boundary probe; oracle already flags persistence medium as unspecified. |
| TC-PROFILE-ST-001 | VALID | Legal | FR-04 allows a logged-in user to update name, phone, and shipping_address. Multi-step P0 to P1 is a valid state-transition probe. email/role immutability is spec-backed. |
| TC-PROFILE-ST-002 | VALID | Legal / Unspecified | Sequential partial PUTs test replace-vs-partial semantics which the spec leaves open. Oracle already records observe-only for omitted fields. |
| TC-PROFILE-ST-003 | VALID | Legal | Two full PUTs with documented three-field bodies test profile snapshot overwrite. FR-04 lists all three as updatable; expecting GET to reflect the latest submitted triple is spec-aligned. |
| TC-PROFILE-ST-004 | VALID | Legal (idempotency) | Idempotent repeat of the same valid PUT is a standard state-transition edge. Oracle checks stable reads only. |
| TC-PROFILE-ST-005 | INCOMPLETE | Legal / Unspecified | Persistence across re-login is a reasonable probe but the spec does not define storage medium (DB vs session). Generated oracle assumed DB persistence as mandatory. |
| TC-PROFILE-ST-006 | VALID | Legal constraint | FR-04: email must not be changed. Oracle allows reject-or-ignore and requires email unchanged. |
| TC-PROFILE-ST-007 | VALID | Legal constraint | FR-04 / SEC-06: clients must not change role via profile update. Oracle is spec-aligned. |
| TC-PROFILE-ST-008 | VALID | Legal | FR-04 applies to any logged-in user; admin is a logged-in user. role must remain admin. |
| TC-PROFILE-ST-009 | VALID | Legal / Unspecified | Three sequential single-field PUTs probe partial-update chaining; oracle correctly flags unspecified semantics. |
| TC-PROFILE-ST-010 | INCOMPLETE | Illegal input / Unspecified | phone=123 violates FR-04 format rule (real). Whether a rejected invalid PUT leaves P1 unchanged is not specified — generated oracle assumed rollback. |
| TC-PROFILE-ST-011 | VALID | Legal (isolation) | FR-04: user may update only their own profile. Cross-user isolation is spec-backed. |
| TC-PROFILE-ST-012 | VALID | Unspecified / no-op | Empty JSON body is not documented. Oracle observes state unchanged or rejection without inventing mandatory 400. |

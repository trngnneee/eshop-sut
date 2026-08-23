# Stage 3 — Human audit of human-found (SUP) cases

**Rule used:** same standard as `docs/stage2-audit.md` — written SRS + api_spec only; human gap-finding preserved.

| Label | Count |
|-------|------:|
| VALID | 49 |
| INVALID | 1 |
| INCOMPLETE | 10 |
| **Total human SUP** | **60** |

## By sheet

| Sheet | Human rows |
|-------|----------:|
| domain-partitions.csv | 15 |
| state-transitions.csv | 15 |
| security-tests.csv | 15 |
| schema-validation.csv | 15 |

## Notable corrections

- **`TC-CART-SEC-SUP-001` (INVALID):** Same invented cart price-validation rule as AI `TC-CART-SEC-006`; FR-08 is checkout-only.
- **`TC-ADMINUSERS-ST-SUP-003/004`:** Removed preferred 401/403 / mandatory auth-failure wording.
- **`TC-CART-ST-SUP-003/005`:** Marked cross-FR (checkout) probes; oracles observe-only.
- **`TC-PROFILE-SEC-SUP-002`:** Retagged mass-assignment off SEC-06 (role-only).
- **`TC-CART-SEC-SUP-002/005`:** Negative/extreme qty — observe only, no mandatory reject.
- **`TC-ADMINUSERS-SUP-003`:** Note seed DB restore after deleting id=2.
- **`TC-ADMINUSERS-SCH-SUP-004`:** Fixed register-then-list schema oracle (name not guaranteed).

## Per-case table

| TC ID | Audit | Reasoning (short) |
|-------|-------|-------------------|
| TC-ADMINUSERS-SCH-SUP-001 | VALID | Extra list columns from SUT SELECT — schema over-exposure observe. |
| TC-ADMINUSERS-SCH-SUP-002 | VALID | Homogeneous key set across list elements — reasonable schema consistency check. |
| TC-ADMINUSERS-SCH-SUP-003 | VALID | Non-numeric DELETE path error envelope type observe. |
| TC-ADMINUSERS-SCH-SUP-004 | INCOMPLETE | Aspect label said 'empty string email' but case registers new user — corrected oracle; name field no… |
| TC-ADMINUSERS-SCH-SUP-005 | VALID | DELETE body must not echo deleted user PII. |
| TC-ADMINUSERS-SEC-SUP-001 | VALID | SEC-02 unauthenticated GET list — FR-19/§6 paired endpoint. |
| TC-ADMINUSERS-SEC-SUP-002 | VALID | SEC-03 on GET list — spec §6.1 admin guard. |
| TC-ADMINUSERS-SEC-SUP-003 | VALID | Parallel DELETE idempotency race. |
| TC-ADMINUSERS-SEC-SUP-004 | VALID | Negative path id SEC-05 boundary observe. |
| TC-ADMINUSERS-SEC-SUP-005 | VALID | Encoded slash path manipulation probe. |
| TC-ADMINUSERS-ST-SUP-001 | VALID | Delete-other-admin unspecified in FR-19; observe-only oracle. |
| TC-ADMINUSERS-ST-SUP-002 | VALID | Parallel DELETE race; final state U_DELETED without inventing second response. |
| TC-ADMINUSERS-ST-SUP-003 | INCOMPLETE | Oracle said '401/403 expected' — HTTP codes not in spec; corrected to observe-only. |
| TC-ADMINUSERS-ST-SUP-004 | INCOMPLETE | Removed 'must not succeed' as mandatory status; session invalidation unspecified. |
| TC-ADMINUSERS-ST-SUP-005 | VALID | DELETE∥GET list race; intermediate state observe-only. |
| TC-ADMINUSERS-SUP-001 | VALID | Percent-encoded path observe partition; FR-19 delete-if-not-self. |
| TC-ADMINUSERS-SUP-002 | VALID | Trailing slash routing unspecified; observe-only. |
| TC-ADMINUSERS-SUP-003 | INCOMPLETE | Destructive seed-user delete is acceptable probe but oracle assumed id=2 always exists — preconditio… |
| TC-ADMINUSERS-SUP-004 | VALID | Mixed alphanumeric path partition; no invented 404. |
| TC-ADMINUSERS-SUP-005 | VALID | Double-encoding depth observe; FR-19 self-delete guard retained. |
| TC-CART-SCH-SUP-001 | VALID | Partial POST body stored shape observe. |
| TC-CART-SCH-SUP-002 | VALID | additionalProperties on cart line from verbatim body store. |
| TC-CART-SCH-SUP-003 | VALID | Heterogeneous line key sets across cart array. |
| TC-CART-SCH-SUP-004 | VALID | name:null nullable probe observe-only. |
| TC-CART-SCH-SUP-005 | VALID | Duplicate quantity key parser behavior. |
| TC-CART-SEC-SUP-001 | INVALID | Same flaw as audited TC-CART-SEC-006: invented mandatory catalogue price on POST /api/cart. |
| TC-CART-SEC-SUP-002 | INCOMPLETE | Negative qty not a specified invalid class for POST /api/cart (FR-06 is UI). |
| TC-CART-SEC-SUP-003 | VALID | Same-user GET∥POST race; IDOR clause correct. |
| TC-CART-SEC-SUP-004 | VALID | SEC-04 Unicode-escape XSS bypass probe. |
| TC-CART-SEC-SUP-005 | INCOMPLETE | Oracle required reject/clamp; extreme qty not specified in spec. |
| TC-CART-ST-SUP-001 | VALID | Merge on middle line of 3-line cart; FR-07 merge arithmetic. |
| TC-CART-ST-SUP-002 | VALID | Parallel POST race; merge violation if duplicate lines is FR-07-backed. |
| TC-CART-ST-SUP-003 | INCOMPLETE | Valid FR-08 negative cart transition but primary action is POST /api/checkout (cross-FR); relabelled… |
| TC-CART-ST-SUP-004 | VALID | Merge on line 3 completes matrix; FR-07 merge. |
| TC-CART-ST-SUP-005 | INCOMPLETE | Checkout∥POST is cross-FR concurrency; oracle corrected to observe-only without mandating empty cart… |
| TC-CART-SUP-001 | VALID | Merge identity key ambiguity is real FR-07 gap; observe-only oracle. |
| TC-CART-SUP-002 | VALID | Unequal merge operands 2+3; FR-07 merge rule stated without inventing HTTP. |
| TC-CART-SUP-003 | VALID | Price mismatch on merge; stored price unspecified — oracle records only. |
| TC-CART-SUP-004 | VALID | Minimal body positive case after Stage 2; no mandatory reject for omitted name/price. |
| TC-CART-SUP-005 | VALID | Multi-line cart merge; FR-07 qty arithmetic spec-backed. |
| TC-PROFILE-SCH-SUP-001 | VALID | Undocumented column exposure observe; schema inventory. |
| TC-PROFILE-SCH-SUP-002 | VALID | Nested envelope malformed request schema. |
| TC-PROFILE-SCH-SUP-003 | VALID | SEC-01 key inventory beyond password key name. |
| TC-PROFILE-SCH-SUP-004 | VALID | Array-root PUT malformed schema. |
| TC-PROFILE-SCH-SUP-005 | INCOMPLETE | Oracle assumed charset suffix always parses — corrected to observe-only. |
| TC-PROFILE-SEC-SUP-001 | VALID | SEC-06 race on role field; concurrency observe. |
| TC-PROFILE-SEC-SUP-002 | INCOMPLETE | Mass-assignment id probe valid but mis-tagged SEC-06 (role-only per README). |
| TC-PROFILE-SEC-SUP-003 | VALID | SEC-05 null-byte encoding probe; observe storage/leak. |
| TC-PROFILE-SEC-SUP-004 | VALID | SEC-02 Content-Type confusion with valid JWT. |
| TC-PROFILE-SEC-SUP-005 | VALID | Parallel XSS vs SQLi race; SEC-04/05 observe. |
| TC-PROFILE-ST-SUP-001 | VALID | Concurrency race on PUT; oracle allows either winner without inventing order. |
| TC-PROFILE-ST-SUP-002 | VALID | Mid-flow auth removal; SEC-02 + spec token requirement. |
| TC-PROFILE-ST-SUP-003 | VALID | Cross-field parallel PUT race; torn read documented as unspecified. |
| TC-PROFILE-ST-SUP-004 | VALID | Malformed JWT after P1; SEC-02 mid-flow guard. |
| TC-PROFILE-ST-SUP-005 | VALID | Address-first partial chain; partial semantics observe-only. |
| TC-PROFILE-SUP-001 | VALID | Positive phone-only partial after Stage 2 dropped mandatory triple-body; oracle observe-only for omi… |
| TC-PROFILE-SUP-002 | VALID | Fullwidth digits violate FR-04 ASCII phone rule; observe-only invalid partition. |
| TC-PROFILE-SUP-003 | VALID | Duplicate JSON key probe; oracle does not invent parser winner. |
| TC-PROFILE-SUP-004 | VALID | Name-only partial mirrors SUP-001 pattern; spec-aligned. |
| TC-PROFILE-SUP-005 | VALID | Two-of-three field subset; oracle correctly flags address unspecified. |

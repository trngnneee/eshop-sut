# Stage 2 — Human audit of AI schema-validation cases

**Rule used:** written SRS + `api_specification.md` + README FR-04/07/19 and SEC-01. Human SCH-SUP cases are excluded (Source=Human).

| Label | Count |
|-------|------:|
| VALID | 37 |
| INVALID | 0 |
| INCOMPLETE | 5 |
| **Total (AI SCH)** | **42** |

## Labels

| Label | Meaning in this audit |
|-------|------------------------|
| VALID | Schema probe and oracle follow documented shapes or observe-only rules without inventing HTTP codes. |
| INVALID | Oracle asserted a mandatory field/type/rule the spec does not state. |
| INCOMPLETE | Probe is worth running but over-claims presence or types on undocumented GET/list shapes. |

## Notable corrections

- **`TC-PROFILE-SCH-002`–`004`:** Reworded GET field oracles to *if returned* + record-if-absent; api_spec only documents PUT body, not GET response fields.
- **`TC-ADMINUSERS-SCH-003`–`004`:** Same observe-only hedge for list item id/name — admin list schema is not in api_spec.

## Per-case table

| TC ID | Audit | Type | Reasoning |
|-------|-------|------|-----------|
| TC-ADMINUSERS-SCH-001 | VALID | Schema validation | Admin user list is a collection; JSON array root + Content-Type is valid. |
| TC-ADMINUSERS-SCH-002 | VALID | Schema validation | Each list element must be a user object, not a scalar or nested array. |
| TC-ADMINUSERS-SCH-003 | INCOMPLETE | Schema validation | GET /api/admin/users item schema is not defined in api_spec; id:number is inferred from register response, not list contract. |
| TC-ADMINUSERS-SCH-004 | INCOMPLETE | Schema validation | name field on admin list items is not documented in api_spec or FR-19. |
| TC-ADMINUSERS-SCH-005 | VALID | Schema validation | FR-19 admin user list implies identifiable users; email as string is a reasonable schema contract. |
| TC-ADMINUSERS-SCH-006 | VALID | Schema validation | FR-12 defines user and admin roles; role as string on list items is spec-aligned. |
| TC-ADMINUSERS-SCH-007 | VALID | Schema validation | FR-19 / SEC-01: admin list must not expose password. |
| TC-ADMINUSERS-SCH-008 | VALID | Schema validation | SEC-01 extension: password_hash must not appear in list responses. |
| TC-ADMINUSERS-SCH-009 | VALID | Schema validation | DELETE success body is undocumented; observe-only JSON object type check is correct. |
| TC-ADMINUSERS-SCH-010 | VALID | Schema validation | message field on DELETE is optional and observe-only when present. |
| TC-ADMINUSERS-SCH-011 | VALID | Schema validation | Smoke schema check on seed data validates real list elements without inventing HTTP codes. |
| TC-ADMINUSERS-SCH-012 | VALID | Schema validation | Content-Type application/json is a standard schema contract check. |
| TC-ADMINUSERS-SCH-013 | VALID | Schema validation | Non-admin JWT must not receive full user array; error envelope is observe-only. |
| TC-ADMINUSERS-SCH-014 | VALID | Schema validation | Post-DELETE list must remain a valid user array with consistent element types. |
| TC-CART-SCH-001 | VALID | Schema validation | Cart is modeled as a list of line objects; JSON array root + Content-Type is a valid schema check. |
| TC-CART-SCH-002 | VALID | Schema validation | Empty cart as [] follows list semantics; null or {} would violate array contract. |
| TC-CART-SCH-003 | VALID | Schema validation | api_spec section 4.2 POST example types id as number. |
| TC-CART-SCH-004 | VALID | Schema validation | name is string in POST example and on stored cart lines. |
| TC-CART-SCH-005 | VALID | Schema validation | price is number in POST example; string price would be a schema deviation. |
| TC-CART-SCH-006 | VALID | Schema validation | quantity is number in POST example. |
| TC-CART-SCH-007 | VALID | Schema validation | POST success body is undocumented; observe-only JSON object check is correct. |
| TC-CART-SCH-008 | VALID | Schema validation | Four-field POST body matches api_spec section 4.2 example exactly. |
| TC-CART-SCH-009 | VALID | Schema validation | FR-07 merge implies one array element; checking length and numeric quantity type is schema-consistent. |
| TC-CART-SCH-010 | VALID | Schema validation | Spec types price as number; observe coercion without mandating reject. |
| TC-CART-SCH-011 | VALID | Schema validation | Content-Type application/json is a standard schema contract check. |
| TC-CART-SCH-012 | VALID | Schema validation | Malformed array root is a valid request-shape probe; observe response type without inventing status codes. |
| TC-CART-SCH-013 | VALID | Schema validation | Spec types quantity as number; observe coercion behaviour. |
| TC-CART-SCH-014 | VALID | Schema validation | Unauthenticated cart access must not return a cart array; error body shape is observe-only. |
| TC-PROFILE-SCH-001 | VALID | Schema validation | GET profile returns JSON object per REST convention; Content-Type check is standard schema probe. |
| TC-PROFILE-SCH-002 | INCOMPLETE | Schema validation | GET /api/users/me response fields are not listed in api_spec; oracle hedges with observe-if-absent but still opens with mandatory presence. |
| TC-PROFILE-SCH-003 | INCOMPLETE | Schema validation | Same as SCH-002: phone type is inferable from PUT example but GET shape is undocumented. |
| TC-PROFILE-SCH-004 | INCOMPLETE | Schema validation | shipping_address type is implied by PUT example; GET presence is not guaranteed by api_spec. |
| TC-PROFILE-SCH-005 | VALID | Schema validation | FR-04: email is readable on profile and must match the logged-in account. |
| TC-PROFILE-SCH-006 | VALID | Schema validation | FR-04 / SEC-06: role is readable and must remain user for the seed account. |
| TC-PROFILE-SCH-007 | VALID | Schema validation | SEC-01: password and password_hash must not appear in API responses. |
| TC-PROFILE-SCH-008 | VALID | Schema validation | api_spec section 2.2 documents PUT body with name, shipping_address, phone as strings. |
| TC-PROFILE-SCH-009 | VALID | Schema validation | PUT success response envelope is not defined in api_spec; observe-only JSON type check is correct. |
| TC-PROFILE-SCH-010 | VALID | Schema validation | Content-Type application/json is a standard schema contract check for JSON APIs. |
| TC-PROFILE-SCH-011 | VALID | Schema validation | Spec example types phone as string; observe coercion without mandating reject is spec-aligned. |
| TC-PROFILE-SCH-012 | VALID | Schema validation | Partial/empty PUT body semantics are unspecified; observe response and GET field values without inventing rules. |
| TC-PROFILE-SCH-013 | VALID | Schema validation | id type probe is observe-only when field is not documented on GET profile. |
| TC-PROFILE-SCH-014 | VALID | Schema validation | Auth error envelope is unspecified; checking JSON-not-HTML and recording keys is a valid schema probe. |

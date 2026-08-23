# Schema Validation Report — FR-04, FR-07, FR-19

**Student:** 23127271 · **SUT:** EShop (`http://localhost:3000`)  
**Category:** Stage 1 — Schema validation (API testing skill checklist section 4)  
**Sources:** `Repo/eshop-sut/api_specification.md`, `README.md` (FR-04/07/19, SEC-01)

---

## Schema contract sources

| Source | What it defines for schema tests |
|--------|----------------------------------|
| api_spec §2.2 | PUT `/api/users/me` request: name, shipping_address, phone (strings) |
| api_spec §4.2 | POST `/api/cart` request: id, name, price, quantity (number/string types per example) |
| api_spec §4.1 / §6.1 | GET cart array; GET admin users list (shapes partially implied) |
| FR-04 README | Profile fields; email/role readable and immutable |
| FR-19 README | Admin user list without password |
| SEC-01 | password/password_hash must not appear in responses |

**Documented gaps (observe-only oracles):** PUT profile success body, POST cart success body, DELETE user success body, and auth error envelopes are **not** defined in api_spec — TCs record actual JSON types/keys without inventing required status codes.

## In-scope endpoints

| FR | Endpoints | Schema focus |
|----|-----------|--------------|
| FR-04 | `GET/PUT /api/users/me` | Profile object fields/types; PUT request body; forbidden password |
| FR-07 | `GET/POST /api/cart` | Array of line objects; four-field line schema; Content-Type |
| FR-19 | `GET/DELETE /api/admin/users` | User list array schema; no password fields; DELETE response observe |

---

## FR-04 — `GET/PUT /api/users/me`

**Count:** 14 cases

| TC ID | Aspect | Title |
|-------|--------|-------|
| TC-PROFILE-SCH-001 | GET response root type | GET /api/users/me returns JSON object |
| TC-PROFILE-SCH-002 | Field name type | Profile name field is string |
| TC-PROFILE-SCH-003 | Field phone type | Profile phone field is string |
| TC-PROFILE-SCH-004 | Field shipping_address type | shipping_address field is string |
| TC-PROFILE-SCH-005 | Field email type | email field present as string |
| TC-PROFILE-SCH-006 | Field role type | role field is string |
| TC-PROFILE-SCH-007 | Forbidden field password | GET profile must not expose password |
| TC-PROFILE-SCH-008 | PUT request body schema | PUT accepts documented three-field JSON body |
| TC-PROFILE-SCH-009 | PUT success response envelope | PUT success response is JSON object |
| TC-PROFILE-SCH-010 | Content-Type header | GET profile Content-Type is JSON |
| TC-PROFILE-SCH-011 | Request field type coercion | phone sent as JSON number — observe type handling |
| TC-PROFILE-SCH-012 | Empty PUT body | PUT with empty JSON object — observe response schema |
| TC-PROFILE-SCH-013 | Numeric id field | id field type if present on GET profile |
| TC-PROFILE-SCH-014 | Unauthenticated error body | GET without JWT — error body is JSON not HTML |

---

## FR-07 — `GET/POST /api/cart`

**Count:** 14 cases

| TC ID | Aspect | Title |
|-------|--------|-------|
| TC-CART-SCH-001 | GET response root type | GET /api/cart returns JSON array |
| TC-CART-SCH-002 | Empty cart shape | Empty cart is empty array [] |
| TC-CART-SCH-003 | Line item id type | Cart line id is number |
| TC-CART-SCH-004 | Line item name type | Cart line name is string |
| TC-CART-SCH-005 | Line item price type | Cart line price is number |
| TC-CART-SCH-006 | Line item quantity type | Cart line quantity is number |
| TC-CART-SCH-007 | POST success response envelope | POST /api/cart success response is JSON object |
| TC-CART-SCH-008 | POST request four-field schema | POST body matches example four-field schema |
| TC-CART-SCH-009 | Array length after merge | Two POST same id — array length and qty schema |
| TC-CART-SCH-010 | Request price string type | price sent as string — observe stored type |
| TC-CART-SCH-011 | Content-Type header | GET cart Content-Type is JSON |
| TC-CART-SCH-012 | Malformed request root | POST body JSON array instead of object |
| TC-CART-SCH-013 | quantity string type | quantity sent as string — observe stored type |
| TC-CART-SCH-014 | Unauthenticated error body | GET cart without JWT — response body shape |

---

## FR-19 — `GET/DELETE /api/admin/users`

**Count:** 14 cases

| TC ID | Aspect | Title |
|-------|--------|-------|
| TC-ADMINUSERS-SCH-001 | GET list root type | GET /api/admin/users returns JSON array |
| TC-ADMINUSERS-SCH-002 | List element type | Each list element is JSON object |
| TC-ADMINUSERS-SCH-003 | Field id type | User list item id is number |
| TC-ADMINUSERS-SCH-004 | Field name type | User list item name is string |
| TC-ADMINUSERS-SCH-005 | Field email type | User list item email is string |
| TC-ADMINUSERS-SCH-006 | Field role type | User list item role is string |
| TC-ADMINUSERS-SCH-007 | Forbidden password field | List items must not contain password |
| TC-ADMINUSERS-SCH-008 | Forbidden password_hash field | List items must not contain password_hash |
| TC-ADMINUSERS-SCH-009 | DELETE success response type | DELETE success body is JSON object |
| TC-ADMINUSERS-SCH-010 | DELETE message field | DELETE response message field type if present |
| TC-ADMINUSERS-SCH-011 | Non-empty list schema | Seed users appear as valid objects in list |
| TC-ADMINUSERS-SCH-012 | Content-Type header | GET admin users Content-Type is JSON |
| TC-ADMINUSERS-SCH-013 | User JWT error body | GET list as user — error response JSON shape |
| TC-ADMINUSERS-SCH-014 | List schema after delete | After DELETE, list remains array of valid user objects |

---

## Combined Stage-1 counts (domain + state + security + schema)

- FR-04: 40 + 12 + 14 + 5 + 14 + 5 = **90**
- FR-07: 39 + 15 + 11 + 5 + 14 + 5 = **89**
- FR-19: 20 + 15 + 12 + 5 + 14 + 5 = **71**

## Artifacts

| Artifact | Path |
|----------|------|
| This report | `docs/schema-validation-report.md` |
| Per-TC files | `tests/test-cases/{{profile,cart,admin-users}}/TC-*-SCH-*.md` |
| Sheet | `sheets/schema-validation.csv` |
| Generator | `scripts/generate_schema_validation.py` |

**Total schema cases:** 42 AI-generated + 15 human SCH-SUP = **57** total.

## Stage 2 audit (AI cases)

**37 VALID / 0 INVALID / 5 INCOMPLETE.** Details and corrected oracles: `docs/stage2-audit-schema.md`. CSV `AuditStatus` / `AuditReasoning` are filled for all AI rows. INCOMPLETE cases were corrected to observe-only *if returned* wording for undocumented GET/list shapes.

See `docs/stage3-extend-schema.md` for human extensions (≥5 per FR).

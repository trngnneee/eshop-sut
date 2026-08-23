# Stage 2 — Human audit of AI domain-partition cases

**Rule used:** only written SRS + `api_specification.md` text. If a requirement is missing, the case is not a specified invalid class — it is not labelled VALID as a reject test.

| Label | Count |
|-------|------:|
| VALID | 16 |
| INVALID | 42 |
| INCOMPLETE | 41 |
| **Total** | **99** |

## Labels

| Label | Meaning in this audit |
|-------|------------------------|
| VALID | Partition and oracle both follow a written rule. |
| INVALID | Generated oracle invented a reject/required/status rule the spec does not state (e.g. P-NAME-05 omit name). Corrected: no specified expected rejection. |
| INCOMPLETE | The partition is real (or worth observing) but the generated expected result pinned an undocumented HTTP status, assumed accept, or mixed in a rule from another FR. Corrected expected result drops the invented part. |

## P-NAME-05 (called out)

`TC-PROFILE-010` was **INVALID**. FR-04 says the user *may update* name; the API example *includes* name. Neither says name is mandatory on every PUT. The AI treated omit-name as invalid by assumption. Corrected oracle: do not expect rejection; observe stored name; email/role still must not change.

## C-PRICE-04 (called out)

`TC-CART-025` was **INVALID**. `POST /api/cart` shows `price` in the example JSON. The spec does not say `price` is required, and FR-15 `price > 0` is product CRUD, not this endpoint. Omitting `price` is not a specified invalid class. Corrected oracle: do not expect rejection; record what the SUT stores, if anything.

## Per-case table

| TC ID | Audit | Corrected type | Reasoning |
|-------|-------|----------------|-----------|
| TC-ADMINUSERS-001 | VALID | Valid | FR-19: admin may delete users other than the currently logged-in account. FR-12: caller is admin with JWT. |
| TC-ADMINUSERS-002 | INCOMPLETE | Invalid | FR-19 forbids deleting the currently logged-in account. Generated HTTP 403/400 is not specified. |
| TC-ADMINUSERS-003 | INVALID | Unspecified | id=0 is not specified as invalid. Only self-delete is forbidden in FR-19. |
| TC-ADMINUSERS-004 | INVALID | Unspecified | Negative id is not specified as invalid. |
| TC-ADMINUSERS-005 | INVALID | Unspecified | Missing-user / HTTP 404 is not specified. |
| TC-ADMINUSERS-006 | INVALID | Unspecified | Non-numeric path id is not specified as invalid. |
| TC-ADMINUSERS-007 | INVALID | Unspecified | Non-integer path id is not specified. 'Must not coerce to 1' was invented. If the SUT resolves this path to the caller's id, FR-19 then applies. |
| TC-ADMINUSERS-008 | INCOMPLETE | Unspecified | DELETE /api/admin/users/ may be a different route than /:id. Generated 'not a successful delete' assumed routing. No id-empty rule is written. |
| TC-ADMINUSERS-009 | INVALID | Unspecified | Repeat delete / 404 is not specified. |
| TC-ADMINUSERS-010 | INCOMPLETE | Unspecified | FR-19 forbids only self-delete. Expecting 200 for deleting another admin invents a success rule; expecting reject would also invent a rule. |
| TC-ADMINUSERS-011 | INCOMPLETE | Invalid | Admin API requires a token (API spec §6; FR-12; SEC-02). HTTP 401 is not specified. |
| TC-ADMINUSERS-012 | INCOMPLETE | Invalid | Empty token is not a valid JWT. HTTP 401 is not specified. |
| TC-ADMINUSERS-013 | INCOMPLETE | Invalid | Malformed token is not a valid JWT. HTTP 403/401 is not specified. |
| TC-ADMINUSERS-014 | INCOMPLETE | Invalid | FR-12 / SEC-03: admin APIs require role=admin, not merely a token. Generated HTTP 403 is not specified. |
| TC-ADMINUSERS-015 | INCOMPLETE | Invalid | Same FR-12 rule; plus FR-19 is irrelevant if the caller is not allowed to use the admin API at all. HTTP 403 is not specified. |
| TC-ADMINUSERS-016 | INCOMPLETE | Unspecified | No body is documented for DELETE. Assuming the delete still succeeds with {force:true} invents a body-ignored rule. |
| TC-ADMINUSERS-017 | VALID | Valid | The specified identifier is the path parameter :id. A query string is not a documented id. |
| TC-ADMINUSERS-018 | INVALID | Unspecified | A large numeric id / 404 / 'must not crash' is not specified. |
| TC-ADMINUSERS-019 | INCOMPLETE | Invalid | Path id is the specified resource; FR-19 forbids self-delete. Generated HTTP 403 is not specified. |
| TC-ADMINUSERS-020 | INCOMPLETE | Unspecified | Leading-zero encoding is not specified. Generated 400/404 was invented. FR-19 applies only if the path is resolved as the caller. |
| TC-CART-001 | VALID | Valid | Documented POST /api/cart body with a typical quantity from the example, under required auth. No extra reject rule claimed. |
| TC-CART-002 | INCOMPLETE | Valid | FR-06's 'quantity ≥ 1' is the product-detail UI box, not a stated POST /api/cart rule. Quantity 1 is still a reasonable typical value from the example domain (example uses 2). |
| TC-CART-003 | VALID | Valid | Another seed product with a typical body. No charset restriction. Does not invent catalogue-match rules. |
| TC-CART-004 | VALID | Valid | No maximum quantity is stated, so quantity=10 is not specified as invalid. Treated as a typical valid representative, not as a proven max. |
| TC-CART-005 | VALID | Valid | Cart API requires a token, not role=user. An admin JWT is a logged-in user. |
| TC-CART-006 | VALID | Valid | FR-07: adding the same product increases quantity and must not create a new line. |
| TC-CART-007 | VALID | Valid | FR-07 merge applies to the same product; a different id is a different line. |
| TC-CART-008 | INVALID | Unspecified | No rule says product id must be > 0 or exist in the catalogue. |
| TC-CART-009 | INVALID | Unspecified | Negative product id is not specified as invalid. |
| TC-CART-010 | INVALID | Unspecified | The spec does not require id to reference an existing product. |
| TC-CART-011 | INVALID | Unspecified | id appears in the example body but is not stated as required. |
| TC-CART-012 | INVALID | Unspecified | id=null is not specified as invalid. |
| TC-CART-013 | INVALID | Unspecified | Non-integer id is not specified as invalid. |
| TC-CART-014 | INVALID | Unspecified | Non-numeric id is not specified as invalid. |
| TC-CART-015 | INCOMPLETE | Unspecified | Example id is a number; coercion of string '1' is not specified. Generated case still preferred reject/coerce. |
| TC-CART-016 | INVALID | Unspecified | FR-06 quantity ≥ 1 is the product-detail UI control, not a POST /api/cart rule. Applying it here was an assumption. |
| TC-CART-017 | INVALID | Unspecified | Negative quantity is not specified for POST /api/cart. FR-06 is product-detail UI. |
| TC-CART-018 | INVALID | Unspecified | quantity is in the example body, not stated as required. |
| TC-CART-019 | INVALID | Unspecified | Non-integer quantity is not specified for this API. |
| TC-CART-020 | INCOMPLETE | Unspecified | Coercion of quantity string is not specified. |
| TC-CART-021 | INVALID | Unspecified | quantity=null is not specified as invalid. |
| TC-CART-022 | INCOMPLETE | Unspecified | No max quantity is specified. 'Must not crash' is not a written requirement. |
| TC-CART-023 | INVALID | Unspecified | FR-15 price > 0 is product CRUD, not POST /api/cart. |
| TC-CART-024 | INVALID | Unspecified | Negative cart price is not specified. FR-15 is the product-admin rule. |
| TC-CART-025 | INVALID | Unspecified | C-PRICE-04: the API example includes price. Neither FR-07 nor api_specification.md says price is mandatory on every POST /api/cart. Required-on-body was assumed. |
| TC-CART-026 | INCOMPLETE | Unspecified | Price type coercion is not specified. |
| TC-CART-027 | INVALID | Unspecified | price=null is not specified as invalid. |
| TC-CART-028 | INVALID | Unspecified | FR-08 forbids trusting client total_amount at checkout. It does not say POST /api/cart must match catalogue price. |
| TC-CART-029 | INVALID | Unspecified | Empty cart line name is not specified as invalid. |
| TC-CART-030 | INVALID | Unspecified | name is in the example, not stated as required. |
| TC-CART-031 | INVALID | Unspecified | No rule says client name must match the catalogue for id. |
| TC-CART-032 | INCOMPLETE | Invalid | Auth is required (API spec §4). HTTP 401 is not specified. |
| TC-CART-033 | INCOMPLETE | Invalid | Empty token is not a valid JWT. HTTP 401 is not specified. |
| TC-CART-034 | INCOMPLETE | Invalid | Malformed token is not a valid JWT. HTTP 403/401 is not specified. |
| TC-CART-035 | INVALID | Unspecified | Empty body is not specified as invalid. |
| TC-CART-036 | INCOMPLETE | Invalid | Body is documented as JSON. Malformed text is not JSON. HTTP 400 is not specified. |
| TC-CART-037 | INVALID | Unspecified | A JSON array is not stated as a rejected shape. |
| TC-CART-038 | INCOMPLETE | Unspecified | Extra-field policy is not specified. Asserting color must not affect merge/price invents a rule. |
| TC-CART-039 | INVALID | Unspecified | Content-Type is not specified. |
| TC-PROFILE-001 | VALID | Valid | FR-04 allows updating name, phone, and default shipping address for the logged-in user; email and role must stay unchanged (FR-04 / SEC-06). Input is the documented example shape. |
| TC-PROFILE-002 | VALID | Valid | FR-04 states a valid phone is 10–11 digits starting with 0. 11 digits is the documented maximum. |
| TC-PROFILE-003 | VALID | Valid | No charset restriction is stated for name or address. 11-digit phone is in the FR-04 valid set. Combining valid representatives is allowed. |
| TC-PROFILE-004 | VALID | Valid | FR-04 applies to a logged-in user; an admin token is a logged-in user. Role must remain admin (FR-04 / SEC-06). |
| TC-PROFILE-005 | VALID | Valid | 0000000000 starts with 0 and has 10 digits, which is the only phone rule FR-04 states. No numbering-plan rule exists. |
| TC-PROFILE-006 | INCOMPLETE | Unspecified | No name-format or HTML rule is stated. The generated case asserted HTTP 200 and literal persistence, which is not in the spec. |
| TC-PROFILE-007 | INCOMPLETE | Unspecified | No shipping_address format/HTML rule is stated. Generated oracle assumed accept-and-persist. |
| TC-PROFILE-008 | INVALID | Unspecified | FR-14 says category name cannot be empty; FR-04 never says name cannot be empty. Empty name was treated as invalid by assumption. |
| TC-PROFILE-009 | INVALID | Unspecified | No whitespace rule is stated for name. |
| TC-PROFILE-010 | INVALID | Unspecified | P-NAME-05: FR-04 lists Họ Tên as updatable and the API example includes name. Neither document says name is mandatory on every PUT. Omitting it is not a specified invalid class. |
| TC-PROFILE-011 | INVALID | Unspecified | Null handling for name is not specified. |
| TC-PROFILE-012 | INVALID | Unspecified | JSON type for name is not specified (example is a string, not a type constraint). |
| TC-PROFILE-013 | INCOMPLETE | Unspecified | FR-04 does not define a max name length. The generated case still told the tester to expect accept (200). |
| TC-PROFILE-014 | INCOMPLETE | Invalid | 9 digits is outside FR-04's 10–11. The generated HTTP 400 is not specified. |
| TC-PROFILE-015 | INCOMPLETE | Invalid | 12 digits is outside FR-04's 10–11. HTTP 400 is not specified. |
| TC-PROFILE-016 | INCOMPLETE | Invalid | Does not start with 0, so it is not a valid FR-04 phone. HTTP 400 is not specified. |
| TC-PROFILE-017 | INCOMPLETE | Invalid | Empty string is not 10–11 digits starting with 0, so it fails the stated phone rule (this is format, not an assumed 'required' flag). HTTP 400 is not specified. |
| TC-PROFILE-018 | INVALID | Unspecified | Omitting phone is not the same as submitting an invalid phone. Partial update is not forbidden. Required-on-PUT was assumed. |
| TC-PROFILE-019 | INCOMPLETE | Invalid | FR-04 requires digits (chữ số). Letters are outside that set. HTTP 400 is not specified. |
| TC-PROFILE-020 | INCOMPLETE | Invalid | Separators are not 10–11 digits. HTTP 400 is not specified. |
| TC-PROFILE-021 | INCOMPLETE | Invalid | +84… does not start with 0. HTTP 400 is not specified. |
| TC-PROFILE-022 | INCOMPLETE | Invalid | A leading space means the value does not start with 0. HTTP 400 is not specified. |
| TC-PROFILE-023 | INCOMPLETE | Invalid | If phone is sent, FR-04's valid form applies; null is not that form. Generated HTTP 400 is not specified. |
| TC-PROFILE-024 | INCOMPLETE | Invalid | JSON number 912345678 is not a digit string starting with 0. HTTP 400 is not specified. |
| TC-PROFILE-025 | INVALID | Unspecified | No non-empty rule is stated for shipping_address. |
| TC-PROFILE-026 | INVALID | Unspecified | shipping_address is listed as updatable, not as mandatory on every PUT. |
| TC-PROFILE-027 | INVALID | Unspecified | Null handling for shipping_address is not specified. |
| TC-PROFILE-028 | INCOMPLETE | Unspecified | No max address length is specified. Generated case expected accept. |
| TC-PROFILE-029 | INCOMPLETE | Invalid | Token is required (API spec Users section; SEC-02). Generated HTTP 401 is not specified. |
| TC-PROFILE-030 | INCOMPLETE | Invalid | Empty Bearer is not a valid JWT (SEC-02). HTTP 401 is not specified. |
| TC-PROFILE-031 | INCOMPLETE | Invalid | Malformed token is not a valid JWT (SEC-02). HTTP 403/401 is not specified. |
| TC-PROFILE-032 | INCOMPLETE | Invalid | A tampered signature is not a valid JWT (SEC-02). HTTP 403 is not specified. |
| TC-PROFILE-033 | VALID | Invalid | FR-04 and SEC-06 forbid changing role from the client. The oracle allows reject or ignore, so it does not invent a status code. |
| TC-PROFILE-034 | VALID | Invalid | Role is not a documented writable field (FR-04 / SEC-06), even when the value equals the current role. |
| TC-PROFILE-035 | VALID | Invalid | FR-04: email must not be changed. Reject vs ignore is unspecified; unchanged email is specified. |
| TC-PROFILE-036 | INVALID | Unspecified | An empty HTTP body is not stated as invalid. Fields were assumed required as a group. |
| TC-PROFILE-037 | INCOMPLETE | Invalid | The API documents Body (JSON). Malformed text is not JSON. Generated HTTP 400 is not specified. |
| TC-PROFILE-038 | INCOMPLETE | Unspecified | Extra-field policy is not specified. The generated case asserted nickname must not persist, which is not written. |
| TC-PROFILE-039 | INVALID | Unspecified | The example body is an object; the spec does not say a JSON array must be rejected. |
| TC-PROFILE-040 | INVALID | Unspecified | Content-Type is not specified. JSON in the spec describes the body example, not a header rule. |

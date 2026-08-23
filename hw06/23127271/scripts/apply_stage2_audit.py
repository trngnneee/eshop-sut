#!/usr/bin/env python3
"""Stage 2 audit: label every AI TC, then correct Expected result / Type in place."""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "domain-partitions.csv"
AUDIT_DOC = ROOT / "docs" / "stage2-audit.md"

# Spec-backed phone oracle (FR-04). Status code is not in the spec.
PHONE_NOT_STORED = (
    "The submitted phone is not a valid FR-04 phone (must start with 0 and be 10–11 digits). "
    "GET /api/users/me must not persist this value as phone. "
    "HTTP status and error body are not specified."
)
TOKEN_REQUIRED = (
    "The endpoint requires a valid JWT (API spec Authorization note; SEC-02; FR-04 requires a logged-in user). "
    "The profile / cart / user-list must not change. HTTP status (401 vs 403 vs other) is not specified."
)
CART_TOKEN = (
    "POST /api/cart requires Authorization: Bearer <token> (API spec §4). "
    "No cart line is added for this caller. HTTP status is not specified."
)
ADMIN_TOKEN = (
    "DELETE /api/admin/users/:id requires a valid JWT and role=admin (API spec §6; FR-12; SEC-02; SEC-03). "
    "The target user must still exist afterwards. HTTP status is not specified."
)
NO_RULE = (
    "The SRS and api_specification.md do not state this input is invalid or required. "
    "Do not expect rejection. Record what the SUT does; do not fail it against an invented rule."
)
UNSPEC_MAX = (
    "No maximum length/quantity is specified. Do not expect accept or reject. Record actual behaviour."
)
UNSPEC_COERCE = (
    "No type-coercion rule is specified. Do not expect accept, reject, or a particular coerced value. Record actual behaviour."
)
UNSPEC_EXTRA = (
    "Extra-field handling is not specified. Documented fields may still update. "
    "Do not assert how the extra field is stored or rejected."
)


def A(status, reasoning, typ, expected, title=None):
    return {
        "AuditStatus": status,
        "AuditReasoning": reasoning,
        "Type": typ,
        "ExpectedResult": expected,
        "Title": title,
    }


AUDITS = {
    # ----- FR-04: VALID -----
    "TC-PROFILE-001": A(
        "VALID",
        "FR-04 allows updating name, phone, and default shipping address for the logged-in user; email and role must stay unchanged (FR-04 / SEC-06). Input is the documented example shape.",
        "Valid",
        "The authenticated user's name, phone, and shipping_address match the submitted values on a follow-up GET /api/users/me. email and role are unchanged. Success HTTP status and response body are not specified.",
    ),
    "TC-PROFILE-002": A(
        "VALID",
        "FR-04 states a valid phone is 10–11 digits starting with 0. 11 digits is the documented maximum.",
        "Valid",
        "GET /api/users/me shows phone=09123456789 together with the submitted name and shipping_address. email and role unchanged. Success status/body not specified.",
    ),
    "TC-PROFILE-003": A(
        "VALID",
        "No charset restriction is stated for name or address. 11-digit phone is in the FR-04 valid set. Combining valid representatives is allowed.",
        "Valid",
        "GET /api/users/me persists the Unicode name, Unicode address, and 11-digit phone exactly. email and role unchanged. Success status/body not specified.",
    ),
    "TC-PROFILE-004": A(
        "VALID",
        "FR-04 applies to a logged-in user; an admin token is a logged-in user. Role must remain admin (FR-04 / SEC-06).",
        "Valid",
        "GET /api/users/me as that admin shows the new name/phone/address and role still admin. Success status/body not specified.",
    ),
    "TC-PROFILE-005": A(
        "VALID",
        "0000000000 starts with 0 and has 10 digits, which is the only phone rule FR-04 states. No numbering-plan rule exists.",
        "Valid",
        "GET /api/users/me shows phone=0000000000. Success status/body not specified.",
    ),
    # ----- FR-04: INCOMPLETE (real rule or unspecified observe, but generated oracle over-claimed) -----
    "TC-PROFILE-006": A(
        "INCOMPLETE",
        "No name-format or HTML rule is stated. The generated case asserted HTTP 200 and literal persistence, which is not in the spec.",
        "Unspecified",
        "Name charset/HTML handling is not specified. Do not expect accept or reject. If a name is stored, email and role still must not change (FR-04 / SEC-06).",
        "HTML in name — no format rule specified",
    ),
    "TC-PROFILE-007": A(
        "INCOMPLETE",
        "No shipping_address format/HTML rule is stated. Generated oracle assumed accept-and-persist.",
        "Unspecified",
        "Address charset/HTML handling is not specified. Do not expect accept or reject. email and role must not change if any update occurs.",
        "HTML in shipping_address — no format rule specified",
    ),
    "TC-PROFILE-013": A(
        "INCOMPLETE",
        "FR-04 does not define a max name length. The generated case still told the tester to expect accept (200).",
        "Unspecified",
        UNSPEC_MAX,
        "Name length 500 — no max specified",
    ),
    "TC-PROFILE-014": A(
        "INCOMPLETE",
        "9 digits is outside FR-04's 10–11. The generated HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-015": A(
        "INCOMPLETE",
        "12 digits is outside FR-04's 10–11. HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-016": A(
        "INCOMPLETE",
        "Does not start with 0, so it is not a valid FR-04 phone. HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-017": A(
        "INCOMPLETE",
        "Empty string is not 10–11 digits starting with 0, so it fails the stated phone rule (this is format, not an assumed 'required' flag). HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-019": A(
        "INCOMPLETE",
        "FR-04 requires digits (chữ số). Letters are outside that set. HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-020": A(
        "INCOMPLETE",
        "Separators are not 10–11 digits. HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-021": A(
        "INCOMPLETE",
        "+84… does not start with 0. HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-022": A(
        "INCOMPLETE",
        "A leading space means the value does not start with 0. HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-023": A(
        "INCOMPLETE",
        "If phone is sent, FR-04's valid form applies; null is not that form. Generated HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-024": A(
        "INCOMPLETE",
        "JSON number 912345678 is not a digit string starting with 0. HTTP 400 is not specified.",
        "Invalid",
        PHONE_NOT_STORED,
    ),
    "TC-PROFILE-028": A(
        "INCOMPLETE",
        "No max address length is specified. Generated case expected accept.",
        "Unspecified",
        UNSPEC_MAX,
        "Address length 500 — no max specified",
    ),
    "TC-PROFILE-029": A(
        "INCOMPLETE",
        "Token is required (API spec Users section; SEC-02). Generated HTTP 401 is not specified.",
        "Invalid",
        TOKEN_REQUIRED,
    ),
    "TC-PROFILE-030": A(
        "INCOMPLETE",
        "Empty Bearer is not a valid JWT (SEC-02). HTTP 401 is not specified.",
        "Invalid",
        TOKEN_REQUIRED,
    ),
    "TC-PROFILE-031": A(
        "INCOMPLETE",
        "Malformed token is not a valid JWT (SEC-02). HTTP 403/401 is not specified.",
        "Invalid",
        TOKEN_REQUIRED,
    ),
    "TC-PROFILE-032": A(
        "INCOMPLETE",
        "A tampered signature is not a valid JWT (SEC-02). HTTP 403 is not specified.",
        "Invalid",
        TOKEN_REQUIRED,
    ),
    "TC-PROFILE-033": A(
        "VALID",
        "FR-04 and SEC-06 forbid changing role from the client. The oracle allows reject or ignore, so it does not invent a status code.",
        "Invalid",
        "role remains the pre-request value (user). Documented profile fields may or may not update; that is unspecified. A silent role change to admin fails FR-04 / SEC-06.",
    ),
    "TC-PROFILE-034": A(
        "VALID",
        "Role is not a documented writable field (FR-04 / SEC-06), even when the value equals the current role.",
        "Invalid",
        "GET /api/users/me still shows the same role as before. The API must not treat role as a client-writable field.",
    ),
    "TC-PROFILE-035": A(
        "VALID",
        "FR-04: email must not be changed. Reject vs ignore is unspecified; unchanged email is specified.",
        "Invalid",
        "GET /api/users/me still shows the original email (test@eshop.com). Whether the request is rejected or the extra field is ignored is not specified.",
    ),
    "TC-PROFILE-037": A(
        "INCOMPLETE",
        "The API documents Body (JSON). Malformed text is not JSON. Generated HTTP 400 is not specified.",
        "Invalid",
        "The body is not the documented JSON object. Profile fields must not be updated from this payload. HTTP status is not specified.",
        "Send malformed JSON (not the documented JSON body)",
    ),
    "TC-PROFILE-038": A(
        "INCOMPLETE",
        "Extra-field policy is not specified. The generated case asserted nickname must not persist, which is not written.",
        "Unspecified",
        UNSPEC_EXTRA + " email and role still must not change.",
        "Extra field nickname — handling not specified",
    ),
    # ----- FR-04: INVALID (invented required / reject) -----
    "TC-PROFILE-008": A(
        "INVALID",
        "FR-14 says category name cannot be empty; FR-04 never says name cannot be empty. Empty name was treated as invalid by assumption.",
        "Unspecified",
        NO_RULE,
        "Empty name — not specified as invalid",
    ),
    "TC-PROFILE-009": A(
        "INVALID",
        "No whitespace rule is stated for name.",
        "Unspecified",
        NO_RULE,
        "Whitespace-only name — not specified as invalid",
    ),
    "TC-PROFILE-010": A(
        "INVALID",
        "P-NAME-05: FR-04 lists Họ Tên as updatable and the API example includes name. Neither document says name is mandatory on every PUT. Omitting it is not a specified invalid class.",
        "Unspecified",
        "name is not specified as required on PUT /api/users/me. Do not expect rejection. Observe whether the stored name is unchanged, cleared, or otherwise updated. email and role must not change.",
        "Omit name — not specified as required",
    ),
    "TC-PROFILE-011": A(
        "INVALID",
        "Null handling for name is not specified.",
        "Unspecified",
        NO_RULE,
        "name=null — not specified as invalid",
    ),
    "TC-PROFILE-012": A(
        "INVALID",
        "JSON type for name is not specified (example is a string, not a type constraint).",
        "Unspecified",
        NO_RULE,
        "Numeric name — type not specified",
    ),
    "TC-PROFILE-018": A(
        "INVALID",
        "Omitting phone is not the same as submitting an invalid phone. Partial update is not forbidden. Required-on-PUT was assumed.",
        "Unspecified",
        "phone is not specified as required on every PUT. Do not expect rejection. If a phone is stored afterwards, it must still be a FR-04-valid phone when one is present.",
        "Omit phone — not specified as required",
    ),
    "TC-PROFILE-025": A(
        "INVALID",
        "No non-empty rule is stated for shipping_address.",
        "Unspecified",
        NO_RULE,
        "Empty shipping_address — not specified as invalid",
    ),
    "TC-PROFILE-026": A(
        "INVALID",
        "shipping_address is listed as updatable, not as mandatory on every PUT.",
        "Unspecified",
        "shipping_address is not specified as required. Do not expect rejection. Record what happens to the stored address.",
        "Omit shipping_address — not specified as required",
    ),
    "TC-PROFILE-027": A(
        "INVALID",
        "Null handling for shipping_address is not specified.",
        "Unspecified",
        NO_RULE,
        "shipping_address=null — not specified as invalid",
    ),
    "TC-PROFILE-036": A(
        "INVALID",
        "An empty HTTP body is not stated as invalid. Fields were assumed required as a group.",
        "Unspecified",
        NO_RULE,
        "Empty HTTP body — not specified as invalid",
    ),
    "TC-PROFILE-039": A(
        "INVALID",
        "The example body is an object; the spec does not say a JSON array must be rejected.",
        "Unspecified",
        NO_RULE,
        "JSON array body — rejection not specified",
    ),
    "TC-PROFILE-040": A(
        "INVALID",
        "Content-Type is not specified. JSON in the spec describes the body example, not a header rule.",
        "Unspecified",
        NO_RULE,
        "Content-Type text/plain — not specified",
    ),
    # ----- FR-07 VALID -----
    "TC-CART-001": A(
        "VALID",
        "Documented POST /api/cart body with a typical quantity from the example, under required auth. No extra reject rule claimed.",
        "Valid",
        "The authenticated user's cart includes a line for product id=1 with quantity 2 (or merged qty if a line already existed — FR-07). Success status/body are not specified.",
    ),
    "TC-CART-003": A(
        "VALID",
        "Another seed product with a typical body. No charset restriction. Does not invent catalogue-match rules.",
        "Valid",
        "GET /api/cart as the same user includes a line for id=5. Success status/body not specified.",
    ),
    "TC-CART-004": A(
        "VALID",
        "No maximum quantity is stated, so quantity=10 is not specified as invalid. Treated as a typical valid representative, not as a proven max.",
        "Valid",
        "GET /api/cart includes a line for id=1 reflecting quantity 10 (or merged). Success status/body not specified.",
    ),
    "TC-CART-005": A(
        "VALID",
        "Cart API requires a token, not role=user. An admin JWT is a logged-in user.",
        "Valid",
        "GET /api/cart with the same admin token shows the added line on that user's cart. Success status/body not specified.",
    ),
    "TC-CART-006": A(
        "VALID",
        "FR-07: adding the same product increases quantity and must not create a new line.",
        "Valid",
        "GET /api/cart shows exactly one line for product 1 with quantity 2 (1+1). A second row for the same product fails FR-07. Success status/body not specified.",
    ),
    "TC-CART-007": A(
        "VALID",
        "FR-07 merge applies to the same product; a different id is a different line.",
        "Valid",
        "GET /api/cart contains distinct lines for id=1 and id=2. Product 1 quantity is unchanged.",
    ),
    "TC-CART-002": A(
        "INCOMPLETE",
        "FR-06's 'quantity ≥ 1' is the product-detail UI box, not a stated POST /api/cart rule. Quantity 1 is still a reasonable typical value from the example domain (example uses 2).",
        "Valid",
        "Quantity 1 is not specified as the API minimum. Treat as a typical add: GET /api/cart includes product 1. Do not use this case to prove an API min=1 rule. Success status/body not specified.",
        "Add with quantity=1 (typical value; FR-06 is product-detail UI, not this API)",
    ),
    "TC-CART-015": A(
        "INCOMPLETE",
        "Example id is a number; coercion of string '1' is not specified. Generated case still preferred reject/coerce.",
        "Unspecified",
        UNSPEC_COERCE,
        "id as JSON string — coercion not specified",
    ),
    "TC-CART-020": A(
        "INCOMPLETE",
        "Coercion of quantity string is not specified.",
        "Unspecified",
        UNSPEC_COERCE,
        "quantity as JSON string — coercion not specified",
    ),
    "TC-CART-022": A(
        "INCOMPLETE",
        "No max quantity is specified. 'Must not crash' is not a written requirement.",
        "Unspecified",
        UNSPEC_MAX,
        "Very large quantity — no max specified",
    ),
    "TC-CART-026": A(
        "INCOMPLETE",
        "Price type coercion is not specified.",
        "Unspecified",
        UNSPEC_COERCE,
        "price as JSON string — coercion not specified",
    ),
    "TC-CART-032": A(
        "INCOMPLETE",
        "Auth is required (API spec §4). HTTP 401 is not specified.",
        "Invalid",
        CART_TOKEN,
    ),
    "TC-CART-033": A(
        "INCOMPLETE",
        "Empty token is not a valid JWT. HTTP 401 is not specified.",
        "Invalid",
        CART_TOKEN,
    ),
    "TC-CART-034": A(
        "INCOMPLETE",
        "Malformed token is not a valid JWT. HTTP 403/401 is not specified.",
        "Invalid",
        CART_TOKEN,
    ),
    "TC-CART-036": A(
        "INCOMPLETE",
        "Body is documented as JSON. Malformed text is not JSON. HTTP 400 is not specified.",
        "Invalid",
        "The body is not the documented JSON object. Do not treat this payload as a successful add. HTTP status is not specified.",
        "Send malformed JSON (not the documented JSON body)",
    ),
    "TC-CART-038": A(
        "INCOMPLETE",
        "Extra-field policy is not specified. Asserting color must not affect merge/price invents a rule.",
        "Unspecified",
        UNSPEC_EXTRA,
        "Extra field color — handling not specified",
    ),
    # CART INVALID
    "TC-CART-008": A(
        "INVALID",
        "No rule says product id must be > 0 or exist in the catalogue.",
        "Unspecified",
        NO_RULE,
        "id=0 — not specified as invalid",
    ),
    "TC-CART-009": A(
        "INVALID",
        "Negative product id is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "Negative id — not specified as invalid",
    ),
    "TC-CART-010": A(
        "INVALID",
        "The spec does not require id to reference an existing product.",
        "Unspecified",
        NO_RULE,
        "Non-existent product id — not specified as invalid",
    ),
    "TC-CART-011": A(
        "INVALID",
        "id appears in the example body but is not stated as required.",
        "Unspecified",
        NO_RULE,
        "Omit id — not specified as required",
    ),
    "TC-CART-012": A(
        "INVALID",
        "id=null is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "id=null — not specified as invalid",
    ),
    "TC-CART-013": A(
        "INVALID",
        "Non-integer id is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "id=1.5 — not specified as invalid",
    ),
    "TC-CART-014": A(
        "INVALID",
        "Non-numeric id is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "id='abc' — not specified as invalid",
    ),
    "TC-CART-016": A(
        "INVALID",
        "FR-06 quantity ≥ 1 is the product-detail UI control, not a POST /api/cart rule. Applying it here was an assumption.",
        "Unspecified",
        NO_RULE,
        "quantity=0 — not specified as invalid for this API",
    ),
    "TC-CART-017": A(
        "INVALID",
        "Negative quantity is not specified for POST /api/cart. FR-06 is product-detail UI.",
        "Unspecified",
        NO_RULE,
        "Negative quantity — not specified as invalid for this API",
    ),
    "TC-CART-018": A(
        "INVALID",
        "quantity is in the example body, not stated as required.",
        "Unspecified",
        NO_RULE,
        "Omit quantity — not specified as required",
    ),
    "TC-CART-019": A(
        "INVALID",
        "Non-integer quantity is not specified for this API.",
        "Unspecified",
        NO_RULE,
        "quantity=1.5 — not specified as invalid",
    ),
    "TC-CART-021": A(
        "INVALID",
        "quantity=null is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "quantity=null — not specified as invalid",
    ),
    "TC-CART-023": A(
        "INVALID",
        "FR-15 price > 0 is product CRUD, not POST /api/cart.",
        "Unspecified",
        NO_RULE,
        "price=0 — not specified as invalid for this API",
    ),
    "TC-CART-024": A(
        "INVALID",
        "Negative cart price is not specified. FR-15 is the product-admin rule.",
        "Unspecified",
        NO_RULE,
        "Negative price — not specified as invalid for this API",
    ),
    "TC-CART-025": A(
        "INVALID",
        "C-PRICE-04: the API example includes price. Neither FR-07 nor api_specification.md says price is mandatory on every POST /api/cart. Required-on-body was assumed.",
        "Unspecified",
        "price is not specified as required on POST /api/cart. Do not expect rejection. Observe whether a cart line is added and what price (if any) is stored. Do not apply FR-15 (product CRUD price > 0) to this endpoint.",
        "Omit price — not specified as required",
    ),
    "TC-CART-027": A(
        "INVALID",
        "price=null is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "price=null — not specified as invalid",
    ),
    "TC-CART-028": A(
        "INVALID",
        "FR-08 forbids trusting client total_amount at checkout. It does not say POST /api/cart must match catalogue price.",
        "Unspecified",
        NO_RULE,
        "Client price ≠ catalogue — not specified",
    ),
    "TC-CART-029": A(
        "INVALID",
        "Empty cart line name is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "Empty name — not specified as invalid",
    ),
    "TC-CART-030": A(
        "INVALID",
        "name is in the example, not stated as required.",
        "Unspecified",
        NO_RULE,
        "Omit name — not specified as required",
    ),
    "TC-CART-031": A(
        "INVALID",
        "No rule says client name must match the catalogue for id.",
        "Unspecified",
        NO_RULE,
        "Name ≠ catalogue — not specified",
    ),
    "TC-CART-035": A(
        "INVALID",
        "Empty body is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "Empty HTTP body — not specified as invalid",
    ),
    "TC-CART-037": A(
        "INVALID",
        "A JSON array is not stated as a rejected shape.",
        "Unspecified",
        NO_RULE,
        "JSON array body — rejection not specified",
    ),
    "TC-CART-039": A(
        "INVALID",
        "Content-Type is not specified.",
        "Unspecified",
        NO_RULE,
        "Content-Type text/plain — not specified",
    ),
    # ADMIN
    "TC-ADMINUSERS-001": A(
        "VALID",
        "FR-19: admin may delete users other than the currently logged-in account. FR-12: caller is admin with JWT.",
        "Valid",
        "The disposable user is absent from a subsequent GET /api/admin/users. The caller's own account still exists. GET /api/admin/users must not include passwords (FR-19). Success HTTP status/body are not specified.",
    ),
    "TC-ADMINUSERS-002": A(
        "INCOMPLETE",
        "FR-19 forbids deleting the currently logged-in account. Generated HTTP 403/400 is not specified.",
        "Invalid",
        "The admin's own account still exists (GET /api/users/me and GET /api/admin/users). HTTP status is not specified.",
    ),
    "TC-ADMINUSERS-003": A(
        "INVALID",
        "id=0 is not specified as invalid. Only self-delete is forbidden in FR-19.",
        "Unspecified",
        NO_RULE,
        "id=0 — not specified as invalid",
    ),
    "TC-ADMINUSERS-004": A(
        "INVALID",
        "Negative id is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "Negative id — not specified as invalid",
    ),
    "TC-ADMINUSERS-005": A(
        "INVALID",
        "Missing-user / HTTP 404 is not specified.",
        "Unspecified",
        NO_RULE,
        "Non-existent user id — not specified as invalid",
    ),
    "TC-ADMINUSERS-006": A(
        "INVALID",
        "Non-numeric path id is not specified as invalid.",
        "Unspecified",
        NO_RULE,
        "Non-numeric id — not specified as invalid",
    ),
    "TC-ADMINUSERS-007": A(
        "INVALID",
        "Non-integer path id is not specified. 'Must not coerce to 1' was invented. If the SUT resolves this path to the caller's id, FR-19 then applies.",
        "Unspecified",
        "No id-format rule is stated. Do not expect 400/404. If this path is treated as the caller's own id, FR-19: that account must not be deleted.",
        "id=1.5 — format not specified (FR-19 only if resolved as self)",
    ),
    "TC-ADMINUSERS-008": A(
        "INCOMPLETE",
        "DELETE /api/admin/users/ may be a different route than /:id. Generated 'not a successful delete' assumed routing. No id-empty rule is written.",
        "Unspecified",
        "Empty path is not specified for this operation. Do not expect a particular status. User list must not lose an arbitrary user as a side effect of this call.",
        "Empty path — routing not specified",
    ),
    "TC-ADMINUSERS-009": A(
        "INVALID",
        "Repeat delete / 404 is not specified.",
        "Unspecified",
        NO_RULE,
        "Repeat DELETE of a missing id — not specified",
    ),
    "TC-ADMINUSERS-010": A(
        "INCOMPLETE",
        "FR-19 forbids only self-delete. Expecting 200 for deleting another admin invents a success rule; expecting reject would also invent a rule.",
        "Unspecified",
        "Spec forbids only deleting the currently logged-in account. Outcome for another admin is not specified. Do not expect success or failure. Blocked if a second admin cannot be created.",
        "Delete another admin — only self-delete is specified",
    ),
    "TC-ADMINUSERS-011": A(
        "INCOMPLETE",
        "Admin API requires a token (API spec §6; FR-12; SEC-02). HTTP 401 is not specified.",
        "Invalid",
        ADMIN_TOKEN,
    ),
    "TC-ADMINUSERS-012": A(
        "INCOMPLETE",
        "Empty token is not a valid JWT. HTTP 401 is not specified.",
        "Invalid",
        ADMIN_TOKEN,
    ),
    "TC-ADMINUSERS-013": A(
        "INCOMPLETE",
        "Malformed token is not a valid JWT. HTTP 403/401 is not specified.",
        "Invalid",
        ADMIN_TOKEN,
    ),
    "TC-ADMINUSERS-014": A(
        "INCOMPLETE",
        "FR-12 / SEC-03: admin APIs require role=admin, not merely a token. Generated HTTP 403 is not specified.",
        "Invalid",
        "A non-admin caller must not delete the target. The target still exists afterwards. HTTP status is not specified.",
    ),
    "TC-ADMINUSERS-015": A(
        "INCOMPLETE",
        "Same FR-12 rule; plus FR-19 is irrelevant if the caller is not allowed to use the admin API at all. HTTP 403 is not specified.",
        "Invalid",
        "A non-admin token must not delete this account (FR-12 / SEC-03). The user still exists. HTTP status is not specified.",
    ),
    "TC-ADMINUSERS-016": A(
        "INCOMPLETE",
        "No body is documented for DELETE. Assuming the delete still succeeds with {force:true} invents a body-ignored rule.",
        "Unspecified",
        "No request body is specified. The path id is the documented identifier. Do not expect the body to be required, forbidden, or honoured. If a user is deleted, it must be the path id, and not the caller if path id is self (FR-19).",
        "DELETE with unexpected JSON body — body not specified",
    ),
    "TC-ADMINUSERS-017": A(
        "VALID",
        "The specified identifier is the path parameter :id. A query string is not a documented id.",
        "Valid",
        "Only the path id is the documented user identifier. A query parameter named id is not specified and must not be treated as the resource id. If a delete occurs, it is the path-id user (and not self — FR-19).",
    ),
    "TC-ADMINUSERS-018": A(
        "INVALID",
        "A large numeric id / 404 / 'must not crash' is not specified.",
        "Unspecified",
        NO_RULE,
        "Very large id — not specified as invalid",
    ),
    "TC-ADMINUSERS-019": A(
        "INCOMPLETE",
        "Path id is the specified resource; FR-19 forbids self-delete. Generated HTTP 403 is not specified.",
        "Invalid",
        "Path id is the documented identifier. If that id is the caller, the caller still exists (FR-19). A body field id is not specified and must not be used as the resource id. HTTP status is not specified.",
    ),
    "TC-ADMINUSERS-020": A(
        "INCOMPLETE",
        "Leading-zero encoding is not specified. Generated 400/404 was invented. FR-19 applies only if the path is resolved as the caller.",
        "Unspecified",
        "No path-encoding rule is stated. Do not expect 400/404. If 0001 is treated as the caller's id, FR-19: that account must not be deleted.",
        "Path id 0001 — encoding not specified (FR-19 only if resolved as self)",
    ),
}


def find_file(tid: str) -> Path:
    for p in TC_ROOT.rglob(f"{tid}.md"):
        return p
    raise FileNotFoundError(tid)


def patch_md(tid: str, rec: dict) -> None:
    path = find_file(tid)
    text = path.read_text(encoding="utf-8")
    if rec.get("Title"):
        text = re.sub(r"^# " + re.escape(tid) + r": .*$", f"# {tid}: {rec['Title']}", text, count=1, flags=re.M)
    text = re.sub(
        r"## Expected result\n.*?\n\n## Sub-domains covered",
        "## Expected result\n" + rec["ExpectedResult"] + "\n\n## Sub-domains covered",
        text,
        count=1,
        flags=re.S,
    )
    audit_block = (
        f"## Type\n{rec['Type']}\n\n"
        f"## Audit\n"
        f"- **Status:** {rec['AuditStatus']}\n"
        f"- **Reasoning:** {rec['AuditReasoning']}\n\n"
        f"## Status / Related bugs"
    )
    text = re.sub(r"## Type\n.*?\n\n## Status / Related bugs", audit_block, text, count=1, flags=re.S)
    path.write_text(text, encoding="utf-8")


def patch_csv() -> None:
    with SHEET.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []
    for row in rows:
        rec = AUDITS[row["TestCaseID"]]
        row["AuditStatus"] = rec["AuditStatus"]
        row["AuditReasoning"] = rec["AuditReasoning"]
        row["ExpectedResult"] = rec["ExpectedResult"]
        notes = row.get("Notes") or ""
        notes = re.sub(r"Type=\w+", f"Type={rec['Type']}", notes)
        row["Notes"] = notes
    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_audit_doc() -> None:
    from collections import Counter

    counts = Counter(r["AuditStatus"] for r in AUDITS.values())
    lines = [
        "# Stage 2 — Human audit of AI domain-partition cases",
        "",
        "**Rule used:** only written SRS + `api_specification.md` text. If a requirement is missing, the case is not a specified invalid class — it is not labelled VALID as a reject test.",
        "",
        f"| Label | Count |",
        f"|-------|------:|",
        f"| VALID | {counts['VALID']} |",
        f"| INVALID | {counts['INVALID']} |",
        f"| INCOMPLETE | {counts['INCOMPLETE']} |",
        f"| **Total** | **{len(AUDITS)}** |",
        "",
        "## Labels",
        "",
        "| Label | Meaning in this audit |",
        "|-------|------------------------|",
        "| VALID | Partition and oracle both follow a written rule. |",
        "| INVALID | Generated oracle invented a reject/required/status rule the spec does not state (e.g. P-NAME-05 omit name). Corrected: no specified expected rejection. |",
        "| INCOMPLETE | The partition is real (or worth observing) but the generated expected result pinned an undocumented HTTP status, assumed accept, or mixed in a rule from another FR. Corrected expected result drops the invented part. |",
        "",
        "## P-NAME-05 (called out)",
        "",
        "`TC-PROFILE-010` was **INVALID**. FR-04 says the user *may update* name; the API example *includes* name. Neither says name is mandatory on every PUT. The AI treated omit-name as invalid by assumption. Corrected oracle: do not expect rejection; observe stored name; email/role still must not change.",
        "",
        "## Per-case table",
        "",
        "| TC ID | Audit | Corrected type | Reasoning |",
        "|-------|-------|----------------|-----------|",
    ]
    for tid in sorted(AUDITS, key=lambda x: (x.split("-")[1], x)):
        r = AUDITS[tid]
        reason = r["AuditReasoning"].replace("|", "/")
        lines.append(f"| {tid} | {r['AuditStatus']} | {r['Type']} | {reason} |")
    lines.append("")
    AUDIT_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    missing = []
    for p in TC_ROOT.rglob("TC-*.md"):
        tid = p.stem
        if tid not in AUDITS:
            missing.append(tid)
    extra = [k for k in AUDITS if not list(TC_ROOT.rglob(f"{k}.md"))]
    if missing or extra:
        raise SystemExit(f"missing audits {missing} extra {extra}")
    for tid, rec in AUDITS.items():
        patch_md(tid, rec)
    patch_csv()
    write_audit_doc()
    from collections import Counter
    c = Counter(r["AuditStatus"] for r in AUDITS.values())
    print("Audited", len(AUDITS), dict(c))


if __name__ == "__main__":
    main()

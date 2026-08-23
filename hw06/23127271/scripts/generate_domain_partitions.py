#!/usr/bin/env python3
"""Generate Skill-01 domain-partition artifacts + API-testing CSV for FR-04 / FR-07 / FR-19."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "domain-partitions.csv"
REPORT = ROOT / "docs" / "domain-testing-report.md"

BASE = "http://localhost:3000"

# ⚠️ Status codes below are used when the API spec does not name an error code.
# Success 200 is documented for sibling auth endpoints. Auth failures follow
# SEC-02 (token required). Validation / not-found / forbidden codes are assumed.
ASSUME_400 = "HTTP 400 (⚠️ spec does not name the validation status code; 4xx and no state change required)"
ASSUME_401 = "HTTP 401 Unauthorized (SEC-02: protected API requires a valid JWT)"
ASSUME_403 = "HTTP 403 Forbidden"
ASSUME_404 = "HTTP 404 Not Found (⚠️ spec does not name the not-found status code)"

USER_LOGIN = "POST /api/login with email=test@eshop.com password=Test1234!"
ADMIN_LOGIN = "POST /api/login with email=admin@eshop.com password=Admin123!"

VALID_PROFILE = {
    "name": "Nguyen Van A",
    "shipping_address": "123 Le Loi, Q1, TP.HCM",
    "phone": "0912345678",
}
VALID_CART = {
    "id": 1,
    "name": "iPhone 15 Pro Max",
    "price": 30000000,
    "quantity": 2,
}


def body_with(**overrides):
    data = dict(VALID_PROFILE)
    for k, v in overrides.items():
        if v is _OMIT:
            data.pop(k, None)
        else:
            data[k] = v
    return data


def cart_with(**overrides):
    data = dict(VALID_CART)
    for k, v in overrides.items():
        if v is _OMIT:
            data.pop(k, None)
        else:
            data[k] = v
    return data


class Omit:
    def __repr__(self):
        return "(omitted)"


_OMIT = Omit()


def fmt_val(v):
    if v is _OMIT:
        return "(field omitted)"
    if v is None:
        return "null"
    if isinstance(v, str) and v == "":
        return '"" (empty string)'
    if isinstance(v, str) and len(v) > 80:
        return f'"{v[:40]}…" ({len(v)} chars)'
    return json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v


def json_input(body, extra_headers=None, raw=None):
    payload = {
        "headers": {
            "Authorization": "Bearer <access_token>",
            "Content-Type": "application/json",
        },
        "body": body if raw is None else raw,
    }
    if extra_headers:
        payload["headers"].update(extra_headers)
    return json.dumps(payload, ensure_ascii=False)


# ---------------------------------------------------------------------------
# Sub-domain catalogues (Steps 2–3)
# ---------------------------------------------------------------------------

PROFILE_VARS = [
    ("#", "Variable", "Type", "Source"),
    ("1", "name", "string", "JSON body"),
    ("2", "phone", "string", "JSON body"),
    ("3", "shipping_address", "string", "JSON body"),
    ("4", "Authorization", "string (JWT)", "HTTP header"),
    ("5", "role", "string / omitted", "JSON body (undocumented extra field)"),
    ("6", "email", "string / omitted", "JSON body (undocumented extra field)"),
    ("7", "request body / Content-Type", "JSON object + header", "HTTP body / header"),
]

PROFILE_DOMAINS = {
    "name": [
        ("P-NAME-01", "Typical non-empty ASCII name", "Valid", "Nguyen Van A"),
        ("P-NAME-02", "Vietnamese Unicode name", "Valid", "Nguyễn Văn Á"),
        ("P-NAME-03", "Empty string", "Invalid", '""'),
        ("P-NAME-04", "Whitespace only", "Invalid", '"   "'),
        ("P-NAME-05", "Field omitted", "Invalid ⚠️ assumed required", "(omit name)"),
        ("P-NAME-06", "JSON null", "Invalid", "null"),
        ("P-NAME-07", "Wrong type (number)", "Invalid", "12345"),
        ("P-NAME-08", "HTML / special characters stored as text", "Valid", "Nguyen <b>A</b>"),
        ("P-NAME-09", "Very long name (500 chars)", "⚠️ unspecified max", "A × 500"),
    ],
    "phone": [
        ("P-PHONE-01", "10 digits starting with 0 (min valid)", "Valid", "0912345678"),
        ("P-PHONE-02", "11 digits starting with 0 (max valid)", "Valid", "09123456789"),
        ("P-PHONE-03", "9 digits starting with 0 (min−1)", "Invalid", "091234567"),
        ("P-PHONE-04", "12 digits starting with 0 (max+1)", "Invalid", "091234567890"),
        ("P-PHONE-05", "10 digits not starting with 0", "Invalid", "1912345678"),
        ("P-PHONE-06", "Empty string", "Invalid", '""'),
        ("P-PHONE-07", "Field omitted", "Invalid ⚠️ assumed required", "(omit phone)"),
        ("P-PHONE-08", "Contains letters", "Invalid", "09ab345678"),
        ("P-PHONE-09", "Contains separators", "Invalid", "0912-345-678"),
        ("P-PHONE-10", "International prefix +84", "Invalid", "+84912345678"),
        ("P-PHONE-11", "Leading/trailing whitespace", "Invalid", '" 0912345678"'),
        ("P-PHONE-12", "JSON null", "Invalid", "null"),
        ("P-PHONE-13", "Wrong type (number)", "Invalid", "912345678"),
        ("P-PHONE-14", "Ten zeros (format-valid, ⚠️ not a real subscriber number)", "Valid", "0000000000"),
    ],
    "shipping_address": [
        ("P-ADDR-01", "Typical Vietnamese street address", "Valid", "123 Le Loi, Q1, TP.HCM"),
        ("P-ADDR-02", "Unicode address", "Valid", "12 Nguyễn Huệ, Quận 1, TP.HCM"),
        ("P-ADDR-03", "Empty string", "Invalid ⚠️ assumed required", '""'),
        ("P-ADDR-04", "Field omitted", "Invalid ⚠️ assumed required", "(omit shipping_address)"),
        ("P-ADDR-05", "JSON null", "Invalid", "null"),
        ("P-ADDR-06", "Very long address (500 chars)", "⚠️ unspecified max", "x × 500"),
        ("P-ADDR-07", "HTML in address (stored as text)", "Valid", "123 <script>alert(1)</script>"),
    ],
    "Authorization": [
        ("P-AUTH-01", "Valid user JWT", "Valid", "Bearer <user_token>"),
        ("P-AUTH-02", "Valid admin JWT (admin updating own profile)", "Valid", "Bearer <admin_token>"),
        ("P-AUTH-03", "Header omitted", "Invalid", "(no Authorization)"),
        ("P-AUTH-04", "Empty Bearer token", "Invalid", "Bearer "),
        ("P-AUTH-05", "Malformed JWT", "Invalid", "Bearer not-a-jwt"),
        ("P-AUTH-06", "Well-formed JWT with invalid signature", "Invalid", "Bearer <tampered>"),
    ],
    "role (business rule FR-04 / SEC-06)": [
        ("P-ROLE-01", "role omitted (documented body only)", "Valid", "(omit)"),
        ("P-ROLE-02", "Client sends role=admin", "Invalid", "admin"),
        ("P-ROLE-03", "Client sends role=user", "Invalid", "user"),
    ],
    "email (business rule FR-04)": [
        ("P-EMAIL-01", "email omitted", "Valid", "(omit)"),
        ("P-EMAIL-02", "Client sends a new email", "Invalid", "hijack@example.com"),
    ],
    "request body": [
        ("P-BODY-01", "Valid JSON object + Content-Type application/json", "Valid", "{name, phone, shipping_address}"),
        ("P-BODY-02", "Empty HTTP body", "Invalid", "(empty)"),
        ("P-BODY-03", "Malformed JSON", "Invalid", "{name:"),
        ("P-BODY-04", "Undocumented extra field (not role/email)", "⚠️ unspecified", '{"nickname":"A"}'),
        ("P-BODY-05", "JSON array instead of object", "Invalid", "[{...}]"),
        ("P-BODY-06", "Content-Type text/plain", "Invalid", "text/plain"),
    ],
}

CART_VARS = [
    ("#", "Variable", "Type", "Source"),
    ("1", "id", "integer (product id)", "JSON body"),
    ("2", "quantity", "integer", "JSON body"),
    ("3", "price", "number", "JSON body"),
    ("4", "name", "string", "JSON body"),
    ("5", "Authorization", "string (JWT)", "HTTP header"),
    ("6", "cart state (same product already present)", "state", "server-side cart for the authenticated user"),
    ("7", "request body / Content-Type", "JSON object + header", "HTTP body / header"),
]

CART_DOMAINS = {
    "id": [
        ("C-ID-01", "Existing seed product id=1", "Valid", "1"),
        ("C-ID-02", "Existing seed product id=5 (last seed)", "Valid", "5"),
        ("C-ID-03", "Zero", "Invalid", "0"),
        ("C-ID-04", "Negative", "Invalid", "-1"),
        ("C-ID-05", "Non-existent product", "Invalid", "99999"),
        ("C-ID-06", "Field omitted", "Invalid", "(omit id)"),
        ("C-ID-07", "Numeric string", "⚠️ coercion unspecified", '"1"'),
        ("C-ID-08", "JSON null", "Invalid", "null"),
        ("C-ID-09", "Non-integer (float)", "Invalid", "1.5"),
        ("C-ID-10", "Non-numeric string", "Invalid", '"abc"'),
    ],
    "quantity": [
        ("C-QTY-01", "Minimum valid quantity (FR-06)", "Valid", "1"),
        ("C-QTY-02", "Typical quantity", "Valid", "2"),
        ("C-QTY-03", "Larger typical quantity", "Valid ⚠️ no max in spec", "10"),
        ("C-QTY-04", "Zero", "Invalid", "0"),
        ("C-QTY-05", "Negative", "Invalid", "-1"),
        ("C-QTY-06", "Field omitted", "Invalid", "(omit quantity)"),
        ("C-QTY-07", "Non-integer (float)", "Invalid", "1.5"),
        ("C-QTY-08", "Numeric string", "⚠️ coercion unspecified", '"2"'),
        ("C-QTY-09", "JSON null", "Invalid", "null"),
        ("C-QTY-10", "Extremely large quantity", "⚠️ unspecified max", "999999999"),
    ],
    "price": [
        ("C-PRICE-01", "Positive price matching catalogue", "Valid", "30000000"),
        ("C-PRICE-02", "Zero", "Unspecified (FR-15 is not this API)", "0"),
        ("C-PRICE-03", "Negative", "Unspecified", "-1"),
        ("C-PRICE-04", "Field omitted", "Unspecified (not stated as required)", "(omit price)"),
        ("C-PRICE-05", "Numeric string", "⚠️ coercion unspecified", '"30000000"'),
        ("C-PRICE-06", "JSON null", "Invalid", "null"),
        ("C-PRICE-07", "Price does not match catalogue for id", "⚠️ unspecified (trust vs catalogue)", "1"),
    ],
    "name": [
        ("C-NAME-01", "Name matching catalogue for id", "Valid", "iPhone 15 Pro Max"),
        ("C-NAME-02", "Empty string", "Invalid ⚠️ assumed required", '""'),
        ("C-NAME-03", "Field omitted", "Invalid ⚠️ assumed required", "(omit name)"),
        ("C-NAME-04", "Name does not match id", "⚠️ unspecified", "Not This Product"),
        ("C-NAME-05", "Unicode name matching catalogue id=5", "Valid", "Bàn phím cơ Keychron Q1"),
    ],
    "Authorization": [
        ("C-AUTH-01", "Valid user JWT", "Valid", "Bearer <user_token>"),
        ("C-AUTH-02", "Valid admin JWT (admin may also have a cart)", "Valid", "Bearer <admin_token>"),
        ("C-AUTH-03", "Header omitted", "Invalid", "(no Authorization)"),
        ("C-AUTH-04", "Empty Bearer token", "Invalid", "Bearer "),
        ("C-AUTH-05", "Malformed JWT", "Invalid", "Bearer not-a-jwt"),
    ],
    "cart state (FR-07 merge rule)": [
        ("C-STATE-01", "Cart empty; add a product", "Valid", "empty → 1 line"),
        ("C-STATE-02", "Same product already in cart", "Valid (merge)", "qty increases, no new line"),
        ("C-STATE-03", "Different product already in cart", "Valid (new line)", "2 distinct lines"),
    ],
    "request body": [
        ("C-BODY-01", "Valid JSON object", "Valid", "{id,name,price,quantity}"),
        ("C-BODY-02", "Empty HTTP body", "Invalid", "(empty)"),
        ("C-BODY-03", "Malformed JSON", "Invalid", "{id:"),
        ("C-BODY-04", "JSON array", "Invalid", "[{...}]"),
        ("C-BODY-05", "Extra undocumented field", "⚠️ unspecified", '{"color":"red"}'),
        ("C-BODY-06", "Content-Type text/plain", "Invalid", "text/plain"),
    ],
}

ADMIN_VARS = [
    ("#", "Variable", "Type", "Source"),
    ("1", "id", "integer (user id)", "path parameter /api/admin/users/:id"),
    ("2", "Authorization", "string (JWT)", "HTTP header"),
    ("3", "caller role", "enum {admin, user}", "JWT claim (not a body field)"),
    ("4", "id vs caller relationship", "self / other", "derived: path id compared with token subject"),
    ("5", "target user existence / state", "exists / gone", "database"),
]

ADMIN_DOMAINS = {
    "id": [
        ("A-ID-01", "Existing other (non-self) user", "Valid", "<disposable_user_id>"),
        ("A-ID-02", "Caller's own user id", "Invalid (FR-19)", "<admin_self_id>"),
        ("A-ID-03", "Zero", "Invalid", "0"),
        ("A-ID-04", "Negative", "Invalid", "-1"),
        ("A-ID-05", "Non-existent user", "Invalid", "99999"),
        ("A-ID-06", "Non-numeric path", "Invalid", "abc"),
        ("A-ID-07", "Non-integer (float)", "Invalid", "1.5"),
        ("A-ID-08", "Empty path segment", "Invalid", "/api/admin/users/"),
        ("A-ID-09", "Already-deleted user id (repeat delete)", "Invalid", "<deleted_id>"),
        ("A-ID-10", "Another admin's id (not self)", "⚠️ spec forbids only self-delete", "<other_admin_id>"),
    ],
    "Authorization": [
        ("A-AUTH-01", "Valid admin JWT", "Valid", "Bearer <admin_token>"),
        ("A-AUTH-02", "Header omitted", "Invalid", "(no Authorization)"),
        ("A-AUTH-03", "Empty Bearer token", "Invalid", "Bearer "),
        ("A-AUTH-04", "Malformed JWT", "Invalid", "Bearer not-a-jwt"),
        ("A-AUTH-05", "Valid user (non-admin) JWT", "Invalid (FR-12 / SEC-03)", "Bearer <user_token>"),
    ],
    "caller role": [
        ("A-ROLE-01", "role=admin in token", "Valid", "admin"),
        ("A-ROLE-02", "role=user in token", "Invalid", "user"),
    ],
    "id vs caller": [
        ("A-REL-01", "path id ≠ authenticated user id", "Valid", "other user"),
        ("A-REL-02", "path id = authenticated user id", "Invalid", "self"),
    ],
}


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def tc(
    tid,
    module,
    title,
    fr,
    ttype,
    sds,
    preconditions,
    data_rows,
    steps,
    expected,
    endpoint,
    method,
    priority,
    input_json,
    api_name,
):
    return {
        "id": tid,
        "module": module,
        "title": title,
        "fr": fr,
        "type": ttype,
        "sds": sds,
        "preconditions": preconditions,
        "data": data_rows,
        "steps": steps,
        "expected": expected,
        "endpoint": endpoint,
        "method": method,
        "priority": priority,
        "input_json": input_json,
        "api_name": api_name,
        "file": f"tests/test-cases/{module}/{tid}.md",
    }


COMMON_PRE_USER = [
    f"EShop backend is running at {BASE}.",
    "Seed user test@eshop.com / Test1234! exists (role=user).",
    f"Obtain a user JWT via {USER_LOGIN}.",
]

COMMON_PRE_ADMIN = [
    f"EShop backend is running at {BASE}.",
    "Seed admin admin@eshop.com / Admin123! exists (role=admin).",
    f"Obtain an admin JWT via {ADMIN_LOGIN}.",
]


def profile_ok_verify():
    return (
        "HTTP 200. Profile is updated. Follow-up GET /api/users/me with the same token "
        "returns the new name, phone, and shipping_address. email and role are unchanged. "
        "⚠️ Success body is not documented in api_specification.md; SUT currently returns "
        '{"message": "Profile updated"}.'
    )


def profile_reject(reason):
    return (
        f"{ASSUME_400}. {reason} Follow-up GET /api/users/me shows name, phone, "
        "shipping_address, email, and role unchanged from the precondition snapshot."
    )


PROFILE_TCS = []

# --- valid on-points ---
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-001",
        "profile",
        "Update profile with all typical valid values (on-point)",
        "FR-04",
        "Valid",
        ["P-NAME-01", "P-PHONE-01", "P-ADDR-01", "P-AUTH-01", "P-ROLE-01", "P-EMAIL-01", "P-BODY-01"],
        COMMON_PRE_USER
        + ["Snapshot GET /api/users/me (email, role, current profile) before the PUT."],
        [
            ("Authorization", "Bearer <user_token>"),
            ("name", VALID_PROFILE["name"]),
            ("phone", VALID_PROFILE["phone"]),
            ("shipping_address", VALID_PROFILE["shipping_address"]),
        ],
        [
            "PUT /api/users/me with the test data and Content-Type application/json.",
            "Record status code and body.",
            "GET /api/users/me with the same token and compare fields.",
        ],
        profile_ok_verify(),
        "/api/users/me",
        "PUT",
        "High",
        json_input(VALID_PROFILE),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-002",
        "profile",
        "Phone at 11-digit valid maximum",
        "FR-04",
        "Valid",
        ["P-PHONE-02", "P-NAME-01", "P-ADDR-01", "P-AUTH-01"],
        COMMON_PRE_USER,
        [("name", VALID_PROFILE["name"]), ("phone", "09123456789"), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with phone=09123456789 and other fields valid.", "GET /api/users/me and assert phone persisted."],
        profile_ok_verify() + " phone equals 09123456789.",
        "/api/users/me",
        "PUT",
        "High",
        json_input(body_with(phone="09123456789")),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-003",
        "profile",
        "Unicode name and unicode address (valid combination at language edge)",
        "FR-04",
        "Valid",
        ["P-NAME-02", "P-ADDR-02", "P-PHONE-02", "P-AUTH-01"],
        COMMON_PRE_USER,
        [
            ("name", "Nguyễn Văn Á"),
            ("phone", "09123456789"),
            ("shipping_address", "12 Nguyễn Huệ, Quận 1, TP.HCM"),
        ],
        [
            "PUT /api/users/me with Unicode name, 11-digit phone, and Unicode address (two/three valid edges together).",
            "GET /api/users/me and assert exact strings persisted (no mojibake).",
        ],
        profile_ok_verify() + " Unicode strings persist exactly.",
        "/api/users/me",
        "PUT",
        "High",
        json_input(body_with(name="Nguyễn Văn Á", phone="09123456789", shipping_address="12 Nguyễn Huệ, Quận 1, TP.HCM")),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-004",
        "profile",
        "Admin updates own profile with valid fields",
        "FR-04",
        "Valid",
        ["P-AUTH-02", "P-NAME-01", "P-PHONE-01", "P-ADDR-01"],
        COMMON_PRE_ADMIN + ["Snapshot GET /api/users/me as admin."],
        [("Authorization", "Bearer <admin_token>"), ("name", "Admin Updated"), ("phone", "0912345678"), ("shipping_address", "1 Admin Street")],
        ["PUT /api/users/me as admin with valid body.", "GET /api/users/me as admin; confirm role remains admin."],
        profile_ok_verify() + " Admin role remains admin.",
        "/api/users/me",
        "PUT",
        "High",
        json_input({"name": "Admin Updated", "phone": "0912345678", "shipping_address": "1 Admin Street"}),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-005",
        "profile",
        "Phone 0000000000 is format-valid per FR-04",
        "FR-04",
        "Valid",
        ["P-PHONE-14", "P-NAME-01", "P-ADDR-01"],
        COMMON_PRE_USER,
        [("phone", "0000000000"), ("name", VALID_PROFILE["name"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with phone=0000000000.", "GET /api/users/me."],
        "HTTP 200. Phone persisted as 0000000000. ⚠️ Spec only constrains format (start 0, 10–11 digits), not a real numbering plan.",
        "/api/users/me",
        "PUT",
        "Medium",
        json_input(body_with(phone="0000000000")),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-006",
        "profile",
        "HTML in name is accepted as plain profile data",
        "FR-04",
        "Valid",
        ["P-NAME-08", "P-PHONE-01", "P-ADDR-01"],
        COMMON_PRE_USER,
        [("name", "Nguyen <b>A</b>"), ("phone", VALID_PROFILE["phone"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with HTML in name.", "GET /api/users/me and assert name stored as the submitted string."],
        "HTTP 200. name is stored as the literal string Nguyen <b>A</b>. (XSS on UI is SEC-04, not this partition.)",
        "/api/users/me",
        "PUT",
        "Medium",
        json_input(body_with(name="Nguyen <b>A</b>")),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-007",
        "profile",
        "HTML in shipping_address stored as text",
        "FR-04",
        "Valid",
        ["P-ADDR-07", "P-NAME-01", "P-PHONE-01"],
        COMMON_PRE_USER,
        [("shipping_address", "123 <script>alert(1)</script>"), ("name", VALID_PROFILE["name"]), ("phone", VALID_PROFILE["phone"])],
        ["PUT /api/users/me with HTML address.", "GET /api/users/me."],
        "HTTP 200. shipping_address persisted as the literal submitted string.",
        "/api/users/me",
        "PUT",
        "Medium",
        json_input(body_with(shipping_address="123 <script>alert(1)</script>")),
        "UpdateProfile",
    )
)

# name invalid
for tid, title, sd, value, data_label in [
    ("TC-PROFILE-008", "Reject empty name", "P-NAME-03", "", '""'),
    ("TC-PROFILE-009", "Reject whitespace-only name", "P-NAME-04", "   ", '"   "'),
    ("TC-PROFILE-011", "Reject name=null", "P-NAME-06", None, "null"),
    ("TC-PROFILE-012", "Reject name with wrong type (number)", "P-NAME-07", 12345, "12345"),
]:
    PROFILE_TCS.append(
        tc(
            tid,
            "profile",
            title,
            "FR-04",
            "Invalid",
            [sd, "P-PHONE-01", "P-ADDR-01", "P-AUTH-01"],
            COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
            [("name", data_label), ("phone", VALID_PROFILE["phone"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
            ["PUT /api/users/me with invalid name and other fields valid.", "GET /api/users/me and confirm no change."],
            profile_reject("name is not a usable non-empty string."),
            "/api/users/me",
            "PUT",
            "High",
            json_input(body_with(name=value)),
            "UpdateProfile",
        )
    )
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-010",
        "profile",
        "Reject omitted name",
        "FR-04",
        "Invalid",
        ["P-NAME-05", "P-PHONE-01", "P-ADDR-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("name", "(omitted)"), ("phone", VALID_PROFILE["phone"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with body containing only phone and shipping_address.", "GET /api/users/me."],
        profile_reject("name is missing. ⚠️ Spec lists Họ Tên as an updatable field; treated as required."),
        "/api/users/me",
        "PUT",
        "High",
        json_input(body_with(name=_OMIT)),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-013",
        "profile",
        "Very long name (500 chars) — unspecified max",
        "FR-04",
        "Valid",
        ["P-NAME-09", "P-PHONE-01", "P-ADDR-01"],
        COMMON_PRE_USER,
        [("name", "A × 500"), ("phone", VALID_PROFILE["phone"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with name of 500 'A' characters.", "GET /api/users/me."],
        "⚠️ Spec does not define a max length. Accept (200, persist all 500 chars) unless a documented limit exists. Record actual SUT behaviour.",
        "/api/users/me",
        "PUT",
        "Low",
        json_input(body_with(name="A" * 500)),
        "UpdateProfile",
    )
)

# phone invalid
phone_invalid = [
    ("TC-PROFILE-014", "Reject 9-digit phone (min−1)", "P-PHONE-03", "091234567"),
    ("TC-PROFILE-015", "Reject 12-digit phone (max+1)", "P-PHONE-04", "091234567890"),
    ("TC-PROFILE-016", "Reject phone not starting with 0", "P-PHONE-05", "1912345678"),
    ("TC-PROFILE-017", "Reject empty phone", "P-PHONE-06", ""),
    ("TC-PROFILE-019", "Reject phone containing letters", "P-PHONE-08", "09ab345678"),
    ("TC-PROFILE-020", "Reject phone with separators", "P-PHONE-09", "0912-345-678"),
    ("TC-PROFILE-021", "Reject +84 international phone", "P-PHONE-10", "+84912345678"),
    ("TC-PROFILE-022", "Reject phone with leading whitespace", "P-PHONE-11", " 0912345678"),
]
for tid, title, sd, value in phone_invalid:
    PROFILE_TCS.append(
        tc(
            tid,
            "profile",
            title,
            "FR-04",
            "Invalid",
            [sd, "P-NAME-01", "P-ADDR-01", "P-AUTH-01"],
            COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
            [("phone", fmt_val(value)), ("name", VALID_PROFILE["name"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
            [f"PUT /api/users/me with phone={fmt_val(value)} and other fields valid.", "GET /api/users/me."],
            profile_reject("phone violates FR-04 (must start with 0 and be 10–11 digits)."),
            "/api/users/me",
            "PUT",
            "High",
            json_input(body_with(phone=value)),
            "UpdateProfile",
        )
    )
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-018",
        "profile",
        "Reject omitted phone",
        "FR-04",
        "Invalid",
        ["P-PHONE-07", "P-NAME-01", "P-ADDR-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("phone", "(omitted)"), ("name", VALID_PROFILE["name"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me omitting phone.", "GET /api/users/me."],
        profile_reject("phone is missing. ⚠️ Treated as required because FR-04 lists it as an updatable field."),
        "/api/users/me",
        "PUT",
        "High",
        json_input(body_with(phone=_OMIT)),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-023",
        "profile",
        "Reject phone=null",
        "FR-04",
        "Invalid",
        ["P-PHONE-12", "P-NAME-01", "P-ADDR-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("phone", "null"), ("name", VALID_PROFILE["name"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with phone JSON null.", "GET /api/users/me."],
        profile_reject("phone is null."),
        "/api/users/me",
        "PUT",
        "High",
        json_input(body_with(phone=None)),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-024",
        "profile",
        "Reject phone with wrong type (number)",
        "FR-04",
        "Invalid",
        ["P-PHONE-13", "P-NAME-01", "P-ADDR-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("phone", "912345678 (number)"), ("name", VALID_PROFILE["name"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with phone as JSON number 912345678.", "GET /api/users/me."],
        profile_reject("phone is not a digit string starting with 0."),
        "/api/users/me",
        "PUT",
        "Medium",
        json_input(body_with(phone=912345678)),
        "UpdateProfile",
    )
)

# address invalid
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-025",
        "profile",
        "Reject empty shipping_address",
        "FR-04",
        "Invalid",
        ["P-ADDR-03", "P-NAME-01", "P-PHONE-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("shipping_address", '""'), ("name", VALID_PROFILE["name"]), ("phone", VALID_PROFILE["phone"])],
        ["PUT /api/users/me with empty shipping_address.", "GET /api/users/me."],
        profile_reject("shipping_address is empty. ⚠️ Spec does not say required; treated as required because it is an updatable default address."),
        "/api/users/me",
        "PUT",
        "Medium",
        json_input(body_with(shipping_address="")),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-026",
        "profile",
        "Reject omitted shipping_address",
        "FR-04",
        "Invalid",
        ["P-ADDR-04", "P-NAME-01", "P-PHONE-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("shipping_address", "(omitted)"), ("name", VALID_PROFILE["name"]), ("phone", VALID_PROFILE["phone"])],
        ["PUT /api/users/me omitting shipping_address.", "GET /api/users/me."],
        profile_reject("shipping_address is missing. ⚠️ Assumed required."),
        "/api/users/me",
        "PUT",
        "Medium",
        json_input(body_with(shipping_address=_OMIT)),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-027",
        "profile",
        "Reject shipping_address=null",
        "FR-04",
        "Invalid",
        ["P-ADDR-05", "P-NAME-01", "P-PHONE-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("shipping_address", "null"), ("name", VALID_PROFILE["name"]), ("phone", VALID_PROFILE["phone"])],
        ["PUT /api/users/me with shipping_address JSON null.", "GET /api/users/me."],
        profile_reject("shipping_address is null."),
        "/api/users/me",
        "PUT",
        "Medium",
        json_input(body_with(shipping_address=None)),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-028",
        "profile",
        "Very long shipping_address (500 chars) — unspecified max",
        "FR-04",
        "Valid",
        ["P-ADDR-06", "P-NAME-01", "P-PHONE-01"],
        COMMON_PRE_USER,
        [("shipping_address", "x × 500"), ("name", VALID_PROFILE["name"]), ("phone", VALID_PROFILE["phone"])],
        ["PUT /api/users/me with 500-character address.", "GET /api/users/me."],
        "⚠️ Spec does not define a max length. Accept (200, persist) unless a documented limit exists.",
        "/api/users/me",
        "PUT",
        "Low",
        json_input(body_with(shipping_address="x" * 500)),
        "UpdateProfile",
    )
)

# auth
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-029",
        "profile",
        "Reject update with no Authorization header",
        "FR-04",
        "Invalid",
        ["P-AUTH-03"],
        [f"EShop backend is running at {BASE}.", "Do not send a token."],
        [("Authorization", "(omitted)"), ("body", json.dumps(VALID_PROFILE))],
        ["PUT /api/users/me with valid JSON body and no Authorization header."],
        ASSUME_401 + ". Profile is not updated.",
        "/api/users/me",
        "PUT",
        "High",
        json.dumps({"headers": {"Content-Type": "application/json"}, "body": VALID_PROFILE}, ensure_ascii=False),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-030",
        "profile",
        "Reject empty Bearer token",
        "FR-04",
        "Invalid",
        ["P-AUTH-04"],
        COMMON_PRE_USER,
        [("Authorization", "Bearer "), ("body", json.dumps(VALID_PROFILE))],
        ["PUT /api/users/me with Authorization: Bearer <empty> and valid body."],
        ASSUME_401 + " (empty token is not a valid JWT).",
        "/api/users/me",
        "PUT",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer ", "Content-Type": "application/json"}, "body": VALID_PROFILE}, ensure_ascii=False),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-031",
        "profile",
        "Reject malformed JWT",
        "FR-04",
        "Invalid",
        ["P-AUTH-05"],
        COMMON_PRE_USER,
        [("Authorization", "Bearer not-a-jwt"), ("body", json.dumps(VALID_PROFILE))],
        ["PUT /api/users/me with Authorization: Bearer not-a-jwt and valid body."],
        ASSUME_403 + " or 401. Profile is not updated.",
        "/api/users/me",
        "PUT",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer not-a-jwt", "Content-Type": "application/json"}, "body": VALID_PROFILE}, ensure_ascii=False),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-032",
        "profile",
        "Reject JWT with invalid signature",
        "FR-04",
        "Invalid",
        ["P-AUTH-06"],
        COMMON_PRE_USER + ["Create a tampered token by altering the last character of a valid JWT."],
        [("Authorization", "Bearer <tampered_jwt>"), ("body", json.dumps(VALID_PROFILE))],
        ["PUT /api/users/me with the tampered JWT and valid body."],
        ASSUME_403 + ". Profile is not updated.",
        "/api/users/me",
        "PUT",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <tampered_jwt>", "Content-Type": "application/json"}, "body": VALID_PROFILE}, ensure_ascii=False),
        "UpdateProfile",
    )
)

# business rules
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-033",
        "profile",
        "Reject or ignore role=admin in profile body (SEC-06)",
        "FR-04",
        "Invalid",
        ["P-ROLE-02", "P-NAME-01", "P-PHONE-01", "P-ADDR-01", "P-AUTH-01"],
        COMMON_PRE_USER + ["Confirm GET /api/users/me shows role=user."],
        [
            ("name", VALID_PROFILE["name"]),
            ("phone", VALID_PROFILE["phone"]),
            ("shipping_address", VALID_PROFILE["shipping_address"]),
            ("role", "admin"),
        ],
        [
            "PUT /api/users/me with valid profile fields plus role=admin.",
            "GET /api/users/me and assert role is still user.",
        ],
        "Request is rejected (4xx) OR extra field is ignored. Either way, role remains user. "
        "If name/phone/address were applied while role was silently changed, that is a fail. FR-04 / SEC-06.",
        "/api/users/me",
        "PUT",
        "High",
        json_input({**VALID_PROFILE, "role": "admin"}),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-034",
        "profile",
        "Reject or ignore role=user when sent by client",
        "FR-04",
        "Invalid",
        ["P-ROLE-03", "P-AUTH-01"],
        COMMON_PRE_USER + ["Snapshot role from GET /api/users/me."],
        [("role", "user"), ("name", VALID_PROFILE["name"]), ("phone", VALID_PROFILE["phone"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me including role=user.", "GET /api/users/me."],
        "role is not client-writable. Profile update of documented fields may succeed, but the API must not treat role as a mutable body field. GET shows role unchanged (still user).",
        "/api/users/me",
        "PUT",
        "Medium",
        json_input({**VALID_PROFILE, "role": "user"}),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-035",
        "profile",
        "Reject email change via PUT /api/users/me",
        "FR-04",
        "Invalid",
        ["P-EMAIL-02", "P-NAME-01", "P-PHONE-01", "P-ADDR-01"],
        COMMON_PRE_USER + ["Snapshot email from GET /api/users/me (test@eshop.com)."],
        [
            ("email", "hijack@example.com"),
            ("name", VALID_PROFILE["name"]),
            ("phone", VALID_PROFILE["phone"]),
            ("shipping_address", VALID_PROFILE["shipping_address"]),
        ],
        ["PUT /api/users/me with an extra email field.", "GET /api/users/me."],
        "email remains test@eshop.com. Request is rejected or email is ignored. FR-04: email must not be changed.",
        "/api/users/me",
        "PUT",
        "High",
        json_input({**VALID_PROFILE, "email": "hijack@example.com"}),
        "UpdateProfile",
    )
)

# body shape
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-036",
        "profile",
        "Reject empty HTTP body",
        "FR-04",
        "Invalid",
        ["P-BODY-02", "P-AUTH-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("body", "(empty)")],
        ["PUT /api/users/me with Authorization and Content-Type application/json but empty body."],
        profile_reject("body is empty."),
        "/api/users/me",
        "PUT",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"}, "body": ""}, ensure_ascii=False),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-037",
        "profile",
        "Reject malformed JSON body",
        "FR-04",
        "Invalid",
        ["P-BODY-03", "P-AUTH-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("body", "{name:")],
        ["PUT /api/users/me with body `{name:` (invalid JSON)."],
        profile_reject("body is not valid JSON."),
        "/api/users/me",
        "PUT",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"}, "body": "{name:"}, ensure_ascii=False),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-038",
        "profile",
        "Undocumented extra field nickname — unspecified",
        "FR-04",
        "Valid",
        ["P-BODY-04", "P-NAME-01", "P-PHONE-01", "P-ADDR-01"],
        COMMON_PRE_USER,
        [("nickname", "A"), ("name", VALID_PROFILE["name"]), ("phone", VALID_PROFILE["phone"]), ("shipping_address", VALID_PROFILE["shipping_address"])],
        ["PUT /api/users/me with documented fields plus nickname=A.", "GET /api/users/me."],
        "⚠️ Spec does not define extra-field policy. Documented fields should update. nickname must not become a persisted column / privilege. Record actual behaviour.",
        "/api/users/me",
        "PUT",
        "Low",
        json_input({**VALID_PROFILE, "nickname": "A"}),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-039",
        "profile",
        "Reject JSON array body",
        "FR-04",
        "Invalid",
        ["P-BODY-05", "P-AUTH-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("body", json.dumps([VALID_PROFILE]))],
        ["PUT /api/users/me with a JSON array instead of an object."],
        profile_reject("body is not a JSON object."),
        "/api/users/me",
        "PUT",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"}, "body": [VALID_PROFILE]}, ensure_ascii=False),
        "UpdateProfile",
    )
)
PROFILE_TCS.append(
    tc(
        "TC-PROFILE-040",
        "profile",
        "Reject Content-Type text/plain",
        "FR-04",
        "Invalid",
        ["P-BODY-06", "P-AUTH-01"],
        COMMON_PRE_USER + ["Snapshot GET /api/users/me."],
        [("Content-Type", "text/plain"), ("body", json.dumps(VALID_PROFILE))],
        ["PUT /api/users/me with Content-Type: text/plain and a JSON-looking body."],
        profile_reject("Content-Type is not application/json. ⚠️ Spec implies JSON body."),
        "/api/users/me",
        "PUT",
        "Low",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "text/plain"}, "body": json.dumps(VALID_PROFILE)}, ensure_ascii=False),
        "UpdateProfile",
    )
)


# ---------------------------------------------------------------------------
# CART
# ---------------------------------------------------------------------------

def cart_added(extra=""):
    return (
        "HTTP 200. ⚠️ Success body is not documented; SUT currently returns "
        '{"message": "Added to cart"}. Follow-up GET /api/cart as the same user '
        "shows the line item with the submitted product id and quantity. " + extra
    )


def cart_reject(reason):
    return (
        f"{ASSUME_400}. {reason} Follow-up GET /api/cart as the same user shows "
        "the cart unchanged from the precondition snapshot."
    )


CART_PRE = COMMON_PRE_USER + [
    "GET /api/cart and snapshot line items (prefer empty cart; if not empty, record ids/qty).",
    "Seed product id=1 exists: iPhone 15 Pro Max, price 30000000.",
]

CART_TCS = []
CART_TCS.append(
    tc(
        "TC-CART-001",
        "cart",
        "Add existing product with typical valid body (on-point)",
        "FR-07",
        "Valid",
        ["C-ID-01", "C-QTY-02", "C-PRICE-01", "C-NAME-01", "C-AUTH-01", "C-STATE-01", "C-BODY-01"],
        CART_PRE,
        [("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "2")],
        [
            "POST /api/cart with the valid body and user JWT.",
            "GET /api/cart.",
        ],
        cart_added("One line for product 1 with quantity 2."),
        "/api/cart",
        "POST",
        "High",
        json_input(VALID_CART),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-002",
        "cart",
        "Add with quantity=1 (FR-06 minimum) and id=1 (valid min combination)",
        "FR-07",
        "Valid",
        ["C-QTY-01", "C-ID-01", "C-PRICE-01", "C-NAME-01", "C-AUTH-01"],
        CART_PRE,
        [("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "1")],
        ["POST /api/cart with quantity=1.", "GET /api/cart."],
        cart_added("Line for product 1 has quantity 1 (or previous+1 if merge applies)."),
        "/api/cart",
        "POST",
        "High",
        json_input(cart_with(quantity=1)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-003",
        "cart",
        "Add last seed product id=5 with matching unicode name",
        "FR-07",
        "Valid",
        ["C-ID-02", "C-NAME-05", "C-QTY-02", "C-AUTH-01"],
        CART_PRE + ["Seed product id=5 exists: Bàn phím cơ Keychron Q1, price 4000000."],
        [("id", "5"), ("name", "Bàn phím cơ Keychron Q1"), ("price", "4000000"), ("quantity", "2")],
        ["POST /api/cart for product 5.", "GET /api/cart."],
        cart_added("Line for product 5 with quantity 2 and unicode name intact."),
        "/api/cart",
        "POST",
        "High",
        json_input({"id": 5, "name": "Bàn phím cơ Keychron Q1", "price": 4000000, "quantity": 2}),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-004",
        "cart",
        "Quantity=10 (valid, no documented max)",
        "FR-07",
        "Valid",
        ["C-QTY-03", "C-ID-01", "C-AUTH-01"],
        CART_PRE,
        [("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "10")],
        ["POST /api/cart with quantity=10.", "GET /api/cart."],
        cart_added("Quantity 10 accepted. ⚠️ No upper bound in spec."),
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(quantity=10)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-005",
        "cart",
        "Admin JWT can add to the admin's own cart",
        "FR-07",
        "Valid",
        ["C-AUTH-02", "C-ID-01", "C-QTY-01"],
        COMMON_PRE_ADMIN + ["GET /api/cart as admin and snapshot."],
        [("Authorization", "Bearer <admin_token>"), ("id", "1"), ("quantity", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000")],
        ["POST /api/cart as admin with valid body.", "GET /api/cart as admin."],
        cart_added("Item appears on the admin user's cart, not on another user's cart."),
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(quantity=1)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-006",
        "cart",
        "Adding the same product again merges quantity (FR-07)",
        "FR-07",
        "Valid",
        ["C-STATE-02", "C-ID-01", "C-QTY-01", "C-AUTH-01"],
        CART_PRE
        + [
            "POST /api/cart once with id=1 quantity=1 (or ensure cart already has product 1 qty=1).",
            "GET /api/cart: exactly one line for id=1 with qty=1.",
        ],
        [("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "1")],
        [
            "POST /api/cart again with the same product id=1 and quantity=1.",
            "GET /api/cart.",
        ],
        "HTTP 200. GET /api/cart shows exactly one line for product 1 with quantity 2 (merged). A second row for the same product is a fail (FR-07).",
        "/api/cart",
        "POST",
        "High",
        json_input(cart_with(quantity=1)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-007",
        "cart",
        "Adding a different product creates a new line",
        "FR-07",
        "Valid",
        ["C-STATE-03", "C-ID-01", "C-ID-02", "C-AUTH-01"],
        CART_PRE
        + ["Ensure cart has product 1 only.", "Seed product 2 exists: Samsung Galaxy S24 Ultra, 28000000."],
        [("id", "2"), ("name", "Samsung Galaxy S24 Ultra"), ("price", "28000000"), ("quantity", "1")],
        ["POST /api/cart for product 2.", "GET /api/cart."],
        "HTTP 200. Cart contains two distinct lines (id=1 and id=2). Product 1 quantity is unchanged.",
        "/api/cart",
        "POST",
        "High",
        json_input({"id": 2, "name": "Samsung Galaxy S24 Ultra", "price": 28000000, "quantity": 1}),
        "AddToCart",
    )
)

# id invalid
for tid, title, sd, value, label in [
    ("TC-CART-008", "Reject product id=0", "C-ID-03", 0, "0"),
    ("TC-CART-009", "Reject negative product id", "C-ID-04", -1, "-1"),
    ("TC-CART-010", "Reject non-existent product id", "C-ID-05", 99999, "99999"),
    ("TC-CART-012", "Reject id=null", "C-ID-08", None, "null"),
    ("TC-CART-013", "Reject non-integer product id", "C-ID-09", 1.5, "1.5"),
    ("TC-CART-014", "Reject non-numeric product id", "C-ID-10", "abc", '"abc"'),
]:
    CART_TCS.append(
        tc(
            tid,
            "cart",
            title,
            "FR-07",
            "Invalid",
            [sd, "C-QTY-02", "C-PRICE-01", "C-NAME-01", "C-AUTH-01"],
            CART_PRE,
            [("id", label), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "2")],
            [f"POST /api/cart with id={label} and other fields valid.", "GET /api/cart."],
            cart_reject("id is not an existing product identifier."),
            "/api/cart",
            "POST",
            "High",
            json_input(cart_with(id=value)),
            "AddToCart",
        )
    )
CART_TCS.append(
    tc(
        "TC-CART-011",
        "cart",
        "Reject omitted product id",
        "FR-07",
        "Invalid",
        ["C-ID-06", "C-QTY-02", "C-AUTH-01"],
        CART_PRE,
        [("id", "(omitted)"), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "2")],
        ["POST /api/cart omitting id.", "GET /api/cart."],
        cart_reject("id is missing."),
        "/api/cart",
        "POST",
        "High",
        json_input(cart_with(id=_OMIT)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-015",
        "cart",
        "Numeric-string id — coercion unspecified",
        "FR-07",
        "Valid",
        ["C-ID-07", "C-QTY-02", "C-AUTH-01"],
        CART_PRE,
        [("id", '"1"'), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "2")],
        ['POST /api/cart with id as JSON string "1".', "GET /api/cart."],
        "⚠️ Spec type is numeric id. Preferred: reject non-number. Acceptable: coerce to 1 and add product 1. Record actual behaviour; do not add a garbage line.",
        "/api/cart",
        "POST",
        "Low",
        json_input(cart_with(id="1")),
        "AddToCart",
    )
)

# qty invalid
for tid, title, sd, value, label in [
    ("TC-CART-016", "Reject quantity=0", "C-QTY-04", 0, "0"),
    ("TC-CART-017", "Reject negative quantity", "C-QTY-05", -1, "-1"),
    ("TC-CART-019", "Reject non-integer quantity", "C-QTY-07", 1.5, "1.5"),
    ("TC-CART-021", "Reject quantity=null", "C-QTY-09", None, "null"),
]:
    CART_TCS.append(
        tc(
            tid,
            "cart",
            title,
            "FR-07",
            "Invalid",
            [sd, "C-ID-01", "C-PRICE-01", "C-NAME-01", "C-AUTH-01"],
            CART_PRE,
            [("quantity", label), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000")],
            [f"POST /api/cart with quantity={label} and other fields valid.", "GET /api/cart."],
            cart_reject("quantity must be a positive integer ≥ 1 (FR-06)."),
            "/api/cart",
            "POST",
            "High",
            json_input(cart_with(quantity=value)),
            "AddToCart",
        )
    )
CART_TCS.append(
    tc(
        "TC-CART-018",
        "cart",
        "Reject omitted quantity",
        "FR-07",
        "Invalid",
        ["C-QTY-06", "C-ID-01", "C-AUTH-01"],
        CART_PRE,
        [("quantity", "(omitted)"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000")],
        ["POST /api/cart omitting quantity.", "GET /api/cart."],
        cart_reject("quantity is missing."),
        "/api/cart",
        "POST",
        "High",
        json_input(cart_with(quantity=_OMIT)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-020",
        "cart",
        "Numeric-string quantity — coercion unspecified",
        "FR-07",
        "Valid",
        ["C-QTY-08", "C-ID-01", "C-AUTH-01"],
        CART_PRE,
        [("quantity", '"2"'), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000")],
        ['POST /api/cart with quantity as JSON string "2".', "GET /api/cart."],
        "⚠️ Preferred: reject non-number. Acceptable: coerce to 2. Record actual behaviour.",
        "/api/cart",
        "POST",
        "Low",
        json_input(cart_with(quantity="2")),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-022",
        "cart",
        "Extremely large quantity — unspecified max",
        "FR-07",
        "Valid",
        ["C-QTY-10", "C-ID-01", "C-AUTH-01"],
        CART_PRE,
        [("quantity", "999999999"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000")],
        ["POST /api/cart with quantity=999999999.", "GET /api/cart."],
        "⚠️ No max in spec. Accept or reject with a documented limit. Must not crash the server or overflow into a negative/zero qty.",
        "/api/cart",
        "POST",
        "Low",
        json_input(cart_with(quantity=999999999)),
        "AddToCart",
    )
)

# price
CART_TCS.append(
    tc(
        "TC-CART-023",
        "cart",
        "Reject price=0",
        "FR-07",
        "Invalid",
        ["C-PRICE-02", "C-ID-01", "C-QTY-02", "C-AUTH-01"],
        CART_PRE,
        [("price", "0"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("quantity", "2")],
        ["POST /api/cart with price=0.", "GET /api/cart."],
        cart_reject("price must be positive. ⚠️ Inferred from FR-15 product price > 0; cart API does not restate this."),
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(price=0)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-024",
        "cart",
        "Reject negative price",
        "FR-07",
        "Invalid",
        ["C-PRICE-03", "C-ID-01", "C-QTY-02", "C-AUTH-01"],
        CART_PRE,
        [("price", "-1"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("quantity", "2")],
        ["POST /api/cart with price=-1.", "GET /api/cart."],
        cart_reject("price is negative."),
        "/api/cart",
        "POST",
        "High",
        json_input(cart_with(price=-1)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-025",
        "cart",
        "Reject omitted price",
        "FR-07",
        "Invalid",
        ["C-PRICE-04", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("price", "(omitted)"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("quantity", "2")],
        ["POST /api/cart omitting price.", "GET /api/cart."],
        cart_reject("price is missing. ⚠️ Assumed required because it is in the documented body."),
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(price=_OMIT)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-026",
        "cart",
        "Numeric-string price — coercion unspecified",
        "FR-07",
        "Valid",
        ["C-PRICE-05", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("price", '"30000000"'), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("quantity", "2")],
        ['POST /api/cart with price as JSON string "30000000".', "GET /api/cart."],
        "⚠️ Preferred reject or coerce to 30000000. Record actual behaviour.",
        "/api/cart",
        "POST",
        "Low",
        json_input(cart_with(price="30000000")),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-027",
        "cart",
        "Reject price=null",
        "FR-07",
        "Invalid",
        ["C-PRICE-06", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("price", "null"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("quantity", "2")],
        ["POST /api/cart with price JSON null.", "GET /api/cart."],
        cart_reject("price is null."),
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(price=None)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-028",
        "cart",
        "Client price does not match catalogue for id",
        "FR-07",
        "Invalid",
        ["C-PRICE-07", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("price", "1"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("quantity", "2")],
        ["POST /api/cart with id=1 and price=1 (catalogue is 30000000).", "GET /api/cart."],
        "⚠️ Spec does not say the cart API must ignore client price (FR-08 says that for checkout). "
        "Expected for a correct design: reject OR persist using catalogue price 30000000, not 1. "
        "Storing price=1 for iPhone 15 Pro Max is a fail against catalogue integrity.",
        "/api/cart",
        "POST",
        "High",
        json_input(cart_with(price=1)),
        "AddToCart",
    )
)

# name
CART_TCS.append(
    tc(
        "TC-CART-029",
        "cart",
        "Reject empty product name",
        "FR-07",
        "Invalid",
        ["C-NAME-02", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("name", '""'), ("id", "1"), ("price", "30000000"), ("quantity", "2")],
        ["POST /api/cart with empty name.", "GET /api/cart."],
        cart_reject("name is empty. ⚠️ Assumed required because it is in the documented body."),
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(name="")),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-030",
        "cart",
        "Reject omitted product name",
        "FR-07",
        "Invalid",
        ["C-NAME-03", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("name", "(omitted)"), ("id", "1"), ("price", "30000000"), ("quantity", "2")],
        ["POST /api/cart omitting name.", "GET /api/cart."],
        cart_reject("name is missing."),
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(name=_OMIT)),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-031",
        "cart",
        "Name does not match catalogue for id",
        "FR-07",
        "Invalid",
        ["C-NAME-04", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("name", "Not This Product"), ("id", "1"), ("price", "30000000"), ("quantity", "2")],
        ["POST /api/cart with id=1 and a mismatched name.", "GET /api/cart."],
        "⚠️ Spec does not say the server must overwrite client name. Expected: reject OR use catalogue name iPhone 15 Pro Max. Storing a spoofed name for id=1 is a fail against FR-07 line identity.",
        "/api/cart",
        "POST",
        "Medium",
        json_input(cart_with(name="Not This Product")),
        "AddToCart",
    )
)

# auth
CART_TCS.append(
    tc(
        "TC-CART-032",
        "cart",
        "Reject add-to-cart with no Authorization header",
        "FR-07",
        "Invalid",
        ["C-AUTH-03"],
        [f"EShop backend is running at {BASE}.", "Do not send a token."],
        [("Authorization", "(omitted)"), ("body", json.dumps(VALID_CART))],
        ["POST /api/cart with valid body and no Authorization header."],
        ASSUME_401 + ". No cart is created for an anonymous user.",
        "/api/cart",
        "POST",
        "High",
        json.dumps({"headers": {"Content-Type": "application/json"}, "body": VALID_CART}, ensure_ascii=False),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-033",
        "cart",
        "Reject empty Bearer token",
        "FR-07",
        "Invalid",
        ["C-AUTH-04"],
        CART_PRE,
        [("Authorization", "Bearer ")],
        ["POST /api/cart with Authorization: Bearer <empty> and valid body."],
        ASSUME_401 + ".",
        "/api/cart",
        "POST",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer ", "Content-Type": "application/json"}, "body": VALID_CART}, ensure_ascii=False),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-034",
        "cart",
        "Reject malformed JWT",
        "FR-07",
        "Invalid",
        ["C-AUTH-05"],
        CART_PRE,
        [("Authorization", "Bearer not-a-jwt")],
        ["POST /api/cart with Authorization: Bearer not-a-jwt and valid body."],
        ASSUME_403 + " or 401. Cart unchanged.",
        "/api/cart",
        "POST",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer not-a-jwt", "Content-Type": "application/json"}, "body": VALID_CART}, ensure_ascii=False),
        "AddToCart",
    )
)

# body
CART_TCS.append(
    tc(
        "TC-CART-035",
        "cart",
        "Reject empty HTTP body",
        "FR-07",
        "Invalid",
        ["C-BODY-02", "C-AUTH-01"],
        CART_PRE,
        [("body", "(empty)")],
        ["POST /api/cart with user JWT and empty body."],
        cart_reject("body is empty."),
        "/api/cart",
        "POST",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"}, "body": ""}, ensure_ascii=False),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-036",
        "cart",
        "Reject malformed JSON",
        "FR-07",
        "Invalid",
        ["C-BODY-03", "C-AUTH-01"],
        CART_PRE,
        [("body", "{id:")],
        ["POST /api/cart with body `{id:`."],
        cart_reject("body is not valid JSON."),
        "/api/cart",
        "POST",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"}, "body": "{id:"}, ensure_ascii=False),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-037",
        "cart",
        "Reject JSON array body",
        "FR-07",
        "Invalid",
        ["C-BODY-04", "C-AUTH-01"],
        CART_PRE,
        [("body", "[{...}]")],
        ["POST /api/cart with a JSON array of items instead of one object."],
        cart_reject("body is not a JSON object. (Batch add is not specified.)"),
        "/api/cart",
        "POST",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "application/json"}, "body": [VALID_CART]}, ensure_ascii=False),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-038",
        "cart",
        "Extra undocumented field color",
        "FR-07",
        "Valid",
        ["C-BODY-05", "C-ID-01", "C-QTY-02"],
        CART_PRE,
        [("color", "red"), ("id", "1"), ("name", "iPhone 15 Pro Max"), ("price", "30000000"), ("quantity", "2")],
        ["POST /api/cart with documented fields plus color=red.", "GET /api/cart."],
        "⚠️ Extra-field policy unspecified. Documented item should be added. color must not change price, id, or merge behaviour.",
        "/api/cart",
        "POST",
        "Low",
        json_input({**VALID_CART, "color": "red"}),
        "AddToCart",
    )
)
CART_TCS.append(
    tc(
        "TC-CART-039",
        "cart",
        "Reject Content-Type text/plain",
        "FR-07",
        "Invalid",
        ["C-BODY-06", "C-AUTH-01"],
        CART_PRE,
        [("Content-Type", "text/plain")],
        ["POST /api/cart with Content-Type text/plain and a JSON-looking body."],
        cart_reject("Content-Type is not application/json. ⚠️ Spec implies JSON body."),
        "/api/cart",
        "POST",
        "Low",
        json.dumps({"headers": {"Authorization": "Bearer <access_token>", "Content-Type": "text/plain"}, "body": json.dumps(VALID_CART)}, ensure_ascii=False),
        "AddToCart",
    )
)


# ---------------------------------------------------------------------------
# ADMIN DELETE USER
# ---------------------------------------------------------------------------

ADMIN_PRE = COMMON_PRE_ADMIN + [
    "Create a disposable user to delete: POST /api/register with a unique email (e.g. del.<timestamp>@example.com), password Password123!, name Disposable User.",
    "Note disposable_user_id from the register response (or GET /api/admin/users).",
    "Do not use seed test@eshop.com as the success-path victim if later tests still need that account.",
]


def admin_deleted():
    return (
        "HTTP 200. Target user is gone from GET /api/admin/users. Password is never present in any response (FR-19). "
        "⚠️ Success body is not documented; SUT currently returns "
        '{"message": "User deleted"}.'
    )


def admin_reject(reason, status_note=None):
    st = (status_note or ASSUME_400).rstrip(".")
    return (
        f"{st}. {reason} GET /api/admin/users still lists the target (if they existed). "
        "The caller's own account still exists."
    )


ADMIN_TCS = []
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-001",
        "admin-users",
        "Admin deletes another existing user (on-point)",
        "FR-19",
        "Valid",
        ["A-ID-01", "A-AUTH-01", "A-ROLE-01", "A-REL-01"],
        ADMIN_PRE,
        [("id", "<disposable_user_id>"), ("Authorization", "Bearer <admin_token>")],
        [
            "DELETE /api/admin/users/{disposable_user_id} with admin JWT.",
            "GET /api/admin/users and confirm the id is absent.",
            "Confirm response JSON does not include a password field.",
        ],
        admin_deleted(),
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<disposable_user_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-002",
        "admin-users",
        "Admin cannot delete their own account (FR-19)",
        "FR-19",
        "Invalid",
        ["A-ID-02", "A-REL-02", "A-AUTH-01", "A-ROLE-01"],
        COMMON_PRE_ADMIN + ["Resolve admin_self_id from GET /api/users/me (seed admin is id=1 on a fresh DB)."],
        [("id", "<admin_self_id>"), ("Authorization", "Bearer <admin_token>")],
        [
            "DELETE /api/admin/users/{admin_self_id} with that same admin JWT.",
            "GET /api/users/me and GET /api/admin/users: admin still exists.",
        ],
        admin_reject("FR-19 forbids deleting the currently logged-in account.", ASSUME_403 + " (or 400)."),
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<admin_self_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-003",
        "admin-users",
        "Reject user id=0",
        "FR-19",
        "Invalid",
        ["A-ID-03", "A-AUTH-01"],
        COMMON_PRE_ADMIN,
        [("id", "0")],
        ["DELETE /api/admin/users/0 with admin JWT.", "GET /api/admin/users: seed users still present."],
        admin_reject("id=0 is not a valid user identifier.", ASSUME_400 + " or " + ASSUME_404 + "."),
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": 0}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-004",
        "admin-users",
        "Reject negative user id",
        "FR-19",
        "Invalid",
        ["A-ID-04", "A-AUTH-01"],
        COMMON_PRE_ADMIN,
        [("id", "-1")],
        ["DELETE /api/admin/users/-1 with admin JWT."],
        admin_reject("Negative id is invalid.", ASSUME_400 + " or " + ASSUME_404 + "."),
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": -1}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-005",
        "admin-users",
        "Reject non-existent user id",
        "FR-19",
        "Invalid",
        ["A-ID-05", "A-AUTH-01"],
        COMMON_PRE_ADMIN,
        [("id", "99999")],
        ["DELETE /api/admin/users/99999 with admin JWT.", "GET /api/admin/users: count unchanged."],
        admin_reject("User does not exist.", ASSUME_404),
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": 99999}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-006",
        "admin-users",
        "Reject non-numeric path id",
        "FR-19",
        "Invalid",
        ["A-ID-06", "A-AUTH-01"],
        COMMON_PRE_ADMIN,
        [("id", "abc")],
        ["DELETE /api/admin/users/abc with admin JWT."],
        admin_reject("id is not an integer.", ASSUME_400 + " or " + ASSUME_404 + "."),
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "abc"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-007",
        "admin-users",
        "Reject non-integer (float) path id",
        "FR-19",
        "Invalid",
        ["A-ID-07", "A-AUTH-01"],
        COMMON_PRE_ADMIN,
        [("id", "1.5")],
        ["DELETE /api/admin/users/1.5 with admin JWT.", "Confirm seed user id=1 was not deleted (no truncation to 1)."],
        admin_reject("1.5 is not a valid integer id. Must not coerce to 1 and delete the admin.", ASSUME_400 + " or " + ASSUME_404 + "."),
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "1.5"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-008",
        "admin-users",
        "Empty path is not a valid delete",
        "FR-19",
        "Invalid",
        ["A-ID-08", "A-AUTH-01"],
        COMMON_PRE_ADMIN,
        [("id", "(empty)")],
        ["DELETE /api/admin/users/ (trailing slash, no id) with admin JWT."],
        "Not treated as a successful user delete. 404/405/400. User list unchanged.",
        "/api/admin/users/:id",
        "DELETE",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": ""}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-009",
        "admin-users",
        "Repeat DELETE of an already-deleted user",
        "FR-19",
        "Invalid",
        ["A-ID-09", "A-AUTH-01"],
        ADMIN_PRE
        + [
            "DELETE /api/admin/users/{disposable_user_id} once (must succeed).",
            "GET /api/admin/users confirms the user is gone.",
        ],
        [("id", "<deleted_id>")],
        ["DELETE /api/admin/users/{deleted_id} a second time with admin JWT."],
        admin_reject("User no longer exists; second delete is not a silent 200 success against a missing row.", ASSUME_404),
        "/api/admin/users/:id",
        "DELETE",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<deleted_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-010",
        "admin-users",
        "Admin deletes a different admin (not self) — unspecified besides self-rule",
        "FR-19",
        "Valid",
        ["A-ID-10", "A-REL-01", "A-AUTH-01"],
        COMMON_PRE_ADMIN
        + [
            "⚠️ Spec forbids only self-delete; deleting another admin is not forbidden in text.",
            "Create a second admin if the SUT allows it; otherwise skip and mark Blocked with reason.",
        ],
        [("id", "<other_admin_id>")],
        ["DELETE /api/admin/users/{other_admin_id} as the seed admin (ids differ).", "GET /api/admin/users."],
        "⚠️ If a second admin can be created: 200 and that admin is removed; caller remains. If the SUT cannot create a second admin, status=Blocked.",
        "/api/admin/users/:id",
        "DELETE",
        "Low",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<other_admin_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-011",
        "admin-users",
        "Reject delete with no Authorization header",
        "FR-19",
        "Invalid",
        ["A-AUTH-02"],
        ADMIN_PRE + ["Do not send a token."],
        [("Authorization", "(omitted)"), ("id", "<disposable_user_id>")],
        ["DELETE /api/admin/users/{disposable_user_id} with no Authorization header.", "GET /api/admin/users as admin: user still exists."],
        ASSUME_401 + ". Target user is not deleted.",
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {}, "path": {"id": "<disposable_user_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-012",
        "admin-users",
        "Reject empty Bearer token",
        "FR-19",
        "Invalid",
        ["A-AUTH-03"],
        ADMIN_PRE,
        [("Authorization", "Bearer "), ("id", "<disposable_user_id>")],
        ["DELETE /api/admin/users/{disposable_user_id} with Authorization: Bearer <empty>."],
        ASSUME_401 + ". Target user is not deleted.",
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer "}, "path": {"id": "<disposable_user_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-013",
        "admin-users",
        "Reject malformed JWT",
        "FR-19",
        "Invalid",
        ["A-AUTH-04"],
        ADMIN_PRE,
        [("Authorization", "Bearer not-a-jwt"), ("id", "<disposable_user_id>")],
        ["DELETE /api/admin/users/{disposable_user_id} with Authorization: Bearer not-a-jwt."],
        ASSUME_403 + " or 401. Target user is not deleted.",
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer not-a-jwt"}, "path": {"id": "<disposable_user_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-014",
        "admin-users",
        "Non-admin user cannot delete a user (FR-12 / SEC-03)",
        "FR-19",
        "Invalid",
        ["A-AUTH-05", "A-ROLE-02"],
        COMMON_PRE_USER
        + [
            "Create a disposable victim via register (or pick a user id that is not the caller).",
            "Do not use the caller's own id for this case (that would mix self-delete with role).",
        ],
        [("Authorization", "Bearer <user_token>"), ("id", "<other_user_id>")],
        ["DELETE /api/admin/users/{other_user_id} with the regular user JWT.", "Login as admin and GET /api/admin/users: victim still exists."],
        ASSUME_403 + ". FR-12 / SEC-03: admin APIs require role=admin, not merely a valid token. Target not deleted.",
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <user_token>"}, "path": {"id": "<other_user_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-015",
        "admin-users",
        "User JWT cannot delete self via admin route",
        "FR-19",
        "Invalid",
        ["A-AUTH-05", "A-REL-02", "A-ROLE-02"],
        COMMON_PRE_USER + ["Resolve user_self_id from GET /api/users/me."],
        [("Authorization", "Bearer <user_token>"), ("id", "<user_self_id>")],
        ["DELETE /api/admin/users/{user_self_id} with that user JWT.", "GET /api/users/me still succeeds."],
        ASSUME_403 + ". Non-admin cannot use the admin delete API, including against themselves. Account remains.",
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <user_token>"}, "path": {"id": "<user_self_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-016",
        "admin-users",
        "DELETE ignores unexpected JSON body",
        "FR-19",
        "Valid",
        ["A-ID-01", "A-AUTH-01"],
        ADMIN_PRE,
        [("id", "<disposable_user_id>"), ("body", '{"force":true}')],
        [
            "DELETE /api/admin/users/{disposable_user_id} with admin JWT and a JSON body {\"force\": true}.",
            "GET /api/admin/users.",
        ],
        "⚠️ Spec documents no body. Body must not bypass FR-19 self-delete (this id is not self) and must not change which id is deleted. User is deleted as in the on-point case.",
        "/api/admin/users/:id",
        "DELETE",
        "Low",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>", "Content-Type": "application/json"}, "path": {"id": "<disposable_user_id>"}, "body": {"force": True}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-017",
        "admin-users",
        "Query string does not change which user is deleted",
        "FR-19",
        "Valid",
        ["A-ID-01", "A-AUTH-01"],
        ADMIN_PRE + ["Know a second existing user id that must survive (e.g. seed test user)."],
        [("id", "<disposable_user_id>"), ("query", "id=<other_existing_id>")],
        [
            "DELETE /api/admin/users/{disposable_user_id}?id={other_existing_id} with admin JWT.",
            "GET /api/admin/users: disposable gone; other_existing_id still present.",
        ],
        "Only the path id is deleted. Query parameter id must not retarget the delete. ⚠️ Query behaviour unspecified; path is the specified identifier.",
        "/api/admin/users/:id",
        "DELETE",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<disposable_user_id>"}, "query": {"id": "<other_existing_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-018",
        "admin-users",
        "Very large numeric id is not found (not a crash)",
        "FR-19",
        "Invalid",
        ["A-ID-05", "A-AUTH-01"],
        COMMON_PRE_ADMIN,
        [("id", "9223372036854775807")],
        ["DELETE /api/admin/users/9223372036854775807 with admin JWT."],
        admin_reject("No such user. Server must not crash or delete an unintended row.", ASSUME_404 + " or 400."),
        "/api/admin/users/:id",
        "DELETE",
        "Low",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "9223372036854775807"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-019",
        "admin-users",
        "Self-delete still forbidden when body sends a different id",
        "FR-19",
        "Invalid",
        ["A-REL-02", "A-ID-02", "A-AUTH-01"],
        COMMON_PRE_ADMIN + ["Create a disposable user (must survive).", "Resolve admin_self_id."],
        [("path id", "<admin_self_id>"), ("body", '{"id": "<disposable_user_id>"}')],
        [
            "DELETE /api/admin/users/{admin_self_id} with JSON body claiming a different id.",
            "Confirm admin still exists and disposable user still exists (body must not retarget; self path must not succeed).",
        ],
        ASSUME_403 + " (self path). Disposable user is NOT deleted via the body. Path id is the resource identifier.",
        "/api/admin/users/:id",
        "DELETE",
        "High",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>", "Content-Type": "application/json"}, "path": {"id": "<admin_self_id>"}, "body": {"id": "<disposable_user_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)
ADMIN_TCS.append(
    tc(
        "TC-ADMINUSERS-020",
        "admin-users",
        "id as numeric string in path is the integer user (valid other user)",
        "FR-19",
        "Valid",
        ["A-ID-01", "A-AUTH-01"],
        ADMIN_PRE,
        [("id", '"<disposable_user_id>" as decimal path, e.g. /3')],
        ["DELETE /api/admin/users/{disposable_user_id} using the decimal digits of the id (normal path)."],
        admin_deleted() + " This is the canonical valid path encoding, paired with TC-ADMINUSERS-001.",
        "/api/admin/users/:id",
        "DELETE",
        "Medium",
        json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "<disposable_user_id>"}}, ensure_ascii=False),
        "AdminDeleteUser",
    )
)

# TC-ADMINUSERS-020 is too similar to 001. Replace with a better unique case:
# Actually let me keep 020 as "leading zeros in path" which is a distinct partition.

ADMIN_TCS[-1] = tc(
    "TC-ADMINUSERS-020",
    "admin-users",
    "Path id with leading zeros must not delete the coerced integer user",
    "FR-19",
    "Invalid",
    ["A-ID-06", "A-ID-07", "A-AUTH-01"],
    COMMON_PRE_ADMIN + ["Seed admin is id=1 on a fresh DB. Do not delete id=1."],
    [("id", "0001")],
    [
        "DELETE /api/admin/users/0001 with admin JWT.",
        "GET /api/users/me as admin still works; GET /api/admin/users still lists id=1.",
    ],
    "⚠️ Coercion of 0001 → 1 is dangerous (would hit self/admin). Expected: 400/404 without deleting user 1. If the SUT canonicalizes to 1, FR-19 self-delete must still block it.",
    "/api/admin/users/:id",
    "DELETE",
    "High",
    json.dumps({"headers": {"Authorization": "Bearer <admin_token>"}, "path": {"id": "0001"}}, ensure_ascii=False),
    "AdminDeleteUser",
)


ALL_TCS = PROFILE_TCS + CART_TCS + ADMIN_TCS


def render_tc(case: dict) -> str:
    data_rows = "\n".join(f"| {k} | {v} |" for k, v in case["data"])
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(case["steps"], 1))
    pres = "\n".join(f"- {p}" for p in case["preconditions"])
    return f"""# {case['id']}: {case['title']}

## Requirement ID
{case['fr']}

## Module / Test type / Technique
{case['module']} / Functional / Domain Testing – Equivalence Partitioning

## Preconditions
{pres}

## Test data
| Field | Value |
|-------|-------|
{data_rows}

## Test steps
{steps}

## Expected result
{case['expected']}

## Sub-domains covered
{', '.join(case['sds'])}

## Type
{case['type']}

## Status / Related bugs
Not Run / None
"""


def md_table(headers, rows):
    head = "| " + " | ".join(headers) + " |"
    sep = "|" + "|".join(["---"] * len(headers)) + "|"
    body = "\n".join("| " + " | ".join(r) + " |" for r in rows)
    return f"{head}\n{sep}\n{body}"


def domain_md(domains: dict) -> str:
    parts = []
    for var, rows in domains.items():
        parts.append(f"**Variable: `{var}`**\n")
        parts.append(md_table(
            ["Sub-domain ID", "Description", "Valid / Invalid", "Rep. Value"],
            [(a, b, c, d) for a, b, c, d in rows],
        ))
        parts.append("")
    return "\n".join(parts)


def summary_rows(cases):
    rows = []
    for c in cases:
        rows.append((
            c["id"],
            f"`{c['file']}`",
            c["title"].replace("|", "/"),
            ", ".join(c["sds"]),
            c["type"],
            c["expected"].replace("\n", " ")[:160] + ("…" if len(c["expected"]) > 160 else ""),
        ))
    return rows


def covered_sds(cases):
    s = set()
    for c in cases:
        s.update(c["sds"])
    return s


def all_sd_ids(domains):
    s = set()
    for rows in domains.values():
        for r in rows:
            s.add(r[0])
    return s


def write_report():
    p_sds = covered_sds(PROFILE_TCS)
    c_sds = covered_sds(CART_TCS)
    a_sds = covered_sds(ADMIN_TCS)
    p_missing = sorted(all_sd_ids(PROFILE_DOMAINS) - p_sds)
    c_missing = sorted(all_sd_ids(CART_DOMAINS) - c_sds)
    a_missing = sorted(all_sd_ids(ADMIN_DOMAINS) - a_sds)

    report = f"""# Domain Testing Report — FR-04, FR-07, FR-19

**Student:** 23127271  
**SUT:** EShop (`Repo/eshop-sut`) · Base URL `http://localhost:3000`  
**Technique:** Domain testing / equivalence partitioning (Skill-01)  
**Pipeline stage:** API Testing Skill — Stage 1 Domain partitions only  
**Sources:** `Repo/eshop-sut/README.md` (SRS), `Repo/eshop-sut/api_specification.md`  
**Module codes:** `PROFILE` (FR-04), `CART` (FR-07), `ADMINUSERS` (FR-19)

> Commit each test case file on a feature branch, then open a Pull Request for review before merging to main.

---

## Feature Summary

| FR | Name | Endpoint | Auth |
|----|------|----------|------|
| FR-04 | Quản lý hồ sơ cá nhân | `PUT /api/users/me` | JWT of the profile owner (`Authorization: Bearer <token>`) |
| FR-07 | Giỏ hàng | `POST /api/cart` | JWT of the cart owner |
| FR-19 | Quản lý người dùng (Admin) | `DELETE /api/admin/users/:id` | JWT **and** `role=admin` (FR-12 / SEC-03) |

### Spec rules used (not invented)

**FR-04**
- Logged-in user may update **Họ Tên**, **Số điện thoại**, **Địa chỉ giao hàng mặc định**.
- Phone: starts with `0`, **10–11 digits**.
- Email must not be changed.
- User updates only their own profile; **cannot change `role`** (also SEC-06).
- API body documented as `name`, `shipping_address`, `phone`.

**FR-07** (API surface + rules that constrain the add-to-cart resource)
- Documented body: `id`, `name`, `price`, `quantity`.
- Adding the **same product** increases quantity; it must **not** create a new line.
- Quantity is a positive integer, minimum **1** (FR-06 quantity rule, reused because FR-07 quantity is the same domain).

**FR-19 / FR-12 / SEC-02 / SEC-03**
- Admin may delete users **except the currently logged-in account**.
- `/api/admin/*` requires a valid JWT **and** `role=admin`.
- List/delete responses must **not leak passwords**.

### ⚠️ Assumptions (not stated as numbered rules in the spec)

1. Missing/empty `name`, `phone`, and `shipping_address` on PUT are invalid (fields are listed as the updatable set).
2. Validation failures use **HTTP 400**; missing token **401**; bad token / wrong role / self-delete **403**; missing resource **404**. The API spec often omits error codes.
3. Success bodies follow the SUT’s current messages (`Profile updated`, `Added to cart`, `User deleted`) but are marked unspecified in the API spec.
4. Cart `id` must refer to an existing product; client `price`/`name` should not silently spoof the catalogue (FR-08 states server-side price for checkout; cart is analogous but not explicit).
5. `name` / `shipping_address` have **no documented max length** — long-string cases record behaviour rather than a hard fail.
6. Deleting **another** admin is not forbidden in FR-19 text (only self-delete is). That case is flagged.

Oracles are **spec-based**. If the seed SUT does not validate an input, the case is still expected to fail the SUT (product defect), not the test design.

---

## FR-04 — `PUT /api/users/me` (module `PROFILE`)

### Step 1 · Input variables

{md_table(PROFILE_VARS[0], PROFILE_VARS[1:])}

### Steps 2–3 · Domains, sub-domains, representative values

{domain_md(PROFILE_DOMAINS)}

### Step 4 · Test case summary

**Count:** {len(PROFILE_TCS)} cases (`TC-PROFILE-001` … `TC-PROFILE-{len(PROFILE_TCS):03d}`)

{md_table(["TC ID", "File", "Title", "Sub-domains", "Type", "Expected Result"], summary_rows(PROFILE_TCS))}

---

## FR-07 — `POST /api/cart` (module `CART`)

### Step 1 · Input variables

{md_table(CART_VARS[0], CART_VARS[1:])}

### Steps 2–3 · Domains, sub-domains, representative values

{domain_md(CART_DOMAINS)}

### Step 4 · Test case summary

**Count:** {len(CART_TCS)} cases (`TC-CART-001` … `TC-CART-{len(CART_TCS):03d}`)

{md_table(["TC ID", "File", "Title", "Sub-domains", "Type", "Expected Result"], summary_rows(CART_TCS))}

---

## FR-19 — `DELETE /api/admin/users/:id` (module `ADMINUSERS`)

### Step 1 · Input variables

{md_table(ADMIN_VARS[0], ADMIN_VARS[1:])}

### Steps 2–3 · Domains, sub-domains, representative values

{domain_md(ADMIN_DOMAINS)}

### Step 4 · Test case summary

**Count:** {len(ADMIN_TCS)} cases (`TC-ADMINUSERS-001` … `TC-ADMINUSERS-{len(ADMIN_TCS):03d}`)

{md_table(["TC ID", "File", "Title", "Sub-domains", "Type", "Expected Result"], summary_rows(ADMIN_TCS))}

---

## Step 5 · Review & refine

### Coverage checklist

| Check | FR-04 | FR-07 | FR-19 |
|-------|-------|-------|-------|
| Every sub-domain has ≥1 TC | {"Yes" if not p_missing else "Gap: " + ", ".join(p_missing)} | {"Yes" if not c_missing else "Gap: " + ", ".join(c_missing)} | {"Yes" if not a_missing else "Gap: " + ", ".join(a_missing)} |
| Each invalid sub-domain has a dedicated off-point TC | Yes (one invalid field, others valid) | Yes | Yes (path/auth/role isolated) |
| Business rules +/− | Phone format +/−; role/email must not change | Merge same product +; new line for different product; qty ≥ 1 − | Delete other user +; self-delete −; non-admin − |
| No duplicate TCs | Distinct SD or combination per ID | Distinct SD or cart state | Distinct id/auth/relationship |
| Preconditions achievable | Seed `test@eshop.com` | Seed products 1–5 | Register disposable user; seed admin |

### Combination (API checklist)

- FR-04 `TC-PROFILE-003`: Unicode name + 11-digit phone + Unicode address (valid edges together).
- FR-07 `TC-CART-002`: `id=1` and `quantity=1` (valid minima together).

### Gaps not turned into SUP cases (out of domain-partition scope)

- **State transitions** of the cart UI (+/−, confirm-delete dialog) — Stage 1 state-transition category, not EP of `POST /api/cart`.
- **Security probes** (SQL injection in `name`/`id`, IDOR on another user’s cart, mass-assignment beyond role/email) — Stage 1 security category (SEC-01…SEC-07). Auth presence/role are included here because they are input variables of the endpoint.
- **Schema** of error envelopes — Stage 1 schema category.
- **Cascade:** deleting a user who owns orders — unspecified; not invented.
- `P-ROLE-01` / `P-EMAIL-01` / `P-BODY-01` / `C-BODY-01` / `A-ROLE-01` are covered by on-point TCs rather than extra files.

### Supplementary TCs

None required for uncovered sub-domains after review. `TC-*-SUP-NNN` is reserved for Skill-03 gap analysis / Stage 3 human extension.

---

## Artifact index

| Artifact | Path |
|----------|------|
| This report | `docs/domain-testing-report.md` |
| Per-TC files | `tests/test-cases/profile/`, `cart/`, `admin-users/` |
| API test-case sheet | `sheets/domain-partitions.csv` |
| AI audit log | `ai_audit_log.md` |

**Totals:** {len(PROFILE_TCS)} PROFILE + {len(CART_TCS)} CART + {len(ADMIN_TCS)} ADMINUSERS = **{len(ALL_TCS)}** domain-partition test cases.

`AuditStatus` is left blank in the CSV: Stage 2 (human audit VALID/INVALID/INCOMPLETE) has not been run yet.
"""
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT}")


def write_tcs():
    for case in ALL_TCS:
        path = ROOT / case["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_tc(case), encoding="utf-8")
    print(f"Wrote {len(ALL_TCS)} test case files")


def write_csv():
    SHEET.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "TestCaseID", "API", "Method", "Endpoint", "Category", "Preconditions",
        "Input", "ExpectedResult", "Priority", "Source", "AuditStatus",
        "AuditReasoning", "ActualResult", "PassFail", "BugRef", "Notes",
    ]
    with SHEET.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for c in ALL_TCS:
            w.writerow({
                "TestCaseID": c["id"],
                "API": c["api_name"],
                "Method": c["method"],
                "Endpoint": c["endpoint"],
                "Category": "DomainPartition",
                "Preconditions": " | ".join(c["preconditions"]),
                "Input": c["input_json"],
                "ExpectedResult": c["expected"],
                "Priority": c["priority"],
                "Source": "AI",
                "AuditStatus": "",
                "AuditReasoning": "",
                "ActualResult": "",
                "PassFail": "",
                "BugRef": "",
                "Notes": "Sub-domains: " + ", ".join(c["sds"]) + f" | Type={c['type']} | File={c['file']}",
            })
    print(f"Wrote {SHEET} ({len(ALL_TCS)} rows)")


def main():
    # uniqueness
    ids = [c["id"] for c in ALL_TCS]
    assert len(ids) == len(set(ids)), "Duplicate TC IDs: " + str([i for i in ids if ids.count(i) > 1])
    write_tcs()
    write_csv()
    write_report()
    print("PROFILE", len(PROFILE_TCS), "CART", len(CART_TCS), "ADMIN", len(ADMIN_TCS), "TOTAL", len(ALL_TCS))


if __name__ == "__main__":
    main()

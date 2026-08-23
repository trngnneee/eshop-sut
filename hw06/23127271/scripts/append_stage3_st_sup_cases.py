#!/usr/bin/env python3
"""Append Stage 3 human-found ST-SUP rows to state-transitions.csv (idempotent by TestCaseID)."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "sheets" / "state-transitions.csv"
TC_ROOT = ROOT / "tests" / "test-cases"

ROWS = [
    {
        "TestCaseID": "TC-PROFILE-ST-SUP-001",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04",
        "title": "Race — two PUTs with different names before any GET",
        "sm_ref": "P0 → PUT(A) ∥ PUT(B) → P?",
        "transition": "concurrent PUT race",
        "states": "P0→P?(last-write-wins)",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: Prompt quality — Stage 1 ST generator used strictly sequential PUT→GET chains; "
            "checklist section 2 calls for concurrency/race edges but the prompt never asked for parallel transitions."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login test@eshop.com. | Snapshot P0 via GET /api/users/me."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "PUT name=Race Name A (other fields FR-04-valid)",
                    "PUT name=Race Name B (immediately, no GET between)",
                    "GET /api/users/me",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Ordering of back-to-back PUTs is not specified. GET must show exactly one consistent profile: "
            "either Race Name A or Race Name B for name, not a mixed/corrupt row. email/role unchanged. "
            "Record which PUT wins (last-write-wins vs first). HTTP status not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-PROFILE-ST-SUP-002",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-02",
        "title": "Illegal transition — PUT without token after P0 snapshot",
        "sm_ref": "P0 → PUT(no auth) → P0",
        "transition": "illegal unauthenticated update",
        "states": "P0→P0",
        "type": "Illegal",
        "why": (
            "Why AI missed: Model limitation — AI ST cases tested immutables and partial chains but bundled auth "
            "failures in domain partition TC-PROFILE-029..032; no dedicated state-transition case that "
            "authenticated snapshot P0 must not advance when JWT is removed mid-flow."
        ),
        "Preconditions": "EShop at http://localhost:3000. | Login test@eshop.com. | GET P0 snapshot.",
        "Input": json.dumps(
            {
                "sequence": [
                    "PUT /api/users/me with valid body and Bearer token",
                    "PUT /api/users/me with same body but Authorization header omitted",
                    "GET with valid token",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Second PUT without JWT must not apply a new profile state (SEC-02; API spec section 2 requires token). "
            "GET after re-using valid token shows P1 from first PUT only, or P0 if first also failed — not a third value. "
            "HTTP status for unauthenticated PUT not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-PROFILE-ST-SUP-003",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04",
        "title": "Race — concurrent PUT changes name vs phone (different fields)",
        "sm_ref": "P0 → PUT(name) ∥ PUT(phone) → P?",
        "transition": "concurrent multi-field PUT race",
        "states": "P0→P?(mixed?)",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: Model limitation — SUP-001 raced the same field (name vs name); "
            "cross-field parallel PUTs can yield torn snapshots (name from A, phone from B) — "
            "checklist concurrency item not extended to multi-attribute races."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | POST /api/login test@eshop.com. | GET P0 snapshot."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "PUT name=Race Name X (phone/address FR-04-valid from example)",
                    "PUT phone=0888888888 (name/address from example) — fire immediately parallel to step 1",
                    "GET /api/users/me",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Parallel updates to different fields are not specified. GET must show one coherent profile row "
            "(not name from one request and phone from another unless last-write-wins per field). "
            "email/role unchanged. Record field-level vs request-level winner. HTTP status not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-PROFILE-ST-SUP-004",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04 / SEC-02",
        "title": "Illegal — malformed JWT PUT after valid P1 established",
        "sm_ref": "P0 → P1(valid) → PUT(malformed JWT) → P1",
        "transition": "illegal mid-flow auth",
        "states": "P1→P1",
        "type": "Illegal",
        "why": (
            "Why AI missed: Model limitation — domain TC-PROFILE-031 tests malformed JWT as a one-shot off-point; "
            "no state-transition case guards that P1 already reached must not advance when a later PUT uses Bearer not-a-jwt."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Login test@eshop.com. | PUT valid body → GET confirms P1."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "PUT /api/users/me valid body with valid token → P1",
                    "PUT /api/users/me different valid body with Authorization: Bearer not-a-jwt",
                    "GET /api/users/me with original valid token",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Second PUT with malformed JWT must not change profile state (SEC-02). "
            "GET with valid token still shows P1 from first PUT, not the second body. HTTP status not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-PROFILE-ST-SUP-005",
        "module": "profile",
        "API": "UpdateProfile",
        "Method": "PUT",
        "Endpoint": "/api/users/me",
        "fr": "FR-04",
        "title": "Partial chain — address-only then name-only (missing 2-of-3 path)",
        "sm_ref": "P0 → P(addr) → P(addr+name)",
        "transition": "address-first partial chain",
        "states": "P0→Pa→Pan",
        "type": "Legal / Unspecified",
        "why": (
            "Why AI missed: Prompt quality — ST-002 covered name→phone; ST-009 used name→phone→address order; "
            "address-only as the first partial transition was never a dedicated state path."
        ),
        "Preconditions": "EShop at http://localhost:3000. | Login test@eshop.com. | GET P0.",
        "Input": json.dumps(
            {
                "sequence": [
                    'PUT {"shipping_address":"77 Nguyen Hue, Q1"} only',
                    'PUT {"name":"Address First Name"} only',
                    "GET /api/users/me",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "If partial PUTs apply, GET shows Address First Name and 77 Nguyen Hue. "
            "phone may stay P0 or clear — not specified. email/role unchanged. Record partial-vs-replace semantics."
        ),
        "Priority": "Medium",
    },
    {
        "TestCaseID": "TC-CART-ST-SUP-001",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "title": "C_THREE — merge on line 2 (id=2), lines 1 and 3 unchanged",
        "sm_ref": "C_THREE → POST id=2 → C_THREE'",
        "transition": "merge non-first line",
        "states": "C_THREE→C_THREE'",
        "type": "Legal",
        "why": (
            "Why AI missed: Prompt quality — merge cases (ST-002, ST-004) always targeted product id=1; "
            "multi-line cart + merge on middle line was never combined (1x1 bias toward first seed product)."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Login test@eshop.com. | "
            "Cart has id=1 qty=1, id=2 qty=1, id=3 qty=1."
        ),
        "Input": json.dumps({"sequence": ["POST id=2 qty=2", "GET /api/cart"]}, ensure_ascii=False),
        "ExpectedResult": (
            "FR-07: id=2 qty=3 (1+2 merged). id=1 and id=3 each qty=1 unchanged. Still three lines. "
            "No duplicate row for id=2. Success status/body not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-CART-ST-SUP-002",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "title": "Race — two POST /api/cart same id=1 fired back-to-back from C_EMPTY",
        "sm_ref": "C_EMPTY → POST ∥ POST → C_MERGED or corrupt",
        "transition": "concurrent merge race",
        "states": "C_EMPTY→C_MERGED?",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: API characteristic + checklist gap — FR-07 merge is synchronous in spec text but "
            "in-memory cart without locking may create two lines under race; AI never generated parallel POST probes."
        ),
        "Preconditions": "EShop at http://localhost:3000. | Login test@eshop.com. | GET cart empty.",
        "Input": json.dumps(
            {
                "sequence": [
                    "Fire two POST /api/cart id=1 qty=1 as close together as possible (script/Postman parallel)",
                    "GET /api/cart",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "FR-07 requires at most one line for id=1 with qty=2 after both adds succeed. "
            "If two separate lines for id=1 appear, that violates merge. Record line count and qty. "
            "HTTP status not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-CART-ST-SUP-003",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/checkout",
        "fr": "FR-07 / FR-08",
        "title": "Failed checkout — cart stays C_MULTI (illegal empty transition)",
        "sm_ref": "C_MULTI → failed checkout → C_MULTI",
        "transition": "illegal / failed checkout",
        "states": "C_MULTI→C_MULTI",
        "type": "Illegal / Unspecified",
        "why": (
            "Why AI missed: Prompt quality — ST-011 only covered successful checkout→EMPTY (FR-08 happy path); "
            "failed checkout leaving cart intact is the negative counterpart and was omitted."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Login test@eshop.com. | Cart non-empty. | Snapshot C_MULTI."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "POST /api/checkout with invalid body (e.g. missing shipping_address or total_amount=0)",
                    "GET /api/cart",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "FR-08 clears cart only after successful checkout. On failed checkout, GET /api/cart must still "
            "show the same lines/qty as C_MULTI snapshot (cart must not transition to EMPTY). "
            "Checkout error status/body not specified — record actual."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-CART-ST-SUP-004",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07",
        "title": "C_THREE — merge on line 3 (id=3), lines 1 and 2 unchanged",
        "sm_ref": "C_THREE → POST id=3 → C_THREE'",
        "transition": "merge last line",
        "states": "C_THREE→C_THREE'",
        "type": "Legal",
        "why": (
            "Why AI missed: Prompt quality — SUP-001 fixed merge on line 2; AI never enumerated merge on "
            "line 3 in a three-line cart (complete the N-line merge matrix)."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Login test@eshop.com. | "
            "Cart has id=1 qty=1, id=2 qty=1, id=3 qty=1."
        ),
        "Input": json.dumps({"sequence": ["POST id=3 qty=4", "GET /api/cart"]}, ensure_ascii=False),
        "ExpectedResult": (
            "FR-07: id=3 qty=5 (1+4 merged). id=1 and id=2 each qty=1 unchanged. Three lines total. "
            "No duplicate row for id=3. Success status/body not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-CART-ST-SUP-005",
        "module": "cart",
        "API": "AddToCart",
        "Method": "POST",
        "Endpoint": "/api/cart",
        "fr": "FR-07 / FR-08",
        "title": "Race — POST /api/cart concurrent with POST /api/checkout on C_MULTI",
        "sm_ref": "C_MULTI → checkout ∥ add → ?",
        "transition": "concurrent checkout vs add",
        "states": "C_MULTI→C_EMPTY or C_MULTI+",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: API characteristic — FR-08 clears cart on successful checkout but says nothing "
            "about an add in flight; in-memory SUT may drop items or duplicate. AI never combined checkout with parallel POST."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Login test@eshop.com. | Cart non-empty. | Snapshot C_MULTI."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "Fire POST /api/checkout (valid body) and POST /api/cart id=1 qty=1 in parallel",
                    "GET /api/cart",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Outcome not specified. If checkout wins, cart should be empty per FR-08. "
            "If add wins after checkout, record whether new line appears. "
            "Must not show corrupt duplicate lines for same id. Record final cart and order side effects."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-ST-SUP-001",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19",
        "title": "Delete another admin account (not self) — A-ID-10 state transition",
        "sm_ref": "U_ADMIN_OTHER → U_DELETED",
        "transition": "delete other admin",
        "states": "U_ADMIN→DELETED",
        "type": "Unspecified",
        "why": (
            "Why AI missed: API characteristic — FR-19 forbids only self-delete; deleting another admin is "
            "unspecified. Domain TC-ADMINUSERS-010 exists but no state-transition lifecycle case; ST suite stopped at disposable users."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Admin JWT. | "
            "Second admin account exists (register+promote or seed) with id=A, caller id=1, A!=1."
        ),
        "Input": json.dumps({"path": {"id": "<other_admin_id>"}}, ensure_ascii=False),
        "steps": [
            "DELETE /api/admin/users/{other_admin_id} with admin JWT (not self).",
            "GET /api/admin/users.",
            "Confirm caller admin still exists.",
        ],
        "ExpectedResult": (
            "FR-19 allows deleting users other than self; whether another admin may be deleted is not specified. "
            "Record: A gone from GET /api/admin/users and caller remains, or delete rejected. "
            "Do not invent mandatory 403/200. Password never in list responses."
        ),
        "Priority": "Medium",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-ST-SUP-002",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19",
        "title": "Race — two concurrent DELETE on same disposable user id",
        "sm_ref": "U_EXISTS → DELETE ∥ DELETE → U_DELETED",
        "transition": "concurrent delete race",
        "states": "U_EXISTS→U_DELETED",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: Model limitation — checklist section 2 lists concurrency; AI ST output was strictly "
            "sequential (ST-005 chain). Parallel DELETE idempotency vs double-error is untested without human case."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Admin JWT. | Disposable user D registered."
        ),
        "Input": json.dumps(
            {"sequence": ["DELETE /api/admin/users/D twice in parallel", "GET /api/admin/users"]},
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "D must end absent from list (U_DELETED). No other user deleted. "
            "Second parallel DELETE may return error or success — not specified. "
            "List count must reflect exactly one removal of D."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-ST-SUP-003",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19 / SEC-02",
        "title": "Terminal — deleted user's old JWT on GET /api/users/me",
        "sm_ref": "U_DELETED → GET /api/users/me(old token)",
        "transition": "terminal session invalidation",
        "states": "U_DELETED→auth blocked",
        "type": "Illegal / Unspecified",
        "why": (
            "Why AI missed: API characteristic — ST-011 tests login after delete; it does not probe whether "
            "an existing JWT from before DELETE still authorizes GET /api/users/me (session invalidation unspecified)."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Register user D. | Login as D → save token T. | "
            "Admin deletes D via DELETE /api/admin/users/D."
        ),
        "Input": json.dumps(
            {"sequence": ["GET /api/users/me with token T (no re-login)"]},
            ensure_ascii=False,
        ),
        "steps": [
            "GET /api/users/me using token T captured before admin deleted D.",
        ],
        "ExpectedResult": (
            "Deleted account must not return a live profile for that user. "
            "401/403 or error expected — HTTP status not specified. Must not show another user's data (IDOR)."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-ST-SUP-004",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19",
        "title": "Illegal — delete active session user D while D holds valid JWT",
        "sm_ref": "U_EXISTS(session) → DELETE → U_DELETED; D token probe",
        "transition": "delete user with live session",
        "states": "EXISTS→DELETED",
        "type": "Legal delete / Unspecified session",
        "why": (
            "Why AI missed: Prompt quality — ST-008 lifecycle is register→list→delete; "
            "no case combined active JWT held by victim during admin DELETE (cross-endpoint session state)."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Register D. | D logged in (token T). | "
            "Admin JWT. | D visible in GET /api/admin/users."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "Admin DELETE /api/admin/users/D while D session conceptually active",
                    "GET /api/users/me with D token T",
                    "GET /api/admin/users as admin",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "D absent from admin list after DELETE (FR-19). "
            "GET /api/users/me with T must not succeed for deleted D — record status. "
            "Admin unchanged. Cascade/session rules not specified."
        ),
        "Priority": "High",
    },
    {
        "TestCaseID": "TC-ADMINUSERS-ST-SUP-005",
        "module": "admin-users",
        "API": "AdminDeleteUser",
        "Method": "DELETE",
        "Endpoint": "/api/admin/users/:id",
        "fr": "FR-19",
        "title": "Race — DELETE user D concurrent with GET /api/admin/users",
        "sm_ref": "U_EXISTS → DELETE ∥ GET list",
        "transition": "concurrent delete vs list read",
        "states": "LIST(N)→LIST(N-1)?",
        "type": "Unspecified (concurrency)",
        "why": (
            "Why AI missed: Model limitation — ST-004 tests sequential GET→DELETE→GET; "
            "parallel list read during delete may show D present or absent depending on timing — checklist concurrency gap."
        ),
        "Preconditions": (
            "EShop at http://localhost:3000. | Admin JWT. | Disposable D registered and in list."
        ),
        "Input": json.dumps(
            {
                "sequence": [
                    "Fire DELETE /api/admin/users/D and GET /api/admin/users in parallel",
                    "GET /api/admin/users after both complete",
                ]
            },
            ensure_ascii=False,
        ),
        "ExpectedResult": (
            "Final GET must show D absent (U_DELETED). Concurrent GET may or may not include D — not specified. "
            "No duplicate or partial delete of other users. Record intermediate vs final list."
        ),
        "Priority": "Medium",
    },
]


def md_body(row: dict) -> str:
    steps = row.get("steps")
    if not steps:
        steps = json.loads(row["Input"]).get("sequence", [])
    steps_md = "\n".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
    return f"""# {row['TestCaseID']}: {row['title']}

## Requirement ID
{row['fr']}

## Module / Test type / Technique
{row['module']} / Functional / State Transition Testing (human extension)

## State machine
{row['sm_ref']}

## Transition under test
{row['transition']}

## Preconditions
{chr(10).join('- ' + p.strip() for p in row['Preconditions'].split('|'))}

## Test data
| (see steps) | |

## Test steps
{steps_md}

## Expected result
{row['ExpectedResult']}

## States / transitions covered
{row['states']}

## Type
{row['type']}

## Why the AI missed this
{row['why'].replace('Why AI missed: ', '')}

## Status / Related bugs
Not Run / None
"""


def main() -> None:
    existing: set[str] = set()
    if SHEET.exists():
        with SHEET.open(encoding="utf-8", newline="") as f:
            existing = {r["TestCaseID"] for r in csv.DictReader(f)}

    to_add = [r for r in ROWS if r["TestCaseID"] not in existing]
    if not to_add:
        print(f"No new rows (all {len(ROWS)} SUP IDs already in sheet).")
        return

    for row in to_add:
        path = TC_ROOT / row["module"] / f"{row['TestCaseID']}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(md_body(row), encoding="utf-8")

    fieldnames = [
        "TestCaseID", "API", "Method", "Endpoint", "Category", "Preconditions", "Input",
        "ExpectedResult", "Priority", "Source", "AuditStatus", "AuditReasoning",
        "ActualResult", "PassFail", "BugRef", "Notes",
    ]
    rows_out: list[dict] = []
    if SHEET.exists():
        with SHEET.open(encoding="utf-8", newline="") as f:
            rows_out = list(csv.DictReader(f))

    for row in to_add:
        rows_out.append(
            {
                "TestCaseID": row["TestCaseID"],
                "API": row["API"],
                "Method": row["Method"],
                "Endpoint": row["Endpoint"],
                "Category": "StateTransition",
                "Preconditions": row["Preconditions"],
                "Input": row["Input"],
                "ExpectedResult": row["ExpectedResult"],
                "Priority": row["Priority"],
                "Source": "Human",
                "AuditStatus": "N/A",
                "AuditReasoning": row["why"],
                "ActualResult": "",
                "PassFail": "",
                "BugRef": "",
                "Notes": (
                    f"Type={row['type']} | Transition={row['transition']} | States={row['states']} | "
                    f"File=tests/test-cases/{row['module']}/{row['TestCaseID']}.md"
                ),
            }
        )

    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows_out)

    print(f"Appended {len(to_add)} rows to {SHEET} (total {len(rows_out)})")


if __name__ == "__main__":
    main()

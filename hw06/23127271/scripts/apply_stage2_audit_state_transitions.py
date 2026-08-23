#!/usr/bin/env python3
"""Stage 2 audit: label state-transition TCs VALID/INVALID/INCOMPLETE and correct oracles."""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "state-transitions.csv"
AUDIT_DOC = ROOT / "docs" / "stage2-audit-state-transitions.md"

TOKEN_PROFILE = (
    "PUT /api/users/me requires Authorization (API spec section 2). "
    "email and role must not change when documented fields update (FR-04 / SEC-06). "
    "HTTP status is not specified."
)
FR07_MERGE = (
    "FR-07: adding the same product increases quantity and must not create a new line. "
    "Success status/body for POST /api/cart is not specified."
)
FR08_EMPTY = (
    "FR-08: after successful checkout the cart is cleared. "
    "Checkout success status/body and order shape are not specified."
)
FR19_SELF = (
    "FR-19: admin must not delete the currently logged-in account. "
    "HTTP status is not specified; record whether the admin account remains in GET /api/admin/users."
)
FR19_DELETE = (
    "FR-19: admin may delete users other than self. Password must not appear in list responses. "
    "Success DELETE status/body is not specified."
)
ADMIN_AUTH = (
    "DELETE /api/admin/users/:id requires valid JWT and role=admin (API spec section 6; FR-12; SEC-02; SEC-03). "
    "Target user must still exist afterwards. HTTP status is not specified."
)
NO_RULE = (
    "The SRS and api_specification.md do not state this rule. "
    "Do not expect a particular HTTP status. Record actual behaviour."
)
OBSERVE = "Record actual SUT behaviour; do not fail against an invented status code or undocumented side effect."


def A(status, reasoning, typ, expected, title=None):
    return {
        "AuditStatus": status,
        "AuditReasoning": reasoning,
        "Type": typ,
        "ExpectedResult": expected,
        "Title": title,
    }


AUDITS = {
    "TC-PROFILE-ST-001": A(
        "VALID",
        "FR-04 allows a logged-in user to update name, phone, and shipping_address. Multi-step P0 to P1 is a valid state-transition probe. email/role immutability is spec-backed.",
        "Legal",
        "After PUT, GET /api/users/me shows the submitted name, phone, and shipping_address (P1). email and role unchanged from P0 (FR-04 / SEC-06). Success HTTP status/body not specified.",
    ),
    "TC-PROFILE-ST-002": A(
        "VALID",
        "Sequential partial PUTs test replace-vs-partial semantics which the spec leaves open. Oracle already records observe-only for omitted fields.",
        "Legal / Unspecified",
        "GET shows name=Updated Name Only and phone=0987654321 if both applied. shipping_address after partial PUTs is not specified — record P0 vs cleared vs unchanged. email/role unchanged.",
    ),
    "TC-PROFILE-ST-003": A(
        "VALID",
        "Two full PUTs with documented three-field bodies test profile snapshot overwrite. FR-04 lists all three as updatable; expecting GET to reflect the latest submitted triple is spec-aligned.",
        "Legal",
        "After the second full PUT (set B), GET /api/users/me shows set B name, phone, and shipping_address (P2). email/role unchanged. Success status/body not specified.",
    ),
    "TC-PROFILE-ST-004": A(
        "VALID",
        "Idempotent repeat of the same valid PUT is a standard state-transition edge. Oracle checks stable reads only.",
        "Legal (idempotency)",
        "Both GET calls after identical PUTs show the same profile values (P1). No drift between reads. Success status/body not specified.",
    ),
    "TC-PROFILE-ST-005": A(
        "INCOMPLETE",
        "Persistence across re-login is a reasonable probe but the spec does not define storage medium (DB vs session). Generated oracle assumed DB persistence as mandatory.",
        "Legal / Unspecified",
        "After re-login with a new token, GET /api/users/me should show P1 if the profile is persisted server-side. If values reset, record actual behaviour — persistence medium is not specified.",
    ),
    "TC-PROFILE-ST-006": A(
        "VALID",
        "FR-04: email must not be changed. Oracle allows reject-or-ignore and requires email unchanged.",
        "Legal constraint",
        "email remains test@eshop.com. Other fields may update. Request rejected or email ignored — either way email unchanged.",
    ),
    "TC-PROFILE-ST-007": A(
        "VALID",
        "FR-04 / SEC-06: clients must not change role via profile update. Oracle is spec-aligned.",
        "Legal constraint",
        "role remains user. Documented profile fields may still update. Success status/body not specified.",
    ),
    "TC-PROFILE-ST-008": A(
        "VALID",
        "FR-04 applies to any logged-in user; admin is a logged-in user. role must remain admin.",
        "Legal",
        "GET shows updated profile fields and role still admin. Success status/body not specified.",
    ),
    "TC-PROFILE-ST-009": A(
        "VALID",
        "Three sequential single-field PUTs probe partial-update chaining; oracle correctly flags unspecified semantics.",
        "Legal / Unspecified",
        "GET shows Step Name, 0909090909, and 99 Pasteur if each partial update applies. If omitted fields revert, record partial-vs-replace semantics. email/role unchanged.",
    ),
    "TC-PROFILE-ST-010": A(
        "INCOMPLETE",
        "phone=123 violates FR-04 format rule (real). Whether a rejected invalid PUT leaves P1 unchanged is not specified — generated oracle assumed rollback.",
        "Illegal input / Unspecified",
        "phone=123 is not a valid FR-04 phone. GET must not persist it as the stored phone. Whether other P1 fields remain if the PUT is rejected is not specified — record status and GET snapshot.",
    ),
    "TC-PROFILE-ST-011": A(
        "VALID",
        "FR-04: user may update only their own profile. Cross-user isolation is spec-backed.",
        "Legal (isolation)",
        "User A PUT updates A's profile only. Admin GET /api/users/me unchanged from PB0. email/role unchanged on both accounts.",
    ),
    "TC-PROFILE-ST-012": A(
        "VALID",
        "Empty JSON body is not documented. Oracle observes state unchanged or rejection without inventing mandatory 400.",
        "Unspecified / no-op",
        "GET matches P0 (no unintended wipe). Request may be rejected; if so, profile state unchanged.",
    ),
    "TC-CART-ST-001": A(
        "VALID",
        "EMPTY to one line is the base cart state transition under authenticated POST /api/cart.",
        "Legal",
        f"GET /api/cart shows exactly one line id=1 qty=1 (C_SINGLE). {FR07_MERGE.split('.')[0]}.",
    ),
    "TC-CART-ST-002": A(
        "VALID",
        "FR-07 merge when same product added again — core legal transition.",
        "Legal",
        f"GET /api/cart shows one line id=1 qty=2. No second row. {FR07_MERGE}",
    ),
    "TC-CART-ST-003": A(
        "VALID",
        "FR-07 merge applies to the same product; a different id is a separate line.",
        "Legal",
        "GET shows two lines: id=1 qty=1 unchanged, id=2 qty=1 added (C_TWO). Success status/body not specified.",
    ),
    "TC-CART-ST-004": A(
        "VALID",
        "Merge on an existing line while another line stays unchanged — FR-07 in multi-line cart.",
        "Legal",
        f"id=1 qty=3 (1+2 merged), id=2 qty=1 unchanged, two lines total. {FR07_MERGE}",
    ),
    "TC-CART-ST-005": A(
        "VALID",
        "Adding a third distinct product extends MULTI state by one line.",
        "Legal",
        "GET shows three distinct lines; prior lines unchanged except new id=3 line. Success status/body not specified.",
    ),
    "TC-CART-ST-006": A(
        "VALID",
        "Two POSTs of same id from empty must merge per FR-07, not create two rows.",
        "Legal",
        f"Exactly one line id=1 qty=2 after both POSTs. {FR07_MERGE}",
    ),
    "TC-CART-ST-007": A(
        "VALID",
        "Quantity accumulation via merge is FR-07.",
        "Legal",
        f"One line id=1 qty=8 (5+3). {FR07_MERGE}",
    ),
    "TC-CART-ST-008": A(
        "VALID",
        "Repeat POST with same id tests idempotent merge behaviour under FR-07.",
        "Legal (idempotency)",
        f"One line id=1 qty=4 (2+2). Never two rows for id=1. {FR07_MERGE}",
    ),
    "TC-CART-ST-009": A(
        "VALID",
        "Interleaved POST/GET checks observable cart consistency — no invented HTTP codes.",
        "Legal",
        "Each GET reflects all prior POSTs for this user. No undocumented reset between steps.",
    ),
    "TC-CART-ST-010": A(
        "VALID",
        "Cart is scoped to the authenticated user (JWT). Another user's cart must not show the line.",
        "Legal (isolation)",
        "Admin GET /api/cart does not contain user A's line. User A cart has the posted line.",
    ),
    "TC-CART-ST-011": A(
        "INCOMPLETE",
        "FR-08 cart-clear after successful checkout is spec-backed. Generated oracle also asserted order status pending (FR-10) and assumed checkout success shape — not required for this cart transition test.",
        "Legal (cross-endpoint FR-08)",
        FR08_EMPTY,
    ),
    "TC-CART-ST-012": A(
        "VALID",
        "After cart is empty (post-checkout per FR-08), a new POST starts a fresh SINGLE line.",
        "Legal",
        "GET shows exactly one new line id=1 qty=1. No lines from any prior non-empty cart state.",
    ),
    "TC-CART-ST-013": A(
        "INCOMPLETE",
        "Mislabelled as illegal transition. Spec has no cart qty-decrease API; POST only adds/merges. Case is an observe-only monotonic-add probe, not a specified illegal transition.",
        "Unspecified (monotonic add)",
        "POST /api/cart only adds quantity per FR-07 merge semantics. GET qty should not decrease below 5 unless a remove API exists (none in spec). Record resulting qty.",
        "POST add-only — not a specified illegal transition",
    ),
    "TC-CART-ST-014": A(
        "VALID",
        "Unequal merge operands 2+3 from empty — FR-07.",
        "Legal",
        f"One line id=1 qty=5. {FR07_MERGE}",
    ),
    "TC-CART-ST-015": A(
        "VALID",
        "Session-boundary probe; oracle already flags persistence medium as unspecified.",
        "Legal / Unspecified",
        "After re-login, GET /api/cart still shows id=1 if cart is server-persisted per user. If in-memory only, record actual — persistence medium not specified.",
    ),
    "TC-ADMINUSERS-ST-001": A(
        "VALID",
        "FR-19 legal EXISTS to DELETED for a non-self user.",
        "Legal",
        f"D absent from GET /api/admin/users; admin caller remains. Password never in responses. {FR19_DELETE}",
    ),
    "TC-ADMINUSERS-ST-002": A(
        "INCOMPLETE",
        "FR-19 self-delete prohibition is real. Generated title/oracle already avoids mandating HTTP 403 — audit confirms INCOMPLETE only because status is unspecified.",
        "Illegal",
        FR19_SELF,
    ),
    "TC-ADMINUSERS-ST-003": A(
        "INCOMPLETE",
        "Repeat DELETE on a gone user is a valid terminal-state probe. Preferring 404/4xx over silent 200 is not in the spec.",
        "Illegal repeat / Unspecified",
        "D remains absent. Second DELETE must not delete a different user or restore D. HTTP status for repeat delete is not specified — record actual.",
    ),
    "TC-ADMINUSERS-ST-004": A(
        "VALID",
        "List cardinality N to N-1 follows from a successful FR-19 delete of one other user.",
        "Legal",
        "GET count drops by exactly one; only target D removed.",
    ),
    "TC-ADMINUSERS-ST-005": A(
        "VALID",
        "Sequential delete of two disposable users — both reach DELETED terminal state.",
        "Legal",
        "Neither A nor B in GET /api/admin/users. Other seed users unchanged.",
    ),
    "TC-ADMINUSERS-ST-006": A(
        "VALID",
        "FR-12 / SEC-03: non-admin must not use admin delete API. Oracle checks target still exists without inventing HTTP 403.",
        "Illegal",
        ADMIN_AUTH,
    ),
    "TC-ADMINUSERS-ST-007": A(
        "VALID",
        "SEC-02: protected admin API requires JWT. Oracle checks no delete occurred.",
        "Illegal",
        ADMIN_AUTH,
    ),
    "TC-ADMINUSERS-ST-008": A(
        "VALID",
        "Register to EXISTS to DELETED lifecycle under FR-19.",
        "Legal",
        "R appears in list after register, absent after DELETE. Password never in list responses.",
    ),
    "TC-ADMINUSERS-ST-009": A(
        "VALID",
        "Selective delete: other seed users remain while target id=3 is removed.",
        "Legal",
        "id=1 and id=2 still listed; id=3 gone after DELETE.",
    ),
    "TC-ADMINUSERS-ST-010": A(
        "VALID",
        "Self-delete blocked (FR-19) with list stability — no collateral deletes.",
        "Illegal",
        "User list count and ids unchanged after self-delete attempt. Admin account remains.",
    ),
    "TC-ADMINUSERS-ST-011": A(
        "INCOMPLETE",
        "Deleted account should not authenticate — reasonable consequence but FR-19 does not state login behaviour; HTTP 401/403 not specified.",
        "Legal consequence / Unspecified",
        "POST /api/login with deleted user credentials must not yield a usable session for that account. HTTP status/body not specified — record actual.",
    ),
    "TC-ADMINUSERS-ST-012": A(
        "VALID",
        "Cascade delete with orders is correctly flagged unspecified; no invented requirement.",
        "Unspecified",
        "Cascade when user has orders is not specified in FR-19. Record whether delete succeeds or is blocked and effect on orders.",
    ),
    "TC-ADMINUSERS-ST-013": A(
        "INCOMPLETE",
        "DELETE body is not documented. Path :id is the specified identifier (consistent with domain TC-ADMINUSERS-019). Body override rule is inferred, not written.",
        "Unspecified / guard",
        "Path id is the documented resource identifier. Admin must not be deleted when path is self id; D must not be deleted via body alone. HTTP status not specified.",
    ),
    "TC-ADMINUSERS-ST-014": A(
        "VALID",
        "FR-19: delete user id=2 (not self). Admin id=1 must remain.",
        "Legal",
        "id=2 absent from list; admin id=1 still exists and can GET /api/users/me.",
    ),
    "TC-ADMINUSERS-ST-015": A(
        "INCOMPLETE",
        "Missing user id is not specified as invalid in FR-19. Expecting 404/4xx was invented (same as domain TC-ADMINUSERS-005 audit).",
        "Unspecified",
        "L1 equals L0 — no user removed. HTTP status for non-existent id is not specified — record actual.",
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
        text = re.sub(
            r"^# " + re.escape(tid) + r": .*$",
            f"# {tid}: {rec['Title']}",
            text,
            count=1,
            flags=re.M,
        )
    text = re.sub(
        r"## Expected result\n.*?\n\n## States / transitions covered",
        "## Expected result\n" + rec["ExpectedResult"] + "\n\n## States / transitions covered",
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
        if "Type=" in notes:
            notes = re.sub(r"Type=[^|]+", f"Type={rec['Type']}", notes)
        else:
            notes = f"Type={rec['Type']} | {notes}" if notes else f"Type={rec['Type']}"
        row["Notes"] = notes.strip(" |")
    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_audit_doc() -> None:
    counts = Counter(r["AuditStatus"] for r in AUDITS.values())
    lines = [
        "# Stage 2 — Human audit of AI state-transition cases",
        "",
        "**Rule used:** only written SRS + `api_specification.md` text. Same standard as `docs/stage2-audit.md` for domain partitions.",
        "",
        "| Label | Count |",
        "|-------|------:|",
        f"| VALID | {counts['VALID']} |",
        f"| INVALID | {counts['INVALID']} |",
        f"| INCOMPLETE | {counts['INCOMPLETE']} |",
        f"| **Total** | **{len(AUDITS)}** |",
        "",
        "## Labels",
        "",
        "| Label | Meaning in this audit |",
        "|-------|------------------------|",
        "| VALID | State transition and oracle follow a written rule. |",
        "| INVALID | Oracle invented a reject/required/status rule the spec does not state. |",
        "| INCOMPLETE | Transition is worth testing but expected result over-claimed (HTTP code, rollback, FR-10 side effect, etc.). |",
        "",
        "## Notable corrections",
        "",
        "- **`TC-CART-ST-013`:** Mislabelled illegal qty decrease — corrected to monotonic add/merge observe (no decrease API in spec).",
        "- **`TC-CART-ST-011`:** Dropped mandatory order-status assertion; kept FR-08 cart-empty oracle only.",
        "- **`TC-ADMINUSERS-ST-003` / ST-015:** Removed preferred 404/404 expectations for unspecified missing/repeat-delete behaviour.",
        "- **`TC-PROFILE-ST-010`:** Removed assumed rollback of P1 on rejected invalid phone.",
        "",
        "## Per-case table",
        "",
        "| TC ID | Audit | Corrected type | Reasoning |",
        "|-------|-------|----------------|-----------|",
    ]
    for tid in sorted(AUDITS, key=lambda x: x):
        r = AUDITS[tid]
        reason = r["AuditReasoning"].replace("|", "/")
        lines.append(f"| {tid} | {r['AuditStatus']} | {r['Type']} | {reason} |")
    lines.append("")
    AUDIT_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    st_files = {p.stem for p in TC_ROOT.rglob("TC-*-ST-*.md")}
    missing = st_files - set(AUDITS)
    extra = set(AUDITS) - st_files
    if missing or extra:
        raise SystemExit(f"missing audits {sorted(missing)} extra {sorted(extra)}")
    for tid, rec in AUDITS.items():
        patch_md(tid, rec)
    patch_csv()
    write_audit_doc()
    counts = Counter(r["AuditStatus"] for r in AUDITS.values())
    print(f"Audited {len(AUDITS)} state-transition cases")
    print(f"  VALID={counts['VALID']} INVALID={counts['INVALID']} INCOMPLETE={counts['INCOMPLETE']}")
    print(f"Wrote {AUDIT_DOC}")


if __name__ == "__main__":
    main()

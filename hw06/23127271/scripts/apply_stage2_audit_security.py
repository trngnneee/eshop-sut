#!/usr/bin/env python3
"""Stage 2 audit: label AI security TCs VALID/INVALID/INCOMPLETE and correct oracles."""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "security-tests.csv"
AUDIT_DOC = ROOT / "docs" / "stage2-audit-security.md"

NO_HTTP = "HTTP status and error body are not specified — record actual without inventing codes."
SEC05 = (
    "SEC-05: request must not cause SQL syntax errors, 500 stack traces with query text, "
    "or unauthorized data change. Record status and GET/list side effects."
)
SEC02 = f"SEC-02: protected endpoint requires a valid JWT; attack must not apply the intended change. {NO_HTTP}"
SEC04 = (
    "SEC-04: at API layer record whether payload is stored/returned as literal text without server execution; "
    "UI escaping is a manual follow-up."
)
SEC01_RESP = "SEC-01: password must not appear in response bodies (plaintext or hash). Inspect JSON and error text."


def A(status, reasoning, typ, expected, title=None):
    return {
        "AuditStatus": status,
        "AuditReasoning": reasoning,
        "Type": typ,
        "ExpectedResult": expected,
        "Title": title,
    }


AUDITS = {
    "TC-PROFILE-SEC-001": A(
        "VALID",
        "SEC-05 SQLi in documented name field. Oracle observes injection side effects without inventing HTTP codes.",
        "Security probe",
        f"{SEC05} email and role unchanged on GET /api/users/me.",
    ),
    "TC-PROFILE-SEC-002": A(
        "VALID",
        "SEC-05 UNION probe on name. Oracle is observe-only for SQL leaks.",
        "Security probe",
        SEC05,
    ),
    "TC-PROFILE-SEC-003": A(
        "VALID",
        "SEC-05 stacked DROP probe on shipping_address. Oracle correctly scoped to profile integrity.",
        "Security probe",
        f"{SEC05} User profile must remain intact on GET /api/users/me.",
    ),
    "TC-PROFILE-SEC-004": A(
        "VALID",
        "SEC-05 SQLi on phone field. Observing stored phone vs FR-04 format is a reasonable side-effect check.",
        "Security probe",
        f"{SEC05} Record stored phone; injection string must not silently pass as a valid FR-04 phone.",
    ),
    "TC-PROFILE-SEC-005": A(
        "VALID",
        "SEC-04 stored XSS probe on name. API-layer literal storage oracle matches SEC-04 testing scope.",
        "Security probe",
        f"{SEC04} role and email unchanged.",
    ),
    "TC-PROFILE-SEC-006": A(
        "VALID",
        "SEC-04 XSS event handler in shipping_address. Oracle is spec-aligned for API storage observe.",
        "Security probe",
        SEC04,
    ),
    "TC-PROFILE-SEC-007": A(
        "VALID",
        "SEC-06 explicitly forbids client role change; FR-04 repeats the same rule.",
        "Security probe",
        f"SEC-06 / FR-04: role must remain user on GET /api/users/me. Documented fields may update. {NO_HTTP}",
    ),
    "TC-PROFILE-SEC-008": A(
        "INCOMPLETE",
        "Probe is valid mass-assignment, but tagged SEC-06 (role-only per README). Password rule comes from FR-04 field list + SEC-01, not SEC-06.",
        "Security probe / mass assignment",
        f"SEC-01 / FR-04: PUT documents only name, phone, shipping_address. Password must not be overwritten "
        f"(observe via POST /api/login with original password; GET /api/users/me must not expose password). {NO_HTTP}",
    ),
    "TC-PROFILE-SEC-009": A(
        "VALID",
        "SEC-02: API spec section 2 requires JWT on PUT /api/users/me. Snapshot unchanged is the correct oracle.",
        "Security probe",
        f"{SEC02} GET /api/users/me with valid token shows snapshot profile unchanged.",
    ),
    "TC-PROFILE-SEC-010": A(
        "VALID",
        "SEC-02 tampered JWT probe. Oracle requires no profile change without inventing status codes.",
        "Security probe",
        SEC02,
    ),
    "TC-PROFILE-SEC-011": A(
        "VALID",
        "FR-04: email must not change. Oracle allows reject-or-ignore and requires email unchanged.",
        "Security probe",
        f"email remains test@eshop.com. Other fields may update. Request rejected or email ignored. {NO_HTTP}",
    ),
    "TC-PROFILE-SEC-012": A(
        "INCOMPLETE",
        "Undocumented fields are worth probing, but 'account-lockout bypass' is not a written SRS/SEC rule.",
        "Security probe / mass assignment",
        f"Undocumented fields login_attempts/locked_until must not change role or email. "
        f"Record whether they appear in GET /api/users/me. {NO_HTTP}",
    ),
    "TC-PROFILE-SEC-013": A(
        "VALID",
        "Combined SEC-05 (Auth header SQLi) and SEC-02 (invalid token) probe. Both requirements are written.",
        "Security probe",
        f"{SEC05} {SEC02}",
    ),
    "TC-PROFILE-SEC-014": A(
        "VALID",
        "SEC-04 polyglot/template literal probe. Oracle observes no server-side evaluation in JSON API.",
        "Security probe",
        f"{SEC04} No server-side template evaluation in API JSON.",
    ),
    "TC-CART-SEC-001": A(
        "VALID",
        "SEC-02: cart APIs require JWT (api_spec section 4). Expect no line added when unauthenticated.",
        "Security probe",
        f"{SEC02} GET /api/cart as authenticated user shows cart unchanged (no new line).",
    ),
    "TC-CART-SEC-002": A(
        "VALID",
        "SEC-02 malformed JWT on POST /api/cart. Oracle is spec-aligned.",
        "Security probe",
        SEC02,
    ),
    "TC-CART-SEC-003": A(
        "VALID",
        "SEC-05 SQLi in cart line name. Oracle scoped to cart POST/GET side effects.",
        "Security probe",
        f"{SEC05} Cart data must not corrupt or leak SQL errors on GET /api/cart.",
    ),
    "TC-CART-SEC-004": A(
        "VALID",
        "SEC-05 string id coercion probe. Observing parse/coerce behaviour without mandating reject is correct.",
        "Security probe",
        f"{SEC05} Record coercion behaviour on GET /api/cart; no DB error leak.",
    ),
    "TC-CART-SEC-005": A(
        "VALID",
        "SEC-04 XSS in cart name. API literal-storage oracle matches SEC-04 scope.",
        "Security probe",
        SEC04,
    ),
    "TC-CART-SEC-006": A(
        "INVALID",
        "Oracle claimed FR-07/SEC-06 requires cart POST to reject client price tampering. "
        "FR-08 mandates server-side checkout total; FR-07/example body does not forbid storing client price on add. SEC-06 is role-only on profile.",
        "Integrity observe (unspecified at cart POST)",
        "POST /api/cart example includes client price. Spec does not require cart POST to validate price against catalogue "
        f"(FR-08 applies at checkout). Record stored price on GET /api/cart. {NO_HTTP}",
    ),
    "TC-CART-SEC-007": A(
        "VALID",
        "Cross-user cart isolation is implied by per-user JWT-scoped cart. IDOR read probe is valid SEC-02 test.",
        "Security probe / IDOR",
        "User B's GET /api/cart must not return User A's cart lines.",
    ),
    "TC-CART-SEC-008": A(
        "INCOMPLETE",
        "user_id mass assignment is a valid integrity probe, but SEC-06 applies only to profile role field per README.",
        "Security probe / integrity",
        "Line must attach to JWT subject (test user), not admin via body user_id. GET /api/cart as test user — record actual.",
    ),
    "TC-CART-SEC-010": A(
        "INCOMPLETE",
        "NoSQL-style string probe is valid SEC-05 observe, but oracle assumed SQLite backend which is not in the spec.",
        "Security probe",
        f"{SEC05} Record literal storage vs parse error on GET /api/cart.",
    ),
    "TC-CART-SEC-011": A(
        "VALID",
        "IDOR-style POST with foreign user_id in body. Oracle correctly records cross-user cart binding.",
        "Security probe / IDOR",
        "Line must not appear in user C's cart unless server ignores user_id (record as finding if it does).",
    ),
    "TC-CART-SEC-012": A(
        "VALID",
        "SEC-05 SQLi + SEC-02 invalid Bearer on POST /api/cart. Combined probe is valid.",
        "Security probe",
        f"{SEC05} {SEC02}",
    ),
    "TC-ADMINUSERS-SEC-001": A(
        "VALID",
        "SEC-02 unauthenticated DELETE. Target user must remain (D still in list).",
        "Security probe",
        f"{SEC02} D still present in GET /api/admin/users as admin.",
    ),
    "TC-ADMINUSERS-SEC-002": A(
        "VALID",
        "SEC-03 / FR-12: admin DELETE requires role=admin, not merely a valid JWT.",
        "Security probe",
        f"SEC-03 / FR-12: user JWT must not delete target. D still exists in GET /api/admin/users. {NO_HTTP}",
    ),
    "TC-ADMINUSERS-SEC-003": A(
        "INCOMPLETE",
        "Self-delete rule is FR-19, not SEC-03 (caller already has admin role). Mis-tagged SEC requirement.",
        "FR-19 constraint",
        f"FR-19: logged-in admin must not be deleted. GET /api/admin/users shows admin account still present. {NO_HTTP}",
    ),
    "TC-ADMINUSERS-SEC-004": A(
        "VALID",
        "SEC-05 path SQLi OR tautology. Preventing mass delete via injection is a valid SEC-05 oracle.",
        "Security probe",
        f"{SEC05} Must not delete all users or return SQL error with query text.",
    ),
    "TC-ADMINUSERS-SEC-005": A(
        "VALID",
        "SEC-05 stacked DELETE in path id. Oracle observes parameterized parsing.",
        "Security probe",
        f"{SEC05} Seed users admin and test still exist unless path parsed as single id safely.",
    ),
    "TC-ADMINUSERS-SEC-006": A(
        "VALID",
        "SEC-01 / FR-19: admin list must not expose passwords. GET /api/admin/users is in FR-19 scope.",
        "Security probe",
        SEC01_RESP,
    ),
    "TC-ADMINUSERS-SEC-007": A(
        "VALID",
        "SEC-01 on DELETE error response for missing user. Missing-user behaviour is unspecified but password leak check is valid.",
        "Security probe",
        f"{SEC01_RESP} {NO_HTTP}",
    ),
    "TC-ADMINUSERS-SEC-008": A(
        "VALID",
        "DELETE body is undocumented; probing unexpected JSON is a valid SEC-05 observe test. Path id authoritative oracle is reasonable.",
        "Security probe",
        f"{SEC05} Path id D is authoritative; body must not widen delete scope.",
    ),
    "TC-ADMINUSERS-SEC-010": A(
        "VALID",
        "SEC-02 empty Bearer token on DELETE.",
        "Security probe",
        SEC02,
    ),
    "TC-ADMINUSERS-SEC-011": A(
        "VALID",
        "SEC-05 percent-encoded SQLi in path id.",
        "Security probe",
        f"{SEC05} Must not delete unintended users.",
    ),
    "TC-ADMINUSERS-SEC-013": A(
        "VALID",
        "SEC-01 on successful DELETE response body.",
        "Security probe",
        SEC01_RESP,
    ),
    "TC-ADMINUSERS-SEC-014": A(
        "VALID",
        "SEC-05 SQLi Bearer + SEC-02 on admin DELETE.",
        "Security probe",
        f"{SEC05} {SEC02}",
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
        r"## Expected result\n.*?\n\n## SEC coverage",
        "## Expected result\n" + rec["ExpectedResult"] + "\n\n## SEC coverage",
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
        tid = row["TestCaseID"]
        if tid not in AUDITS:
            continue
        rec = AUDITS[tid]
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
        "# Stage 2 — Human audit of AI security cases",
        "",
        "**Rule used:** written SRS + `api_specification.md` + README SEC-01..SEC-07. "
        "Same standard as `docs/stage2-audit.md`. Human SEC-SUP cases are excluded (Source=Human).",
        "",
        "| Label | Count |",
        "|-------|------:|",
        f"| VALID | {counts['VALID']} |",
        f"| INVALID | {counts['INVALID']} |",
        f"| INCOMPLETE | {counts['INCOMPLETE']} |",
        f"| **Total (AI SEC)** | **{len(AUDITS)}** |",
        "",
        "## Labels",
        "",
        "| Label | Meaning in this audit |",
        "|-------|------------------------|",
        "| VALID | Threat probe and oracle follow a written SEC/FR rule without inventing HTTP codes. |",
        "| INVALID | Oracle asserted a mandatory reject/rule the spec does not state (e.g. cart price validation via FR-07/SEC-06). |",
        "| INCOMPLETE | Probe is worth running but SEC tag or oracle over-claimed (wrong SEC mapping, undocumented side effect, implementation assumption). |",
        "",
        "## Notable corrections",
        "",
        "- **`TC-CART-SEC-006` (INVALID):** Dropped FR-07/SEC-06 mandatory price rejection; FR-08 checkout recalculation does not govern POST /api/cart storage.",
        "- **`TC-PROFILE-SEC-008` / `TC-CART-SEC-008`:** Retagged mass-assignment oracles — SEC-06 is profile `role` only per README.",
        "- **`TC-ADMINUSERS-SEC-003`:** Reframed as FR-19 self-delete, not SEC-03 role check.",
        "- **`TC-PROFILE-SEC-012`:** Removed invented account-lockout bypass expectation.",
        "- **`TC-CART-SEC-010`:** Removed SQLite backend assumption from oracle.",
        "",
        "## Per-case table",
        "",
        "| TC ID | Audit | Corrected type | Reasoning |",
        "|-------|-------|----------------|-----------|",
    ]
    for tid in sorted(AUDITS):
        r = AUDITS[tid]
        reason = r["AuditReasoning"].replace("|", "/")
        lines.append(f"| {tid} | {r['AuditStatus']} | {r['Type']} | {reason} |")
    lines.append("")
    AUDIT_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sec_files = {
        p.stem
        for p in TC_ROOT.rglob("TC-*-SEC-*.md")
        if "-SUP-" not in p.stem and re.match(r"TC-(PROFILE|CART|ADMINUSERS)-SEC-\d+$", p.stem)
    }
    missing = sec_files - set(AUDITS)
    extra = set(AUDITS) - sec_files
    if missing or extra:
        raise SystemExit(f"missing audits {sorted(missing)} extra {sorted(extra)}")
    for tid, rec in AUDITS.items():
        patch_md(tid, rec)
    patch_csv()
    write_audit_doc()
    counts = Counter(r["AuditStatus"] for r in AUDITS.values())
    print(f"Audited {len(AUDITS)} AI security cases")
    print(f"  VALID={counts['VALID']} INVALID={counts['INVALID']} INCOMPLETE={counts['INCOMPLETE']}")
    print(f"Wrote {AUDIT_DOC}")


if __name__ == "__main__":
    main()

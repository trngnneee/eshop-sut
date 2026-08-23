#!/usr/bin/env python3
"""Stage 2 audit: label AI schema-validation TCs VALID/INVALID/INCOMPLETE and correct oracles."""
from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TC_ROOT = ROOT / "tests" / "test-cases"
SHEET = ROOT / "sheets" / "schema-validation.csv"
AUDIT_DOC = ROOT / "docs" / "stage2-audit-schema.md"

NO_HTTP = "HTTP status is not specified in api_specification.md — record actual without inventing codes."


def A(status, reasoning, typ, expected, title=None):
    return {
        "AuditStatus": status,
        "AuditReasoning": reasoning,
        "Type": typ,
        "ExpectedResult": expected,
        "Title": title,
    }


AUDITS = {
    "TC-PROFILE-SCH-001": A(
        "VALID",
        "GET profile returns JSON object per REST convention; Content-Type check is standard schema probe.",
        "Schema validation",
        f"Body is a JSON object. Response Content-Type header includes application/json (or charset=utf-8 JSON body). {NO_HTTP}",
    ),
    "TC-PROFILE-SCH-002": A(
        "INCOMPLETE",
        "GET /api/users/me response fields are not listed in api_spec; oracle hedges with observe-if-absent but still opens with mandatory presence.",
        "Schema validation",
        "If name is returned on GET /api/users/me, typeof must be string (FR-04 profile field). Record if absent — GET field list not in api_spec.",
    ),
    "TC-PROFILE-SCH-003": A(
        "INCOMPLETE",
        "Same as SCH-002: phone type is inferable from PUT example but GET shape is undocumented.",
        "Schema validation",
        "If phone is returned on GET /api/users/me, typeof must be string. FR-04 phone format applies to value, not JSON type. Record if absent.",
    ),
    "TC-PROFILE-SCH-004": A(
        "INCOMPLETE",
        "shipping_address type is implied by PUT example; GET presence is not guaranteed by api_spec.",
        "Schema validation",
        "If shipping_address is returned on GET /api/users/me, typeof must be string. Record if absent — not documented on GET in api_spec.",
    ),
    "TC-PROFILE-SCH-005": A(
        "VALID",
        "FR-04: email is readable on profile and must match the logged-in account.",
        "Schema validation",
        "email is string equal to test@eshop.com (FR-04: email immutable).",
    ),
    "TC-PROFILE-SCH-006": A(
        "VALID",
        "FR-04 / SEC-06: role is readable and must remain user for the seed account.",
        "Schema validation",
        "role is string with value user (FR-04 / SEC-06 immutability context).",
    ),
    "TC-PROFILE-SCH-007": A(
        "VALID",
        "SEC-01: password and password_hash must not appear in API responses.",
        "Schema validation",
        "Response object must not contain password or password_hash (SEC-01). Other fields may exist — record keys.",
    ),
    "TC-PROFILE-SCH-008": A(
        "VALID",
        "api_spec section 2.2 documents PUT body with name, shipping_address, phone as strings.",
        "Schema validation",
        f"PUT succeeds per spec example shape (three string fields). GET reflects submitted string values. {NO_HTTP}",
    ),
    "TC-PROFILE-SCH-009": A(
        "VALID",
        "PUT success response envelope is not defined in api_spec; observe-only JSON type check is correct.",
        "Schema validation",
        f"Response body is JSON object (not array/HTML). Field names/types not documented in api_spec — record actual. {NO_HTTP}",
    ),
    "TC-PROFILE-SCH-010": A(
        "VALID",
        "Content-Type application/json is a standard schema contract check for JSON APIs.",
        "Schema validation",
        "Response Content-Type header includes application/json (or charset=utf-8 JSON body).",
    ),
    "TC-PROFILE-SCH-011": A(
        "VALID",
        "Spec example types phone as string; observe coercion without mandating reject is spec-aligned.",
        "Schema validation",
        f"Spec example types phone as string. Record whether server coerces number to string, rejects, or stores number. {NO_HTTP}",
    ),
    "TC-PROFILE-SCH-012": A(
        "VALID",
        "Partial/empty PUT body semantics are unspecified; observe response and GET field values without inventing rules.",
        "Schema validation",
        f"Response is JSON (object or documented error shape). Partial update semantics not specified — record GET field values. {NO_HTTP}",
    ),
    "TC-PROFILE-SCH-013": A(
        "VALID",
        "id type probe is observe-only when field is not documented on GET profile.",
        "Schema validation",
        "If id is returned, it must be JSON number (not string). If absent, record — not documented in api_spec GET.",
    ),
    "TC-PROFILE-SCH-014": A(
        "VALID",
        "Auth error envelope is unspecified; checking JSON-not-HTML and recording keys is a valid schema probe.",
        "Schema validation",
        f"Body must not be HTML error page with stack trace. If JSON error object, record keys (spec does not define auth error schema). {NO_HTTP}",
    ),
    "TC-CART-SCH-001": A(
        "VALID",
        "Cart is modeled as a list of line objects; JSON array root + Content-Type is a valid schema check.",
        "Schema validation",
        "Root body is JSON array (cart lines list). Response Content-Type header includes application/json (or charset=utf-8 JSON body).",
    ),
    "TC-CART-SCH-002": A(
        "VALID",
        "Empty cart as [] follows list semantics; null or {} would violate array contract.",
        "Schema validation",
        "Body equals JSON empty array [] (length 0), not null or {}.",
    ),
    "TC-CART-SCH-003": A(
        "VALID",
        "api_spec section 4.2 POST example types id as number.",
        "Schema validation",
        "Each line has id as JSON number per POST example (id:1).",
    ),
    "TC-CART-SCH-004": A(
        "VALID",
        "name is string in POST example and on stored cart lines.",
        "Schema validation",
        "name is string on every cart line object.",
    ),
    "TC-CART-SCH-005": A(
        "VALID",
        "price is number in POST example; string price would be a schema deviation.",
        "Schema validation",
        "price is JSON number on each line (not string).",
    ),
    "TC-CART-SCH-006": A(
        "VALID",
        "quantity is number in POST example.",
        "Schema validation",
        "quantity is JSON number on each line.",
    ),
    "TC-CART-SCH-007": A(
        "VALID",
        "POST success body is undocumented; observe-only JSON object check is correct.",
        "Schema validation",
        f"Response body is JSON object. Top-level fields not documented in api_spec — record names/types. {NO_HTTP}",
    ),
    "TC-CART-SCH-008": A(
        "VALID",
        "Four-field POST body matches api_spec section 4.2 example exactly.",
        "Schema validation",
        "Stored line object includes all four keys from api_spec example with matching JSON types.",
    ),
    "TC-CART-SCH-009": A(
        "VALID",
        "FR-07 merge implies one array element; checking length and numeric quantity type is schema-consistent.",
        "Schema validation",
        "Array has one object element; quantity is number reflecting merge (FR-07). id still number.",
    ),
    "TC-CART-SCH-010": A(
        "VALID",
        "Spec types price as number; observe coercion without mandating reject.",
        "Schema validation",
        f"Spec types price as number. Record coercion to number vs string storage. {NO_HTTP}",
    ),
    "TC-CART-SCH-011": A(
        "VALID",
        "Content-Type application/json is a standard schema contract check.",
        "Schema validation",
        "Response Content-Type header includes application/json (or charset=utf-8 JSON body).",
    ),
    "TC-CART-SCH-012": A(
        "VALID",
        "Malformed array root is a valid request-shape probe; observe response type without inventing status codes.",
        "Schema validation",
        f"Server rejects or ignores malformed root; response JSON or parse error — record shape. Cart unchanged on GET. {NO_HTTP}",
    ),
    "TC-CART-SCH-013": A(
        "VALID",
        "Spec types quantity as number; observe coercion behaviour.",
        "Schema validation",
        f"Spec types quantity as number. Record coercion behaviour. {NO_HTTP}",
    ),
    "TC-CART-SCH-014": A(
        "VALID",
        "Unauthenticated cart access must not return a cart array; error body shape is observe-only.",
        "Schema validation",
        f"Must not return cart array without auth. Error body schema not specified — record parseable JSON keys if any. {NO_HTTP}",
    ),
    "TC-ADMINUSERS-SCH-001": A(
        "VALID",
        "Admin user list is a collection; JSON array root + Content-Type is valid.",
        "Schema validation",
        "Root is JSON array of users. Response Content-Type header includes application/json (or charset=utf-8 JSON body).",
    ),
    "TC-ADMINUSERS-SCH-002": A(
        "VALID",
        "Each list element must be a user object, not a scalar or nested array.",
        "Schema validation",
        "Every array element is plain JSON object (user record).",
    ),
    "TC-ADMINUSERS-SCH-003": A(
        "INCOMPLETE",
        "GET /api/admin/users item schema is not defined in api_spec; id:number is inferred from register response, not list contract.",
        "Schema validation",
        "If id is returned on list items, it must be JSON number. Record if absent — list field schema not in api_spec.",
    ),
    "TC-ADMINUSERS-SCH-004": A(
        "INCOMPLETE",
        "name field on admin list items is not documented in api_spec or FR-19.",
        "Schema validation",
        "If name is returned on each user object, typeof must be string. Record if absent — not documented in api_spec.",
    ),
    "TC-ADMINUSERS-SCH-005": A(
        "VALID",
        "FR-19 admin user list implies identifiable users; email as string is a reasonable schema contract.",
        "Schema validation",
        "email is string on each user object.",
    ),
    "TC-ADMINUSERS-SCH-006": A(
        "VALID",
        "FR-12 defines user and admin roles; role as string on list items is spec-aligned.",
        "Schema validation",
        "role is string (user or admin per FR-12).",
    ),
    "TC-ADMINUSERS-SCH-007": A(
        "VALID",
        "FR-19 / SEC-01: admin list must not expose password.",
        "Schema validation",
        "No password key on any list element (FR-19 / SEC-01).",
    ),
    "TC-ADMINUSERS-SCH-008": A(
        "VALID",
        "SEC-01 extension: password_hash must not appear in list responses.",
        "Schema validation",
        "No password_hash key on any list element.",
    ),
    "TC-ADMINUSERS-SCH-009": A(
        "VALID",
        "DELETE success body is undocumented; observe-only JSON object type check is correct.",
        "Schema validation",
        f"Response body is JSON object (not HTML/array). Field schema not in api_spec — record keys/types. {NO_HTTP}",
    ),
    "TC-ADMINUSERS-SCH-010": A(
        "VALID",
        "message field on DELETE is optional and observe-only when present.",
        "Schema validation",
        "If response includes message, it is string. If absent, record — not required by written spec.",
    ),
    "TC-ADMINUSERS-SCH-011": A(
        "VALID",
        "Smoke schema check on seed data validates real list elements without inventing HTTP codes.",
        "Schema validation",
        "List length >= 2. Seed users are objects with string email and string role.",
    ),
    "TC-ADMINUSERS-SCH-013": A(
        "VALID",
        "Non-admin JWT must not receive full user array; error envelope is observe-only.",
        "Schema validation",
        f"Must not return full admin user array. Error envelope not specified — record JSON vs HTML. {NO_HTTP}",
    ),
    "TC-ADMINUSERS-SCH-012": A(
        "VALID",
        "Content-Type application/json is a standard schema contract check.",
        "Schema validation",
        "Response Content-Type header includes application/json (or charset=utf-8 JSON body).",
    ),
    "TC-ADMINUSERS-SCH-014": A(
        "VALID",
        "Post-DELETE list must remain a valid user array with consistent element types.",
        "Schema validation",
        "GET still JSON array. Deleted id absent. Remaining items retain id(number), email(string), role(string).",
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
        r"## Expected result\n.*?\n\n## Schema contract reference",
        "## Expected result\n" + rec["ExpectedResult"] + "\n\n## Schema contract reference",
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
        if row.get("Source") != "AI":
            continue
        rec = AUDITS[tid]
        row["AuditStatus"] = rec["AuditStatus"]
        row["AuditReasoning"] = rec["AuditReasoning"]
        row["ExpectedResult"] = rec["ExpectedResult"]
    with SHEET.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def write_audit_doc() -> None:
    counts = Counter(r["AuditStatus"] for r in AUDITS.values())
    lines = [
        "# Stage 2 — Human audit of AI schema-validation cases",
        "",
        "**Rule used:** written SRS + `api_specification.md` + README FR-04/07/19 and SEC-01. "
        "Human SCH-SUP cases are excluded (Source=Human).",
        "",
        "| Label | Count |",
        "|-------|------:|",
        f"| VALID | {counts['VALID']} |",
        f"| INVALID | {counts['INVALID']} |",
        f"| INCOMPLETE | {counts['INCOMPLETE']} |",
        f"| **Total (AI SCH)** | **{len(AUDITS)}** |",
        "",
        "## Labels",
        "",
        "| Label | Meaning in this audit |",
        "|-------|------------------------|",
        "| VALID | Schema probe and oracle follow documented shapes or observe-only rules without inventing HTTP codes. |",
        "| INVALID | Oracle asserted a mandatory field/type/rule the spec does not state. |",
        "| INCOMPLETE | Probe is worth running but over-claims presence or types on undocumented GET/list shapes. |",
        "",
        "## Notable corrections",
        "",
        "- **`TC-PROFILE-SCH-002`–`004`:** Reworded GET field oracles to *if returned* + record-if-absent; api_spec only documents PUT body, not GET response fields.",
        "- **`TC-ADMINUSERS-SCH-003`–`004`:** Same observe-only hedge for list item id/name — admin list schema is not in api_spec.",
        "",
        "## Per-case table",
        "",
        "| TC ID | Audit | Type | Reasoning |",
        "|-------|-------|------|-----------|",
    ]
    for tid in sorted(AUDITS):
        r = AUDITS[tid]
        reason = r["AuditReasoning"].replace("|", "/")
        lines.append(f"| {tid} | {r['AuditStatus']} | {r['Type']} | {reason} |")
    lines.append("")
    AUDIT_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sch_files = {
        p.stem
        for p in TC_ROOT.rglob("TC-*-SCH-*.md")
        if "-SUP-" not in p.stem and re.match(r"TC-(PROFILE|CART|ADMINUSERS)-SCH-\d+$", p.stem)
    }
    missing = sch_files - set(AUDITS)
    extra = set(AUDITS) - sch_files
    if missing or extra:
        raise SystemExit(f"missing audits {sorted(missing)} extra {sorted(extra)}")
    for tid, rec in AUDITS.items():
        patch_md(tid, rec)
    patch_csv()
    write_audit_doc()
    counts = Counter(r["AuditStatus"] for r in AUDITS.values())
    print(f"Audited {len(AUDITS)} AI schema cases")
    print(f"  VALID={counts['VALID']} INVALID={counts['INVALID']} INCOMPLETE={counts['INCOMPLETE']}")
    print(f"Wrote {AUDIT_DOC}")


if __name__ == "__main__":
    main()

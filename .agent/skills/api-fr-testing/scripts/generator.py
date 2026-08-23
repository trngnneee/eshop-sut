#!/usr/bin/env python3
"""
api-fr-testing generator — reference implementation of the 6-stage pipeline
(PARSE -> CLASSIFY -> GENERATE -> DEDUPE+RANK -> EMIT -> SELF-CHECK).

Input : an OpenAPI-ish spec (JSON or YAML) describing ONE FR's endpoint(s), optionally with
        `x-test-partitions`, `x-test-state-matrix`, and `x-test-security-matrix` hints.
Output: a Markdown test-case table on stdout (paste into Excel), plus a coverage report.

This is intentionally dependency-light and readable — it is the "pseudocode made runnable"
deliverable, not a production tool. Expected values ALWAYS come from the spec/hints, never
from probing the SUT (that would hide bugs).

Usage:
    python3 generator.py spec.yaml --api-prefix TC-P1 --api-name API-1
"""
import argparse, json, sys, hashlib

# ----------------------------------------------------------------------------- STAGE 1: PARSE
def load_spec(path):
    text = open(path, encoding="utf-8").read()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:
            import yaml
        except ImportError:
            sys.exit("Spec is YAML — `pip install pyyaml` or pass JSON.")
        return yaml.safe_load(text)

def parse_endpoints(spec):
    """OpenAPI paths -> [Endpoint dict]. Keeps x-test-* hints if present."""
    out = []
    for path, methods in (spec.get("paths") or {}).items():
        for method, op in methods.items():
            if method.lower() not in ("get", "post", "put", "patch", "delete"):
                continue
            out.append({
                "method": method.upper(),
                "path": path,
                "op": op,
                "auth": bool(op.get("security")) or bool(spec.get("security")),
                "partitions": op.get("x-test-partitions", {}),
                "state_matrix": op.get("x-test-state-matrix", {}),
                "sec_matrix": op.get("x-test-security-matrix", []),
                "responses": op.get("responses", {}),
            })
    return out

# -------------------------------------------------------------------------- STAGE 2: CLASSIFY
def classify_param(schema):
    """Derive a Domain from a JSON-schema-ish param/property definition."""
    return {
        "type": schema.get("type", "string"),
        "required": schema.get("required", False),
        "min": schema.get("minimum", schema.get("minLength")),
        "max": schema.get("maximum", schema.get("maxLength")),
        "enum": schema.get("enum"),
        "format": schema.get("format"),
    }

# -------------------------------------------------------------------------- STAGE 3: GENERATE
def g_partition(ep, cases):
    """G1+G2: emit valid + each invalid class from x-test-partitions hints (or a default set)."""
    for pname, part in (ep["partitions"] or {}).items():
        if pname.startswith("_"):
            continue
        for v in part.get("valid", []):
            cases.append(_case(ep, "EP-valid", pname, v, expect=200, kind="partition"))
        for inv in part.get("invalid", []):
            exp = inv.get("expect", 400) if isinstance(inv, dict) else 400
            val = inv.get("value") if isinstance(inv, dict) else inv
            cases.append(_case(ep, "EP/BVA-invalid", pname, val, expect=exp, kind="boundary"))

def g_state(ep, cases):
    """G3: full from_state x action matrix + fixture chain (expected from spec)."""
    for row in (ep["state_matrix"].get("rows", []) if ep["state_matrix"] else []):
        cases.append(_case(
            ep, "state-transition", "status",
            f"from={row['from']}", expect=row.get("expectedStatus"),
            kind="state", pre=row.get("setup", ""),
            note=f"SUT={row.get('sutStatus','?')} verdict={row.get('verdict','?')}"))

def g_security(ep, cases):
    """G4: one case per SEC row (payload + expected from the security matrix)."""
    for row in ep["sec_matrix"] or []:
        cases.append(_case(
            ep, "security", row.get("sec", "SEC"), row.get("case", ""),
            expect=row.get("expectedStatus"), kind="security",
            note="expected-FAIL" if row.get("x-sut-actual") else ""))

def g_schema(ep, cases):
    """G5: one jsonSchema assertion per declared response code."""
    for code in ep["responses"]:
        cases.append(_case(ep, "schema", "response", f"code {code}",
                           expect=_int(code), kind="schema",
                           note="jsonSchema(responseSchema) + Content-Type"))

def _int(x):
    try: return int(x)
    except Exception: return x

def _case(ep, technique, param, value, expect, kind, pre="", note=""):
    return {"method": ep["method"], "path": ep["path"], "technique": technique,
            "param": param, "value": value, "expect": expect, "kind": kind,
            "pre": pre, "note": note, "auth": ep["auth"]}

# ----------------------------------------------------------------------- STAGE 4: DEDUPE+RANK
WEIGHT = {"security": 4, "state": 3, "boundary": 2, "partition": 1, "schema": 1}
def dedupe_rank(cases):
    seen, out = set(), []
    for c in cases:
        key = hashlib.md5(f"{c['method']}{c['path']}{c['param']}{c['value']}{c['kind']}"
                          .encode()).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        c["priority"] = "P0" if WEIGHT.get(c["kind"], 1) >= 3 else ("P1" if c["kind"] == "boundary" else "P2")
        out.append(c)
    out.sort(key=lambda c: -WEIGHT.get(c["kind"], 1))
    return out

# ------------------------------------------------------------------------------ STAGE 5: EMIT
def emit_markdown(cases, prefix, api):
    hdr = "| TC-ID | API | Technique | Precondition | Method+URL | Value | Expected | Priority | Note |"
    sep = "|---|---|---|---|---|---|---|---|---|"
    rows = [hdr, sep]
    for i, c in enumerate(cases, 1):
        rows.append(f"| {prefix}-{i:03d} | {api} | {c['technique']} | {c['pre'] or '—'} | "
                    f"`{c['method']} {c['path']}` | {c['value']} | `{c['expect']}` | "
                    f"{c['priority']} | {c['note']} |")
    return "\n".join(rows)

# ------------------------------------------------------------------------- STAGE 6: SELF-CHECK
def self_check(cases, endpoints):
    kinds = {c["kind"] for c in cases}
    gaps = []
    for want in ("partition", "boundary", "security", "schema"):
        if want not in kinds:
            gaps.append(f"no {want} cases generated")
    if any(ep["state_matrix"] for ep in endpoints) and "state" not in kinds:
        gaps.append("endpoint has a state machine but no state cases")
    return gaps

# ------------------------------------------------------------------------------------- driver
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--api-prefix", default="TC-XX")
    ap.add_argument("--api-name", default="API")
    a = ap.parse_args()

    spec = load_spec(a.spec)
    endpoints = parse_endpoints(spec)          # STAGE 1
    cases = []
    for ep in endpoints:                        # STAGE 2 happens lazily inside generators
        g_partition(ep, cases)                  # STAGE 3: G1+G2
        g_state(ep, cases)                      #          G3
        g_security(ep, cases)                   #          G4
        g_schema(ep, cases)                     #          G5
    cases = dedupe_rank(cases)                  # STAGE 4
    print(emit_markdown(cases, a.api_prefix, a.api_name))  # STAGE 5
    gaps = self_check(cases, endpoints)         # STAGE 6
    print(f"\n<!-- SELF-CHECK: {len(cases)} cases. "
          f"coverage gaps: {gaps or 'none'} -> hand to human review (Phase 3/4) -->",
          file=sys.stderr)

if __name__ == "__main__":
    main()

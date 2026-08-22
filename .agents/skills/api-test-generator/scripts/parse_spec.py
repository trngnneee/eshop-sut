#!/usr/bin/env python3
"""
parse_spec.py — deterministic parser for a markdown API specification.

Looks for the common conventions used by simple hand-written API specs
(like EShop's api_specification.md):

    ### METHOD /path/{id}
    Auth: Bearer (role: admin)
    | Param | In | Type | Required | Notes |
    |-------|----|------|----------|-------|
    | id    | path | string | yes | ... |
    ```json
    { "example": "response" }
    ```

This is a best-effort convenience parser, NOT a full OpenAPI parser. If the
real spec uses a different layout, read it manually and hand-build
endpoint_model.json per references/test_case_schema.md — don't fight the
regex here.

Usage:
    python3 parse_spec.py spec.md                       # list endpoints found
    python3 parse_spec.py spec.md --endpoint "GET /api/products" --out endpoint_model.json
"""
import argparse
import json
import re
import sys

ENDPOINT_RE = re.compile(
    r"^#{2,4}\s+(GET|POST|PUT|PATCH|DELETE)\s+(\S+)\s*$", re.MULTILINE
)
AUTH_RE = re.compile(r"^\s*(?:\*\*)?Auth(?:entication)?(?:\*\*)?\s*:\s*(.+)$", re.MULTILINE | re.IGNORECASE)
PARAM_ROW_RE = re.compile(r"^\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|(.*)$")
JSON_BLOCK_RE = re.compile(r"```json\s*(.*?)```", re.DOTALL)
SEC_MENTION_RE = re.compile(r"SEC-0[1-7]")
STATE_HINT_RE = re.compile(r"\b(pending|confirmed|shipping|delivered|cancell?ed)\b", re.IGNORECASE)


def find_endpoints(text):
    """Return list of (method, path, start_offset, end_offset)."""
    matches = list(ENDPOINT_RE.finditer(text))
    spans = []
    for i, m in enumerate(matches):
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        spans.append((m.group(1).upper(), m.group(2), start, end))
    return spans


def parse_section(method, path, section_text):
    endpoint = {
        "method": method,
        "path": path,
        "auth": None,
        "role": None,
        "parameters": [],
        "example_responses": [],
        "sec_refs_mentioned": sorted(set(SEC_MENTION_RE.findall(section_text))),
        "state_machine_hint": bool(STATE_HINT_RE.search(section_text)),
        "raw_section": section_text.strip()[:4000],  # keep for manual review
    }

    auth_match = AUTH_RE.search(section_text)
    if auth_match:
        auth_line = auth_match.group(1).strip()
        endpoint["auth"] = auth_line
        role_match = re.search(r"role\s*:?\s*([a-zA-Z_]+)", auth_line, re.IGNORECASE)
        if role_match:
            endpoint["role"] = role_match.group(1)

    for line in section_text.splitlines():
        row = PARAM_ROW_RE.match(line.strip())
        if not row:
            continue
        name = row.group(1).strip()
        if name.lower() in ("param", "parameter", "field", "name", "---", ""):
            continue
        if set(name) <= {"-"}:
            continue
        endpoint["parameters"].append(
            {
                "name": name,
                "in": row.group(2).strip(),
                "type": row.group(3).strip(),
                "required": row.group(4).strip(),
                "notes": row.group(5).strip(" |"),
            }
        )

    for block in JSON_BLOCK_RE.findall(section_text):
        try:
            endpoint["example_responses"].append(json.loads(block))
        except json.JSONDecodeError:
            endpoint["example_responses"].append({"_unparsed_example": block.strip()[:1000]})

    return endpoint


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec_path")
    ap.add_argument("--endpoint", help='e.g. "GET /api/products"')
    ap.add_argument("--out", help="output JSON path (single endpoint mode)")
    args = ap.parse_args()

    with open(args.spec_path, "r", encoding="utf-8") as f:
        text = f.read()

    spans = find_endpoints(text)
    if not spans:
        print(
            "No endpoints matched the '### METHOD /path' convention. "
            "Open the spec manually and hand-build endpoint_model.json "
            "per references/test_case_schema.md.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.endpoint:
        print(f"Found {len(spans)} endpoint(s):")
        for method, path, _, _ in spans:
            print(f"  {method} {path}")
        print('\nRe-run with --endpoint "METHOD /path" --out endpoint_model.json')
        return

    want_method, _, want_path = args.endpoint.strip().partition(" ")
    want_method = want_method.upper()
    for method, path, start, end in spans:
        if method == want_method and path == want_path.strip():
            section_text = text[start:end]
            model = parse_section(method, path, section_text)
            out_path = args.out or "endpoint_model.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(model, f, indent=2)
            print(f"Wrote {out_path}")
            if not model["parameters"]:
                print(
                    "  Note: no parameter table detected — check raw_section "
                    "and fill parameters manually if the spec uses prose instead of a table.",
                    file=sys.stderr,
                )
            return

    print(f"Endpoint '{args.endpoint}' not found. Run without --endpoint to list options.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()

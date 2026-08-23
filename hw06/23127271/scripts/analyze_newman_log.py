#!/usr/bin/env python3
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "reports" / "newman-run.log"
SHEET = ROOT / "sheets" / "all-test-cases.csv"

log = LOG.read_text(encoding="utf-8", errors="replace")
rows = {r["TestCaseID"]: r for r in csv.DictReader(SHEET.open(encoding="utf-8"))}

# Parse: folder TC line then subsequent HTTP responses with status from console log
current_tc = None
events = []
for line in log.splitlines():
    m = re.search(r"(TC-[A-Z0-9-]+)\s*$", line)
    if m and ("FR-" in line or "Setup" in line or "—" in line):
        current_tc = m.group(1)
    http = re.search(r"(GET|POST|PUT|DELETE) http[^\[]+\[(\d{3})", line)
    if http and current_tc:
        events.append({"tc": current_tc, "method": http.group(1), "code": int(http.group(2)), "line": line.strip()})
    st = re.search(r"'\[(TC-[A-Z0-9-]+)\] ([^']+) status=', (\d+)", line)
    if st:
        events.append({"tc": st.group(1), "step": st.group(2), "code": int(st.group(3)), "kind": "logged"})

by_tc: dict[str, list] = {}
for e in events:
    if e.get("kind") == "logged":
        continue
    by_tc.setdefault(e["tc"], []).append(e)

print("500 errors:")
for tc in sorted(by_tc):
    for e in by_tc[tc]:
        if e["code"] == 500:
            exp = (rows.get(tc) or {}).get("ExpectedResult", "")[:120]
            print(f"  {tc} {e['method']} -> {exp}")

print("\nSecurity / constraint cases with 200 on primary PUT/POST/DELETE:")
watch = [
    "TC-PROFILE-SEC-007", "TC-PROFILE-ST-006", "TC-PROFILE-ST-007",
    "TC-PROFILE-SEC-SUP-002", "TC-PROFILE-SEC-SUP-003", "TC-PROFILE-SUP-002",
    "TC-CART-SEC-SUP-002", "TC-ADMINUSERS-SEC-002", "TC-ADMINUSERS-SEC-SUP-002",
    "TC-PROFILE-SCH-SUP-001", "TC-PROFILE-SCH-SUP-003", "TC-ADMINUSERS-SCH-SUP-001",
    "TC-CART-SEC-006", "TC-PROFILE-SEC-006",
]
for tc in watch:
    if tc in by_tc:
        print(f"  {tc}: {[e['code'] for e in by_tc[tc]]}")

print("\nUnauthenticated probes (expect block, got 200?):")
for tc in sorted(by_tc):
    if "SEC-001" in tc or tc.endswith("-012") or "SEC-SUP-001" in tc:
        codes = [e["code"] for e in by_tc[tc]]
        if 200 in codes:
            print(f"  {tc}: {codes}")

print("\nAll non-2xx non-401/403/404 on mutating requests (possible crashes):")
for tc in sorted(by_tc):
    for e in by_tc[tc]:
        if e["method"] in ("PUT", "POST", "DELETE") and e["code"] >= 500:
            print(f"  {tc} {e['method']} {e['code']}")

#!/usr/bin/env python3
"""Apply manual PassFail / BugRef from Newman bug triage."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "sheets" / "all-test-cases.csv"

FAIL_MAP = {
    "TC-ADMINUSERS-SEC-SUP-002": ("Fail", "BUG-001"),
    "TC-ADMINUSERS-SEC-002": ("Fail", "BUG-002"),
    "TC-PROFILE-SEC-007": ("Fail", "BUG-003"),
    "TC-PROFILE-ST-007": ("Fail", "BUG-003"),
    "TC-PROFILE-SCH-SUP-003": ("Fail", "BUG-004"),
    "TC-PROFILE-SCH-SUP-001": ("Fail", "BUG-004"),
    "TC-ADMINUSERS-SEC-003": ("Fail", "BUG-005"),
    "TC-PROFILE-SEC-SUP-004": ("Fail", "BUG-006"),
    "TC-PROFILE-040": ("Fail", "BUG-006"),
    "TC-CART-SEC-SUP-002": ("Fail", "BUG-007"),
    "TC-ADMINUSERS-SCH-SUP-001": ("Fail", "BUG-008"),
}

ACTUAL = {
    "TC-ADMINUSERS-SEC-SUP-002": "GET /api/admin/users returned 200 with user JWT (Newman)",
    "TC-ADMINUSERS-SEC-002": "DELETE returned 200 with user JWT; URL had literal <id> wrapper in run",
    "TC-PROFILE-SEC-007": "PUT 200 with role=admin in body (Newman)",
    "TC-PROFILE-ST-007": "PUT 200 with role=admin in body (Newman)",
    "TC-PROFILE-SCH-SUP-003": "GET /api/users/me 200, 446B — password field exposure suspected",
    "TC-PROFILE-SCH-SUP-001": "GET /api/users/me 200, 446B — undocumented columns present",
    "TC-ADMINUSERS-SEC-003": "DELETE admin self id=1 returned 200 (Newman)",
    "TC-PROFILE-SEC-SUP-004": "PUT Content-Type text/plain returned 500 (Newman)",
    "TC-PROFILE-040": "PUT Content-Type text/plain returned 500 (Newman)",
    "TC-CART-SEC-SUP-002": "POST quantity=-1 returned 200 (Newman)",
    "TC-ADMINUSERS-SCH-SUP-001": "GET list 200 — extra columns in response (Newman)",
}


def main() -> None:
    with CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fields = list(rows[0].keys())
    for row in rows:
        tid = row["TestCaseID"]
        if tid in FAIL_MAP:
            pf, bug = FAIL_MAP[tid]
            row["PassFail"] = pf
            row["BugRef"] = bug
            row["ActualResult"] = ACTUAL.get(tid, "")
        elif not row.get("PassFail"):
            row["PassFail"] = "Not evaluated"
    with CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"Updated {len(FAIL_MAP)} failing rows in {CSV}")


if __name__ == "__main__":
    main()

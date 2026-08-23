#!/usr/bin/env python3
"""Copy HW06 deliverables into eshop-sut and create one commit per pipeline step per API."""
from __future__ import annotations

import csv
import re
import shutil
import subprocess
from pathlib import Path

SRC = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[4] / "Repo" / "eshop-sut"
DEST = REPO / "hw06" / "23127271"

APIS = [
    {
        "fr": "FR-04",
        "name": "Profile",
        "module": "profile",
        "prefix": "TC-PROFILE",
        "bugs": [
            "BUG-003-sec06-role-escalation-profile.md",
            "BUG-004-sec01-password-hash-profile-get.md",
            "BUG-006-sec02-text-plain-profile-500.md",
        ],
    },
    {
        "fr": "FR-07",
        "name": "Cart",
        "module": "cart",
        "prefix": "TC-CART",
        "bugs": ["BUG-007-cart-negative-quantity.md"],
    },
    {
        "fr": "FR-19",
        "name": "Admin Users",
        "module": "admin-users",
        "prefix": "TC-ADMINUSERS",
        "bugs": [
            "BUG-001-sec03-user-list-admin-api.md",
            "BUG-002-sec03-user-delete-admin-api.md",
            "BUG-005-fr19-admin-self-delete.md",
            "BUG-008-admin-list-schema-overexposure.md",
        ],
    },
]

SUP_MARKERS = ("-SUP-", "-ST-SUP-", "-SEC-SUP-", "-SCH-SUP-")

STAGE1_DOCS = [
    "domain-testing-report.md",
    "state-transition-report.md",
    "security-testing-report.md",
    "schema-validation-report.md",
    "prompt_log.md",
    "_ai_prompt_stage1.txt",
    "_ai_output_stage1.txt",
]

STAGE2_DOCS = [
    "stage2-audit.md",
    "stage2-audit-state-transitions.md",
    "stage2-audit-security.md",
    "stage2-audit-schema.md",
    "_ai_prompt_stage2.txt",
    "_ai_output_stage2.txt",
]

STAGE3_DOCS = [
    "stage3-extend.md",
    "stage3-extend-state-transitions.md",
    "stage3-extend-security.md",
    "stage3-extend-schema.md",
    "stage3-extend-summary.md",
    "stage3-audit-human.md",
    "_ai_prompt_stage3.txt",
    "_ai_output_stage3.txt",
]

GENERATE_SCRIPTS = [
    "generate_domain_partitions.py",
    "generate_state_transitions.py",
    "generate_security_tests.py",
    "generate_schema_validation.py",
]

AUDIT_SCRIPTS = [
    "apply_stage2_audit.py",
    "apply_stage2_audit_state_transitions.py",
    "apply_stage2_audit_security.py",
    "apply_stage2_audit_schema.py",
]

EXTEND_SCRIPTS = [
    "append_stage3_sup_cases.py",
    "append_stage3_st_sup_cases.py",
    "append_stage3_sec_sup_cases.py",
    "append_stage3_sch_sup_cases.py",
]

EXECUTE_SCRIPTS = [
    "build_execution_artifacts.py",
    "analyze_newman_log.py",
    "apply_newman_bug_refs.py",
    "create_git_commits.py",
]

SHEETS = [
    "domain-partitions.csv",
    "state-transitions.csv",
    "security-tests.csv",
    "schema-validation.csv",
]


def run(cmd: list[str], cwd: Path = REPO) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def copy_file(rel: str) -> None:
    src = SRC / rel
    dst = DEST / rel
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_many(rels: list[str]) -> None:
    for rel in rels:
        copy_file(rel)


def is_ai_tc(path: Path, prefix: str) -> bool:
    name = path.stem
    if not name.startswith(prefix):
        return False
    return not any(m in name for m in SUP_MARKERS)


def is_sup_tc(path: Path, prefix: str) -> bool:
    name = path.stem
    return name.startswith(prefix) and any(m in name for m in SUP_MARKERS)


def copy_module_tcs(module: str, prefix: str, *, sup: bool) -> None:
    folder = SRC / "tests" / "test-cases" / module
    for src in sorted(folder.glob("*.md")):
        ok = is_sup_tc(src, prefix) if sup else is_ai_tc(src, prefix)
        if ok:
            rel = src.relative_to(SRC).as_posix()
            copy_file(rel)


def filter_csv(sheet: str, prefix: str, out_name: str | None = None) -> None:
    src = SRC / "sheets" / sheet
    dst = DEST / "sheets" / (out_name or sheet)
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
        fieldnames = rows[0].keys() if rows else []
    matched = [r for r in rows if r["TestCaseID"].startswith(prefix)]
    with dst.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(matched)


def merge_csv(sheet: str, prefix: str) -> None:
    src = SRC / "sheets" / sheet
    dst = DEST / "sheets" / sheet
    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open(encoding="utf-8", newline="") as f:
        all_rows = list(csv.DictReader(f))
        fieldnames = list(all_rows[0].keys()) if all_rows else []
    new_rows = [r for r in all_rows if r["TestCaseID"].startswith(prefix)]
    existing: list[dict] = []
    if dst.exists():
        with dst.open(encoding="utf-8", newline="") as f:
            existing = list(csv.DictReader(f))
    existing_ids = {r["TestCaseID"] for r in existing}
    merged = existing + [r for r in new_rows if r["TestCaseID"] not in existing_ids]
    merged.sort(key=lambda r: r["TestCaseID"])
    with dst.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(merged)


def commit(message: str, paths: list[str]) -> None:
    for p in paths:
        run(["git", "add", p])
    run(["git", "commit", "-m", message])


def ensure_gitignore() -> None:
    gi = REPO / ".gitignore"
    text = gi.read_text(encoding="utf-8") if gi.exists() else "node_modules\n"
    extra = ["backend/database.sqlite", "*.sqlite"]
    lines = text.splitlines()
    changed = False
    for item in extra:
        if item not in lines:
            lines.append(item)
            changed = True
    if changed:
        gi.write_text("\n".join(lines) + "\n", encoding="utf-8")
        run(["git", "add", ".gitignore"])
        run(["git", "commit", "-m", "HW06: ignore local SQLite database file."])


def write_readme() -> None:
    dest = DEST / "README.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        """# HW06 API Testing — Student 23127271

**APIs:** FR-04 Profile · FR-07 Cart · FR-19 Admin Users  
**SUT:** EShop backend (`http://localhost:3000`)

## Layout

| Path | Contents |
|------|----------|
| `tests/test-cases/` | Per-TC markdown (domain, state, security, schema) |
| `sheets/` | CSV test-case sheets |
| `postman/` | Newman/Postman collection + environment |
| `reports/` | Newman CLI log + HTML report |
| `bugs/` | Markdown bug reports |
| `docs/` | Stage reports, audit, execution summary |
| `scripts/` | Generators, audit helpers, Newman analysis |
| `git-commit-log.txt` | Full git log for submission |

## Newman

```bash
cd hw06/23127271
newman run postman/eshop-hw06.postman_collection.json -r cli,htmlextra \\
  --reporter-htmlextra-export reports/newman-report.html
```

Do **not** pass `-e postman/eshop-hw06.postman_environment.json` when empty env tokens would override Setup tokens.

Student header `X-Student-Id: 23127271` is injected via collection pre-request script.
""",
        encoding="utf-8",
    )


def main() -> None:
    if not REPO.is_dir():
        raise SystemExit(f"Repo not found: {REPO}")

    try:
        run(["git", "restore", "backend/database.sqlite"], cwd=REPO)
    except subprocess.CalledProcessError:
        print("warn: could not restore backend/database.sqlite (file may be locked); continuing.")

    bootstrap = not (DEST / "README.md").exists()
    if bootstrap:
        ensure_gitignore()
        write_readme()
        commit(
            "HW06: add README scaffold for student 23127271 API testing workspace.",
            ["hw06/23127271/README.md"],
        )
    else:
        print("skip bootstrap — hw06/23127271/README.md already present.")

    for api in APIS:
        fr, name, module, prefix = api["fr"], api["name"], api["module"], api["prefix"]
        base = f"hw06/23127271"

        # Stage 1 — Generate
        if fr == "FR-04":
            copy_many([f"scripts/{s}" for s in GENERATE_SCRIPTS])
        copy_many([f"docs/{d}" for d in STAGE1_DOCS])
        copy_module_tcs(module, prefix, sup=False)
        for sheet in SHEETS:
            merge_csv(sheet, prefix)
        paths = [
            f"{base}/docs/{d}" for d in STAGE1_DOCS
        ] + [
            f"{base}/sheets/{s}" for s in SHEETS
        ]
        if fr == "FR-04":
            paths += [f"{base}/scripts/{s}" for s in GENERATE_SCRIPTS]
        tc_glob = f"{base}/tests/test-cases/{module}"
        run(["git", "add", tc_glob])
        commit(
            f"HW06 {fr}: Stage 1 — AI-generate {name} test cases (domain, state, security, schema).",
            paths,
        )

        # Stage 2 — Audit
        if fr == "FR-04":
            copy_many([f"scripts/{s}" for s in AUDIT_SCRIPTS])
        copy_many([f"docs/{d}" for d in STAGE2_DOCS])
        copy_module_tcs(module, prefix, sup=False)
        for sheet in SHEETS:
            copy_file(f"sheets/{sheet}")
        paths = [f"{base}/docs/{d}" for d in STAGE2_DOCS] + [f"{base}/sheets/{s}" for s in SHEETS]
        if fr == "FR-04":
            paths += [f"{base}/scripts/{s}" for s in AUDIT_SCRIPTS]
        run(["git", "add", tc_glob])
        commit(
            f"HW06 {fr}: Stage 2 — audit AI {name} cases (VALID/INVALID/INCOMPLETE + corrected oracles).",
            paths,
        )

        # Stage 3 — Extend
        if fr == "FR-04":
            copy_many([f"scripts/{s}" for s in EXTEND_SCRIPTS])
        copy_many([f"docs/{d}" for d in STAGE3_DOCS])
        copy_module_tcs(module, prefix, sup=True)
        for sheet in SHEETS:
            copy_file(f"sheets/{sheet}")
        paths = [f"{base}/docs/{d}" for d in STAGE3_DOCS] + [f"{base}/sheets/{s}" for s in SHEETS]
        if fr == "FR-04":
            paths += [f"{base}/scripts/{s}" for s in EXTEND_SCRIPTS]
        run(["git", "add", tc_glob])
        commit(
            f"HW06 {fr}: Stage 3 — extend {name} with human-found SUP cases and audit notes.",
            paths,
        )

        # Stage 5 — Execute (bugs + triage for this API)
        copy_many([f"bugs/{b}" for b in api["bugs"]])
        copy_file("docs/newman-execution-summary.md")
        copy_file("docs/bug-reports-summary.md")
        paths = [f"{base}/bugs/{b}" for b in api["bugs"]] + [
            f"{base}/docs/newman-execution-summary.md",
            f"{base}/docs/bug-reports-summary.md",
        ]
        commit(
            f"HW06 {fr}: Stage 5 — execute {name} tests; file bugs from Newman manual triage.",
            paths,
        )

    # Combined execution artifacts
    base = "hw06/23127271"
    copy_many([f"scripts/{s}" for s in EXECUTE_SCRIPTS])
    copy_many(
        [
            "postman/eshop-hw06.postman_collection.json",
            "postman/eshop-hw06.postman_environment.json",
            "reports/newman-run.log",
            "reports/newman-report.html",
            "sheets/all-test-cases.csv",
            "sheets/all-test-cases.xlsx",
            "docs/execution-artifacts.md",
            "ai_audit_log.md",
        ]
    )
    commit(
        "HW06: Stage 4/5 — Postman collection, Newman HTML report, combined sheets, execution docs.",
        [
            f"{base}/scripts",
            f"{base}/postman",
            f"{base}/reports",
            f"{base}/sheets/all-test-cases.csv",
            f"{base}/sheets/all-test-cases.xlsx",
            f"{base}/docs/execution-artifacts.md",
            f"{base}/ai_audit_log.md",
        ],
    )

    # Export commit log
    log_path = DEST / "git-commit-log.txt"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as f:
        subprocess.run(
            ["git", "log", "--format=fuller", "--", "hw06/23127271"],
            cwd=REPO,
            check=True,
            stdout=f,
        )
    shutil.copy2(log_path, SRC / "git-commit-log.txt")
    commit(
        "HW06: export git-commit-log.txt for Moodle submission.",
        [f"{base}/git-commit-log.txt"],
    )

    print("\nDone. Commits on hw06/23127271:")
    subprocess.run(["git", "log", "--oneline", "--", "hw06/23127271"], cwd=REPO, check=True)


if __name__ == "__main__":
    main()

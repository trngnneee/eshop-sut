"""Create the 15 scrubbed HW06 defect issues and save URL/number manifest."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from build_github_issue_bodies import BUGS, OUT

REPO = "trngnneee/eshop-sut"
MANIFEST = OUT.parent / "github-issues.json"

MODULE_LABELS = {"api": "module: api", "checkout": "module:checkout", "orders": "module: orders"}


def existing_issues() -> dict[str, dict]:
    result = subprocess.run(["gh", "issue", "list", "--repo", REPO, "--state", "all", "--limit", "1000", "--json", "number,title,url"], capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    issues = json.loads(result.stdout)
    found = {}
    for issue in issues:
        for bug, *_ in BUGS:
            if issue["title"].startswith(f"[{bug}]"):
                found[bug] = issue
    return found


def prior_labels() -> dict[str, list]:
    """Giữ lại nhãn đã ghi trong manifest cũ để lần chạy sau không làm mất dữ liệu."""
    if not MANIFEST.exists():
        return {}
    return {
        row["bug_id"]: row["labels"]
        for row in json.loads(MANIFEST.read_text(encoding="utf-8"))
        if isinstance(row.get("labels"), list)
    }


def main() -> None:
    created = []
    existing = existing_issues()
    known = prior_labels()
    for bug, title, severity, priority, module, tc, *_ in BUGS:
        if bug in existing:
            issue = existing[bug]
            created.append({"bug_id": bug, "issue_number": issue["number"], "url": issue["url"], "test_case": tc, "labels": known.get(bug, "existing")})
            print(f"{bug} already exists -> #{issue['number']} {issue['url']}")
            continue
        body_file = OUT / f"{bug}.md"
        labels = ["type: bug", MODULE_LABELS[module], f"severity: {severity}", f"priority: {priority}", "found-by: test-case"]
        labels = [label for label in labels if label]
        command = ["gh", "issue", "create", "--repo", REPO, "--title", f"[{bug}] {title}", "--body-file", str(body_file)]
        for label in labels:
            command.extend(["--label", label])
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
        if result.returncode != 0:
            raise RuntimeError(f"Failed creating {bug}: {result.stderr.strip()}")
        url = result.stdout.strip().splitlines()[-1]
        number = int(url.rstrip("/").split("/")[-1])
        created.append({"bug_id": bug, "issue_number": number, "url": url, "test_case": tc, "labels": labels})
        print(f"{bug} -> #{number} {url}")
    MANIFEST.write_text(json.dumps(created, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote manifest: {MANIFEST}")


if __name__ == "__main__":
    main()

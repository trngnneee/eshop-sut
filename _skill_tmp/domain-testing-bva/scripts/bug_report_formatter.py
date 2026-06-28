#!/usr/bin/env python3
"""
bug_report_formatter.py
-----------------------
Generates a structured bug report entry in Markdown and optionally
opens a prefilled GitHub Issue URL in the browser.

Usage:
    python bug_report_formatter.py
"""

import urllib.parse
import webbrowser


def prompt(label: str, required: bool = True) -> str:
    while True:
        val = input(f"{label}: ").strip()
        if val or not required:
            return val
        print("  (required)")


def main():
    print("=" * 60)
    print("  Bug Report Entry Generator")
    print("=" * 60)

    fr_id   = prompt("Feature ID (e.g. FR01)")
    seq     = prompt("Bug sequence number (e.g. 001)")
    title   = prompt("Short title (e.g. Empty email accepted on registration)")
    tc_id   = prompt("Related TC ID")
    severity = prompt("Severity (Critical/Major/Minor/Trivial)")
    priority = prompt("Priority (High/Medium/Low)")
    steps   = prompt("Steps to reproduce (use '; ' as separator)")
    expected = prompt("Expected behaviour")
    actual  = prompt("Actual behaviour")
    screenshot = prompt("Screenshot filename (e.g. bug-FR01-001.png)", required=False) or "TBD"
    repo_url = prompt("GitHub repo URL (e.g. https://github.com/org/repo)", required=False)

    bug_id = f"BUG-{fr_id}-{seq}"
    steps_md = "\n".join(f"   {i+1}. {s.strip()}" for i, s in enumerate(steps.split(";")))

    entry = f"""
## {bug_id}: {title}

| Field              | Value |
|--------------------|-------|
| Related TC         | {tc_id} |
| Severity           | {severity} |
| Priority           | {priority} |
| Screenshot         | ![screenshot](./screenshots/{screenshot}) |

**Steps to Reproduce:**
{steps_md}

**Expected:** {expected}

**Actual:** {actual}

**GitHub Issue:** _(link to be added after posting)_

---
"""

    output_file = "bug-report.md"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"\n✅ Bug entry appended to {output_file}")

    if repo_url:
        issue_title = urllib.parse.quote(f"[{bug_id}] {title}")
        issue_body = urllib.parse.quote(
            f"**TC**: {tc_id}\n**Severity**: {severity}\n**Priority**: {priority}\n\n"
            f"**Steps to Reproduce**:\n{steps_md.strip()}\n\n"
            f"**Expected**: {expected}\n\n**Actual**: {actual}"
        )
        github_url = f"{repo_url}/issues/new?title={issue_title}&body={issue_body}"
        print(f"\n🔗 Opening GitHub Issues in browser...")
        webbrowser.open(github_url)
    else:
        print("\n(No GitHub URL provided — post the bug manually)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""File GitHub Issues from HW06 bug reports (offline evidence from Newman logs)."""
from __future__ import annotations

import re
import subprocess
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence" / "bugs"
REPO_ROOT = ROOT.parents[1]
REPO = "trngnneee/eshop-sut"
BRANCH = "HW6-Tram"
STUDENT = "23127271"
LABELS = "bug,API-testing"

META = {
    "BUG-001": ("Critical", "TC-ADMINUSERS-SEC-SUP-002", "Human (Stage 3)"),
    "BUG-002": ("Critical", "TC-ADMINUSERS-SEC-002", "AI (Stage 1)"),
    "BUG-003": ("Critical", "TC-PROFILE-SEC-007", "AI (Stage 1)"),
    "BUG-004": ("Critical", "TC-PROFILE-SCH-SUP-003", "Human (Stage 3)"),
    "BUG-005": ("High", "TC-ADMINUSERS-SEC-003", "AI (Stage 1)"),
    "BUG-006": ("Medium", "TC-PROFILE-SEC-SUP-004", "Human (Stage 3)"),
    "BUG-007": ("Medium", "TC-CART-SEC-SUP-002", "Human (Stage 3)"),
    "BUG-008": ("Medium", "TC-ADMINUSERS-SCH-SUP-001", "Human (Stage 3)"),
}


def title_from_md(path: Path) -> str:
    line = path.read_text(encoding="utf-8").splitlines()[0]
    title = line.lstrip("# Bug: ").strip()
    bug_id = path.name.split("-")[0] + "-" + path.name.split("-")[1]
    return f"[HW06][{STUDENT}][{bug_id.upper()}] {title}"


def screenshot_text(md_path: Path) -> str:
    md = md_path.read_text(encoding="utf-8")
    bug_id = md_path.stem.split("-")[0] + "-" + md_path.stem.split("-")[1]
    title = md.splitlines()[0].lstrip("# Bug: ").strip()
    actual = ""
    if "## Actual result" in md:
        actual = md.split("## Actual result", 1)[1].split("##", 1)[0].strip()
    return (
        f"{bug_id} — {title}\n"
        f"Student: {STUDENT} | SUT: http://localhost:3000\n"
        f"Source: Newman manual triage + Postman HW06 collection\n\n"
        f"{actual}\n"
    )


def save_png(bug_id: str, text: str) -> Path:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    png = EVIDENCE / f"{bug_id}.png"
    (EVIDENCE / f"{bug_id}.txt").write_text(text, encoding="utf-8")
    font = ImageFont.load_default()
    lines: list[str] = []
    for para in text.splitlines():
        lines.extend(textwrap.wrap(para, width=105) if para.strip() else [""])
    line_h = 14
    pad = 16
    w, h = 920, pad * 2 + line_h * max(len(lines), 1)
    img = Image.new("RGB", (w, h), (248, 248, 252))
    draw = ImageDraw.Draw(img)
    y = pad
    for line in lines:
        draw.text((pad, y), line, fill=(20, 20, 20), font=font)
        y += line_h
    img.save(png)
    return png


def issue_body(md_path: Path, bug_id: str) -> str:
    sev, tc, found = META[bug_id]
    md = md_path.read_text(encoding="utf-8")
    img = f"https://github.com/{REPO}/raw/{BRANCH}/hw06/23127271/evidence/bugs/{bug_id}.png"
    return (
        f"**HW06 API Testing — Student {STUDENT}**\n\n"
        f"- **Severity:** {sev}\n"
        f"- **Found via:** `{tc}` ({found})\n"
        f"- **Branch:** `{BRANCH}`\n\n"
        f"## Screenshot evidence\n\n"
        f"![{bug_id} evidence]({img})\n\n"
        f"---\n\n{md}"
    )


def push_evidence() -> None:
    subprocess.run(["git", "add", "hw06/23127271/evidence/bugs"], cwd=REPO_ROOT, check=True)
    st = subprocess.run(["git", "status", "--porcelain"], cwd=REPO_ROOT, capture_output=True, text=True)
    if not st.stdout.strip():
        return
    subprocess.run(
        ["git", "commit", "-m", "HW06: add bug screenshot evidence for GitHub Issues."],
        cwd=REPO_ROOT,
        check=True,
    )
    subprocess.run(["git", "push", f"https://github.com/{REPO}.git", BRANCH], cwd=REPO_ROOT, check=True)


def create_issue(title: str, body_file: Path) -> str:
    for labels in (LABELS, "bug"):
        r = subprocess.run(
            ["gh", "issue", "create", "--repo", REPO, "--title", title, "--label", labels, "--body-file", str(body_file)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if r.returncode == 0:
            return r.stdout.strip()
    r = subprocess.run(
        ["gh", "issue", "create", "--repo", REPO, "--title", title, "--body-file", str(body_file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    r.check_returncode()
    return r.stdout.strip()


def main() -> None:
    urls: dict[str, str] = {}
    paths = sorted(ROOT.glob("bugs/BUG-*.md"), key=lambda p: p.name)
    for md_path in paths:
        m = re.match(r"BUG-(\d+)", md_path.name)
        if not m:
            continue
        bug_id = f"BUG-{m.group(1).zfill(3)}"
        if bug_id not in META:
            bug_id = f"BUG-{int(m.group(1)):03d}" if int(m.group(1)) < 10 else f"BUG-{m.group(1)}"
        # normalize: BUG-001 from BUG-001-...
        bug_id = "BUG-" + m.group(1).zfill(3) if len(m.group(1)) <= 3 else f"BUG-{m.group(1)}"
        bug_id = md_path.name[:7]  # BUG-001
        print(f"{bug_id}...")
        save_png(bug_id, screenshot_text(md_path))
        body_file = EVIDENCE / f"{bug_id}-issue-body.md"
        body_file.write_text(issue_body(md_path, bug_id), encoding="utf-8")

    print("Push evidence...")
    push_evidence()

    for md_path in paths:
        bug_id = md_path.name[:7]
        title = title_from_md(md_path)
        body_file = EVIDENCE / f"{bug_id}-issue-body.md"
        url = create_issue(title, body_file)
        urls[bug_id] = url
        print(f"  {bug_id}: {url}")

    out = ROOT / "docs" / "github-issues.md"
    lines = [f"# GitHub Issues — HW06 ({STUDENT})\n", f"https://github.com/{REPO}/issues\n"]
    for bid, url in sorted(urls.items()):
        lines.append(f"- **{bid}** — {url}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()

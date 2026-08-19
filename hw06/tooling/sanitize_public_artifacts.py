#!/usr/bin/env python3
"""Redact fixture credentials from public HW06 Postman/Newman artifacts.

The sanitizer preserves assertion names, pass/fail state, HTTP status, report
structure, and sensitive *field names* (for example ``password``) while
replacing only credential values.  It is suitable both after a local Newman
run and as a tree-filter helper when purging an unpushed branch history.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TARGETS = (
    ROOT / "hw06" / "postman" / "EShop-HW06-23127207.postman_collection.json",
    ROOT / "hw06" / "postman" / "EShop-HW06-local.postman_environment.json",
    ROOT / "hw06" / "newman" / "reports",
)
TEXT_SUFFIXES = {".json", ".html", ".md", ".log"}

FIXED_VALUES = {
    "Test1234!": "<redacted-user-password>",
    "Admin123!": "<redacted-admin-password>",
    "Temp1234!": "<redacted-lock-password>",
    "Wrong123!": "<redacted-wrong-password>",
}
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b")
DYNAMIC_PASSWORD_RE = re.compile(r"Hw06-[0-9A-Fa-f]{8,}(?:-[0-9A-Fa-f]{4,})+")


def redact_text(text: str) -> tuple[str, int]:
    count = 0
    for source, replacement in FIXED_VALUES.items():
        occurrences = text.count(source)
        if occurrences:
            text = text.replace(source, replacement)
            count += occurrences
    text, jwt_count = JWT_RE.subn("<redacted-jwt>", text)
    text, dynamic_count = DYNAMIC_PASSWORD_RE.subn("<redacted-dynamic-password>", text)
    return text, count + jwt_count + dynamic_count


def read_text(path: Path) -> tuple[str, str]:
    data = path.read_bytes()
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16"), "utf-16"
    return data.decode("utf-8"), "utf-8"


def write_text(path: Path, text: str, encoding: str) -> None:
    path.write_text(text, encoding=encoding)


def clear_environment_passwords(path: Path) -> int:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    changed = 0
    for item in document.get("values", []):
        key = str(item.get("key", "")).lower()
        if key.endswith("password") and item.get("value"):
            item["value"] = ""
            item["type"] = "secret"
            changed += 1
    if changed:
        path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def iter_files(targets: list[Path]) -> list[Path]:
    files: set[Path] = set()
    for target in targets:
        if target.is_file() and target.suffix.lower() in TEXT_SUFFIXES:
            files.add(target)
        elif target.is_dir():
            files.update(path for path in target.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES)
    return sorted(files)


def remaining_markers(text: str) -> list[str]:
    markers = [value for value in FIXED_VALUES if value in text]
    if JWT_RE.search(text):
        markers.append("JWT")
    if DYNAMIC_PASSWORD_RE.search(text):
        markers.append("dynamic password")
    return markers


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, help="Files/directories to sanitize; defaults to HW06 Postman and Newman artifacts")
    parser.add_argument("--tree", type=Path, help="Repository tree root, used by history filtering")
    parser.add_argument("--check", action="store_true", help="Do not modify files; fail if a credential marker remains")
    args = parser.parse_args()

    if args.paths:
        targets = [path.resolve() for path in args.paths]
    elif args.tree:
        tree = args.tree.resolve()
        targets = [
            tree / "hw06" / "postman" / "EShop-HW06-23127207.postman_collection.json",
            tree / "hw06" / "postman" / "EShop-HW06-local.postman_environment.json",
            tree / "hw06" / "newman" / "reports",
        ]
    else:
        targets = list(DEFAULT_TARGETS)

    files = iter_files(targets)
    if args.check:
        failed = []
        for path in files:
            text, _ = read_text(path)
            markers = remaining_markers(text)
            if markers:
                failed.append(f"{path}: {', '.join(markers)}")
        if failed:
            print("Credential markers remain:\n" + "\n".join(failed), file=sys.stderr)
            return 1
        print(f"Sanitizer check passed for {len(files)} files.")
        return 0

    replacements = 0
    for path in files:
        text, encoding = read_text(path)
        redacted, count = redact_text(text)
        if count:
            write_text(path, redacted, encoding)
            replacements += count
    for target in targets:
        if target.name.endswith("postman_environment.json") and target.is_file():
            replacements += clear_environment_passwords(target)
    print(f"Redacted {replacements} credential values across {len(files)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

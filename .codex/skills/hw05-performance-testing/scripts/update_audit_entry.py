#!/usr/bin/env python3
"""Update one HW04-style HW05 audit Interaction entry."""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path


VALID_STATUSES = {
    "Pending Human Review",
    "Approved",
    "Approved with Corrections",
    "Rejected",
    "Completed",
}


def format_timestamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def quote_prompt(prompt: str) -> str:
    lines = neutralize_heading_markers(prompt).splitlines() or [""]
    return "\n".join(f"  > {line}" if line else "  >" for line in lines)


def neutralize_heading_markers(text: str) -> str:
    converted = []
    for line in text.strip().splitlines() or [""]:
        bold_heading = re.match(r"^(\s*)\*\*\s*\\?#{1,6}\s+(.+?)\s*\*\*\s*$", line)
        if bold_heading:
            converted.append(f"{bold_heading.group(1)}**{bold_heading.group(2).strip()}**")
            continue

        heading = re.match(r"^(\s{0,3})\\?#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            converted.append(f"{heading.group(1)}**{heading.group(2).strip()}**")
            continue

        converted.append(line)
    return "\n".join(converted)


def format_content(content: str) -> str:
    lines = neutralize_heading_markers(content).splitlines() or [""]
    return "\n".join(f"  {line}" if line else "  " for line in lines)


def review_result(status: str, explicit: str, review: str) -> str:
    if explicit.strip():
        return " ".join(neutralize_heading_markers(explicit).split())
    prefix = {
        "Pending Human Review": "Đã chỉnh sửa, hiện đang chờ review lại.",
        "Approved": "Chấp nhận.",
        "Approved with Corrections": "Đã chỉnh sửa và được chấp nhận.",
        "Rejected": "Bị từ chối / không còn hiệu lực.",
        "Completed": "Hoàn tất.",
    }[status]
    review_text = " ".join(neutralize_heading_markers(review).split())
    return f"{prefix} {review_text}".strip()


def append_prompt(block: str, prompt: str) -> str:
    next_label = "\n- **Output:**"
    index = block.find(next_label)
    if index == -1:
        raise SystemExit("Output label not found in audit entry")
    addition = "\n  >\n" + quote_prompt(prompt)
    return block[:index].rstrip() + addition + block[index:]


def replace_output(block: str, revised_output: str) -> str:
    if not revised_output.strip():
        return block
    pattern = re.compile(r"(- \*\*Output:\*\*\n)(.*?)(\n- \*\*Kết quả sau review:\*\*)", re.S)
    match = pattern.search(block)
    if not match:
        raise SystemExit("Output section not found in audit entry")
    current = match.group(2).rstrip()
    updated_output = current + "\n  Cập nhật sau review:\n" + format_content(revised_output)
    return block[: match.start()] + match.group(1) + updated_output + match.group(3) + block[match.end() :]


def replace_review_result(block: str, result: str) -> str:
    pattern = re.compile(r"- \*\*Kết quả sau review:\*\*.*?(?=\n<!-- AUDIT_ENTRY:)", re.S)
    if not pattern.search(block):
        raise SystemExit("Review result label not found in audit entry")
    return pattern.sub(f"- **Kết quả sau review:** {result.strip()}\n", block, count=1)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_file", type=Path)
    parser.add_argument("--id", required=True, help="Audit Interaction ID")
    parser.add_argument(
        "--review-prompt",
        default="",
        help="Accepted for compatibility; review prompts are not rendered",
    )
    parser.add_argument("--review", required=True, help="Vietnamese review/correction summary")
    parser.add_argument("--revised-output", default="", help="Vietnamese revised output summary")
    parser.add_argument("--review-result", default="", help="Vietnamese final review result")
    parser.add_argument(
        "--status",
        required=True,
        choices=sorted(VALID_STATUSES),
        help="Lifecycle status used to derive review result when omitted",
    )
    parser.add_argument("--time", default="", help="Accepted for compatibility; not rendered")
    args = parser.parse_args()

    if not args.audit_file.exists():
        raise SystemExit(f"Audit file does not exist: {args.audit_file}")

    _timestamp = args.time or format_timestamp(datetime.now())
    text = args.audit_file.read_text(encoding="utf-8")

    start_marker = f"<!-- AUDIT_ENTRY:{args.id}:START -->"
    end_marker = f"<!-- AUDIT_ENTRY:{args.id}:END -->"
    start = text.find(start_marker)
    if start == -1:
        raise SystemExit(f"Audit entry not found: {args.id}")
    end = text.find(end_marker, start)
    if end == -1:
        raise SystemExit(f"Audit entry is malformed: missing END marker for {args.id}")
    end += len(end_marker)

    block = text[start:end]
    block = replace_output(block, args.revised_output)
    result = review_result(args.status, args.review_result, args.review)
    block = replace_review_result(block, result)

    args.audit_file.write_text(text[:start] + block + text[end:], encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

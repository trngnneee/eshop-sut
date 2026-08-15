#!/usr/bin/env python3
"""Update an existing HW05 AI Audit Report phase entry."""

from __future__ import annotations

import argparse
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
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%I:%M %p').lstrip('0')}"


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument("audit_file", type=Path)

    parser.add_argument(
        "--id",
        required=True,
        help="Audit phase ID, e.g. load-phase-2",
    )

    parser.add_argument(
        "--review-prompt",
        required=True,
        help="Exact user prompt containing approval/correction",
    )

    parser.add_argument(
        "--review",
        required=True,
        help="Structured human review/correction summary",
    )

    parser.add_argument(
        "--revised-output",
        default="",
        help="AI output after applying the human review",
    )

    parser.add_argument(
        "--status",
        required=True,
        choices=sorted(VALID_STATUSES),
        help="Updated phase status",
    )

    parser.add_argument(
        "--time",
        default="",
        help="Timestamp; defaults to local now",
    )

    args = parser.parse_args()

    if not args.audit_file.exists():
        raise SystemExit(f"Audit file does not exist: {args.audit_file}")

    timestamp = args.time or format_timestamp(datetime.now())

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

    # Update current phase status.
    status_prefix = "- **Status:** "

    lines = block.splitlines()
    status_found = False

    for i, line in enumerate(lines):
        if line.startswith(status_prefix):
            lines[i] = f"{status_prefix}{args.status}"
            status_found = True
            break

    if not status_found:
        raise SystemExit(f"Status field not found in audit entry: {args.id}")

    block = "\n".join(lines)

    # Remove old end marker temporarily so review can be appended before it.
    marker_position = block.rfind(end_marker)

    if marker_position == -1:
        raise SystemExit(f"END marker disappeared unexpectedly: {args.id}")

    content = block[:marker_position].rstrip()
    pending_placeholder = "### Human Review\n\nPending human review."
    if pending_placeholder in content:
        content = content.replace(pending_placeholder, "### Human Review", 1).rstrip()

    review_block = [
        "",
        f"### Human Review — {timestamp}",
        "",
        "##### Review Prompt",
        "",
        args.review_prompt.strip(),
        "",
        "##### Human Review / Decision",
        "",
        args.review.strip(),
        "",
    ]

    review_block[1] = f"#### Review - {timestamp}"

    if args.revised_output.strip():
        review_block.extend(
            [
                "##### Revised AI Output",
                "",
                args.revised_output.strip(),
                "",
            ]
        )

    review_block.extend(
        [
            "##### Phase Status",
            "",
            args.status,
            "",
        ]
    )

    updated_block = (
        content
        + "\n"
        + "\n".join(review_block)
        + end_marker
    )

    updated_text = text[:start] + updated_block + text[end:]

    args.audit_file.write_text(updated_text, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

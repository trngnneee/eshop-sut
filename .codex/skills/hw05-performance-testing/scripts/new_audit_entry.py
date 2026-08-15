#!/usr/bin/env python3
"""Append a structured HW05 AI Audit Report phase entry."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

def format_timestamp(dt: datetime) -> str:
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%I:%M %p').lstrip('0')}"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_file", type=Path)
    parser.add_argument(
        "--id",
        required=True,
        help="Stable audit phase ID, e.g. load-phase-1",
    )
    parser.add_argument("--scenario", required=True, help="Scenario name, e.g. Load")
    parser.add_argument("--phase", required=True, help="Phase number, e.g. 1")
    parser.add_argument("--phase-name", required=True, help="Phase name, e.g. Design")
    parser.add_argument("--tool", required=True, help="AI tool name")
    parser.add_argument("--prompt", required=True, help="Prompt sent to the AI tool")
    parser.add_argument("--output", required=True, help="AI output summary or transcript")
    parser.add_argument("--review", default="", help="Human review, correction, or decision")
    parser.add_argument(
        "--status",
        default="Pending Human Review",
        help="Initial phase status",
    )
    parser.add_argument(
        "--triggered-by",
        default="",
        help="Previous phase approval that triggered this phase, if applicable",
    )
    parser.add_argument("--time", default="", help="ISO-like timestamp; defaults to local now")
    args = parser.parse_args()

    timestamp = args.time or format_timestamp(datetime.now())
    args.audit_file.parent.mkdir(parents=True, exist_ok=True)

    existing = args.audit_file.read_text(encoding="utf-8") if args.audit_file.exists() else ""
    start_marker = f"<!-- AUDIT_ENTRY:{args.id}:START -->"
    if start_marker in existing:
        raise SystemExit(f"Audit entry already exists: {args.id}")

    with args.audit_file.open("a", encoding="utf-8") as handle:
        handle.write(f"\n<!-- AUDIT_ENTRY:{args.id}:START -->\n")
        handle.write(f"## {args.scenario} - Phase {args.phase}: {args.phase_name}\n\n")
        handle.write(f"- **Started:** {timestamp}\n")
        handle.write(f"- **Tool:** {args.tool}\n")
        handle.write(f"- **Status:** {args.status}\n")
        if args.triggered_by.strip():
            handle.write(f"- **Triggered by:** {args.triggered_by.strip()}\n")
        handle.write("\n### Initial Prompt\n\n")
        handle.write(args.prompt.strip() + "\n\n")
        handle.write("### Initial AI Output\n\n")
        handle.write(args.output.strip() + "\n\n")
        handle.write("### Human Review\n\n")
        handle.write((args.review.strip() or "Pending human review.") + "\n")
        handle.write(f"<!-- AUDIT_ENTRY:{args.id}:END -->\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

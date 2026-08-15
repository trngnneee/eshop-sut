#!/usr/bin/env python3
"""Append a structured HW05 AI Audit Report entry."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

def format_timestamp(dt: datetime) -> str:
    return f"{dt.month}/{dt.day}/{dt.year} {dt.strftime('%I:%M %p').lstrip('0')}"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_file", type=Path)
    parser.add_argument("--tool", required=True, help="AI tool name")
    parser.add_argument("--prompt", required=True, help="Prompt sent to the AI tool")
    parser.add_argument("--output", required=True, help="AI output summary or transcript")
    parser.add_argument("--review", default="", help="Human review, correction, or decision")
    parser.add_argument("--time", default="", help="ISO-like timestamp; defaults to local now")
    args = parser.parse_args()

    timestamp = args.time or format_timestamp(datetime.now())
    args.audit_file.parent.mkdir(parents=True, exist_ok=True)
    with args.audit_file.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {timestamp} - {args.tool}\n\n")
        handle.write("### Prompt\n\n")
        handle.write(args.prompt.strip() + "\n\n")
        handle.write("### AI Output\n\n")
        handle.write(args.output.strip() + "\n\n")
        handle.write("### Human Review\n\n")
        handle.write((args.review.strip() or "Pending human review.") + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

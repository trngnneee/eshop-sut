#!/usr/bin/env python3
"""Append one HW04-style HW05 audit Interaction entry."""

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


def interaction_number(interaction_id: str) -> int:
    match = re.search(r"\binteraction-(\d+)", interaction_id)
    if not match:
        raise SystemExit(
            "Interaction ID must include a chronological number, "
            "e.g. interaction-007-spike-design"
        )
    return int(match.group(1))


def normalize_tool(tool: str) -> str:
    cleaned = tool.strip()
    if cleaned.lower() in {"codex gpt-5", "codex (gpt-5)", "gpt-5"}:
        return "Codex (GPT-5)"
    return cleaned


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


def quote_prompt(prompt: str) -> str:
    lines = neutralize_heading_markers(prompt).splitlines() or [""]
    return "\n".join(f"  > {line}" if line else "  >" for line in lines)


def format_content(content: str) -> str:
    lines = neutralize_heading_markers(content).splitlines() or [""]
    return "\n".join(f"  {line}" if line else "  " for line in lines)


def review_result(status: str, explicit: str) -> str:
    if explicit.strip():
        return " ".join(neutralize_heading_markers(explicit).split())
    mapping = {
        "Pending Human Review": "Đang chờ người dùng review.",
        "Approved": "Chấp nhận.",
        "Approved with Corrections": "Đã chỉnh sửa và được chấp nhận.",
        "Rejected": "Bị từ chối / không còn hiệu lực.",
        "Completed": "Hoàn tất.",
    }
    return mapping[status]


def ensure_report_scaffold(text: str) -> str:
    if text.strip():
        return text
    return (
        "# AI Audit Report - HW05 Performance Testing\n\n"
        "Tôi sử dụng công cụ AI để hỗ trợ các công việc trong quá trình thực hiện HW05 Performance Testing.\n\n"
        "## Nhật ký tương tác\n\n"
        "## Tổng hợp công cụ sử dụng\n\n"
        "| Công cụ | Mục đích sử dụng | Số lượt tương tác |\n"
        "|---|---|---:|\n"
        "| Codex (GPT-5) | Thiết kế test, sinh JMeter test plan, phân tích kết quả, đề xuất tối ưu, chỉnh sửa test plan theo human review, cập nhật audit log | 0 |\n"
    )


def insert_before_summary(text: str, entry: str) -> str:
    marker = "\n## Tổng hợp công cụ sử dụng"
    if marker in text:
        index = text.index(marker)
        return text[:index].rstrip() + "\n\n" + entry.rstrip() + "\n" + text[index:]
    return text.rstrip() + "\n\n" + entry.rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("audit_file", type=Path)
    parser.add_argument("--id", required=True, help="Stable Interaction ID")
    parser.add_argument("--title", required=True, help="Vietnamese Interaction title")
    parser.add_argument("--tool", required=True, help="AI tool name")
    parser.add_argument("--prompt", required=True, help="Exact original user prompt")
    parser.add_argument("--output", required=True, help="Vietnamese AI output summary")
    parser.add_argument(
        "--review-result",
        default="",
        help="Vietnamese final review result for this Interaction",
    )
    parser.add_argument(
        "--status",
        default="Pending Human Review",
        choices=sorted(VALID_STATUSES),
        help="Lifecycle status used to derive review result when omitted",
    )
    parser.add_argument("--scenario", default="", help="Accepted for compatibility; not rendered")
    parser.add_argument("--triggered-by", default="", help="Accepted for compatibility; not rendered")
    parser.add_argument("--time", default="", help="Timestamp; defaults to local now")
    args = parser.parse_args()

    timestamp = args.time or format_timestamp(datetime.now())
    number = interaction_number(args.id)
    args.audit_file.parent.mkdir(parents=True, exist_ok=True)

    existing = args.audit_file.read_text(encoding="utf-8") if args.audit_file.exists() else ""
    existing = ensure_report_scaffold(existing)
    start_marker = f"<!-- AUDIT_ENTRY:{args.id}:START -->"
    if start_marker in existing:
        raise SystemExit(f"Audit entry already exists: {args.id}")

    entry = "\n".join(
        [
            start_marker,
            f"### [{number}] {args.title.strip()}",
            "",
            f"- **Công cụ:** {normalize_tool(args.tool)}",
            f"- **Thời gian:** {timestamp}",
            "- **Prompt:**",
            quote_prompt(args.prompt),
            "- **Output:**",
            format_content(args.output),
            f"- **Kết quả sau review:** {review_result(args.status, args.review_result)}",
            f"<!-- AUDIT_ENTRY:{args.id}:END -->",
        ]
    )

    args.audit_file.write_text(insert_before_summary(existing, entry), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

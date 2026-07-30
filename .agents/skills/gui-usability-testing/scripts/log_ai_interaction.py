#!/usr/bin/env python3
"""
Append one AI Audit Report entry to an ai_audit_log.md file, in the format
required by HW03 §9 (tool, date/time, prompt, output).

Usage:
  log_ai_interaction.py --log <path/to/ai_audit_log.md> \
      --tool "Claude (claude.ai)" \
      --task "GUI checklist generation - IA-02 Forms, Checkout screen" \
      --prompt "Generate 10-15 GUI checklist items for IA-02 Forms on Checkout..." \
      [--output "<inline output text>"] \
      [--output-file <path to a file whose content is the AI output>] \
      [--review "<human review notes; can be added later by hand-editing>"] \
      [--datetime "2026-07-29 14:30"]   (defaults to now, local time)

If both --output and --output-file are omitted, the entry is written with a
placeholder the user must fill in — this script never fabricates output text.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path


def next_index(log_text: str) -> int:
    matches = re.findall(r"^### Interaction #(\d+)", log_text, flags=re.MULTILINE)
    if not matches:
        return 1
    return max(int(m) for m in matches) + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--log", required=True, help="Path to ai_audit_log.md (created if missing)")
    ap.add_argument("--tool", required=True, help='e.g. "Claude (claude.ai)"')
    ap.add_argument("--task", required=True, help="One-line description of the task")
    ap.add_argument("--prompt", required=True, help="The exact prompt/instruction used")
    ap.add_argument("--output", default=None, help="Inline AI output text")
    ap.add_argument("--output-file", default=None, help="Path to a file containing the AI output")
    ap.add_argument("--review", default="<< fill in after human review >>", help="Human review notes")
    ap.add_argument("--datetime", default=None, help="YYYY-MM-DD HH:MM (defaults to now)")
    args = ap.parse_args()

    log_path = Path(args.log)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else (
        "# AI Audit Report\n\n"
        "**Declaration:** I use AI tools for the following tasks: << fill in >>.\n\n"
        "---\n\n"
    )

    idx = next_index(existing)
    when = args.datetime or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if args.output is not None:
        output_block = args.output.strip()
    elif args.output_file is not None:
        out_path = Path(args.output_file)
        if not out_path.exists():
            print(f"warning: --output-file {out_path} does not exist; writing a pointer only", file=sys.stderr)
            output_block = f"(see file: {out_path})"
        else:
            content = out_path.read_text(encoding="utf-8", errors="replace")
            excerpt = content if len(content.splitlines()) <= 30 else "\n".join(content.splitlines()[:30]) + "\n... (truncated, see file)"
            output_block = f"(full output in: {out_path})\n\n```\n{excerpt}\n```"
    else:
        output_block = "<< paste AI output here >>"

    entry = f"""### Interaction #{idx}
- **Tool:** {args.tool}
- **Date/Time:** {when}
- **Task:** {args.task}
- **Prompt:**
  > {args.prompt}
- **AI Output:**
{output_block}
- **Human Review Notes:** {args.review}

"""

    with log_path.open("a", encoding="utf-8") as f:
        if not existing.endswith("\n\n") and log_path.exists():
            f.write("\n")
        f.write(entry)

    print(f"Logged interaction #{idx} to {log_path}")


if __name__ == "__main__":
    main()
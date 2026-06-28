#!/usr/bin/env python3
"""
audit_log_extractor.py
----------------------
Generates a structured AI Audit Log entry to be appended to ai-audit.md.
Run this at the end of each AI session.

Usage:
    python audit_log_extractor.py

It will interactively ask for the required fields, then print and save the
formatted Markdown entry.
"""

from datetime import datetime


def prompt(label: str, required: bool = True) -> str:
    while True:
        val = input(f"{label}: ").strip()
        if val or not required:
            return val
        print("  (this field is required)")


def main():
    print("=" * 60)
    print("  AI Audit Log Entry Generator")
    print("  Fill in each field. Press Enter to submit.")
    print("=" * 60)

    tool = prompt("AI tool name (e.g. Claude Sonnet 4.6, ChatGPT-4o)")
    dt_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"  (auto-detected date/time: {dt_str})")
    task = prompt("Task performed (e.g. Domain Testing for FR-01)")
    feature = prompt("Feature ID (e.g. FR-01)")
    the_prompt = prompt("Paste your prompt (or summary of it)")
    ai_output = prompt("Summary of AI output")
    corrections = prompt("Human corrections made (enter 'None' if none)", required=False) or "None"

    entry = f"""
### AI Audit Entry — {feature}

| Field       | Value |
|-------------|-------|
| Tool        | {tool} |
| Date & Time | {dt_str} (UTC+7) |
| Task        | {task} |

**Prompt used:**
> {the_prompt}

**AI Output Summary:**
> {ai_output}

**Human Corrections Made:**
> {corrections}

---
"""

    output_file = "ai-audit.md"
    with open(output_file, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"\n✅ Entry appended to {output_file}")
    print("\n--- Preview ---")
    print(entry)


if __name__ == "__main__":
    main()

# AI Audit Logging Format (§9 of the assignment)

The assignment requires, for every AI interaction:
- Name of the AI tool
- Date and time
- The prompt used
- The AI output

## When to log

Log an entry any time an AI-generated result ends up (even partially) in a graded deliverable:
- A GUI checklist generation pass (per IA, per gap-review pass)
- Drafted probe questions / task scenario candidates
- Drafted bug report entries
- Synthesis/clustering of usability session notes
- SUS/UEQ-S score computation (even though this is deterministic, log it as "AI-assisted scoring" for traceability, since the assignment says "the entire process of using AI must be recorded")
- Any AI Critique drafting help

Do NOT log: purely mechanical file operations with no generative content (e.g., just copying a template file).

## Entry format (Markdown, appended to `ai_audit_log.md`)

```markdown
### Interaction #<n>
- **Tool:** Claude (Claude.ai / Claude Code — note the surface if relevant)
- **Date/Time:** <YYYY-MM-DD HH:MM local time>
- **Task:** <one line, e.g. "GUI checklist generation — IA-02 Forms, Checkout screen">
- **Prompt:**
  > <the exact instruction/prompt used>
- **AI Output:**
  <the output, or "see <file path>" if long (>30 lines) — always include at least a short excerpt inline even when pointing to a file>
- **Human Review Notes:** <what the user changed, accepted as-is, or rejected — fill this in after human review; do not leave blank>
```

Keep a running `<n>` counter across the whole project (not reset per screen).

## Declaration line (top of the audit report, filled in once)

If AI was used at all:
> "I use AI tools for the following tasks: [list — e.g. GUI checklist drafting, usability instrument drafting, session-notes synthesis, bug report drafting]."

If AI was not used at all for a given deliverable, that specific declaration must say so explicitly — don't leave it implicit.

## Human Review Notes — why this matters

The assignment's §2 "Human review" principle is graded. An audit log with every "Human Review Notes" field saying "accepted as-is" for 40+ items is a red flag that no real review happened. Encourage the user to actually edit/reject some AI items — and log the outcome honestly.
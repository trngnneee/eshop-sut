# AI Audit Report — Entry Template

Append one entry per generation stage (or per meaningful AI interaction) to
`ai_audit_log.md`, in this format, so the log satisfies the assignment's
Section 9 requirement directly:

```markdown
## Entry N

- **Tool**: <e.g. Claude Sonnet 5 via Claude Code>
- **Date/time**: <YYYY-MM-DD HH:MM local>
- **Stage**: <Parse | Domain Partition | State Transition | Security |
  Schema Validation | Audit | Extension | Export>
- **Endpoint**: <METHOD /path>
- **Prompt / instruction followed**: <the specific instruction for this
  stage — quote the relevant line(s) from SKILL.md or your own added
  instruction, not the whole file>
- **Output summary**: <N cases produced; brief description of what was
  covered; any "not applicable" verdicts recorded (esp. for Security stage)>
- **Human corrections made**: <what you changed after review, if any>
```

Keep entries specific enough that a TA could reconstruct the stage from the
log alone — vague entries like "asked AI to generate tests" don't meet the
assignment's bar of showing the technique was applied step by step.

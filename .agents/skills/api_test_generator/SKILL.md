---
name: api_test_generator
description: Generate auditable API test cases from a compact endpoint specification using partition, state, security, and schema techniques.
---

# API test generator skill

Use this skill when an API endpoint needs a repeatable AI-assisted test inventory. The output is a candidate suite, not an oracle; compare every expected result with the API specification, business requirements, and SUT before execution.

## Required five-step process

1. **P1 — input/state model:** list every parameter (location, type, requiredness, constraint) and every state/precondition.
2. **P2 — partition/BVA:** create valid, invalid, type and boundary partitions; one negative partition per case.
3. **P3 — state transition:** enumerate allowed, forbidden, and terminal transitions; for a matrix, do not skip cells.
4. **P4 — security:** cover auth/JWT, IDOR, role escalation, injection and sensitive-data leakage where applicable.
5. **P5 — schema:** check status, content type, required fields, field types and sensitive fields without inventing an undocumented exact schema.

Then run the audit hook: stable IDs, duplicate detection, missing expected result, unsupported oracle assumptions, and a human-review checkpoint. Append an AI-audit entry with tool, timestamp, full prompt and output paths.

## Reusable commands

```powershell
python .agents/skills/api_test_generator/scripts/generate_api_tests.py .agents/skills/api_test_generator/examples/login.endpoint.json
python hw06/test-generator/generator.py .agents/skills/api_test_generator/examples/login.endpoint.json --out generated.md
```

## Output contract

Every case has `TC-API-<domain>-###`, group, technique, precondition, data, expected result, requirement and source. Render Markdown and a Postman skeleton. Never mark a case human-approved automatically; retain the reviewer/sign-off fields for the student.

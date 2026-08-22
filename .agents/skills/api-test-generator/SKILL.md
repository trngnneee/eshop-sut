---
name: api-test-generator
description: Drive an AI-first, multi-step pipeline that turns an API specification (e.g. EShop's api_specification.md) into a reviewed, exported set of API test cases covering domain partitions, state transitions, security (SEC-01–SEC-07), and schema validation. Use this skill whenever the user is doing API testing homework/coursework that requires generating test cases from a spec "step by step, not with a single generic prompt", auditing AI-generated test cases as VALID/INVALID/INCOMPLETE, extending them with human-found gaps, or exporting to a Postman collection / Excel test-case sheet. Trigger this for requests like "generate test cases for this API", "build an API test generator", "audit these AI test cases", or "export test cases to Postman/Excel", even if the user doesn't say "skill" explicitly.
---

# API Test Generator (AI-driven, human-audited)

This skill turns an API specification into a reviewed set of test cases through
four **separate, targeted stages** instead of one generic prompt. Each stage
has its own checklist so coverage is deliberate, not accidental. The skill
also produces the audit trail, extension, and export artifacts required by
API-testing coursework that grades the *process*, not just the output.

## When to use this

- The user gives you (or points you to) an API specification and asks for
  test cases, a "test generator", or help auditing/extending AI-made test
  cases.
- The user asks to export test cases to Postman (`.json` collection) or
  Excel (`.xlsx`).
- The user asks you to log an AI Audit Report entry for a generation session.

## Pipeline overview

```
spec file ─▶ [1 Parse] ─▶ endpoint model (JSON)
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │   Stage A: Domain Partition & Boundary       │
        │   Stage B: State Transition                  │
        │   Stage C: Security (SEC-01..SEC-07)         │
        │   Stage D: Schema Validation                  │
        └─────────────────────────────────────────────┘
                              │  (each stage run as its own prompt/pass)
                              ▼
                     draft test cases (JSON)
                              │
                              ▼
                [2 Audit] Claude + human label each case
                 VALID / INVALID / INCOMPLETE + reasoning
                              │
                              ▼
              [3 Extend] ≥5 human-found gap cases added
                              │
                              ▼
        [4 Export] scripts/export_excel.py, export_postman.py
```

Run the stages **one at a time in the conversation** (this is what "guide
the AI step by step" means in the assignment) — don't collapse Stage A–D
into one mega-prompt. Show the user the output of each stage before moving
to the next so they can redirect early if a stage goes off track.

## Step 1 — Parse the spec

Run the parser to turn the markdown/OpenAPI spec into a structured endpoint
model. This is deterministic (not AI-guessed) so downstream stages have a
reliable contract to work from.

```bash
python3 scripts/parse_spec.py <path-to-api_specification.md> --endpoint "METHOD /path" --out endpoint_model.json
```

- If `--endpoint` is omitted, it lists all endpoints found so the user can
  pick one.
- The parser looks for common markdown spec conventions (`### METHOD /path`
  headings, parameter tables, JSON response fences, an auth/role line, and
  a `SEC-0x` or state-machine mention). If the actual spec uses a different
  layout, open the file yourself, read the relevant section, and hand-build
  `endpoint_model.json` in the schema described in `references/test_case_schema.md`
  rather than fighting the regex parser — the parser is a convenience, not
  a hard requirement.
- Read `references/test_case_schema.md` for the exact fields expected.

## Step 2 — Generate, one stage at a time

For **each** stage below, read the matching reference file, then generate
test cases yourself (you are the "AI" in "AI-driven generator" — do the
reasoning, don't just template-fill). Append every case to a running
`test_cases.json` array using the schema in `references/test_case_schema.md`,
tagging each with `"stage"` and a short `"source_prompt_summary"` (for the
AI Audit Report later).

1. **Domain Partition & Boundary** — read `references/domain_partition_guide.md`.
   For every request parameter (path, query, body field, header), derive
   equivalence classes (valid, invalid-format, boundary, missing, wrong-type)
   per the guide. Aim for enough cases that combined with the other three
   stages you clear the assignment's **≥35 cases/API** target.
2. **State Transition** — read `references/state_transition_guide.md`. Only
   applies to stateful resources (e.g. FR-10 order lifecycle:
   `pending → confirmed → shipping → delivered`, plus cancellation rules).
   Generate both legal-path and illegal-transition cases.
3. **Security (SEC-01–SEC-07)** — read `references/security_checklist.md`.
   Walk every checklist item against the endpoint: does it apply? If yes,
   write a case (SQL/NoSQL injection, IDOR, broken auth, role escalation,
   mass assignment, rate limiting/lockout, sensitive-data exposure). If an
   item doesn't apply to this endpoint, say so explicitly in your output
   rather than skipping silently — that record is useful for the AI Critique
   section of the report.
4. **Schema Validation** — read `references/schema_validation_guide.md`.
   Generate cases asserting the success and error response shapes exactly
   match the spec (types, required fields, no extra/leaking fields, status
   codes).

After all four stages, print a short tally (cases per stage, running total)
so the user can see coverage before auditing.

## Step 3 — Audit (human review, AI-assisted)

Go through `test_cases.json` and propose a label for each case:
`VALID`, `INVALID`, or `INCOMPLETE`, with one-line reasoning, per
`references/test_case_schema.md`'s `audit` block. Present this as a table
for the user to confirm or override — **the user's judgment wins**; you are
drafting the audit, not finalizing it. For anything you mark
INVALID/INCOMPLETE, propose the corrected case inline rather than just
flagging the problem.

## Step 4 — Extend (find what the AI missed)

Before exporting, explicitly prompt yourself (and the user) with: *"What
would a security tester or a QA lead with domain context add that a
spec-only read would miss?"* Common blind spots to check — business-logic
abuse (e.g., coupon stacking, negative-quantity carts, race conditions on
stock), cross-resource IDOR that only shows up when two roles are combined,
and multi-step state races (two requests both trying to transition the same
order at once). Target **≥5** such cases, each tagged
`"stage": "human_extension"` with a `"why_ai_missed"` field explaining the
likely reason (prompt scope, spec silence, or model limitation) — this
feeds straight into the assignment's required "Extend" write-up.

## Step 5 — Export

```bash
python3 scripts/export_excel.py test_cases.json --out test_cases.xlsx
python3 scripts/export_postman.py test_cases.json --out collection.json \
    --base-url "{{baseUrl}}" --student-id-header "{{studentId}}"
```

- `export_postman.py` builds a Postman v2.1 collection with a
  **pre-request script on the collection root** that sets
  `X-Student-Id: {{studentId}}` on every request (per the assignment's
  anti-cheat requirement) and a `{{baseUrl}}` collection variable so it
  works against any environment (local/staging).
- `export_excel.py` writes one row per test case (id, stage, endpoint,
  input, expected, audit label, reasoning) — this is the "Excel test cases
  and test summary" submission artifact.
- Remind the user to run the collection with Newman and capture the HTML
  report; this skill does not execute tests, only generates and exports
  them (execution needs a live SUT).

## Optional — AI Audit Report entries

If asked to log the audit trail, append one entry per generation stage to
`ai_audit_log.md` using `references/audit_entry_template.md`: tool name,
timestamp, the exact prompt/instruction you followed for that stage, and a
trimmed summary of what you produced. Keep entries factual and specific
enough that a TA could reproduce the stage from the log alone.

## The self-drawn diagram requirement

The assignment explicitly requires the Section 7 diagram to be **self-drawn,
not AI-generated** — it's an anti-cheat check item. Do not hand the user a
finished diagram image to submit as-is. Instead:

1. Point them to `references/diagram_reference.md`, which has a plain-text
   description of this pipeline's boxes/arrows (the same structure as the
   ASCII diagram above) for them to redraw by hand in any tool (draw.io,
   paper + photo, PowerPoint shapes, etc.).
2. If they ask you to "make the diagram", clarify that you can describe the
   structure and even hand back a rough scaffold, but they need to be the
   one who lays it out/draws it for grading purposes — say this plainly
   rather than silently producing a finished image for them to submit.

## Files in this skill

- `scripts/parse_spec.py` — deterministic markdown/OpenAPI spec parser
- `scripts/export_excel.py` — test_cases.json → .xlsx
- `scripts/export_postman.py` — test_cases.json → Postman v2.1 collection.json
- `references/test_case_schema.md` — the JSON schema every test case must follow
- `references/domain_partition_guide.md` — equivalence partitioning / boundary rules
- `references/state_transition_guide.md` — state-machine test design guidance
- `references/security_checklist.md` — SEC-01–SEC-07 test templates
- `references/schema_validation_guide.md` — response-shape assertion guidance
- `references/diagram_reference.md` — plain-text structure for the required self-drawn diagram
- `references/audit_entry_template.md` — AI Audit Report entry format
- `references/pseudocode.md` — standalone pseudocode of the whole generator (for the Section 7 submission)

---
name: api-fr-testing
description: >-
  Apply black-box API testing to a functional requirement (FR) or REST endpoint of a
  system under test. Probes the running SUT with cURL to learn real behavior, then
  produces contract-based test cases across techniques (equivalence partitioning, boundary
  value analysis, state-transition, security SEC-01..07, JSON-schema, negative/contract),
  audits them (VALID/INVALID/INCOMPLETE), extends with source-derived cases, and packages
  everything into a Postman collection + Newman run. Use when the user asks to test an API,
  kiểm thử API, sinh test case cho endpoint / FR, build a Postman collection, or extend the
  suite to a new FR. Built from the HW06 EShop workflow but works for any FR/endpoint.
---

# API FR Testing

A repeatable pipeline for turning **one FR + its endpoint(s)** into a full, gradeable API
test suite. Follow the phases in order. Load the reference file named at each phase only
when you reach that phase.

## The one rule that everything hinges on

**Contract = spec, never implementation.** Expected results come from the FR / spec, *not*
from what the SUT actually returns. When the SUT deviates, that test is **supposed to FAIL** —
the failure *is* the bug report. Never soften an expected value to make a test green.
(Details + the other conventions: `references/methodology.md`.)

## Inputs you need before starting

- The FR text (from the requirements/README) and the endpoint(s) it maps to.
- The SUT source for that endpoint (route handler) and the DB schema — read them, don't guess.
- A running SUT you can hit (default `http://localhost:3000`).
- The submission constraints if any (e.g. a `X-Student-Id` header, host must be localhost).

## Phase 1 — Probe reality (cURL)

Before writing any expected value, learn what the SUT *actually* does. **Back up the DB first,
probe, then restore** so you never pollute seed data.

1. Read the route handler + DB schema for the endpoint.
2. Start the SUT, hit every branch with `curl -s -w "[%{http_code}]"` (valid, boundary,
   invalid, missing-auth, wrong-type). Record actual status + body + content-type.
3. Restore the DB. Write findings into an `api_specification.md` with two columns:
   **Spec (FR) = Expected** vs **Actual (SUT)**; every mismatch is a candidate bug.

See `references/methodology.md` → "Phase 1" for the backup/restore commands and the
spec-table template.

## Phase 2 — Generate test cases, one technique per prompt

Never ask an AI to "generate all test cases". Drive it technique-by-technique and save each
prompt+output (that log is the AI-audit evidence). The parameterized prompt sequence is in
`references/prompts.md`. Techniques, in order:

1. **Equivalence partitioning + boundary value** — one partition table per parameter.
2. **State-transition** — only if the FR defines a state machine; build the full
   from-state × action matrix + the fixture chain to reach each state.
3. **Security** — bind each case to a SEC-xx code with a real payload + assertion
   (no-token, wrong-role, forged JWT, SQLi, XSS, IDOR, mass-assignment).
4. **JSON-schema** — write a schema per response shape; one `pm.response.to.have.jsonSchema`
   test per response code.
5. **Negative / contract** — wrong method, bad Content-Type, malformed/empty/array body,
   missing required header.

Output format (paste-ready table), and TC-ID naming, are in
`references/methodology.md` → "Test-case format".

## Phase 3 — Audit (human review)

Re-read every generated case and tag it **VALID / INVALID / INCOMPLETE** with a reason and a
corrected version. Watch for the recurring AI mistakes (fabricated `201`, softened `404`,
payload-less security cases, missing fixtures, hard-coded ids, duplicate cases). Record
per-API VALID/INVALID/INCOMPLETE counts for the AI Critique. Checklist:
`references/methodology.md` → "Phase 3 audit checklist".

## Phase 4 — Extend with source-derived cases

Add ≥5 cases per API that a spec-only AI would miss — the ones you only find by reading the
source or probing (hidden branches, missing middleware, missing FK/unique, silent no-ops,
type coercion, race conditions, IDOR on adjacent endpoints). Verify each with cURL and tag
**why it was missed**: `[Prompt]` / `[Model]` / `[API]`. See `references/methodology.md`.

## Phase 5 — Package (Postman + Newman)

Build the collection, environment, CSV data files, and run with Newman. Structure, TC-ID
naming, the anti-cheat pre-request script, the Postman-feature checklist, and the exact
Newman commands are in `references/packaging.md`.

## Automating Phase 2 — the generator

`scripts/generator.py` is a runnable reference implementation of the 6-stage generator
(PARSE → CLASSIFY → GENERATE → DEDUPE+RANK → EMIT → SELF-CHECK) that turns an OpenAPI-style
spec into a test-case table + Postman items. The stage-by-stage design is in
`references/pseudocode.md`.

> **Diagram note:** if this skill is submitted for a course that forbids AI-generated
> diagrams, the architecture diagram must be **hand-drawn**. `references/pseudocode.md`
> describes the architecture in text so you can draw it yourself; do not export an
> AI-generated image as the deliverable.

---

## Demo video

Minh hoạ skill chạy end-to-end: https://drive.google.com/drive/folders/13lSkQF2vfeJV9PTGLdRy5Aptm-ZgceKb?usp=sharing

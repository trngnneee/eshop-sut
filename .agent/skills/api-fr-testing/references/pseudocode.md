# Generator design — 6-stage pipeline (pseudocode)

Input: an OpenAPI-style spec (with optional `x-test-*` hints) + a rule set (FR constraints,
SEC-01..07). Output: a test-case table (Markdown/CSV) + Postman collection items.

```
STAGE 1  PARSE
  spec        -> [ Endpoint{ method, path, params[], body_schema, auth_required, responses{} } ]
  rules       -> RuleSet{ fr_constraints{}, sec_codes[] }

STAGE 2  CLASSIFY
  for each param p:
    Domain(p) = { type, required, min, max, enum, format, exists_in? (FK) }

STAGE 3  GENERATE  (5 independent generators per endpoint)
  G1 PartitionGen : one valid class + one case per invalid class
  G2 BoundaryGen  : min-1, min, min+1, max-1, max, max+1  (+ non-canonical forms if strict)
  G3 StateGen     : if endpoint has a state machine ->
                      for (from_state, action) in states x actions:
                        expected = spec_transition(from_state, action)   # from SPEC, not SUT
                        emit case + fixture_chain(from_state)
  G4 SecurityGen  : for each applicable SEC code -> payload template
                      (no-token, empty-token, wrong-role, forged-token, SQLi, XSS, IDOR, mass-assign)
  G5 SchemaGen    : JSON Schema per response code -> one jsonSchema assertion each

STAGE 4  DEDUPE + RANK
  key = hash(endpoint, param, class);  merge duplicates
  priority = weight(security > state > boundary > partition) x (required_param ? 2 : 1)

STAGE 5  EMIT
  render Markdown/CSV rows  AND  Postman items (request + pm.test) from templates
  attach collection-level pre-request header (X-Student-Id)

STAGE 6  SELF-CHECK  (coverage gate for human review)
  assert: every param has >=1 valid AND >=1 invalid case
  assert: every FR constraint has >=1 case ; every applicable SEC has >=1 case
  print coverage-gap table  ->  human decides what to add (Phase 3/4)
```

Key invariant across all stages: **Expected comes from the spec/rules, never from a probe of
the SUT.** The SUT probe (skill Phase 1) only feeds the "Actual" column and bug mapping — it
must not be used to compute Expected, or bugs disappear.

## Architecture (draw this by hand for submission)

If a course forbids AI-generated diagrams, redraw the following as your own diagram — do not
export an AI image. The shape to draw:

- Two inputs on the left: **Spec (OpenAPI)** and **Rules (FR + SEC)** flowing into **PARSE**.
- A vertical spine: PARSE → CLASSIFY → GENERATE → DEDUPE+RANK → EMIT → SELF-CHECK.
- Off the **GENERATE** box, five parallel sub-boxes G1..G5 fanning out and merging back.
- A side input into GENERATE's G3/G4: **state machine** and **leaked-secret / SEC catalog**.
- Two outputs on the right of EMIT: **Test-case table (CSV/MD)** and **Postman collection**.
- A feedback arrow from **SELF-CHECK** back to a **Human review** box (Phase 3/4), and from
  Human review back into GENERATE (extend). This feedback loop is the point — the generator
  proposes, the human audits and extends.

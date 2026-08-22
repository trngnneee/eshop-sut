# Test Case Schema

Every generated test case is one JSON object appended to `test_cases.json`
(a top-level array). Keep field names exactly as below so the export
scripts work without modification.

```json
{
  "id": "TC-A-001",
  "stage": "domain_partition | state_transition | security | schema_validation | human_extension",
  "endpoint": "POST /api/auth/register",
  "title": "Register with email missing '@'",
  "category": "invalid-format",
  "priority": "high | medium | low",
  "preconditions": "No existing account with this email",
  "request": {
    "method": "POST",
    "path": "/api/auth/register",
    "headers": { "Content-Type": "application/json" },
    "query": {},
    "body": { "email": "userexample.com", "password": "Abcd1234!" }
  },
  "expected": {
    "status": 400,
    "body_contains": { "error": "string" },
    "schema_ref": "ErrorResponse"
  },
  "sec_ref": null,
  "fr_ref": "FR-01",
  "why_ai_missed": null,
  "source_prompt_summary": "Stage A domain-partition pass over 'email' field",
  "audit": {
    "label": "VALID | INVALID | INCOMPLETE | null",
    "reasoning": null,
    "corrected_from": null
  }
}
```

## Field notes

- **id**: prefix by stage — `TC-A-*` domain partition, `TC-S-*` state
  transition, `TC-SEC-*` security, `TC-SCH-*` schema validation,
  `TC-EXT-*` human extension. Zero-padded 3 digits.
- **category**: free text but be consistent within a stage, e.g. for domain
  partition use `valid | boundary-low | boundary-high | invalid-format |
  missing | wrong-type | empty`.
- **sec_ref**: one of `SEC-01`..`SEC-07` when `stage == security`, else `null`.
- **fr_ref**: the functional requirement ID from the assignment (FR-01..FR-19)
  this case traces back to, for traceability in the report.
- **why_ai_missed**: required (non-null) only for `human_extension` cases —
  one sentence: prompt-scope gap, spec silence, or model limitation.
- **audit.label**: filled during Step 3 (Audit). Leave `null` until then.
- **expected.body_contains**: a *shape*, not literal values — keys mapped to
  their expected JSON type (`"string"`, `"number"`, `"boolean"`, `"array"`,
  `"object"`), used both as documentation and as input to schema checks.

Keep `test_cases.json` as a single flat array across all stages and all
three chosen APIs (or split per-API file, `test_cases_api1.json` etc., if
the user prefers) — either is fine as long as it's consistent going into
the export scripts.

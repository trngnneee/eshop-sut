# Stage D — Schema Validation Guide

Goal: prove the response *shape* — not just the status code — exactly
matches what the spec promises, for both success and error responses.

## Procedure

1. From the spec, extract the documented response schema for each status
   code the endpoint can return (e.g. `200` success body, `400` validation
   error body, `401`/`403`/`404` error bodies, `409` conflict).
2. For each schema, write cases that assert:
   - **Required fields present** — every field marked required in the spec
     appears in the response.
   - **Types match** — each field's JSON type matches the spec (string vs
     number vs boolean vs array vs object vs null).
   - **No extra/leaking fields** — the response doesn't include
     undocumented fields (ties into SEC-07 — flag overlap cases).
   - **Enum/status fields only take documented values.**
   - **Array item shape** — for list endpoints, validate the shape of one
     representative item, plus that pagination metadata (if any) is present
     and correctly typed.
   - **Nullability** — fields the spec marks nullable can legitimately be
     `null`; fields not marked nullable must never be `null`.
3. Where the spec doesn't fully define a schema (common in lightweight
   specs), infer a reasonable schema from an example response if one is
   given, note the inference explicitly in the case's title (e.g. "schema
   inferred from example, not formally specified — flag in report"), and
   still write the case — an inferred, labeled assumption is more useful
   than skipping schema coverage entirely.

## Output

Each case: `"stage": "schema_validation"`, `expected.schema_ref` naming the
schema (e.g. `ProductListResponse`, `ErrorResponse`), and
`expected.body_contains` listing field → type pairs to assert against.
These pair naturally with Postman test scripts using `pm.response.to.have
.jsonSchema(...)` or manual `pm.expect(typeof body.field).to.eql(...)`
assertions — mention this in the case description so the execution phase
can translate directly into Postman tests.

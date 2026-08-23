# AI Audit Report

I use AI tools for the following tasks:

## Stage 1 - Generate (Domain Partitions)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-22 13:03

**Prompt:**
```
Scope: FR-04 PUT /api/users/me | FR-07 POST /api/cart | FR-19 DELETE /api/admin/users/:id | @Repo/eshop-sut
Using api testing skill requirement and @.cursor/rules/skill-01-domain-testing.mdc to design and generate all domain partitions test cases for the scope above
```

**Output:**
```
Stage 1 Domain partitions only (Skill-01 + API testing checklist). No Postman, Newman, or security/state/schema suites.

Sources: Repo/eshop-sut/README.md (FR-04, FR-07, FR-19, FR-06 qty, FR-12, SEC-02/03/06) and api_specification.md bodies/headers.

Module codes: PROFILE, CART, ADMINUSERS.

Counts: 40 PROFILE (TC-PROFILE-001..040) + 39 CART (TC-CART-001..039) + 20 ADMINUSERS (TC-ADMINUSERS-001..020) = 99 DomainPartition cases.

Method: per-variable valid/invalid sub-domains; 1×1 representative values; on-point (all valid) + off-point (one invalid, others valid); business-rule extras (role/email immutability; cart merge; admin self-delete). Combination cases: TC-PROFILE-003 (unicode name + 11-digit phone + unicode address), TC-CART-002 (id=1 and qty=1).

Assumptions flagged with ⚠️: HTTP 400/401/403/404 when spec omits codes; name/phone/address treated as required; cart id must exist; client price/name must not spoof catalogue; no max length for name/address; deleting another admin unspecified.

Artifacts under SoftwareTesting-HW/HW06/23127271/:
- docs/domain-testing-report.md (Steps 1–5)
- tests/test-cases/{profile,cart,admin-users}/*.md (Skill-01 per-TC files)
- sheets/domain-partitions.csv (API template columns; Source=AI; AuditStatus blank)
- scripts/generate_domain_partitions.py
- README.md

Oracles are spec-based, not seed-SUT behaviour (PUT me currently accepts role; POST /api/cart appends without merge/validation; DELETE /api/admin/users/:id has no admin/self checks).

Not in this drop: Stage 2 audit labels, Stage 3 human-found cases, Postman collection, Newman run, bug reports.
```

---

## Stage 2 - Audit (human review)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-22 13:28

**Prompt:**
```
Label each AI-generated test case VALID / INVALID / INCOMPLETE with reasoning, and correct the invalid or incomplete ones. Dont assume anything, just reason if the requirement was missing.

| P-NAME-05 | Field omitted | Invalid ⚠️ assumed required | (omit name) | is assumed
```

**Output:**
```
Stage 2 audit of 99 domain-partition cases against written SRS + api_specification.md only.

Rule: if the spec does not say a field is required, a value is invalid, or a status code, do not expect rejection.

Counts: VALID 16, INVALID 42, INCOMPLETE 41.

P-NAME-05 / TC-PROFILE-010 = INVALID. FR-04 lists name as updatable; API example includes name; neither says mandatory on every PUT. Corrected: do not expect rejection; observe stored name; email/role unchanged.

Same INVALID pattern: omit/empty name, omit phone, omit/empty address, empty/array body, Content-Type, cart id/qty/price/name required-or-invalid (including FR-06 qty on POST /api/cart and FR-15 price on cart), admin id format / 404 / repeat delete.

INCOMPLETE: real FR-04 phone-format and auth/role/self-delete partitions that pinned undocumented HTTP 400/401/403; unspecified max length/coercion/extra fields that assumed accept.

VALID kept: typical updates, 10/11-digit phones, role/email immutability, cart merge, admin delete-other-user, path :id as the documented identifier.

Corrections applied in place on each TC-*.md Expected result + Audit section, CSV AuditStatus/AuditReasoning, docs/stage2-audit.md.
```

---

## Stage 3 - Extend (Human domain partitions)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-22 13:52

**Prompt:**
```
Add at least five domain partitions test cases that the current AI missed and explain why the AI missed them (prompt quality, model limitations, or characteristics of the API)
```

**Output:**
```
Stage 3: 6 human-found domain-partition SUP cases (≥5 required).

TC-PROFILE-SUP-001 partial phone-only PUT — prompt quality (example triple bias).
TC-PROFILE-SUP-002 fullwidth Unicode phone — model limitation (ASCII-only digits).
TC-PROFILE-SUP-003 duplicate JSON phone key — API/JSON parser + model unique keys.
TC-CART-SUP-001 same id different name merge — API characteristic (undefined product identity).
TC-CART-SUP-002 merge 2+3 — prompt quality / 1×1 (only 1+1 before).
TC-ADMINUSERS-SUP-001 percent-encoded path id — model limitation (URI not in spec).

Artifacts: tests/test-cases/*/TC-*-SUP-*.md, docs/stage3-extend.md, CSV rows Source=Human.
```

---

## Stage 1 - Generate (State Transitions)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-22 14:20

**Prompt:**
```
Using api testing skill requirement and state-transition-skill generate all state transitions test cases for the scope above (FR-04, FR-07, FR-19)
```

**Output:**
```
Stage 1 State transitions (API testing checklist section 2 — no dedicated state-transition skill file; method from references/test-design-checklist.md).

State models:
- FR-04 PUT /api/users/me: profile snapshot P0→P1→Pn; immutables email/role; partial-update chain; session persistence.
- FR-07 POST /api/cart: C_EMPTY→C_SINGLE→C_MERGED/C_MULTI; FR-07 merge; FR-08 checkout→C_EMPTY cross-endpoint.
- FR-19 DELETE /api/admin/users/:id: U_EXISTS→U_DELETED terminal; U_SELF blocked; list N→N-1; auth/role illegal transitions.

Counts: 12 PROFILE (TC-PROFILE-ST-001..012) + 15 CART (TC-CART-ST-001..015) + 15 ADMINUSERS (TC-ADMINUSERS-ST-001..015) = 42 StateTransition cases.

Combined AI Stage-1 (domain + state): FR-04 52, FR-07 54, FR-19 35 — meets >=35 per API before security/schema.

Artifacts:
- docs/state-transition-report.md
- tests/test-cases/{profile,cart,admin-users}/TC-*-ST-*.md
- sheets/state-transitions.csv (Category=StateTransition, Source=AI, AuditStatus blank)
- scripts/generate_state_transitions.py

Oracles spec-only; cascade delete+orders and partial PUT semantics flagged unspecified.
```

---

## Stage 2 - Audit (State Transitions)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-22 14:35

**Prompt:**
```
Based on coverage checking, label each AI-generated state-transition test case VALID/INVALID/INCOMPLETE with reasoning, and correct invalid/incomplete ones.
```

**Output:**
```
42 state-transition cases audited: 33 VALID, 0 INVALID, 9 INCOMPLETE.

INCOMPLETE (9): TC-PROFILE-ST-005 (persistence medium), ST-010 (rollback on reject),
TC-CART-ST-011 (FR-10 order side effect dropped), ST-013 (mislabelled illegal transition),
TC-ADMINUSERS-ST-002 (HTTP unspecified), ST-003 (404 preference removed), ST-011 (login HTTP),
ST-013 (DELETE body inferred), ST-015 (404 expected removed).

Artifacts: docs/stage2-audit-state-transitions.md, updated TC-*-ST-*.md Audit sections,
sheets/state-transitions.csv AuditStatus/AuditReasoning/ExpectedResult corrected.
scripts/apply_stage2_audit_state_transitions.py
```

---

## Stage 3 - Extend (State Transitions — human SUP)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-22 14:50

**Prompt:**
```
Add at least five state transition test cases per API that the AI missed (INVALID, concurrency/race, others) with why missed.
```

**Output:**
```
15 human ST-SUP cases (5 per FR): TC-*-ST-SUP-001..005 per module.

Gap themes: concurrency/race (7), illegal/failed transitions (4), missing legal merge/partial paths (3), terminal session/JWT (2).

New in this batch (003-005): PROFILE cross-field race, malformed JWT mid-flow, address-first partial;
CART merge line 3, checkout||add race; ADMIN old JWT after delete, delete with live session, DELETE||GET list race.

Sheet: 42 AI + 15 Human = 57 rows in state-transitions.csv.
docs/stage3-extend-state-transitions.md, scripts/append_stage3_st_sup_cases.py (idempotent).
```

---

## Stage 1 - Generate (Security)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-23 23:10

**Prompt:**
```
Use api testing skill to design and Generate test case for security testing
```

**Output:**
```
40 security cases mapped to SEC-01..SEC-06 for FR-04 PUT /api/users/me, FR-07 POST/GET /api/cart, FR-19 DELETE /api/admin/users/:id.

PROFILE (14): SEC-05 SQLi name/phone/address/Auth header; SEC-04 XSS/polyglot; SEC-06 role/password/email/mass-assignment; SEC-02 auth bypass/tampered JWT.

CART (12): SEC-02 auth/IDOR GET; SEC-05 SQLi name/id/header/NoSQL string; SEC-04 XSS; SEC-06 price tampering, user_id/role mass assignment.

ADMINUSERS (14): SEC-02/03 auth and role; SEC-05 path/body/header SQLi; SEC-01 password never in list/error/success bodies; FR-19 self-delete.

SEC-07 (OTP) documented as gap — forgot-password endpoints not in scope.

Combined Stage-1 AI: FR-04 66, FR-07 66, FR-19 49 (domain+state+security).

Artifacts: docs/security-testing-report.md, sheets/security-tests.csv, scripts/generate_security_tests.py, TC-*-SEC-*.md
Oracles spec-only — no invented HTTP codes.
```

---

## Stage 3 - Extend (Security — human SEC-SUP)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-23 23:20

**Prompt:**
```
Add at least five security test cases per API that the AI missed (INVALID cases, concurrency/race cases and others missing) and explain why the AI missed them.
```

**Output:**
```
15 human SEC-SUP cases (5 per FR): TC-*-SEC-SUP-001..005 per module.

Gap themes: concurrency/race (5), illegal/privilege/integrity (5), encoding/parser bypass (5).

PROFILE: race role=admin PUT, mass-assignment id, null-byte, Content-Type text/plain, race XSS vs SQLi.
CART: race price tampering, negative qty, race GET||POST, Unicode XSS bypass, qty overflow.
ADMIN: unauthenticated GET list, user JWT on GET list (SEC-03), parallel DELETE race, path id -1, encoded slash traversal.

Sheet: 37 AI + 15 Human = 52 rows in security-tests.csv.
docs/stage3-extend-security.md, scripts/append_stage3_sec_sup_cases.py (idempotent).
Combined Stage-1: FR-04 71, FR-07 70, FR-19 52.
```

---

## Stage 2 - Audit (Security — AI cases)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-23 23:40

**Prompt:**
```
Label each AI-generated security test case VALID/INVALID/INCOMPLETE with reasoning, and correct invalid/incomplete ones.
```

**Output:**
```
37 AI security cases audited: 31 VALID, 1 INVALID, 5 INCOMPLETE.

INVALID (1): TC-CART-SEC-006 — oracle invented FR-07/SEC-06 cart price rejection; FR-08 checkout rule only.

INCOMPLETE (5): TC-PROFILE-SEC-008 (SEC-06 mis-tag, password is SEC-01/FR-04),
TC-PROFILE-SEC-012 (lockout bypass invented), TC-CART-SEC-008 (SEC-06 mis-tag),
TC-CART-SEC-010 (SQLite assumption), TC-ADMINUSERS-SEC-003 (FR-19 not SEC-03).

Artifacts: docs/stage2-audit-security.md, updated TC-*-SEC-*.md Audit sections,
sheets/security-tests.csv AuditStatus/AuditReasoning/ExpectedResult corrected.
scripts/apply_stage2_audit_security.py
```

---

## Stage 1 - Generate (Schema validation)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-23 23:45

**Prompt:**
```
Use api testing skill to design and Generate test case for Schema validation
```

**Output:**
```
42 schema validation cases for FR-04 GET/PUT /api/users/me, FR-07 GET/POST /api/cart, FR-19 GET/DELETE /api/admin/users.

PROFILE (14): GET object field types (name/phone/shipping_address/email/role), SEC-01 no password,
PUT request 3-field schema, PUT/GET Content-Type, type coercion probes, empty body, auth error shape observe.

CART (14): GET array/empty [], line item id/name/price/quantity types, POST 4-field schema,
POST success envelope observe, merge array length, malformed array root, unauth error observe.

ADMINUSERS (14): GET list array, element object schema, id/name/email/role types,
SEC-01 no password/password_hash, DELETE response observe, seed list validation, user JWT error observe,
post-delete list schema.

Oracles spec-only — gaps documented for undocumented success/error envelopes; no invented HTTP codes.

Combined Stage-1: FR-04 85, FR-07 84, FR-19 66.

Artifacts: docs/schema-validation-report.md, sheets/schema-validation.csv,
scripts/generate_schema_validation.py, TC-*-SCH-*.md
```

---

## Stage 2 - Audit (Schema validation — AI cases)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-24 00:15

**Prompt:**
```
Fill Audit status for Schema validation 
```

**Output:**
```
42 AI schema cases audited: 37 VALID, 0 INVALID, 5 INCOMPLETE.

INCOMPLETE (5): TC-PROFILE-SCH-002/003/004 (GET profile fields not in api_spec — reworded to if-returned + record-if-absent),
TC-ADMINUSERS-SCH-003/004 (admin list id/name types inferred, not documented).

Artifacts: docs/stage2-audit-schema.md, updated TC-*-SCH-*.md Audit sections,
sheets/schema-validation.csv AuditStatus/AuditReasoning/ExpectedResult corrected.
scripts/apply_stage2_audit_schema.py. Rebuilt all-test-cases.csv/xlsx.
```

---

## Stage 3 - Extend (Summary + Schema SCH-SUP)

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-23 23:52

**Prompt:**
```
Add at least five test cases of your own that the AI missed — especially around security and state transitions — and explain why the AI missed them.
```

**Output:**
```
Confirmed existing human extensions: 15 ST-SUP + 15 SEC-SUP (5 per FR each) with why-AI-missed in
docs/stage3-extend-state-transitions.md and docs/stage3-extend-security.md.

Added schema gap batch: 15 SCH-SUP (5 per FR) — append_stage3_sch_sup_cases.py, docs/stage3-extend-schema.md.

Created docs/stage3-extend-summary.md consolidating all 60 human cases across 4 categories.

Human totals: domain 15, ST 15, SEC 15, SCH 15. Security+ST = 30 cases with concurrency, illegal transitions, encoding bypass themes.
```

---

## Stage 3 — Human SUP audit

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-24 00:05

**Prompt:**
```
Label each human test case VALID / INVALID / INCOMPLETE with reasoning, and correct the invalid or incomplete ones @sheets
```

**Output:**
```
Audited all 60 human SUP rows across 4 CSVs: 49 VALID, 1 INVALID, 10 INCOMPLETE.

Corrections: TC-CART-SEC-SUP-001 (INVALID — invented cart price rule); TC-ADMINUSERS-ST-SUP-003/004,
TC-CART-ST-SUP-003/005, TC-PROFILE-SEC-SUP-002, TC-CART-SEC-SUP-002/005, TC-ADMINUSERS-SUP-003,
TC-PROFILE-SCH-SUP-005, TC-ADMINUSERS-SCH-SUP-004 — observe-only oracles, no invented HTTP codes.

Artifacts: docs/stage3-audit-human.md, scripts/apply_stage3_audit_human.py,
Audit sections in TC-*-{SUP,ST-SUP,SEC-SUP,SCH-SUP}.md, updated sheets/*.csv AuditStatus columns.
```

---

## Stage 4 — Execution artifacts

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-24 00:10

**Prompt:**
```
Build execution artifacts from @sheets
```

**Output:**
```
Merged 4 category CSVs → sheets/all-test-cases.csv (280 rows) + all-test-cases.xlsx (Summary tab).

Postman: postman/eshop-hw06.postman_collection.json (280 TC folders, ~338 requests),
postman/eshop-hw06.postman_environment.json, collection pre-request X-Student-Id: 23127271,
Setup folder (login user/admin, register disposable), FR-04/07/19 nested folders.

Script: scripts/build_execution_artifacts.py. Doc: docs/execution-artifacts.md.
```

---

## Stage 5 — Execute and report bugs

- **Tool**: Cursor Grok 4.6
- **Date/time**: 2026-08-24 00:35

**Prompt:**
```
Check newman-run.log and write bug report
```

**Output:**
```
Newman: 343 requests, 1019 assertions, 0 automated failures (observe-only scripts).

Manual triage vs ExpectedResult → 8 product bugs (5 from human SUP cases):
BUG-001 SEC-03 user list (TC-ADMINUSERS-SEC-SUP-002), BUG-002 SEC-003 user DELETE,
BUG-003 SEC-06 role escalation, BUG-004 SEC-01 password hash on GET /users/me,
BUG-005 FR-19 admin self-delete, BUG-006 500 on text/plain PUT,
BUG-007 negative cart qty, BUG-008 admin list schema over-exposure.

Artifacts: docs/bug-reports-summary.md, docs/newman-execution-summary.md,
bugs/BUG-001..008.md, scripts/apply_newman_bug_refs.py, updated all-test-cases.csv/xlsx.
```


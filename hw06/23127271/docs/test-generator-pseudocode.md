# AI-Driven API Test Generator — Pseudocode

**Student:** 23127271  
**SUT:** EShop (`http://localhost:3000`)  
**Scope:** FR-04 Profile · FR-07 Cart · FR-19 Admin Users  
**Diagram:** [`test-generator-diagram.mmd`](test-generator-diagram.mmd)  
**Agent Skill:** `.cursor/skills/api-testing/SKILL.md`

This pseudocode matches the pipeline in the flowchart. Each numbered block maps to a node in `test-generator-diagram.mmd`.

---

## Data structures

```text
STRUCT SpecContext
    feature_id        // e.g. "FR-04"
    endpoint          // e.g. "PUT /api/users/me"
    method, path
    request_fields[]  // name, phone, shipping_address, ...
    security_rules[]  // SEC-02, SEC-05, SEC-06, ...
    business_rules[]  // email immutable, role immutable, ...
    response_schema   // fields documented in api_specification.md
END STRUCT

STRUCT TestCase
    id                // TC-PROFILE-001, TC-PROFILE-SEC-SUP-002, ...
    category          // DomainPartition | StateTransition | Security | SchemaValidation
    method, endpoint
    preconditions[]
    input             // headers, body, path params
    expected_result   // spec-based oracle; no invented HTTP codes
    priority          // High | Medium | Low
    source            // AI | Human
    audit_status      // VALID | INVALID | INCOMPLETE | (blank before audit)
    audit_reasoning
    actual_result     // filled after execution
    pass_fail         // Pass | Fail | Not evaluated
    bug_ref           // BUG-001, ...
END STRUCT
```

---

## Main pipeline

```text
FUNCTION MAIN(api_spec_path, endpoints[], student_id, base_url)
    all_cases ← empty list

    FOR EACH endpoint IN endpoints
        // ── 0. SPEC PARSER ──
        ctx ← PARSE_SPEC(api_spec_path, endpoint)
        IF ctx IS incomplete THEN
            ABORT "Missing spec section — ask human before generating"
        END IF

        // ── 1. PROMPT ROUTER + 2. AI GENERATOR (per category) ──
        FOR EACH category IN [DomainPartition, StateTransition, Security, SchemaValidation]
            checklist ← LOAD_CHECKLIST(category)
                // Domain: Skill-01 partitions + boundaries
                // State: legal/illegal transitions from FR rules
                // Security: SEC-01..SEC-07 map to concrete probes
                // Schema: response shape vs api_specification.md

            prompt ← BUILD_PROMPT(ctx, category, checklist, TEST_CASE_TEMPLATE)
            raw_output ← CALL_AI(tool="Cursor Grok", prompt)
            LOG_AI_INTERACTION(tool, timestamp, prompt, raw_output)
                // append-only → ai_audit_log.md

            raw_cases ← PARSE_AI_OUTPUT(raw_output)

            // ── 3. HUMAN AUDIT GATE ──
            audited_cases ← HUMAN_AUDIT(raw_cases, ctx)
            all_cases ← MERGE(all_cases, audited_cases)
        END FOR

        // ── 4. HUMAN EXTEND ──
        gaps ← DETECT_GAPS(all_cases, ctx)
            // concurrency, privilege on sibling endpoints, encoding, Content-Type
        human_cases ← DESIGN_SUPPLEMENTAL_CASES(gaps, min_count=5)
        FOR EACH hc IN human_cases
            hc.source ← Human
            hc.why_ai_missed ← CLASSIFY_GAP(gaps[hc])
                // Prompt quality | Model limitation | API characteristic
            LOG_AI_INTERACTION("Human extend", hc.id, hc.why_ai_missed)
        END FOR
        all_cases ← MERGE(all_cases, human_cases)
    END FOR

    // ── 5. ARTIFACT BUILDER ──
    EXPORT_CSV(all_cases, "sheets/all-test-cases.csv")
    EXPORT_EXCEL(all_cases, "sheets/all-test-cases.xlsx", summary_tab=TRUE)
    collection ← BUILD_POSTMAN(all_cases, base_url, student_id)
    INJECT_PRE_REQUEST_SCRIPT(collection,
        "pm.request.headers.upsert({ key: 'X-Student-Id', value: studentId });")
    WRITE_JSON(collection, "postman/eshop-hw06.postman_collection.json")

    // ── 6. EXECUTOR ──
    log ← RUN_NEWMAN(collection)
        // observe-only scripts: record status 100–599, do not auto-fail oracles
    WRITE_HTML(log, "reports/newman-report.html")
    WRITE_TEXT(log, "reports/newman-run.log")

    // ── 7. BUG TRIAGE ──
    results ← MANUAL_TRIAGE(log, all_cases)
        // Newman 0 assertion failures ≠ SUT passed all oracles
    bugs ← FILTER_GENUINE_BUGS(results)

    FOR EACH bug IN bugs
        WRITE_BUG_REPORT(bug, "bugs/BUG-NNN-*.md")
        CREATE_GITHUB_ISSUE(bug, screenshot)
        UPDATE_SHEET(bug.test_case_id,
            actual_result=bug.actual,
            pass_fail="Fail",
            bug_ref=bug.id)
    END FOR

    RETURN all_cases, collection, log, bugs
END FUNCTION
```

---

## Module details (diagram nodes)

### 0. PARSE_SPEC

```text
FUNCTION PARSE_SPEC(api_spec_path, endpoint) → SpecContext
    text ← READ_FILE(api_spec_path)
    ctx ← EXTRACT(endpoint, text)
        // method, path, auth, body fields, FR-xx rules, SEC-xx applicability
    ctx.response_schema ← EXTRACT_RESPONSE_SHAPE(endpoint, text)
    RETURN ctx
END FUNCTION
```

### 1. BUILD_PROMPT

```text
FUNCTION BUILD_PROMPT(ctx, category, checklist, template) → string
    // Anti-pattern: never "generate all test cases for this API in one prompt"
    prompt ← "Scope: " + ctx.feature_id + " " + ctx.method + " " + ctx.path
    prompt ← prompt + "\nCategory: " + category
    prompt ← prompt + "\nSpecContext: " + SERIALIZE(ctx)
    prompt ← prompt + "\nChecklist: " + checklist
    prompt ← prompt + "\nOutput columns: " + template
    prompt ← prompt + "\nRules: spec-based oracles only; flag assumptions with warning"
    RETURN prompt
END FUNCTION
```

### 3. HUMAN_AUDIT

```text
FUNCTION HUMAN_AUDIT(cases[], ctx) → cases[]
    FOR EACH tc IN cases
        IF tc.expected_result CONTRADICTS ctx.business_rules OR ctx.security_rules THEN
            tc.audit_status ← INVALID
            tc.expected_result ← FIX_TO_MATCH_SPEC(tc, ctx)
            tc.audit_reasoning ← "Oracle assumed rule not in spec"
        ELSE IF tc.expected_result INVENTS_HTTP_CODE(ctx) THEN
            tc.audit_status ← INCOMPLETE
            tc.expected_result ← "Record actual; do not invent status codes"
            tc.audit_reasoning ← "Spec omits HTTP code for this case"
        ELSE IF tc.precondition IS UNREACHABLE THEN
            tc.audit_status ← INVALID
            tc.audit_reasoning ← "Precondition cannot be set up"
        ELSE
            tc.audit_status ← VALID
            tc.audit_reasoning ← "Aligned with spec / SEC requirement"
        END IF
        // Never delete silently — keep corrected version + reasoning
    END FOR
    RETURN cases
END FUNCTION
```

### 4. HUMAN_EXTEND

```text
FUNCTION DETECT_GAPS(cases[], ctx) → gap_list
    gaps ← empty list
    IF NO case tests privilege on sibling endpoints THEN gaps.append(PrivilegeGap)
    IF NO concurrency probe for mutable resource THEN gaps.append(ConcurrencyGap)
    IF NO Content-Type confusion probe THEN gaps.append(ParserGap)
    IF NO encoding bypass (null-byte, unicode-escape) THEN gaps.append(EncodingGap)
    RETURN gaps
END FUNCTION

FUNCTION DESIGN_SUPPLEMENTAL_CASES(gaps, min_count) → TestCase[]
    new_cases ← []
    FOR EACH gap IN gaps UNTIL len(new_cases) >= min_count
        tc ← CREATE_PROBE(gap)
        tc.id ← "TC-" + MODULE + "-" + CATEGORY + "-SUP-" + NEXT_ID
        new_cases.append(tc)
    END FOR
    RETURN new_cases
END FUNCTION
```

### 5. BUILD_POSTMAN

```text
FUNCTION BUILD_POSTMAN(cases[], base_url, student_id) → collection
    collection ← NEW_COLLECTION("eshop-hw06")
    SET_VARIABLE(collection, "baseUrl", base_url)
    SET_VARIABLE(collection, "studentId", student_id)
    ADD_FOLDER(collection, "00 — Setup (run first)")
        // login user/admin, capture tokens and ids
    FOR EACH tc IN cases
        folder ← ADD_FOLDER(collection, tc.id)
        FOR EACH step IN tc.steps
            req ← ADD_REQUEST(folder, step.method, step.url, step.body, step.headers)
            ADD_TEST_SCRIPT(req, OBSERVE_ONLY_ORACLE)
                // pm.test records status; does not assert spec oracle as Pass/Fail
        END FOR
    END FOR
    RETURN collection
END FUNCTION
```

### 7. MANUAL_TRIAGE

```text
FUNCTION MANUAL_TRIAGE(newman_log, cases[]) → results[]
    FOR EACH tc IN cases
        actual ← EXTRACT_FROM_LOG(newman_log, tc.id)
        tc.actual_result ← actual
        IF actual VIOLATES tc.expected_result AND NOT test_case_defect(tc) THEN
            tc.pass_fail ← "Fail"
            results.append(GenuineBug(tc))
        ELSE IF actual SATISFIES tc.expected_result THEN
            tc.pass_fail ← "Pass"
        ELSE
            tc.pass_fail ← "Not evaluated"  // inconclusive / observe-only
        END IF
    END FOR
    RETURN results
END FUNCTION
```

---

## Example run (this homework)

```text
endpoints ← [
    "PUT /api/users/me",      // FR-04 — 100 TC
    "POST /api/cart",         // FR-07 — 99 TC
    "DELETE /api/admin/users/:id"  // FR-19 — 81 TC
]

MAIN("api_specification.md", endpoints, student_id="23127271", base_url="http://localhost:3000")

// Totals after 3 APIs:
//   280 test cases (220 AI + 60 Human)
//   343 Newman requests (Setup + multi-step TCs)
//   8 genuine bugs (11 Fail rows in sheet; 8 unique BUG-00x)
//
// Illustrative AI-missed bug (Human Extend → Triage):
//   TC-ADMINUSERS-SEC-SUP-002  GET /api/admin/users with user JWT → 200
//   → BUG-001 (SEC-03 / FR-12 admin guard missing on list endpoint)
```

---

## Diagram ↔ implementation map

| Diagram node | Implementation in this repo |
|--------------|----------------------------|
| 0. Spec Parser | Manual read of `Repo/eshop-sut/api_specification.md` |
| 1. Prompt Router | `.cursor/skills/api-testing/SKILL.md` |
| Gen-D | `scripts/generate_domain_partitions.py` |
| Gen-ST | `scripts/generate_state_transitions.py` |
| Gen-SEC | `scripts/generate_security_tests.py` |
| Gen-SCH | `scripts/generate_schema_validation.py` |
| 2. AI Generator | Cursor Grok sessions (logged in `ai_audit_log.md`) |
| 3. Human Audit | `scripts/apply_stage2_audit*.py` |
| 4. Human Extend | `scripts/append_stage3_*_sup_cases.py` |
| 5. Artifact Builder | `scripts/build_execution_artifacts.py` |
| 6. Executor | Newman → `reports/newman-report.html` |
| 7. Bug Triage | `bugs/BUG-*.md`, `scripts/apply_newman_bug_refs.py` |
| AI Audit Log | `ai_audit_log.md` |
| Loop (3 APIs) | FR-04 → FR-07 → FR-19 merged into one collection |

---

## Design decisions (G9.5)

1. **Split prompts by test technique** — avoids single-shot AI omitting security edges (e.g. GET list SEC-03).
2. **Human audit is a blocking gate** — Postman is built only from audited + extended cases.
3. **Spec-based oracles** — do not invent HTTP 400/403 when the spec is silent; Newman scripts are observe-only.
4. **Human extend targets gap classes** — concurrency, privilege on related endpoints, Content-Type, encoding.
5. **Append-only AI audit log** — every LLM call is recorded for the mandatory AI Audit Report appendix.

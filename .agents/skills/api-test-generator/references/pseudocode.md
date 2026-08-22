# Pseudocode — AI-driven API Test Generator

This is the standalone pseudocode artifact for the assignment's Section 7
("Provide a self-drawn diagram and pseudocode of the design"). Pair it with
your own hand-drawn version of the diagram in `diagram_reference.md`.

```
FUNCTION generate_test_suite(spec_file, endpoint_selector, student_context):

    # --- Step 1: Parse (deterministic) ---
    raw_spec        <- read(spec_file)
    endpoint_model  <- parse_endpoint(raw_spec, endpoint_selector)
        # method, path, parameters[], auth/role, example responses,
        # mentioned SEC-0x refs, state-machine hints
    IF endpoint_model.parameters is empty:
        endpoint_model <- manual_fallback_review(raw_spec, endpoint_selector)

    test_cases <- []

    # --- Step 2: Generate, one stage at a time ---
    FOR stage IN [DomainPartition, StateTransition, Security, SchemaValidation]:
        guide      <- load_reference_guide(stage)
        stage_cases <- []

        SWITCH stage:
            CASE DomainPartition:
                FOR param IN endpoint_model.parameters:
                    classes <- derive_equivalence_classes(param, guide)
                    FOR class IN classes:
                        stage_cases.append(build_case(stage, endpoint_model, param, class))

            CASE StateTransition:
                IF endpoint_model.state_machine_hint:
                    state_graph <- reconstruct_state_graph(endpoint_model, raw_spec)
                    FOR transition IN state_graph.legal_transitions:
                        stage_cases.append(build_case(stage, endpoint_model, transition, expect=PASS))
                    FOR transition IN state_graph.illegal_transitions(state_graph):
                        stage_cases.append(build_case(stage, endpoint_model, transition, expect=REJECT))

            CASE Security:
                FOR sec_item IN [SEC_01..SEC_07]:
                    IF applies(sec_item, endpoint_model):
                        stage_cases.append(build_case(stage, endpoint_model, sec_item, expect=SAFE_OUTCOME))
                    ELSE:
                        record_not_applicable(sec_item, endpoint_model)   # kept for the audit/critique

            CASE SchemaValidation:
                FOR status_code IN endpoint_model.expected_status_codes:
                    schema <- extract_or_infer_schema(endpoint_model, status_code)
                    stage_cases.append(build_case(stage, endpoint_model, schema, expect=SHAPE_MATCH))

        test_cases.extend(stage_cases)
        report_progress(stage, count=len(stage_cases), running_total=len(test_cases))

    # --- Step 3: Audit (AI-drafted, human-confirmed) ---
    FOR case IN test_cases:
        draft_label, reasoning <- ai_review(case, endpoint_model)
        case.audit.label      <- human_confirm_or_override(draft_label, reasoning)
        IF case.audit.label IN [INVALID, INCOMPLETE]:
            case <- propose_correction(case)

    # --- Step 4: Extend (human + AI, gap-hunting) ---
    gap_prompts <- [
        "business-logic abuse the spec doesn't state explicitly",
        "cross-resource IDOR combining two roles",
        "concurrent/racing state transitions",
    ]
    extension_cases <- []
    FOR prompt IN gap_prompts:
        candidate <- ai_propose_edge_case(prompt, endpoint_model, existing=test_cases)
        IF human_confirms(candidate) AND len(extension_cases) < 5:
            candidate.why_ai_missed <- explain_gap(prompt)
            extension_cases.append(candidate)
    test_cases.extend(extension_cases)

    # --- Step 5: Export (deterministic) ---
    write_json(test_cases, "test_cases.json")
    export_excel(test_cases, "test_cases.xlsx")
    export_postman_collection(test_cases, "collection.json",
                               inject_header="X-Student-Id", value=student_context.id)

    RETURN test_cases
END FUNCTION
```

## Complexity / design notes

- The four generation stages are **independent passes with independent
  checklists**, not one prompt — this satisfies the assignment's "guide the
  AI step by step" requirement and makes each stage individually auditable.
- Parsing and exporting are deterministic code (no AI variance); only the
  *generation* and *audit-drafting* steps involve the AI, keeping the
  AI-dependent surface area small and reviewable.
- `record_not_applicable` matters for grading: showing that a security
  checklist item was considered and knowingly excluded is stronger evidence
  of rigor than silence.
- The extension step is deliberately human-in-the-loop first: prompts are
  generic gap categories, not spec-specific answers, so the AI still has to
  reason about *this* endpoint rather than pattern-match a memorized case.

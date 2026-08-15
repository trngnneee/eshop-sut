---
name: hw05-performance-testing
description: Complete the HW05 AI-assisted performance-testing assignment for the EShop SUT. Use when Codex must design, generate, execute, analyze, critique, document, or package JMeter or k6 Load/Stress/Spike tests; create endpoint-specific CSV data; analyze .jtl logs; find AI metric misinterpretations; propose continuous performance testing; maintain an AI Audit Report; or prepare HW05 submission evidence.
---

# HW05 Performance Testing

## Workflow

Use this skill as an assignment conductor. Keep the work evidence-based: never fabricate screenshots, `.jtl` files, HTML reports, resource-monitor captures, demo-video links, GitHub issues, hardware reports, or git history.

1. Read the assignment brief and local SUT docs:
   - `docs/HW05_Performance_Testing.md`
   - `api_specification.md`
   - `README.md`
   - backend/frontend config files for actual ports and endpoints
2. Ask for missing student-specific values only when they cannot be inferred: StudentID, chosen endpoint ownership, demo-video link, self-assessed grade, and GitHub repo/issues URL.
3. Use one selected end-to-end workflow that covers all three backend
   endpoint groups:
   - auth-heavy
   - read-heavy
   - transactional
4. Use the exact same E2E workflow in all three scenarios:
   Load, Stress, and Spike. Keep the request sequence and business flow
   consistent; only the workload profile and scenario-specific configuration
   may differ.
5. Make the E2E workflow data-driven using one or more CSV input files.
   Parameterize requests with values such as credentials, search terms,
   product IDs, quantities, and checkout/order data. CSV files may be shared
   across Load, Stress, and Spike when appropriate. Name each test plan
   `{StudentID}_{ScenarioType}_{YYYYMMDD}`.
6. Use three distinct report/listener views across the three plans. For JMeter, prefer `View Results Tree`, `Summary Report`, and `Aggregate Report`. For k6, use clearly distinct outputs/views.
7. Run as much of the test suite as the local environment permits. Capture and record:
   - raw `.jtl` logs
   - HTML report folders
   - screenshots showing the test tool and backend resource monitor together
   - hardware evidence and a spec table
   - account-lockout reset steps when relevant
   - genuine bugs/performance issues with screenshots and GitHub issue links
8. Run a short 10-15 minute endurance/soak test to identify the local hardware threshold with concrete numbers such as max stable RPS, p95, error rate, CPU, and memory ceiling.
9. Analyze raw results with AI, then do a human review. Cite correct values from `.jtl` logs wherever the AI misread or overclaimed.
10. Propose a continuous performance-testing model that watches commits, decides whether to run tests, and flags p95 regressions. Include a flow chart and trade-offs.
11. Maintain an AI Audit Report for every AI interaction: tool name, date/time, prompt, output, and human correction/review.
12. Create a new git commit for each meaningful procedure step when the user wants the assignment history prepared.

## Planning Guidance

Prefer JMeter unless the user requests k6. Use k6 only when the repo/environment already supports it or the user wants the bonus path.

Choose conservative starting parameters, then tune from evidence:

- Load: expected steady traffic, realistic think-time, modest ramp-up, low error tolerance.
- Stress: gradually increase users or arrival rate until p95/error rate/resource limits break the target.
- Spike: abrupt traffic jump and recovery observation; include before/after steady windows.
- Endurance: sustained load near the strongest stable setting found before the system degrades.

For login tests, avoid invalidly locking all test accounts unless that is the intended observation. Include reset steps or fresh credentials between runs.

## Mandatory Human Review Gates

For each scenario (Load, Stress, Spike), follow the phases below in order.
Do not skip phases and do not continue past a review gate without an
explicit user response.


### Phase 1 — Design

Analyze the verified E2E workflow and propose:

- workload model
- VU/thread count
- ramp-up/ramp-down
- duration
- think time
- CSV usage
- correlation
- assertions
- JMeter structure
- report/listener type

Do not generate the final `.jmx` yet.

At the end:

1. Summarize the proposed design.
2. Create the Phase 1 audit section.
3. Mark the phase as `Pending Human Review`.
4. Ask the user to approve the design or provide corrections.
5. STOP.

Do not continue until the user replies.

### Phase 2 — Generate Initial Test Plan

After the user approves or corrects the design:

1. Apply the human feedback.
2. Generate the initial `.jmx` test plan.
3. Validate endpoints, CSV variables, correlation, assertions,
   naming convention, and listener configuration.
4. Summarize what was generated.

Then STOP again.

Ask the user to review the generated test plan.

Do not proceed to execution or result analysis until the user confirms.

Before stopping:

1. Update the Phase 1 audit section with the user's review/corrections
   and mark its final status.
2. Create the Phase 2 audit section containing:
   - the prompt that started Phase 2,
   - the generated test-plan summary,
   - validation results,
   - `Human Review: Pending`.
3. Ask the user to review the generated test plan.
4. STOP.

### Phase 3 — Execution

The student executes the test on the local machine and captures the
required real evidence.

Do not fabricate execution results.

Wait until a real `.jtl` file and execution evidence are available.

Then STOP.

### Phase 4 — Result Analysis

When a real `.jtl` file is available:

1. Run `scripts/analyze_jtl.py`.
2. Compute objective metrics from the raw `.jtl` log.
3. Analyze the performance results using those computed metrics.
4. Propose performance thresholds, such as:
   - p95 response-time threshold
   - acceptable error-rate threshold
   - throughput/RPS target where appropriate
5. Explain the rationale for each proposed threshold.
6. Clearly separate:
   - objective metrics computed from the raw logs,
   - AI interpretation,
   - AI-proposed performance thresholds.

Then STOP.

Ask the user to review:
- the AI interpretation,
- the proposed thresholds,
- any metric misinterpretations or unsupported conclusions.

Do not write the final scenario conclusion yet.

Before stopping:

1. Save the computed metrics, AI interpretation, and proposed thresholds.
2. Append the interaction to the AI Audit Report.
3. Mark `Human Review: Pending`.
4. STOP.

### Phase 5 — Human Review and Finalization
After receiving the user's review:
1. Update the Phase 4 audit section with:
   - exact human-review prompt,
   - identified AI misinterpretations,
   - human corrections,
   - corrected raw-log values,
   - Phase 4 status: `Approved` or `Approved with Corrections`.
2. Apply the human corrections to the scenario analysis.
3. Document:
   - AI mistakes or unsupported claims,
   - correct raw-log evidence,
   - review of AI-proposed thresholds.
4. Finalize the scenario report section.
5. Record the finalization result in the audit trail.
6. Mark the scenario as completed only after all required evidence exists.

## Reports

When writing deliverables, use `references/report-checklist.md` for the required evidence list and self-assessment coverage.

When analyzing `.jtl` files, run `scripts/analyze_jtl.py` to compute objective metrics before asking AI to interpret them. Use those computed values as the source of truth during the misinterpretation hunt.

Use `scripts/new_audit_entry.py` when a new scenario phase begins.

Use `scripts/update_audit_entry.py` when the user reviews, approves,
or corrects work belonging to an existing phase.

The final AI Audit appendix must preserve the original AI proposal,
the human review, and any revised AI output for each phase.
Do not reconstruct the audit from memory at the end.

## Automatic AI Audit Logging

Maintain the AI Audit Report by scenario and phase rather than creating
a separate top-level entry for every message.

Each phase has one audit section identified by:

`{Scenario} + {Phase}`

For example:

- Load / Phase 1 — Design
- Load / Phase 2 — Generate Test Plan
- Load / Phase 4 — Result Analysis

### When a phase starts

1. Use `scripts/new_audit_entry.py` to create one audit section for the phase.
2. Record:
   - AI tool name
   - date and time
   - scenario
   - phase
   - exact initial user prompt
   - initial AI output
   - `Human Review: Pending` when the phase ends at a review gate
3. Do not create another top-level audit section for the same phase.

### When the user reviews the phase

If the user approves, rejects, or corrects work from the current phase:

1. Update the SAME audit section using `scripts/update_audit_entry.py`.
2. Preserve the original prompt and original AI output.
3. Append:
   - review date/time
   - exact human-review prompt
   - human approval/correction
   - revised AI output, if the AI changed the artifact
   - updated phase status
4. Do not create a new top-level audit entry for review messages that
   belong to the current phase.

### Phase status

Use one of:

- `Pending Human Review`
- `Approved`
- `Approved with Corrections`
- `Rejected`
- `Completed`

### Moving to another phase

Create a new audit section only when the workflow actually moves to
a new phase or scenario.

### Audit integrity

Never delete or replace the original prompt or initial AI output.
Updates must append review and revision information inside the same
phase section.

Before every mandatory STOP, verify that the current phase audit section
has been created or updated successfully.

If audit logging fails, report the failure and do not silently claim that
the interaction was recorded.

## Validation

- Load, Stress, and Spike all execute the same selected E2E workflow
- the E2E workflow covers auth-heavy, read-heavy, and transactional endpoints
- the request sequence is consistent across all three scenarios
- the workflow is data-driven using one or more CSV files
- CSV datasets may be shared across scenarios when appropriate
- scenario filenames follow `{StudentID}_{ScenarioType}_{YYYYMMDD}`
- report/listener types are not repeated
- raw `.jtl` logs and HTML report folders are present for executed runs
- execution evidence shows the test tool together with backend resource usage
- hardware evidence and a hardware-spec table are present
- endurance threshold is reported with concrete numbers
- AI analysis includes proposed performance thresholds
- human review records AI misinterpretations or unsupported claims
- AI critique is 200-300 words
- submission archive name follows `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`
- claims in the report trace back to logs, screenshots, commits, or links
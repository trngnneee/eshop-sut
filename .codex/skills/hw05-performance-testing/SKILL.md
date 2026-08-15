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

Treat each meaningful AI-assisted task as one Interaction. Create a new
Interaction only when the task meaningfully changes, such as moving from test
design to test-plan generation, from test-plan generation to result analysis,
or from scenario work to a general assignment task such as AI critique or
submission validation.

Feedback stays inside the same Interaction. If the user corrects something,
asks for a revision, clarifies requirements, rejects the result, approves the
result, asks to re-analyze the same result, or asks to modify the generated
artifact, do not append the full feedback prompt to the report. Keep only the
main prompt that started the Interaction, then summarize the feedback and final
state in the output summary and review outcome. Do not create a new Interaction
for review messages that belong to the current task.

Use these lifecycle values internally and as script input:

- `Pending Human Review`
- `Approved`
- `Approved with Corrections`
- `Rejected`
- `Completed`

The report does not render a separate `Status` metadata line. Express the
current lifecycle state in Vietnamese under `Kết quả sau review`.

For each scenario (Load, Stress, Spike), keep the same review gates and do not
continue past a review gate without an explicit user response.

### Test Design Interaction

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

Before stopping:

1. Summarize the proposed design.
2. Create the design Interaction audit entry.
3. Record the review outcome as pending human review.
4. Ask the user to approve the design or provide corrections.
5. STOP.

Do not continue until the user replies.

### Test Plan Generation Interaction

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

1. Update the design Interaction with the user's review/corrections and final
   review outcome.
2. Create the test-plan generation Interaction containing:
   - the prompt that started the Interaction, unless it was already recorded
     as the design review prompt,
   - a concise Vietnamese summary of generated artifacts,
   - validation results,
   - a pending human review outcome.
3. Ask the user to review the generated test plan.
4. STOP.

### Execution Evidence

The student executes the test on the local machine and captures the
required real evidence.

Do not fabricate execution results.

Wait until a real `.jtl` file and execution evidence are available.

Then STOP.

### Result Analysis Interaction

When a real `.jtl` file is available:

1. Run `scripts/analyze_jtl.py`.
2. Compute objective metrics from the raw `.jtl` log.
3. Analyze the performance results using those computed metrics.
4. Propose performance thresholds, such as:
   - p95 response-time threshold
   - acceptable error-rate threshold
   - throughput/RPS target where appropriate
5. Explain the rationale for each proposed threshold.
6. Propose backend, database, test-data, or test-environment optimizations.
   For each recommendation, include:
   - the exact recommendation,
   - the metric or observation that motivated it,
   - the expected effect,
   - the evidence category:
     `Supported by raw evidence`, `Plausible but not proven`, or
     `Unsupported / possible hallucination`.
7. Clearly separate:
   - objective metrics computed from the raw logs,
   - per-sampler/endpoint metrics computed from the raw logs,
   - AI interpretation,
   - AI-proposed performance thresholds,
   - AI-proposed optimizations and their evidence categories.

Use this result-analysis output structure outside the audit report:

```md
Objective Metrics From Raw JTL

| Metric | Value | Source |
|---|---:|---|

Per-Sampler Metrics From Raw JTL

| Sampler / endpoint | Samples | Error % | Avg ms | p95 ms | p99 ms | Throughput req/s |
|---|---:|---:|---:|---:|---:|---:|

AI Interpretation

AI-Proposed Thresholds

| Threshold | Proposed value | Rationale | Raw metric used |
|---|---:|---|---|

AI-Proposed Optimizations

| Recommendation | Evidence category | Metric / observation used | Expected effect |
|---|---|---|---|
```

Then STOP.

Ask the user to review:
- the AI interpretation,
- the proposed thresholds,
- the proposed optimizations and evidence categories,
- any metric misinterpretations or unsupported conclusions.

Do not write the final scenario conclusion yet.

Before stopping:

1. Save the computed metrics, AI interpretation, and proposed thresholds.
2. Save the AI-proposed optimizations and evidence categories.
3. Create the result-analysis Interaction if it does not already exist.
4. If the result-analysis Interaction already exists, update that same
   Interaction.
5. Record the review outcome as pending human review.
6. Ask the user to review the AI interpretation, thresholds,
   optimizations, and any unsupported claims.
7. STOP.

### Human Review and Finalization

After receiving the user's review:

1. Update the same result-analysis Interaction with:
   - exact human-review prompt,
   - identified AI misinterpretations,
   - human corrections,
   - corrected raw-log values,
   - recommendation classifications,
   - final review outcome.
2. Apply the human corrections to the scenario analysis.
3. Document:
   - AI mistakes or unsupported claims,
   - correct raw-log evidence,
   - review of AI-proposed thresholds.
   - review of AI-proposed optimizations.
4. Include a human review table in the scenario report when needed:

```md
| AI claim or recommendation | Raw evidence / correct value | Human decision | Reason |
|---|---|---|---|
```

Use these decisions:

- `Correct`
- `Corrected`
- `Unsupported`
- `Hallucinated`
- `Feasible`
- `Plausible but not proven`

5. Finalize the scenario report section.
6. Record the finalization result in the audit trail.
7. Mark the scenario as completed only after all required evidence exists.

## Reports

When writing deliverables, use `references/report-checklist.md` for the required evidence list and self-assessment coverage.

When analyzing `.jtl` files, run `scripts/analyze_jtl.py` to compute objective metrics before asking AI to interpret them. Use those computed values as the source of truth during the misinterpretation hunt.

Audit helper scripts live under this skill directory:

- `.codex/skills/hw05-performance-testing/scripts/new_audit_entry.py`
- `.codex/skills/hw05-performance-testing/scripts/update_audit_entry.py`
- `.codex/skills/hw05-performance-testing/scripts/analyze_jtl.py`

When instructions below mention `scripts/...`, resolve that path relative to
`.codex/skills/hw05-performance-testing/` unless a repo-level `scripts/`
directory exists with the same helper.

Use `scripts/new_audit_entry.py` when a new Interaction begins.

Use `scripts/update_audit_entry.py` when the user reviews, approves, rejects,
or corrects work belonging to an existing Interaction.

The final AI Audit appendix must preserve the main prompt for each Interaction,
human review decisions, revised AI output summaries, lifecycle meaning, and
audit marker comments. Feedback prompts may be omitted from the rendered report
when their meaning is already captured in the review outcome. Do not
reconstruct the audit from memory at the end.

## Automatic AI Audit Logging

Maintain the AI Audit Report by Interaction. An Interaction is a meaningful
AI-assisted task, not every message. Examples include:

- Load Test Design
- Load Test Plan Generation
- Load Result Analysis
- Stress Test Design
- Stress Test Plan Generation
- Stress Result Analysis
- Spike Test Design
- Spike Test Plan Generation
- Spike Result Analysis
- Endurance Test Design
- Endurance Result Analysis
- Continuous Performance Testing Proposal
- AI Critique
- Submission Validation

Before taking any assignment action, inspect `reports/AI_Audit_Report.md` and
identify the latest open Interaction:

- If the latest Interaction's review result says it is waiting for human
  review, treat the next relevant user message as a review, correction, or
  approval of that same Interaction.
- Do not generate a `.jmx`, analyze `.jtl`, finalize conclusions, or open a
  new Interaction that depends on the pending work until the current
  Interaction has been explicitly approved.
- If the user asks to "continue" or "proceed" while the current Interaction is
  pending, first record that prompt as review input for the current
  Interaction. Only then start the next meaningful Interaction if the prompt
  clearly approves the current work.
- If the prompt contains corrections but not approval, update the same
  Interaction and keep the review outcome pending.

Each Interaction has one audit section identified by a stable chronological
marker ID. Use IDs such as:

- `interaction-001-load-design`
- `interaction-002-load-generation`
- `interaction-003-load-analysis`
- `interaction-004-stress-design`
- `interaction-005-stress-generation`
- `interaction-006-stress-analysis`
- `interaction-010-endurance-design`
- `interaction-011-endurance-analysis`
- `interaction-012-continuous-testing`
- `interaction-013-ai-critique`
- `interaction-014-submission-validation`

### When an Interaction Starts

1. Use `scripts/new_audit_entry.py` to create one audit section for the
   Interaction.
2. Record:
   - AI tool name
   - date and time as `YYYY-MM-DD HH:MM`
   - exact main user prompt that started the Interaction, preserved in its
     original wording
   - Vietnamese summary of the AI output, including important artifacts,
     metrics, validation, and recommendations
   - review outcome in Vietnamese
3. Keep the main prompt as a blockquote. Do not append later feedback prompts
   to `Prompt`; summarize feedback in `Output` or `Kết quả sau review`.
   Convert any Markdown headings inside captured prompts or summaries into
   plain text or bold labels so they do not become document-level headings.
4. Do not create another top-level audit section for the same Interaction.

Example:

```bash
python .codex/skills/hw05-performance-testing/scripts/new_audit_entry.py reports/AI_Audit_Report.md \
  --id interaction-001-load-design \
  --title "Load Test - Thiet ke kich ban kiem thu" \
  --tool "Codex GPT-5" \
  --prompt "<exact initial prompt>" \
  --output "<Vietnamese output summary>" \
  --status "Pending Human Review"
```

### When the User Reviews an Interaction

If the user approves, rejects, or corrects work from the current Interaction:

1. Update the same audit section using `scripts/update_audit_entry.py`.
2. Preserve existing prompt history and output summary.
3. Do not append the exact review prompt to the `Prompt` blockquote.
4. Append a concise revised-output summary when the AI changed the artifact.
5. Replace the Vietnamese review outcome for that Interaction, including the
   substance of the human correction or decision.
6. Do not create a new audit entry for review messages that belong to the
   current Interaction.

Example:

```bash
python .codex/skills/hw05-performance-testing/scripts/update_audit_entry.py reports/AI_Audit_Report.md \
  --id interaction-001-load-design \
  --review-prompt "<exact review prompt>" \
  --review "<human decision or correction>" \
  --revised-output "<Vietnamese revised-output summary, if any>" \
  --status "Approved with Corrections"
```

### Audit Integrity

Never delete or replace the original main prompt, output summaries, timestamps,
lifecycle meaning, or marker comments. Review feedback prompts do not need to
be retained verbatim in the rendered report as long as their decisions and
corrections remain represented in the same Interaction section.

Before every mandatory STOP, verify that the current Interaction audit section
has been created or updated successfully.

If audit logging fails, report the failure and do not silently claim that the
Interaction was recorded.

### Interaction Lifecycle

1. Interaction starts:
   - create the audit section
   - save the initial prompt
   - save the initial AI output summary
   - set the review outcome to pending if a review gate is required
2. User requests corrections:
   - update the same Interaction section
   - keep the original main prompt unchanged
   - summarize the human correction in the review outcome
   - append the revised AI output summary when applicable
   - keep the review outcome pending if the revised result still requires
     approval
3. User approves:
   - update the same Interaction section
   - keep the original main prompt unchanged
   - set the review outcome to approved or approved with corrections
4. Start a new Interaction only when the task meaningfully changes.

### Audit Report Structure

Use this renderable Vietnamese HW04-style structure:

```md
# AI Audit Report - HW05 Performance Testing

Bao cao nay ghi lai cac lan tuong tac voi cong cu AI trong qua trinh thuc hien HW05 Performance Testing.

## Nhat ky tuong tac

<!-- AUDIT_ENTRY:{interaction-id}:START -->
### [{N}] {Interaction Title}

- **Cong cu:** {AI tool}
- **Thoi gian:** {YYYY-MM-DD HH:MM}
- **Prompt:**
  > {exact user prompt}
- **Output:**
  {Vietnamese summary of AI output}
- **Ket qua sau review:** {Vietnamese review result and lifecycle state}
<!-- AUDIT_ENTRY:{interaction-id}:END -->

## Tong hop cong cu su dung

| Cong cu | Muc dich su dung | So luot tuong tac |
|---|---|---:|
| Codex (GPT-5) | Ho tro thiet ke, sinh file JMeter, phan tich ket qua va chinh sua bao cao | {count} |
```

Use Vietnamese diacritics in the actual report when the file encoding supports
UTF-8. The ASCII labels above are only for portable examples in this skill.

Keep the audit hierarchy visually consistent:

- `#` only for the report title
- `##` only for `Nhật ký tương tác` and `Tổng hợp công cụ sử dụng`
- `###` only for Interaction entries, formatted as `### [N] Title`
- No rendered `####` or `#####` headings in the AI Audit Report
- No separate structural sections for initial prompt, initial output, or review

Do not allow headings copied inside prompts, AI output summaries, reviews, or
revised output summaries to visually override their parent audit section.
Preserve their visible text, but neutralize Markdown heading markers by using
plain text or bold labels.

### Special Reopen Handling

If a phase is reopened after testing proves the previous plan is unsuitable,
do not delete the historical entry. Update the same Interaction's review
outcome to state that the previous approval is superseded and the revised
artifact is pending review.

For the current Stress Phase 2 history, preserve that:

- the old generated Stress test plan existed and was executed
- the phase was reopened after review
- previous approval should be treated as superseded
- the revised Stress plan uses a continuous stepped profile `10 -> 20 -> 35 -> 50`
- the revised plan is pending review and has not yet been accepted for rerun

For Stress result analysis based on the old invalidated run, keep the
historical Interaction but mark it as rejected or no longer valid. Do not use
it as the final Stress conclusion until a new accepted plan is executed and
real evidence is available.

### Interaction Transition Rule

If one user message both approves/reviews the current Interaction and requests
the next task:

1. Summarize the review/approval part in the current Interaction's review
   outcome.
2. Create the next Interaction only when the prompt clearly starts a new
   meaningful task.
3. Do not duplicate the same user prompt as the next Interaction's initial
   prompt. If no separate prompt exists, use a neutral note such as
   `<No separate initial prompt; started after prior approval/review.>`.

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
- AI analysis includes objective totals, per-sampler metrics, proposed
  performance thresholds, and proposed optimizations
- human review records AI misinterpretations, corrected raw-log values,
  unsupported claims, and optimization feasibility classifications
- AI critique is 200-300 words
- submission archive name follows `<StudentID>_HW05_AI_Performance_<SelfAssessedGrade>.zip`
- claims in the report trace back to logs, screenshots, commits, or links

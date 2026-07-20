---
name: state-transition-testing
description: Generate complete risk-based test cases using State Transition Testing. The agent identifies States, Actions/Events, valid and invalid Transitions, builds State Transition Table using States × Actions, and generates Markdown test cases for State Coverage, Transition Coverage, 1-switch Coverage, n-switch Coverage, End-to-End Test, and Final State Test without reducing or removing required test cases.
---

# Role

You are a Software Testing Engineer.

Your responsibility:

* Analyze software requirements
* Extract system States
* Identify Actions / Events that trigger State changes
* Build State Transition Model
* Create State Transition Table using States × Actions
* Identify valid and invalid Transitions
* Generate complete Markdown Test Case files
* Generate State Transition analysis report
* Ensure traceability between Requirement → State → Action → Transition → Coverage → Test Case

---

# Language Rule

All outputs MUST be Vietnamese.

Keep these technical terms unchanged:

* State Transition Testing
* State
* Action
* Event
* Transition
* State Coverage
* Transition Coverage
* 1-switch Coverage
* n-switch Coverage
* End-to-End Test
* Final State Test
* Test Case
* Coverage

---

# Testing Approach

This skill applies:

## State Transition Testing

Purpose:

* Verify system behavior when the system changes State
* Verify valid Transitions between States
* Verify invalid Transitions
* Detect missing Transitions
* Detect unreachable States
* Detect unexpected dead-end States
* Verify complete workflows
* Verify Final State stability
* Detect State corruption
* Verify security-sensitive State changes

Use State Transition Testing when:

* System behavior depends on current State
* Actions produce different results depending on State
* Requirement describes a workflow
* There are multiple steps
* There are Initial, Intermediate, Error, or Final States
* Some Actions are valid only in specific States
* Authentication/session logic exists
* OTP/token/password reset logic exists
* Order/payment/status logic exists
* Approval/rejection flow exists
* Account lock/unlock flow exists
* Security or authorization depends on State

---

# Step 1: Requirement Analysis

Before generating tests:

ONLY read specification documents.

Allowed:

* README.md
* /Requirements/*
* Feature documentation
* api_specification.md
* docs/use-case.md
* docs/functional-requirements.md

DO NOT:

* Read source code
* Infer behavior from implementation
* Guess missing business rules
* Invent undefined States
* Invent undefined Actions
* Invent undefined Events
* Assume timeout, retry, lock, cancel, expired, or error behavior unless specified

If information is missing, write exactly:

"Đặc tả không định nghĩa quy tắc này."

Extract:

* Feature name
* Requirement ID
* Module
* User roles
* Initial State
* Intermediate States
* Final States
* Error States
* Actions / Events
* Valid Transitions
* Invalid Transitions
* Guards / Conditions
* Expected behavior
* Error behavior
* Security-sensitive behavior
* Boundary or timeout behavior

Generate:

# Requirement Summary

Format:

Chức năng:

Requirement ID:

Module:

Mô tả:

User Roles:

Initial State:

States:

Final States:

Actions / Events:

Business Rules:

Expected Results:

Missing Rules:

---

# Step 2: Identify State Transition Requirement

Determine whether State Transition Testing is required.

Use State Transition Testing when:

* The requirement describes a workflow
* The system moves from one State to another
* Actions depend on current State
* Some Actions are valid only in specific States
* There are Final States
* There are Error States
* There are timeout, expired, cancelled, locked, rejected, approved, completed, or failed States
* Invalid Actions must be rejected
* Security or authorization depends on State

If State Transition Testing is not suitable:

Explain reason.

Example:

"State Transition Testing không phù hợp vì đặc tả chỉ mô tả kiểm tra giá trị đầu vào đơn lẻ, không có thay đổi State hoặc workflow."

---

# Step 3: Extract States

Identify all States from the specification.

Format:

## States

| ID | State         | Type         | Description                 |
| -- | ------------- | ------------ | --------------------------- |
| S0 | Initial state | Initial      | Mô tả trạng thái bắt đầu    |
| S1 | Example state | Intermediate | Mô tả trạng thái trung gian |
| S2 | Completed     | Final        | Mô tả trạng thái kết thúc   |

State Types:

* Initial
* Intermediate
* Final
* Error
* Locked
* Expired
* Cancelled
* Rejected
* Completed
* Failed

Rules:

* Each State must come from specification
* Do not create States not defined in specification
* If a State is implied but not explicitly defined, mark it as:

"Đặc tả không định nghĩa quy tắc này."

* Final State means the workflow ends or no further business transition is expected
* Error State must only be used when specification defines error behavior as a State
* UI screen must not be treated as State unless it represents business/system behavior
* Button visibility must not be treated as State unless it changes system behavior

---

# Step 4: Extract Actions / Events

Identify all Actions or Events that may trigger State changes.

Format:

## Actions / Events

| ID | Action / Event      | Description                      |
| -- | ------------------- | -------------------------------- |
| A1 | Submit email        | Người dùng gửi email             |
| A2 | Enter valid OTP     | Người dùng nhập OTP hợp lệ       |
| A3 | Enter invalid OTP   | Người dùng nhập OTP không hợp lệ |
| A4 | Submit new password | Người dùng gửi mật khẩu mới      |

Rules:

* Action is usually triggered by user
* Event can be system-generated, such as timeout, expiration, or scheduled processing
* Do not invent Actions not defined in specification
* Do not invent timeout or expiration Event unless specification defines it
* If timeout or expiration is not specified, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 5: Build State Transition Table using States × Actions

Create a complete State Transition Table using:

States × Actions

Formula:

Number of table rows = Number of States × Number of Actions

Each row represents:

Current State + Action/Event → Next State + Result

Format:

## State Transition Table

| Row | Current State | Action / Event | Valid / Invalid | Next State | Result / Expected Behavior                  |
| --- | ------------- | -------------- | --------------- | ---------- | ------------------------------------------- |
| 1   | S0            | A1             | Valid           | S1         | Chuyển sang trạng thái S1                   |
| 2   | S0            | A2             | Invalid         | S0         | Từ chối Action, giữ nguyên State            |
| 3   | S1            | A2             | Valid           | S2         | Chuyển sang trạng thái S2                   |
| 4   | S2            | A1             | Invalid         | S2         | Không cho phép thao tác vì đã ở Final State |

Rules:

* Use all States as Current State
* Use all Actions / Events for each State
* Mark every row as Valid or Invalid
* Every State × Action combination must appear in the table
* Do not skip any State × Action row
* For invalid Transition, define whether system:

  * Rejects Action
  * Shows error message
  * Keeps current State
  * Moves to Error State

If specification does not define invalid Transition behavior, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 6: Build Transition List

Extract Transitions from the State Transition Table.

Format:

## Transition List

| Transition ID | Current State | Action / Event | Next State | Valid / Invalid | Result                     |
| ------------- | ------------- | -------------- | ---------- | --------------- | -------------------------- |
| T1            | S0            | A1             | S1         | Valid           | Chuyển sang bước tiếp theo |
| T2            | S0            | A2             | S0         | Invalid         | Từ chối Action             |
| T3            | S1            | A2             | S2         | Valid           | Xác minh thành công        |

Rules:

* Each row from the States × Actions table can become a Transition
* Valid Transitions must always be tested
* Invalid Transitions must be tested if specification defines expected behavior
* Self-transition is allowed when the system stays in the same State after an Action
* Final State Transitions must be checked carefully
* Same Current State + Action must not produce multiple Next States unless guard conditions are defined

---

# Step 7: State Transition Validation

Perform validation before generating Test Cases.

## 1. Completeness

Check:

* All States are included
* All Actions are checked against every State
* All State × Action rows are present
* All valid Transitions are defined
* Invalid Transitions are defined or explicitly marked as missing
* All Final States are identified

## 2. Reachability

Check:

* Every State can be reached from Initial State
* No unreachable State exists unless specification defines it

## 3. Dead-end State

Check:

* Final States are expected dead-end states
* Non-final States must not be unexpected dead-end states

## 4. Consistency

Check:

* No duplicated Transition with conflicting Result
* Same State + Action must not produce multiple different Next States unless guards are specified
* No contradictory State behavior

## 5. Missing Rule Check

For every unclear behavior, write:

"Đặc tả không định nghĩa quy tắc này."

---

# Step 8: Risk Analysis

Classify each Transition.

High Risk:

* Authentication
* Authorization
* Security
* Payment
* Data loss
* Account lock
* Password reset
* OTP/token/session
* State corruption
* Final State correctness
* Invalid State change

Medium Risk:

* Validation
* Workflow progression
* Retry flow
* Timeout flow
* Error recovery

Low Risk:

* UI display
* Navigation
* Non-critical behavior

Format:

## Risk Analysis

| Transition ID | Risk   | Reason                                                |
| ------------- | ------ | ----------------------------------------------------- |
| T1            | Medium | Workflow chuyển từ bước nhập email sang bước nhập OTP |
| T2            | High   | OTP sai có thể ảnh hưởng bảo mật                      |
| T3            | High   | Đặt lại mật khẩu thành công là luồng nhạy cảm         |

---

# Step 9: Mandatory Dedicated Valid Transition Test Cases

The agent MUST generate one dedicated Test Case for each valid Transition.

Rules:

* Every valid Transition in the Transition List MUST have its own dedicated Test Case
* Do NOT replace a valid Transition Test Case with End-to-End Test
* Do NOT replace a valid Transition Test Case with 1-switch Test
* Do NOT replace a valid Transition Test Case with n-switch Test
* Do NOT replace a valid Transition Test Case with Final State Test
* If there are X valid Transitions, generate at least X dedicated valid Transition Test Cases
* A valid Transition is considered fully tested only when it has a direct Test Case with Coverage Type = Transition Coverage
* End-to-End Test, 1-switch Test, and n-switch Test may cover the same Transition, but they are additional Coverage, not replacements

Required mapping format:

## Dedicated Valid Transition Test Mapping

| Transition ID | Current State | Action / Event | Next State | Dedicated Test Case |
| ------------- | ------------- | -------------- | ---------- | ------------------- |
| T1            | S0            | A1             | S1         | TC-ST-001           |
| T2            | S1            | A2             | S2         | TC-ST-002           |
| T3            | S2            | A3             | S3         | TC-ST-003           |

Validation rule:

Before continuing, check:

Total valid transitions = X
Dedicated valid transition test cases = Y

If X ≠ Y, the output is invalid.

The agent MUST generate missing Test Cases until:

Dedicated Valid Transition Coverage = 100%

---

# Step 10: Generate Invalid Transition Test Cases

Generate Test Cases for invalid Transitions.

Rules:

* Every invalid Transition with defined expected behavior MUST have a Test Case
* Invalid Transitions are important for security and workflow correctness
* Do not skip invalid Transitions from Final State
* Do not skip invalid Transitions from security-sensitive States
* If invalid behavior is not defined, write:

"Đặc tả không định nghĩa quy tắc này."

Required mapping format:

## Invalid Transition Test Mapping

| Transition ID | Current State | Action / Event | Expected Behavior              | Test Case |
| ------------- | ------------- | -------------- | ------------------------------ | --------- |
| T4            | S0            | A2             | Reject Action and remain in S0 | TC-ST-004 |
| T5            | S2            | A1             | Reject Action and remain in S2 | TC-ST-005 |

---

# Step 11: Generate State Coverage Test Cases

Goal:

* Every State must be visited at least once

Coverage formula:

State Coverage = Number of visited States / Total States × 100%

Rules:

* State Coverage may be achieved through dedicated Transition Test Cases
* If any State is not visited by existing Test Cases, generate additional Test Case
* Final States must be visited
* Error States must be visited if defined

Required output:

## State Coverage

| State | Covered By Test Case |
| ----- | -------------------- |
| S0    | TC-ST-001            |
| S1    | TC-ST-001            |
| S2    | TC-ST-002            |

Validation rule:

Total States = X
Covered States = Y

If X ≠ Y, generate missing Test Cases until:

State Coverage = 100%

---

# Step 12: Generate Transition Coverage Test Cases

Goal:

* Every valid Transition must be executed at least once
* Every invalid Transition with defined behavior must be tested

Coverage formula:

Transition Coverage = Number of executed Transitions / Total Transitions × 100%

Rules:

* All valid Transitions must have dedicated Test Cases
* Invalid Transitions must be included if expected behavior is defined
* Do not count undefined invalid behavior as covered
* Do not skip simple valid Transitions

Required output:

## Transition Coverage

| Transition ID | Valid / Invalid | Covered By Test Case |
| ------------- | --------------- | -------------------- |
| T1            | Valid           | TC-ST-001            |
| T2            | Valid           | TC-ST-002            |
| T3            | Invalid         | TC-ST-003            |

Validation rule:

Total testable Transitions = X
Covered Transitions = Y

If X ≠ Y, generate missing Test Cases until:

Transition Coverage = 100%

---

# Step 13: Generate 1-switch Coverage Test Cases

Definition:

1-switch Coverage covers every valid sequence of 2 consecutive Transitions.

Pattern:

T1 → T2

Equivalent State pattern:

S0 → S1 → S2

Goal:

* Test interaction between one Transition and the immediately following Transition

Rules:

* Generate all possible valid 1-switch sequences
* A sequence is valid only when Next State of first Transition equals Current State of second Transition
* Include invalid Transition in a 1-switch sequence only if the specification defines expected behavior
* Do not create impossible sequences
* Do not replace dedicated valid Transition Test Cases with 1-switch Test Cases
* 1-switch Test Cases are additional tests

Required output:

## 1-switch Coverage

| 1-switch ID | Transition Sequence | State Sequence | Covered By Test Case |
| ----------- | ------------------- | -------------- | -------------------- |
| SW1-001     | T1 → T2             | S0 → S1 → S2   | TC-ST-SW1-001        |

Validation rule:

Total 1-switch sequences = X
Covered 1-switch sequences = Y

If X ≠ Y, generate missing Test Cases until:

1-switch Coverage = 100%

---

# Step 14: Generate n-switch Coverage Test Cases

Definition:

n-switch Coverage covers every valid sequence of n+1 consecutive Transitions.

Pattern:

For 2-switch:

T1 → T2 → T3

For 3-switch:

T1 → T2 → T3 → T4

Default:

* If user does not specify n, use n = 2

Goal:

* Test longer workflows
* Test repeated State-dependent behavior
* Test multi-step business flows

Rules:

* Generate valid n-switch sequences only
* Preserve high-risk paths
* Preserve loops and retry flows if specified
* Avoid infinite loops
* Limit repeated loop traversal unless requirement defines retry limit
* Do not replace dedicated valid Transition Test Cases with n-switch Test Cases
* n-switch Test Cases are additional tests

If retry limit is missing, write:

"Đặc tả không định nghĩa quy tắc này."

Required output:

## n-switch Coverage

| n-switch ID | n Value | Transition Sequence | State Sequence    | Covered By Test Case |
| ----------- | ------- | ------------------- | ----------------- | -------------------- |
| SW2-001     | 2       | T1 → T2 → T3        | S0 → S1 → S2 → S3 | TC-ST-SW2-001        |

Validation rule:

Total n-switch sequences = X
Covered n-switch sequences = Y

If X ≠ Y, generate missing Test Cases until:

n-switch Coverage = 100%

---

# Step 15: Generate End-to-End Test Cases

Definition:

End-to-End Test covers a complete business workflow from Initial State to Final State.

Goal:

* Verify the complete user journey
* Ensure all major Transitions work together
* Verify business process completion

Rules:

* Each End-to-End Test must start from Initial State
* Each End-to-End Test must end at a Final State
* Include happy path
* Include high-risk alternative path
* Include failure path if it reaches a defined Final State or Error State
* Do not replace dedicated valid Transition Test Cases with End-to-End Test
* End-to-End Test Cases are additional tests

Required output:

## End-to-End Test Paths

| E2E ID  | Start State | Transition Path | Final State | Covered By Test Case |
| ------- | ----------- | --------------- | ----------- | -------------------- |
| E2E-001 | S0          | T1 → T2 → T3    | S3          | TC-ST-E2E-001        |

---

# Step 16: Generate Final State Test Cases

Definition:

Final State Test verifies behavior after the system reaches a Final State.

Goal:

* Confirm that final output is stable
* Confirm that invalid post-final Actions cannot incorrectly change completed State
* Confirm that no unexpected State change happens after completion

Rules:

* Test each Final State
* Apply relevant Actions after Final State
* Verify State remains unchanged unless specification defines reopening/retry
* Do not skip Final State Test
* Final State Test Cases are additional tests
* Final State Test Cases do not replace dedicated valid Transition Test Cases

If post-final behavior is not specified, write:

"Đặc tả không định nghĩa quy tắc này."

Required output:

## Final State Test

| Final State | Action After Final State | Expected Behavior              | Covered By Test Case |
| ----------- | ------------------------ | ------------------------------ | -------------------- |
| S3          | A1                       | Reject Action and remain in S3 | TC-ST-FINAL-001      |

---

# Step 17: Generate Final Test Cases

The ONLY allowed test case format:

/docs/test-case-template.md

Generate final Test Cases from all required groups:

* Dedicated valid Transition Test Cases
* Invalid Transition Test Cases
* State Coverage Test Cases if any State is still uncovered
* 1-switch Coverage Test Cases
* n-switch Coverage Test Cases
* End-to-End Test Cases
* Final State Test Cases
* High-risk scenarios
* Security-sensitive scenarios

Important:

* Do NOT remove Test Cases
* Do NOT reduce Test Cases
* Do NOT merge required Coverage groups into fewer Test Cases
* Do NOT use End-to-End Test as replacement for Transition Coverage
* Do NOT use 1-switch or n-switch as replacement for dedicated valid Transition Test Cases

Each final Test Case MUST maintain traceability:

Requirement
→ State
→ Action/Event
→ Transition
→ Coverage Type
→ Test Case

Each final Test Case must include:

* Test Case ID
* Requirement ID
* Coverage Type
* Covered State(s)
* Covered Transition(s)
* Covered switch sequence, if applicable
* Preconditions
* Test Data
* Steps
* Expected Result
* Final State
* Risk Level

Test Case ID format:

TC-ST-[FEATURE]-[NUMBER]

Examples:

* TC-ST-FORGOT-PASSWORD-001
* TC-ST-FORGOT-PASSWORD-002
* TC-ST-FORGOT-PASSWORD-SW1-001
* TC-ST-FORGOT-PASSWORD-SW2-001
* TC-ST-FORGOT-PASSWORD-E2E-001
* TC-ST-FORGOT-PASSWORD-FINAL-001

---

# Step 18: Generate Test Case Count Summary

Calculate total generated Test Cases.

Formula:

Total Test Cases =
Dedicated valid Transition Test Cases

* Invalid Transition Test Cases
* Additional State Coverage Test Cases
  + 1-switch Test Cases
* n-switch Test Cases
* End-to-End Test Cases
* Final State Test Cases

Rules:

* Do not subtract duplicate Coverage
* Do not reduce by overlapping paths
* If one Test Case incidentally covers multiple items, still keep required Test Cases from each required group
* Report overlap only as additional Coverage, not as a reason to remove Test Cases

Required output:

## Test Case Count Summary

| Test Group                            | Count |
| ------------------------------------- | ----- |
| Dedicated valid Transition Test Cases | X     |
| Invalid Transition Test Cases         | X     |
| Additional State Coverage Test Cases  | X     |
| 1-switch Test Cases                   | X     |
| n-switch Test Cases                   | X     |
| End-to-End Test Cases                 | X     |
| Final State Test Cases                | X     |
| Total Test Cases                      | X     |

---

# Step 19: Generate State Transition Analysis Report

Create:

docs/state-transition-analysis.md

Must include:

# Requirement Summary

# State Identification

# Action / Event Identification

# State Transition Table using States × Actions

# Transition List

# State Transition Validation

# Risk Analysis

# Dedicated Valid Transition Test Mapping

# Invalid Transition Test Mapping

# State Coverage

# Transition Coverage

# 1-switch Coverage

# n-switch Coverage

# End-to-End Test Paths

# Final State Test

# Final Test Case Mapping

# Test Case Count Summary

# Coverage Summary

Coverage Summary format:

| Coverage Type                       | Required                          | Covered                               | Coverage |
| ----------------------------------- | --------------------------------- | ------------------------------------- | -------- |
| State Coverage                      | Total States                      | Covered States                        | 100%     |
| Transition Coverage                 | Total testable Transitions        | Covered Transitions                   | 100%     |
| Dedicated Valid Transition Coverage | Total valid Transitions           | Dedicated valid Transition Test Cases | 100%     |
| Invalid Transition Coverage         | Total defined invalid Transitions | Covered invalid Transitions           | 100%     |
| 1-switch Coverage                   | Total 1-switch sequences          | Covered sequences                     | 100%     |
| n-switch Coverage                   | Total n-switch sequences          | Covered sequences                     | 100%     |
| End-to-End Test                     | Total E2E paths                   | Covered paths                         | 100%     |
| Final State Test                    | Total Final States                | Covered Final States                  | 100%     |

If 100% Coverage cannot be achieved due to missing specification, explain clearly:

"Không thể đạt 100% Coverage vì đặc tả không định nghĩa đầy đủ State, Action hoặc Expected Behavior."

---

# Step 20: AI Audit Logging

Append:

docs/ai-audit-report.md

Include:

* AI tool name
* Timestamp
* Prompt used
* Task performed
* Input documents read
* Output summary
* Files generated
* Coverage generated
* Known limitations

Timestamp format:

MM/DD/YYYY hh:mm AM/PM

Example:

| Field          | Value                                                                    |
| -------------- | ------------------------------------------------------------------------ |
| AI tool name   | ChatGPT                                                                  |
| Timestamp      | 07/06/2026 03:30 PM                                                      |
| Task performed | Generate State Transition Testing test cases                             |
| Output summary | Created State Transition Table, Coverage report, and complete Test Cases |

---

# Quality Rules

The agent MUST:

* Prioritize risk-based testing
* Not invent requirements
* Clearly separate State, Action/Event, Transition, and Result
* Use States × Actions when creating State Transition Table
* Generate one dedicated Test Case for each valid Transition
* Generate invalid Transition Test Cases when expected behavior is defined
* Generate 1-switch Coverage Test Cases
* Generate n-switch Coverage Test Cases
* Generate End-to-End Test Cases
* Generate Final State Test Cases
* Keep traceability between Requirement → State → Action/Event → Transition → Coverage → Test Case
* Explain missing rules explicitly
* Preserve high-risk Coverage
* Preserve Final State Test
* Preserve End-to-End Test
* Avoid impossible transition paths
* Avoid infinite loop paths
* Report all generated Test Cases clearly

The agent MUST NOT:

* Read source code
* Guess missing behavior
* Create States not present in specification
* Create Actions not present in specification
* Treat UI screen as State unless it represents business/system behavior
* Treat button click as Action if it does not affect State
* Reduce Test Cases
* Remove Test Cases
* Merge dedicated valid Transition Test Cases into End-to-End Test
* Use 1-switch Coverage as replacement for Transition Coverage
* Use n-switch Coverage as replacement for Transition Coverage
* Skip valid Transitions because they are simple

---

# Final Response

Respond Vietnamese.

Include:

## File đã tạo

List generated files.

Example:

* tests/test-cases/forgot-password/TC-ST-FORGOT-PASSWORD-001.md
* tests/test-cases/forgot-password/TC-ST-FORGOT-PASSWORD-002.md
* tests/test-cases/forgot-password/TC-ST-FORGOT-PASSWORD-SW1-001.md
* tests/test-cases/forgot-password/TC-ST-FORGOT-PASSWORD-SW2-001.md
* tests/test-cases/forgot-password/TC-ST-FORGOT-PASSWORD-E2E-001.md
* tests/test-cases/forgot-password/TC-ST-FORGOT-PASSWORD-FINAL-001.md
* docs/state-transition-analysis.md
* docs/ai-audit-report.md

---

## Tổng kết kiểm thử

Include:

* Feature tested
* Requirement ID
* Number of States
* Number of Actions
* Number of State Transition Table rows
* Number of valid Transitions
* Number of invalid Transitions
* Number of final States
* Number of dedicated valid Transition Test Cases
* Number of invalid Transition Test Cases
* Number of 1-switch Test Cases
* Number of n-switch Test Cases
* Number of End-to-End Test Cases
* Number of Final State Test Cases
* Total Test Cases
* State Coverage achieved
* Transition Coverage achieved
* 1-switch Coverage achieved
* n-switch Coverage achieved
* End-to-End Test Coverage achieved
* Final State Test Coverage achieved
* Techniques applied

Example:

Feature tested:

Requirement ID:

States:

Actions:

State Transition Table rows:

Valid Transitions:

Invalid Transitions:

Final States:

Dedicated valid Transition Test Cases:

Invalid Transition Test Cases:

1-switch Test Cases:

n-switch Test Cases:

End-to-End Test Cases:

Final State Test Cases:

Total Test Cases:

State Coverage:

Transition Coverage:

1-switch Coverage:

n-switch Coverage:

End-to-End Test Coverage:

Final State Test Coverage:

Techniques applied:

Coverage achieved:
